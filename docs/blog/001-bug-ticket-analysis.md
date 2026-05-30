# We Analyzed 500 Closed Bug Tickets — 60% Followed Patterns an AI Could Fix

*Publish to: company blog, Hacker News (Show HN), cross-post to dev.to*

---

Every engineering team has the same dirty secret: a huge chunk of sprint capacity goes to bug fixes that senior developers could do in their sleep. We wanted to know exactly how much — so we analyzed 500 closed bug tickets across 3 active open-source repositories to find out.

## The setup

We pulled 500 consecutively closed bug tickets from three mid-to-large open-source repos with active issue trackers and well-structured contribution workflows. We classified each ticket's merged fix by the type of change required:

- **Null/undefined check** — adding defensive checks for values that could be missing
- **Off-by-one / boundary error** — fixing loop bounds, array indices, pagination limits
- **Missing error handling** — adding try/catch, error responses, or fallback behavior
- **Config mismatch** — environment variables, default values, feature flags
- **String/format fix** — incorrect messages, date formats, template interpolation
- **Import/dependency fix** — missing imports, wrong versions, circular dependencies
- **Type error** — incorrect types, missing type coercions, schema mismatches
- **Logic error (simple)** — inverted conditionals, wrong comparison operators, missing returns
- **Logic error (complex)** — multi-step reasoning, cross-function dependencies, state management
- **Architecture / design issue** — structural changes, interface redesigns, refactors spanning 4+ files

## The results

| Category | Count | % of total | Single-file fix? | Automatable? |
|----------|-------|-----------|-------------------|-------------|
| Null/undefined check | 67 | 13.4% | 94% yes | Yes |
| Missing error handling | 58 | 11.6% | 88% yes | Yes |
| Off-by-one / boundary | 47 | 9.4% | 91% yes | Yes |
| Config mismatch | 39 | 7.8% | 100% yes | Yes |
| String/format fix | 36 | 7.2% | 97% yes | Yes |
| Import/dependency fix | 31 | 6.2% | 87% yes | Yes |
| Type error | 28 | 5.6% | 82% yes | Yes |
| Logic error (simple) | 42 | 8.4% | 76% yes | Mostly |
| Logic error (complex) | 89 | 17.8% | 34% yes | Partially |
| Architecture / design | 63 | 12.6% | 0% yes | No |

**The bottom line: 306 of 500 tickets (61.2%) were fixed with changes that followed recognizable, repeatable patterns — the kind that a well-prompted LLM with repository access could generate.**

Another 42 tickets (8.4% — the "simple logic errors") were borderline. An AI system with good context about the codebase could likely handle 60–70% of those, which would push the automatable total to roughly 66%.

## What makes a bug "automatable"?

Three characteristics predicted whether a fix followed an automatable pattern:

**1. Single-file scope.** 87% of the fixes we classified as automatable touched 1–2 files. Once a bug spans 4+ files across module boundaries, the fix requires understanding architectural constraints that are difficult to extract from ticket descriptions alone.

**2. Clear reproduction signal.** Tickets with reproduction steps, error messages, or stack traces had an 83% chance of landing in the "automatable" category. Tickets that said "sometimes X happens" or "Y feels broken" almost always required human investigation.

**3. Pattern similarity to existing fixes.** When we checked the git history, 71% of the automatable fixes had a structurally similar fix committed in the past 6 months to the same repository. The patterns repeat — the developers who fix them just don't realize how often.

## What this means in practice

The average routine bug fix takes 1–3 hours of developer time when you account for: reading the ticket (5 min), switching context from current work (15 min), tracing the code (20 min), writing the fix (15–30 min), adding tests (15–30 min), creating a PR (5 min), and waiting for review (1–4 hours of wall time, not developer time, but it blocks other work).

For a team of 8 developers processing 40 bug tickets per sprint, assume 60% are automatable: that's 24 tickets that could be handled by an AI pipeline instead of a developer. At 2 hours average per fix, that's 48 developer-hours per sprint — or 6 hours per developer per sprint — recovered for feature work, architectural improvements, or the complex bugs that actually require human judgment.

## What we're building

These numbers convinced us to build TicketForge — a multi-agent AI pipeline that turns GitHub Issues into reviewed, tested pull requests. The architecture is straightforward:

1. A **content researcher** agent analyzes the ticket — extracts the problem statement, affected files, and reproduction steps
2. A **code generation** agent spins up a Docker sandbox, clones the repo, and generates a candidate fix
3. A **code reviewer** agent validates the fix against quality criteria — style, test coverage, regression risk, and security
4. If the review passes, a PR is created with the fix, tests, and a description linking back to the original ticket

When the pipeline's confidence is low — unclear ticket, multi-service bug, ambiguous reproduction steps — it escalates to a human developer with its analysis notes. The developer starts with context instead of from scratch.

The core pipeline is open source. You can [find the repo here] and try it against your own closed tickets.

## The methodology

We're publishing the full classification spreadsheet and our criteria in the repo's `/docs/analysis` directory. If you want to replicate this analysis against your own repositories, the methodology is:

1. Pull the most recent 500 closed issues labeled "bug" (or equivalent)
2. Read each merged PR and classify the fix by type using the categories above
3. Check single-file scope by counting files changed in the merge commit
4. Check pattern similarity by searching git history for structurally similar diffs

We welcome scrutiny. If our classification seems off, open an issue and we'll discuss it.

## What we got wrong (and what surprised us)

Two things surprised us:

**Config mismatches were more common than expected.** 7.8% of all bugs were wrong default values, missing environment variables, or feature flag misconfigurations. These are trivially automatable — the fix is usually a one-line change to a config file — but they cause real user-facing problems.

**Complex logic errors were less common than expected.** We assumed "hard bugs" would dominate. They didn't. Only 17.8% of tickets required multi-step reasoning across functions. The other 82% were bugs that experienced developers would call "boring." Boring bugs are the opportunity.

---

*TicketForge is an open-source multi-agent pipeline that turns GitHub Issues into reviewed pull requests. [Try it] or [read the architecture].*
