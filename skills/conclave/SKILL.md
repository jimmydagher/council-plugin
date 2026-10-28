---
name: conclave
description: >
  Use to "convene the conclave", "brainstorm this idea with a panel", "what am
  I missing about this idea", "get different perspectives on this", or
  "/council:conclave". Maps an idea rather than picking a winner or ruling on
  it: a panel of independent sub-agents, each a different lens (customer,
  economics, systems, builder, skeptic, risk, operations, trust, ...), forms a
  position blind, cross-examines the others, and takes a final stance. A chair
  reports where the panel converged, where it split, what nobody knows, the
  options it surfaced, and one next step with kill criteria. Flags: --quick (4
  lenses, no cross-examination), --seats N (3-12, default 6).
---

Before anything else, read the "What this council reviews" and "Shared process, every expert" sections of `../../references/shared-context.md`. The area/expert argument rules there do not apply to this skill; its own flags are below.

This skill **explores one idea with a panel and reports what the panel found, including where it disagrees**. To find a stronger version of the idea, point the user to `council:arena`; to get a guilty / not guilty ruling on it as stated, to `council:court`; to review a written document, design or proposal, to `council:it` or `council:business`.

## Arguments

| Flag | Effect |
|------|--------|
| *(none)* | Panel of 6, three rounds |
| `--quick` | Panel of 4, Round 1 only, then the report |
| `--seats N` | Panel of N, whole number 3-12, three rounds |

- Flags are case-insensitive and may come in any order. Everything else the user typed is the idea and its context.
- **Errors** — stop and list the valid flags above when: a flag is not in the table; `--quick` and `--seats` are both given; `--seats` has no value, a non-number, or a number outside 3-12.
- **No idea, or no goal or decision can be inferred** — ask one round of clarifying questions, each with a suggested answer, before spending any sub-agent calls.
- **Decoration guard** — if the user has plainly already decided and wants approval, say so in one line and offer `council:court` instead. If the question is a factual lookup or a cheap, reversible choice, say a direct answer or a small experiment fits better and ask whether to run anyway. Otherwise proceed.

## Cost check

Sub-agent calls: full run = **3N + 1** (N positions, N cross-examinations, N final stances, 1 chair): 3 → 10, 6 → 19, 12 → 37. `--quick` = **N + 1**: 3 → 4, 4 → 5. Plus one per file re-requested for a missing required line.

Before starting, say in one line: panel size, mode and the call count. If the count is over 20, ask for confirmation first.

## Run folder

All files go under `~/.council/conclave/<run-id>/` — `~` is the user's home directory (`%USERPROFILE%` on Windows, `$HOME` elsewhere), resolved when the run starts and used as a full path everywhere (sub-agent briefs get the resolved path). `run-id` = local time `YYYYMMDD-HHMMSS`; if that folder already exists, append `-2`, `-3`, …. Never write into or edit the user's project or the current directory, and never write anywhere else. If the folder can't be created or written, say why and stop — never fall back to the current directory.

```text
~/.council/conclave/<run-id>/
├── notes.md          — the field notes every sub-agent gets
├── panel.md          — the seated lenses (id, lens, counterweight)
├── r1/lNN.md         — blind positions
├── r2/lNN.md         — cross-examinations (full run only)
├── r3/lNN.md         — final stances (full run only)
├── count.md          — the stance count, written by the main session
├── REPORT.md         — written by the chair
├── ledger.md         — prediction and review date, written by the chair
└── state.md          — steps done, next step
```

Use absolute paths in every sub-agent prompt.

**Keep the main session lean:** hold only paths, lens ids and the one-line replies sub-agents return. Read no position or cross-examination; read round 3 files only for their `STANCE` lines.

**Stay out of the panel:** the main session never argues, takes a stance, or edits the count or the report.

**Resume:** `state.md` is the source of truth. After a context compaction, or if interrupted, re-read it and continue from the first unfinished step. A step is finished when its output files exist.

## Process

### 1. Field notes

Write `notes.md`:

```markdown
# Field notes
## The idea
<the user's idea, in their words, plus any context they gave>
## The decision
<what the user is deciding, or "exploring" if nothing yet>
## Goal
<what success looks like>
## Facts stated
<every number, audience, constraint, prior attempt and alternative the user gave — "none stated" if none>
## Assumptions being made
<what the idea takes for granted — "none" only if truly none>
## Unknowns that could change the answer
<what is missing — "not stated" if the user gave no basis>
## Reversibility and deadline
<how hard it is to undo, and when it must be decided — "not stated" if absent>
## Rules of the conclave
- Work only from these notes. A fact they do not state is unknown: label it UNKNOWN or ASSUMPTION, never FACT.
- Say what you think and why. Do not hedge to be agreeable.
```

