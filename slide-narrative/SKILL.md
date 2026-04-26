---
name: slide-narrative
description: Templates and structural rules for assembling diagrams into a presentation. Audience-driven deck patterns (exec, eng review, onboarding, customer pitch), one-decision-per-slide enforcement, and the slide-shapes that work. Pairs with marp or python-pptx — this skill is structure, those are renderers.
metadata:
  author: shekerkamma — addition to markdown-viewer/skills
---

# Slide Narrative — Deck Structure & Patterns

**Quick Start:** Identify the audience → pick a template (exec / eng review / onboarding / pitch) → fill in one-idea-per-slide → render with [marp](../marp/SKILL.md) or [python-pptx](../python-pptx/SKILL.md).

This skill is **prose-only** — no rendering. It teaches *what shape a deck should have*, not how to produce the file.

## Why deck structure matters more than visuals

Most decks fail because they were built bottom-up: someone made the diagrams first, then strung them together with bullets. The result is a slide-show of artifacts, not an argument.

Decks that land are built top-down:

1. **Who is in the room?** (audience)
2. **What decision do you need from them?** (ask)
3. **What is the minimum sequence of slides that gets them from "I haven't thought about this" to making the decision?** (narrative)
4. **Which slides need diagrams?** (visuals — *now* you reach for [mermaid](../mermaid/SKILL.md) / [c4](../c4/SKILL.md) / [architecture](../architecture/SKILL.md))

If the talk works without slides, the slides will work. If the talk doesn't work without slides, the slides won't save it.

## Critical Rules

### Rule 1: Every deck has exactly one ask
Before drafting slide 1, write the **ask** in one sentence:

> "Approve the migration from RDS to Aurora by end of Q2."
> "Greenlight Project Apollo's $1.2M budget."
> "Adopt C4 as the standard architecture notation across engineering."

If you can't write it, you don't have a deck — you have a status update. Status updates should be docs, not slides.

### Rule 2: One idea per slide
A slide carries one claim. The bullets on the slide are *evidence for that claim*, not a list of unrelated points.

Bad: a "Status" slide with five bullet points about five different topics.
Good: five separate slides, each titled with the claim ("Migration is on schedule", "Cost projection holds", "Risk is concentrated in Service X").

When in doubt: title the slide with a complete sentence, not a noun phrase. *"Q2 architecture review"* is a noun phrase. *"We need to split the order service in Q3"* is a claim.

### Rule 3: Diagram = the slide, not a slide decoration
If you have a diagram, it should *be* the slide. Not "title at top, three bullets, then a diagram squashed into the corner". Use [marp](../marp/SKILL.md)'s `![bg](diagram.svg)` or `![bg right:55%]` so the diagram dominates.

The bullets next to a diagram should be the **implications**, not the contents. The diagram already shows the contents.

```
Bad:
  [Diagram of three services]
  - We have three services
  - They talk to each other
  - One uses Postgres

Good:
  [Diagram of three services]
  - Order service is the bottleneck — 70% of latency
  - Splitting it unblocks the Q3 traffic forecast
  - Estimated 4 weeks, 2 engineers
```

### Rule 4: Open with the ask, close with the ask
The first content slide states what you want. The last content slide restates it. Everything in between is justification.

This violates the "save the punchline for the end" instinct, but exec decks specifically reward it: half the audience will be in their email and only catch the bookends. Make sure both bookends carry the ask.

### Rule 5: Audience drives template, not topic
Same architecture, different audiences need different decks:

| Audience | What they need | Deck shape |
|---|---|---|
| **Execs** | The ask + the cost + the risk | Cover → ask → 3 reasons → ask. 5–8 slides. |
| **Engineers (review)** | The architecture, the alternatives, the open questions | Context → containers → trade-offs → open Qs. 10–15 slides. |
| **New hires** | Mental model of the system | Context → containers → key flows → glossary. 15–25 slides, more diagrams. |
| **Customers** | Why we'll solve their problem | Their problem → our solution → proof → call-to-action. 5–10 slides, low density. |

Don't reuse a customer pitch deck for an architecture review. The shape is wrong.

### Rule 6: Speaker notes carry the talk; slides carry the visuals
A slide stuffed with text means the speaker isn't sure what they'll say. Move it to speaker notes ([marp](../marp/SKILL.md): `<!-- ... -->`; [python-pptx](../python-pptx/SKILL.md): `slide.notes_slide.notes_text_frame.text`).

The reverse trap: tiny terse slides + zero notes = unrecoverable if the speaker calls in sick. Always notes.

### Rule 7: Rule-of-three for sections
Long decks need structure. Split into three sections, **never more than four**. The brain stops counting at three. Section dividers are full-bleed slides with the section name only.

```
Cover
Section 1: Where we are
  ...
Section 2: Where we're going
  ...
Section 3: What we need from you
  ...
```

## Templates

### Template A — Exec ask (5–8 slides)

