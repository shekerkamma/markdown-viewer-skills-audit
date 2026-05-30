# How We Built a Ticket-to-PR Pipeline Using the CodeActAgent Pattern

*Publish to: company blog, Hacker News, cross-post to dev.to*
*Target audience: senior engineers and architects evaluating the system*

---

TicketForge is a multi-agent AI pipeline that turns GitHub Issues into reviewed, tested pull requests. This post is a deep dive into the architecture — how the agents communicate, why we chose Docker sandboxing over alternatives, and how the event stream makes every decision auditable.

## The problem with general-purpose agent frameworks

When we first considered building an autonomous bug fix pipeline, the obvious approach was to wire up LangChain or CrewAI. We tried. We abandoned the effort after two weeks.

The problems were structural, not incidental. General-purpose agent frameworks are designed for broad flexibility — they support dozens of tool types, memory backends, and orchestration patterns. But that flexibility comes with overhead that's wrong for code workflows:

- **No built-in sandboxing.** Code generation agents need to execute code safely. LangChain's tool abstraction treats shell execution as just another tool, with no isolation guarantees. We needed Docker containers with `--network=none` as a hard constraint.
- **Fragile orchestration.** Multi-agent handoffs in CrewAI rely on sequential task definitions that break when an agent needs to iterate (generate fix → run tests → fix failures → run tests again). Our code generation step needs a loop, not a chain.
- **No audit trail.** Both frameworks log tool calls, but neither provides a structured event stream where every agent action, observation, and decision is persisted with full context. For developer trust, we needed complete transparency.

So we built on the pattern that actually works for code: the OpenHands CodeActAgent architecture.

## Architecture overview

```
GitHub Issue Webhook
       |
       v
  Webhook Handler (FastAPI)
       |
       v
  ARQ Task Queue (Redis)
       |
       v
  Pipeline Orchestrator
       |
       +---> Content Researcher (Claude Sonnet)
       |          |
       |          v
       |     Structured Analysis
       |          |
       +---> CodeAct Agent (Claude Opus)
       |          |
       |          v
       |     Docker Sandbox
       |     - Clone repo (--depth 1)
       |     - Read affected files
       |     - Generate fix (up to 3 iterations)
       |     - Run tests (compare against baseline)
       |     - Extract git diff
       |          |
       +---> Code Reviewer (Claude Sonnet)
       |          |
       |          v
       |     4-dimension review
       |     (style, tests, regression, security)
       |          |
       +---> PR Creator
       |          |
       |          v
       |     Push branch, open PR, link to issue
       |
       v
  Event Stream (PostgreSQL JSONB)
```

Every arrow in this diagram is an `AgentResult` — a structured response containing `success`, `output`, `confidence`, `error`, and `tokens_used`. The pipeline orchestrator makes escalation decisions based on these results at each step.

## The agent abstraction

Every agent extends a single base class:

```python
class BaseAgent(ABC):
    name: str

    async def log_action(self, action_type, payload)
    async def log_observation(self, observation)
    async def log_decision(self, decision, confidence)
    async def log_error(self, error)

    @abstractmethod
    async def run(self, context: dict) -> AgentResult
```

This is deliberately minimal. The base class handles event logging. Each agent implements `run()` with its specific logic. The `AgentResult` dataclass is the contract:

```python
@dataclass
class AgentResult:
    success: bool
    output: dict | str | None = None
    confidence: float = 0.0
    error: str | None = None
    tokens_used: int = 0
```

The `confidence` field is what makes escalation work. When any agent returns `confidence < 0.4`, the pipeline escalates to a human developer with the partial analysis attached. This is the "escalate over guess" principle — a visible failure is better than a bad PR.

## Docker sandbox: the trust foundation

All code generation runs inside Docker containers with these constraints:

```python
container = client.containers.run(
    "ticketforge-sandbox",
    network_mode="none",       # No network access
    mem_limit="2g",            # 2GB memory ceiling
    nano_cpus=int(1e9),        # 1 CPU
)
```

The `--network=none` flag is non-negotiable. An AI agent with repository access and network access is a supply chain attack vector. By removing the network, the agent can read and modify code but cannot exfiltrate data, download packages, or call external APIs. The trade-off is that the sandbox image must include all necessary tooling (Python, Node.js, git, test runners) — we handle this with a pre-built base image.

