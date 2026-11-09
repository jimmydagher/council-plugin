---
name: council
description: >
  Use to "convene the whole council", "run everything on this", "full council
  review", or "/council" alone. Activates every council skill on one document
  or idea, in a fixed order: council:it, council:business, council:conclave,
  council:court, council:arena, then one combined summary. Flags: --quick
  (passed to conclave, court and arena), --peer (passed to it and business).
  Token-heavy by design. To run one skill or expert instead, use
  /council:<skill> (e.g. /council:it --security).
argument-hint: "[--quick] [--peer] [document|idea]"
---

# Council: all skills

Before anything else, read `../../references/shared-context.md`.

## Arguments

- `--quick` is passed to `council:conclave`, `council:court` and `council:arena`. `--peer` is passed to `council:it` and `council:business`. Both are case-insensitive, in any order, repeats ignored.
- An expert flag (`--security`, `--finance`, ...) or a skill-specific flag (`--field`, `--seats`, `--jury`, `--baseline`) is an error here: say it was not recognized, point to `/council:<skill>` for it, and stop.
- Anything else is the document or idea. If it is unclear, ask before starting.

## How the run goes

1. **Say what is about to run** — all five skills, the flags passed on, and that it is token-heavy — then start; don't ask for confirmation.
2. **Run in this order**, reading each skill's `SKILL.md` (`../<name>/SKILL.md`) and following it exactly with its own process, output format and run-file rules, each under its own heading: `it`, `business`, `conclave`, `court`, `arena`. Announce each ("Step 3/5 — `council:conclave`").
3. **A skill that doesn't fit the input still runs** as far as it can: the two area skills review a document, so for a bare idea give them the idea written out as a short proposal and say so; the three idea skills take the document's central proposal as the idea, stated once and reused so all three work on the same wording.
4. **Run files** go only under `~/.council/<skill>/<run-id>/`, never in the project.

## Council Summary

Close with one section, built from what the five skills actually returned and nothing new:

- **Where they agree** — findings or concerns raised by two or more skills.
- **Where they conflict** — each conflict and what would settle it.
- **Verdict and next step** — the court's verdict, the IT and business verdicts, the arena's champion version, and one concrete next step.

Don't restate the five outputs; link back to them by heading.
