---
name: court
description: >
  Use to "put this idea on trial", "court this idea", "jury this decision",
  "make the case for and against this", "find the holes before I commit",
  or "/council:court". Returns a verdict on one idea or decision as the user
  stated it, rather than improving it or reviewing a document: a prosecutor
  files numbered charges, a defense answers them, a jury of independent
  sub-agents (each a different business or IT perspective) votes on every
  charge and on the idea overall without seeing each other's votes, and a
  judge writes the verdict with the changes that would flip the most votes.
  Flags: --quick (5 jurors), --jury N (3-12, default 9).
---

Before anything else, read the "What this council reviews" and "Shared process, every expert" sections of `../../references/shared-context.md`. The area/expert argument rules there do not apply to this skill; its own flags are below.

This skill **tries one idea as stated and returns a verdict**. To find a stronger version of the idea, point the user to `council:arena`; to review an existing document, design or proposal, to `council:it` or `council:business`.

## Arguments

| Flag | Effect |
|------|--------|
| *(none)* | Jury of 9 |
| `--quick` | Jury of 5 |
| `--jury N` | Jury of N, whole number 3–12 |

- Flags are case-insensitive and may come in any order. Everything else the user typed is the idea and its context.
- **Errors** — stop and list the valid flags above when: a flag is not in the table; `--quick` and `--jury` are both given; `--jury` has no value, a non-number, or a number outside 3–12.
- **No idea, or no goal or decision can be inferred** — ask one round of clarifying questions, each with a suggested answer, before spending any sub-agent calls. The jury judges on the specifics given, so ask for the numbers, audience, what has been tried and the alternative when they are missing and matter.

## Cost check

Sub-agent calls = **N + 5**: 2 openings, 2 rebuttals, N jurors, 1 judge. (5 → 10, 9 → 14, 12 → 17; plus one per malformed ballot re-run.)

Before starting, say in one line: jury size and the call count. No confirmation is needed.

## Run folder

All files go under `~/.council/court/<run-id>/` — `~` is the user's home directory (`%USERPROFILE%` on Windows, `$HOME` elsewhere), resolved when the run starts and used as a full path everywhere (sub-agent briefs get the resolved path). `run-id` = local time `YYYYMMDD-HHMMSS`; if that folder already exists, append `-2`, `-3`, …. Never write into or edit the user's project or the current directory, and never write anywhere else. If the folder can't be created or written, say why and stop — never fall back to the current directory.

```text
~/.council/court/<run-id>/
├── case.md                          — the one case file every sub-agent gets
├── jury.md                          — the seated jurors (id, seat, juror)
├── filings/
│   ├── prosecution-opening.md
│   ├── defense-opening.md
│   ├── prosecution-rebuttal.md
│   └── defense-rebuttal.md
├── ballots/jNN.md                   — one per juror
├── tally.md                         — the count, written by the main session
├── VERDICT.md                       — written by the judge
└── state.md                         — steps done, next step
```

Use absolute paths in every sub-agent prompt.

**Keep the main session lean:** hold only paths, juror ids and the one-line replies sub-agents return. Read no filing until the end; read ballots only for their vote lines (see Tally).

**Stay out of the case:** the main session never argues a side, never votes, and never edits the tally or the verdict.

**Resume:** `state.md` is the source of truth. After a context compaction, or if interrupted, re-read `state.md` and continue from the first unfinished step. A step is finished when its output file exists.

## Process

### 1. Case file

Write `case.md`:

```markdown
# Case file
## The idea
<the user's idea, in their words, plus any context they gave>
## The decision
<what the user is deciding — e.g. "launch this", "quit to do this", "adopt this tool">
## Goal
<what success looks like>
## Stated facts
<every number, audience, constraint, prior attempt and alternative the user gave — "none stated" if none>
## Rules of the court
- Argue and judge only from this case file and the filings. A fact it does not state is unknown: argue it as a gap, never assume it either way.
- The question is whether the idea, as described, achieves its goal. Not whether a better idea exists.
- GUILTY means the idea fails as described. NOT GUILTY means it holds up as described.
```

