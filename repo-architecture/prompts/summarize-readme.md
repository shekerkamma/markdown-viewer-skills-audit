# README Summarization Prompt

Phase 1.5 of the [repo-architecture](../SKILL.md) skill. Produces the
`readme_summary` field of `structure.json` from the raw README text.

## Input

The raw `README.md` content of a public GitHub repo (utf-8 string, any length).

## Output

A 200-word summary, plain text, no markdown formatting. Single paragraph or
short paragraphs. The summary is read by the classifier in Phase 2 — it is not
shown to the end user.

## What the summary must answer

The classifier needs to assign each module to a semantic layer. To do that
well, it needs to know:

1. **What does the project do?** One sentence on the core function.
2. **Who uses it?** Humans? Other systems? Developers? End users? Operators?
3. **What are the core nouns and verbs?** The domain vocabulary that will
   appear in module names and decide layer assignments.
4. **What external systems does it talk to?** Databases, APIs, SaaS products,
   cloud providers, hardware. These map to the `external` and `infra` layers.
5. **Is it a system or a content collection?** Cookbooks, example repos, and
   doc sites are not classifiable into layers — call this out so the
   classifier can refuse early per Rule 5 of `classify-modules.md`.

## Rules

- **Stay grounded in the README.** Do not infer features that aren't stated.
- **No marketing voice.** "Lightning-fast, cutting-edge, enterprise-grade" is
  noise. Strip it.
- **Use the project's own terms.** If the README calls something a "workflow,"
  call it a workflow in the summary, not a "pipeline."
- **No bullet points or headers.** Plain prose. The classifier reads it as
  context, not as data.
- **If the README is empty or boilerplate** (just the language template, no
  actual content), output the literal string `INSUFFICIENT_README` and
  nothing else. The classifier will refuse on this signal.

## Example output (good)

> SAP-O2C-Automation is a multi-agent system that automates the SAP
> Order-to-Cash business process by replacing 17 Power Automate flows with
> Python agents. A root coordinator dispatches to specialized sub-agents
> (product, inventory, sales order, outbound delivery, and analytics) which
> reason via Gemini and invoke SAP OData services through an MCP server
> written in TypeScript. Authentication and credential handling go through
> SAP BTP API Management, so the agent layer never touches secrets directly.
> The system runs on Google ADK with Gemini for LLM reasoning, and includes
> a mock OData server so the full workflow can be developed and tested
> without a live SAP system. Target user: a developer prototyping enterprise
> automation. External systems: SAP S/4HANA Cloud, Gemini API, SAP BTP.

## Example output (refusal)

> INSUFFICIENT_README