Fill each section only from what the user said or what is plainly implied. Every sub-agent gets this file unchanged.

Read `lenses.md` (this skill's folder) and seat the first N lenses in its seating order (4 for `--quick`). Write `panel.md` as a table: id, lens, counterweight (the partner id if that lens is seated, else "none seated"). Write `state.md` with the panel and "Next: round 1".

### 2. Round 1 — blind positions

One sub-agent per lens, in waves of at most 8 in parallel. Each gets only its own lens card, copied from `lenses.md`:

> You are lens `<lNN>` on a panel exploring an idea. Your lens — <lens name>: <the lens's Method, Blind spot and Must answer text from lenses.md>
>
> Read the field notes at `<notes.md>`. Read only that file. You decide alone; you will not see any other lens's position.
>
> Take your lens's view of the idea as described. Write your position to `<r1/lNN.md>` in exactly this format, one item per line:
>
> ```text
> POSITION: <one sentence: what you think of the idea, from your lens>
> CLAIM 1 [FACT]: <a claim the notes directly support>
> CLAIM 2 [INFERENCE]: <a claim that follows from the notes but is not stated>
> CLAIM 3 [UNKNOWN]: <something missing that could change the answer>
> BLIND SPOT: <where your own lens could mislead you on this idea>
> ASK: <the one thing you most want answered before deciding>
> ```
>
> Give 3 to 6 claims, numbered, each labeled FACT (the notes state it), INFERENCE (follows from the notes), ASSUMPTION (needed but unverified) or UNKNOWN (missing information). Include at least one UNKNOWN or ASSUMPTION. Nothing else in the file; under about 400 words. Reply with one line: `<lNN>: <your position in a few words>`.

Check each file for a `POSITION` line, at least one `CLAIM` line, `BLIND SPOT` and `ASK`. Re-run a missing-line file once with the same prompt; if still malformed, record that lens as **abstained** and drop it from later rounds. Update `state.md`. In `--quick`, go to step 5.

### 3. Round 2 — cross-examination

One sub-agent per lens that did not abstain, in waves of at most 8:

> You are lens `<lNN>` (<lens name>) on a panel exploring an idea. Your counterweight is <lMM (lens name), or "none seated — use the position you most disagree with">.
>
> Read the field notes at `<notes.md>` and every Round 1 position in `<r1/>`. Read only those files.
>
> Challenge, do not summarize. Write `<r2/lNN.md>` in exactly this format:
>
> ```text
> CHALLENGE l04: "<the exact claim you attack>" — <the evidence it lacks or the scenario where it fails>
> CHALLENGE l09: "<the exact claim you attack>" — <the evidence it lacks or the scenario where it fails>
> VIEW l01: AGREE — <what agreeing costs the idea>
> VIEW l02: DISAGREE — <why>
> VIEW l03: NO VIEW — <why your lens cannot judge it>
> ```
>
> Two `CHALLENGE` lines: the first at your counterweight, the second at any other position; each quotes the claim it attacks. One `VIEW` line for every other lens that filed a position, in id order. AGREE must name what agreement costs the idea, or it is invalid. Challenge only what you believe is wrong or unsupported, and concede what is true. Under about 400 words. Reply with one line: `<lNN>: challenged <ids>`.

Update `state.md`.

### 4. Round 3 — final stance

One sub-agent per lens that did not abstain, in waves of at most 8:

> You are lens `<lNN>` (<lens name>) on a panel exploring an idea. Read the field notes at `<notes.md>`, every Round 1 position in `<r1/>` and every Round 2 cross-examination in `<r2/>`. Read only those files. Pay most attention to the challenges aimed at you.
>
> Decide where you stand now. Write `<r3/lNN.md>` in exactly this format, one item per line:
>
> ```text
> STANCE: BACK IF — <one-line reason, and the condition>
> MOVED: NO — <what changed your mind, or what you held against which challenge>
> COMPROMISE: <what you could accept short of your ideal>
> KILL: <the evidence that would make you drop your stance>
> ```
>
> `STANCE` is BACK (pursue the idea as described), BACK IF (pursue it only if the stated condition is met) or OPPOSE (do not pursue it as described). `MOVED` is YES or NO. If your stance did not change, say which challenge you held against and why it failed. Do not move to agree for its own sake. Under about 300 words. Reply with one line: `<lNN>: <your stance>`.

Check each file for `STANCE`, `MOVED`, `COMPROMISE` and `KILL` lines; re-run once if malformed, otherwise record the lens as **abstained**. Update `state.md`.

### 5. Count

The main session counts; it does not judge. From each round 3 file read only the lines matching:

- `^STANCE: (BACK|BACK IF|OPPOSE) — .+$`
- `^MOVED: (YES|NO) — .+$`

Count stances cast (abstentions excluded). BACK and BACK IF together are the **yes** side. A strict majority of yes: **leaning yes**; a strict majority of OPPOSE: **leaning no**; anything else: **split**. This is a signal for the chair, not a verdict. Examples: 6 lenses, 2 BACK, 2 BACK IF, 2 OPPOSE → leaning yes, 4 to 2. 6 lenses, 3 / 3 → split. 6 lenses, 2 abstained, 2 yes / 2 OPPOSE → split.

Write `count.md`:

```markdown
# Count
Panel: <N> seated, <A> abstained
Reading: <leaning yes | leaning no | split>, <yes> yes (<b> BACK, <bi> BACK IF), <no> OPPOSE
| Lens | Stance | Moved |
|------|--------|-------|
| l01 | <BACK / BACK IF / OPPOSE / abstained> | <YES / NO / –> |
```

In `--quick` there are no stances: write `count.md` as "Not counted: --quick has no final stances." Update `state.md`.

### 6. Chair

One sub-agent:

> You are the chair. Read the field notes at `<notes.md>`, the panel at `<panel.md>`, every file in `<r1/>`, `<r2/>` and `<r3/>` (those that exist) and the count at `<count.md>`. Read only the files named here. You never take a stance of your own. The count is final: copy it exactly and never change it.
>
> Write `<REPORT.md>` in the format below, and `<ledger.md>` as: **Prediction** (what you expect happens if the user follows the recommendation), **Owner** (the user), **Review date** (the user's deadline if the notes give one, otherwise "to be set"), **What would change this** (the evidence from the KILL lines, or the open UNKNOWNs in `--quick`).
>
> Rules: do not average the panel into a middle position; every real disagreement stays a disagreement, with each side's strongest reason. Keep minority stances. Put unresolved items first. Treat agreement as weak evidence if all blind positions were alike, or if no lens moved and none held its stance against a concrete challenge — say so. If a lens had no counterweight, say so. A split panel gets a recommendation that is the test or question that would break the tie, not a pick. Disregard a challenge that quotes no claim and an AGREE that names no cost. Add no option that no lens raised. Reply with one line: `report written: <reading>`.
>
> <the Output structure below, from "## Conclave Report" to the end>

### 7. Result

Mark the run complete in `state.md`, read `REPORT.md`, and show it in chat as written.

## Output structure

## Conclave Report

### Panel

Size, mode (full / quick), the run folder path (the user can delete it), and any lens seated without its counterweight or abstained.

### Unresolved first

Open questions and UNKNOWNs that could change the answer. For each: the lens that raised it and a cheap way to check it.

### Where the panel splits

Each live disagreement: the positions, which lenses hold each, the strongest reason on each side, and the evidence that would settle it. Never merged into a compromise. If the panel did not split, say so, and whether that agreement looks earned or weak.

### Where it converged

Points held by a strict majority after challenge, each labeled FACT / INFERENCE / ASSUMPTION, with how hard it was challenged. In `--quick`, points raised by a majority of blind positions, noting they were not cross-examined.

### Options surfaced

Directions any lens raised that the user had not stated, each with its source lens. Not ranked into a winner.

### Count

The reading from `count.md` (leaning yes / leaning no / split, with the numbers), or "not counted" in `--quick`.

### Recommendation

The chair's recommendation: what to do, acceptable compromises, **kill criteria** (the evidence that should make the user stop), and one concrete next step doable this week. For a split panel, the test or question that would break the tie.

### Ledger

Prediction, owner, review date and what would change the answer (from `ledger.md`).

### Next step

One line: `/council:arena` to build stronger versions of an option; `/council:court` to try the leading version; `/council:business` or `/council:it` once it is written up.

*This report is a structured set of perspectives from language models, not professional advice, and a panel agreeing is not proof.*