Fill The decision, Goal and Stated facts only from what the user said or what is plainly implied; write "not stated" otherwise. Every sub-agent gets this file unchanged.

Read `jurors.md` (this skill's folder) and seat the first N jurors in its seating order. Write `jury.md` as a table: id, seat, juror. Write `state.md` with the jury and "Next: openings".

### 2. Openings

Two sub-agents in parallel:

**Prosecution:**

> You are the prosecutor. Read the case file at `<case.md>`. Build the strongest **honest** case that the idea fails as described. File 1 to 5 numbered charges, strongest first, to `<filings/prosecution-opening.md>`, each as:
>
> `## Charge <n>: <one-line claim>` — then **Rests on:** the fact in the case file (or the gap in it) the charge depends on, and **Failure scenario:** a concrete way the idea fails because of it.
>
> File only charges you believe hold; a weak charge discredits the strong ones. If you find fewer than five, file fewer. Under about 600 words. Reply with one line: `prosecution filed <count> charges`.

**Defense:**

> You are the defense. Read the case file at `<case.md>`. Build the strongest **honest** case that the idea works as described: what it achieves, for whom, and which facts in the case file support it. Name its real strengths and the conditions under which it succeeds; do not claim facts the case file doesn't state. Write it to `<filings/defense-opening.md>`, under about 600 words. Reply with one line: `defense opened: <its strongest point in a few words>`.

Update `state.md`.

### 3. Rebuttals

Two sub-agents in parallel; each reads both openings:

**Prosecution rebuttal:**

> You are the prosecutor. Read the case file at `<case.md>`, your opening at `<filings/prosecution-opening.md>`, and the defense's opening at `<filings/defense-opening.md>`. Answer the defense's claims point by point: which rest on facts the case file doesn't state, which don't follow, and which you accept. Accept what is true. You may withdraw a charge the defense's opening shows is wrong; you may not add new charges. Write `<filings/prosecution-rebuttal.md>`, under about 400 words. Reply with one line: `prosecution rebutted: <withdrawn count> charges withdrawn`.

**Defense rebuttal:**

> You are the defense. Read the case file at `<case.md>`, your opening at `<filings/defense-opening.md>`, and the prosecution's opening at `<filings/prosecution-opening.md>`. Answer every charge by number: **Concede** (and say what it costs the idea) or **Rebut** (with evidence from the case file or reasoning — not just disagreement). Concede only what is true; rebut charges that misread the case, lack a concrete scenario, or overstate the harm. Conceding everything is as wrong as rebutting everything. Write `<filings/defense-rebuttal.md>`, under about 400 words. Reply with one line: `defense rebutted: <conceded> conceded, <rebutted> rebutted`.

Record withdrawn charges in `state.md`. A withdrawn charge stays numbered and is not voted on. If every charge is withdrawn, the ballots carry no `CHARGE` lines and the jury votes on the overall verdict only.

### 4. Jury

One sub-agent per seated juror, in waves of at most 8 in parallel. Each gets only its own persona, copied from `jurors.md`:

> You are juror `<jNN>` on a jury deciding whether an idea holds up. Your perspective — <juror name> (<seat>): <the juror's paragraph from jurors.md>
>
> Read the case file at `<case.md>` and the four filings: `<filings/prosecution-opening.md>`, `<filings/defense-opening.md>`, `<filings/prosecution-rebuttal.md>`, `<filings/defense-rebuttal.md>`. Read only the files named here. You decide alone; you will not see any other juror's vote.
>
> Judge from your perspective but on the record: a claim with no support in the case file or filings counts for nothing, from either side. Charges <withdrawn list, or "none"> were withdrawn; skip them.
>
> Write your ballot to `<ballots/jNN.md>` in exactly this format, one line each, using an em dash before each reason:
>
> ```text
> CHARGE 1: PROVEN — <one-line reason>
> CHARGE 2: NOT PROVEN — <one-line reason>
> VERDICT: GUILTY — <one-line reason>
> FLIP: <the fewest changes to the idea that would flip your verdict, separated by semicolons>
> ```
>
> One `CHARGE` line for every charge not withdrawn, in number order, each PROVEN or NOT PROVEN. `VERDICT` is GUILTY (the idea fails as described) or NOT GUILTY (it holds up as described). `FLIP` names only what you actually need, most important first: your vote must flip once every change listed is made. Nothing else in the file. Reply with one line: `<jNN>: <GUILTY or NOT GUILTY>`.

### 5. Tally

The main session counts; it does not judge. From each ballot read only lines matching:

- `^CHARGE (\d+): (PROVEN|NOT PROVEN) — .+$`
- `^VERDICT: (GUILTY|NOT GUILTY) — .+$`
- `^FLIP: .+$`

A ballot missing a `CHARGE` line for any charge being voted on, its `VERDICT` line or its `FLIP` line is malformed: re-run that juror once with the same prompt. If it is still malformed, record that juror as **abstained** on everything.

Count votes cast (abstentions excluded):

- **Charge** — more PROVEN than NOT PROVEN: **sustained**; more NOT PROVEN: **dismissed**; equal: **hung**.
- **Overall** — more GUILTY than NOT GUILTY: **GUILTY**; more NOT GUILTY: **NOT GUILTY**; equal: **HUNG**.

Examples: 9 jurors, 5 GUILTY / 4 NOT GUILTY → GUILTY, 5 to 4. 9 jurors, one abstained, 4 / 4 → HUNG, 4 to 4 (1 abstained).

Write `tally.md`:

```markdown
# Tally
Jury: <N> seated, <A> abstained
Verdict: <GUILTY | NOT GUILTY | HUNG>, <for> to <against>
| Charge | Proven | Not proven | Result |
|--------|--------|------------|--------|
| 1 | <n> | <n> | <sustained / dismissed / hung> |
Withdrawn: <charge numbers, or none>
| Juror | Verdict |
|-------|---------|
| j01 | <GUILTY / NOT GUILTY / abstained> |
```

Update `state.md`.

### 6. Judgment

One sub-agent:

> You are the judge. Read the case file at `<case.md>`, the four filings in `<filings/>`, every ballot in `<ballots/>`, the jury list at `<jury.md>`, and the tally at `<tally.md>`. Read only the files named here. The tally is final: copy its counts exactly and never change them.
>
> Write `<VERDICT.md>` in the format below. For **Conditions for acquittal**, split the FLIP lines of jurors who voted GUILTY into single changes and group the same change across jurors; rank the changes by how many jurors ask for each, most first, naming them. A juror's vote flips only when every change on its FLIP line is made, so end the section with one line per combination that flips votes (e.g. "changes 1 and 2 flip j04 and j05"). For **What must not change**, do the same with the FLIP lines of jurors who voted NOT GUILTY. Do not add changes no juror named. Reply with one line: `verdict written: <verdict>, <for> to <against>`.
>
> <the Output structure below, from "## Court Verdict" to the end>

### 7. Result

Mark the run complete in `state.md`, read `VERDICT.md`, and show it in chat as written.

## Output structure

## Court Verdict

One line: jury size, the run folder path (the user can delete it).

### Verdict

**GUILTY / NOT GUILTY / HUNG, <for> to <against>** (plus abstentions, if any) — then one sentence on what decided it.

### Charges

| # | Charge | Result | Proven – not proven | Why |
|---|--------|--------|---------------------|-----|

Withdrawn charges are listed with "withdrawn" as the result.

### What the defense got right

The strengths that held up — points the prosecution accepted or the jurors cited in NOT GUILTY votes or NOT PROVEN reasons. If none held, say so.

### Jurors

| Juror | Perspective | Verdict | Reason |
|-------|-------------|---------|--------|

### Conditions for acquittal

Ranked changes, each with the GUILTY jurors who ask for it, then which combination of changes flips which votes. If no juror voted GUILTY, say "none needed".

### What must not change

Changes that would turn NOT GUILTY votes, each with its count. If no juror voted NOT GUILTY, omit this section.

### Next step

One line. GUILTY or HUNG: suggest `/council:arena` to find a stronger version of the idea. NOT GUILTY: suggest writing it up and running `/council:business` or `/council:it` on it.

*This verdict is a structured second opinion from language models, not legal, financial or professional advice.*