The sandbox lifecycle:
1. **Create** — spin up container with repo URL and branch as environment variables
2. **Entrypoint** — clone the repo with `--depth 1` (shallow clone for performance)
3. **Exec** — pipeline sends commands via `container.exec_run()`
4. **Diff** — extract `git diff` after the fix is applied
5. **Destroy** — container is stopped and removed, regardless of outcome

We pre-pull the sandbox image on service startup to avoid cold-start latency on the first pipeline run.

## The iterative fix loop

The CodeAct agent doesn't generate a fix once and hope for the best. It runs an iterative loop:

```
Iteration 1: Read files → Generate fix → Apply patch → Run tests
  Tests pass? → Extract diff, done
  Tests fail? → Capture failure output

Iteration 2: Include failure context → Generate revised fix → Run tests
  Tests pass? → Extract diff, done
  Tests fail? → One more try

Iteration 3: Final attempt with accumulated context
  Tests pass? → Extract diff, done
  Tests fail? → Return best-effort diff with low confidence
```

A critical detail: before generating any fix, we run the test suite to capture a **baseline**. Many repos have pre-existing test failures. Without a baseline, the agent would loop forever trying to fix failures it didn't cause. We compare after-fix results against the baseline — if no *new* failures are introduced, the fix passes.

## The review gate

The code reviewer evaluates every diff against four dimensions:

| Dimension | What it checks | Rejection threshold |
|-----------|---------------|-------------------|
| Style | Code conventions, naming, formatting | No auto-reject |
| Tests | New/updated tests, assertion quality | Configurable per repo |
| Regression | Side effects, breaking changes | No auto-reject |
| Security | OWASP top 10, hardcoded secrets, injection | Score < 0.3 = reject |

The security dimension has a hard rejection threshold. If the reviewer scores security below 0.3, the fix is rejected regardless of other dimensions. This prevents the pipeline from ever creating a PR that introduces a security vulnerability.

Review criteria are configurable per repository via a JSONB config field:

```json
{
  "review": {
    "require_tests": true,
    "security_check": true,
    "min_confidence": 0.6
  }
}
```

A team that works in a codebase without test infrastructure can disable `require_tests` so the reviewer doesn't reject every fix for missing tests.

## The event stream

Every agent action is persisted to PostgreSQL as a JSONB event:

```json
{
  "id": "evt_abc123",
  "pipeline_run_id": "run_xyz789",
  "agent_name": "code_act_agent",
  "event_type": "action",
  "payload": {
    "action_type": "generate_fix",
    "iteration": 2,
    "files_read": ["api/handlers.py", "tests/test_handlers.py"]
  },
  "timestamp": "2026-05-30T14:23:17Z"
}
```

Events are typed: `action` (agent did something), `observation` (agent noticed something), `decision` (agent chose something with a confidence score), and `error` (something went wrong). The event stream serves three purposes:

1. **Debugging** — when a fix is wrong, trace back through the events to understand why the agent made each decision
2. **Trust** — developers can see exactly what happened, which builds confidence to approve agent PRs
3. **Analytics** — aggregate event data across pipeline runs to identify patterns (which agents fail most, which fix categories succeed)

The dashboard streams events in real-time via Server-Sent Events (SSE), so a developer watching the dashboard can see the pipeline working as it happens.

## What we learned

**Sonnet for analysis, Opus for generation.** We use Claude Sonnet (cheaper, faster) for ticket analysis and code review — tasks that require understanding but not generation. We use Claude Opus (more capable, more expensive) for code generation — the task where output quality directly determines success. This split reduces API costs by roughly 60% compared to using Opus for everything.

**Shallow clones matter.** Cloning a large repo with full history inside a container can take minutes. `--depth 1` reduces this to seconds for most repositories. The agent doesn't need git history — it needs the current state of the code.

**Pre-existing test failures are the norm, not the exception.** More than half of the repos we tested had at least one failing test on main. Without baseline capture, the agent would escalate every ticket from these repos. The baseline comparison was one of the most impactful reliability improvements we made.

**Escalation is a feature, not a failure.** Our target escalation rate is 30–40%. Below 15% suggests the system is overconfident. Above 60% suggests it's not adding enough value. The right escalation rate means the system handles what it can and is honest about what it can't.

---

*TicketForge is open source. [Read the code], [try it on your repo], or [join the discussion].*