```
1. Cover                       Title, your name, date
2. The ask                     "Approve X by Y because Z"  ← state it now
3. Status quo                  Why doing nothing is bad — 1 chart or 1 number
4. The proposal                What we want to do — 1 diagram (Context-level)
5. Cost & timeline             $ + weeks + headcount, in a table
6. Risks & mitigations         Top 2 risks, each with a one-line mitigation
7. The ask, restated           Same words as slide 2 — yes/no question
```

Good for: budget approval, hiring asks, strategy pivots, vendor decisions.

### Template B — Engineering review (10–15 slides)

```
 1. Cover
 2. Agenda                     3 sections, decisions needed
 3. [SECTION] Context
 4. System Context (C4)        Who uses it, what it talks to
 5. Constraints                SLOs, compliance, scale targets
 6. [SECTION] Proposal
 7. Container diagram (C4)     Or sequence / state / ER
 8. Key trade-off #1           "We chose X over Y because Z"
 9. Key trade-off #2
10. [SECTION] Decisions
11. Open question 1            One paragraph + your recommendation
12. Open question 2
13. Risks                      Likelihood × impact, prioritized
14. What we need from you      The actual decision asks
15. Backup slides              Reference architectures, alternatives considered
```

Good for: architecture reviews, design docs, vendor evaluations, RFC presentations.

### Template C — New-hire onboarding (15–25 slides)

```
 1. Cover                      "Engineering onboarding — Order Service"
 2. What this service does     One sentence + one diagram
 3. Mental model               System Context (where we sit in the world)
 4. The team                   Names, focus areas, who-to-ask-what
 5–8. Container architecture   Component-by-component
 9–12. Critical user flows     Sequence diagrams: checkout, refund, …
13. Data model                 ER diagram of core tables
14. Operational view           Deployment diagram, dashboards, runbooks
15. Conventions                Coding, testing, PR review
16. First-week checklist       Concrete tasks
17. Glossary                   Acronyms
18+ Reference / appendix
```

Good for: onboarding decks, internal documentation, engineering wikis exported as decks.

### Template D — Customer pitch (5–10 slides)

```
1. Cover
2. Their world today           Frame their problem, not your product
3. Why this is hard            Specifics — "this is why incumbents fail"
4. What we do                  In one sentence
5. How it works                One diagram, customer-shaped (not C4!)
6. Proof                       Metric, logo, case study
7. What it costs               Pricing, simple table
8. Next step                   "Pilot for 30 days?" / "Demo next week?"
```

Good for: sales decks, partnership pitches, conference talks.

## Slide shapes that work

| Shape | When |
|---|---|
| **Title + 3 bullets** | The most boring shape. Default. Use 80% of the time. |
| **Title + 1 number** | Single most-important metric. Big font. |
| **Title + full-bleed diagram** | Architecture, sequence, mental model |
| **Title + table** | Comparisons, pricing, decision matrices |
| **Two-column (left text, right diagram)** | Diagram + implications |
| **Section divider** | Full-bleed color, section name only |

Avoid: 4-quadrant slides, slides with 7+ bullets, slides where the title is a question and the body answers it (just put the answer in the title).

## Pairing with rendering skills

| You wrote… | Render with |
|---|---|
| Markdown deck source by hand | [marp](../marp/SKILL.md) |
| A script that fills a template per row of data | [python-pptx](../python-pptx/SKILL.md) |
| Diagrams that need to land in the deck | [diagram-export](../diagram-export/SKILL.md), then embed |

## Anti-patterns

- **The "all our work" slide.** Every accomplishment crammed onto one slide. Split, or move to a doc.
- **The architecture deck with no architecture.** Bullets describing services. Use C4 or quit.
- **The 60-slide deck for a 30-min meeting.** Cut. The first cut is always the easiest 20%.
- **The deck whose final slide is "Q&A" or "Thank you".** Wasted real estate. Restate the ask instead.
- **Reading the slide aloud.** If you'd read it, it shouldn't be on the slide.
- **Animations.** Outside of pedagogical step-throughs, never. They don't survive `.pptx` export from most renderers, distract on Zoom, and confuse exporters.

## Best Practices

1. **Write the speaker notes first.** Yes, first. The notes are the talk. The slides are visual support for the talk.
2. **Outline in plain text before opening any tool.** A deck outline that doesn't work in `.txt` won't work as `.pptx`.
3. **Time-box.** Targets: exec deck 60s/slide, eng review 90s/slide, customer pitch 45s/slide. If your deck doesn't fit the time slot at those rates, cut.
4. **Rehearse once with a colleague who doesn't know the project.** They'll find the slide where you lost them. That's the slide to fix.
5. **One person owns the deck.** Decks-by-committee become decks-by-nobody. Single editor; the team gives input but doesn't push slides.
6. **Save the .md / .py source.** Decks evolve — version-control the source so next quarter's update is a diff, not a rewrite.
