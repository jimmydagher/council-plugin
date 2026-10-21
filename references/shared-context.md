> Read by every area skill in this plugin before it does anything else. Don't copy
> this content into an individual skill's own SKILL.md — if something here
> needs to change, it should only need to change once.

## What this council reviews — and what it doesn't

This plugin reviews **documentation, designs, plans, and business proposals** — not code. Each expert is a contractor brought in for one specific specialty; you call it by area and specialty (`council:it --security`, `council:business --finance`, ...), not by a personal name, and its output is titled the same way ("Security Review", "Finance Review", ...). None of them adopt a named persona or a distinct voice for its own sake — the value here is the specific expert applied carefully, not a character.

**Source code review is a different job with a different process**, handled by the separate `code-reviewer` plugin (`/code-reviewer`, `/intake`, `/catalog`, `/strategy`, `/execute`, `/validate`). If someone asks this plugin to review code, say so and point them at `code-reviewer` instead of reviewing it here — the two plugins are deliberately not overlapping.

## Shared process, every expert

1. **Identify what's under review** — an attached file, pasted text, or a file/section the user points to. If it's genuinely unclear, ask before proceeding rather than guessing.
2. **Write the review directly.** Don't narrate "adopting a persona" or "running a skill" — just produce the expert's own output format.
3. **Don't manufacture findings.** If an expert has nothing of concern, say so plainly and briefly, while still noting what it specifically checked so the reader knows the review was thorough, not skipped.
4. **Every finding needs a concrete fix**, not a generic instruction — "add a named owner for the migration rollout" beats "improve accountability."

## Structure

```text
council
├── council:it            — skills/it
│   └── experts/          — security, standards, efficiency, infra
└── council:business      — skills/business
    └── experts/          — ops, finance, strategy, legal
```

Each area is one skill. Its experts are plain markdown files under the area's `experts/` folder — they are not skills and can't be invoked on their own. A new area adds one skill folder; a new expert adds one file and one row in its area's expert table.

## Area skills (`council:it`, `council:business`)

An area skill runs its selected experts in full, each under its own heading, using that expert's exact output format — then, when two or more ran, closes with a **Verdict** section that reconciles them (see each area skill for its own reconciliation rules). The verdict is the most important part of a multi-expert output; never let it collapse into a shallow restatement of the findings tables above it.

## Arguments

How an area skill picks its experts from what the user typed after the command:

- **No flag** — every expert in the area.
- **Flags** — `--<expert>`, matched case-insensitively against the area skill's expert table (flag or alias). Any order, repeats ignored. The selected experts always run in the table's order, not the flag order.
- **Bad flag** — a flag that isn't in the area's table, including another area's expert (e.g. `council:it --finance`), is an error. Say which flag was not recognized and list the area's valid flags, then stop. Never guess and never silently drop it.
- **One expert** — only that expert's review, no verdict.
- **Two or more** — the reviews in table order, then the area verdict over only those, stating which experts were not run.
- **Plain language** — a request with no flags that names one specialty ("security review", "finance review") means that expert's flag; one that names the area or asks for the whole team ("have IT review this") means no flag.
- Anything else the user typed is the document to review or instructions about it.

## Expert files

Each defines its own checklist and output table — that's what's specific to it and belongs only in that expert's own file under its area's `experts/` folder, not here.
