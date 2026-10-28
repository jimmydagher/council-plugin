---
name: arena
description: >
  Use to "arena this idea", "make versions of this idea fight",
  "stress-test this idea", "brainstorm the best version of ...", "find the
  strongest version of this idea", or "/council:arena". Generates ideas
  rather than reviewing a document: several sub-agents, each dealt a
  different strategy card, pitch their own version of the idea, attack and
  defend in single-elimination matches, and a blind judge scores each match
  on a fixed rubric. Returns the champion pitch, ideas worth salvaging from
  the losers, and its open risks. Flags: --quick (4 competitors),
  --field N (2-16, default 8), --baseline (also judge against the user's
  current version).
---

Before anything else, read the "What this council reviews" and "Shared process, every expert" sections of `../../references/shared-context.md`. The area/expert argument rules there do not apply to this skill; its own flags are below.

This skill **generates and stress-tests an idea**. To review an existing document, design or proposal, point the user to `council:it` or `council:business` instead.

## Arguments

| Flag | Effect |
|------|--------|
| *(none)* | Field of 8 |
| `--quick` | Field of 4 |
| `--field N` | Field of N, whole number 2–16 |
| `--baseline` | Also judge the champion against the user's current version |

- Flags are case-insensitive and may come in any order. Everything else the user typed is the idea and its context.
- **Errors** — stop and list the valid flags above when: a flag is not in the table; `--quick` and `--field` are both given; `--field` has no value, a non-number, or a number outside 2–16.
- **No idea, or too vague to brief** (no goal or no audience can be inferred) — ask one round of clarifying questions, each with a suggested answer, before spending any sub-agent calls.
- **`--baseline` without a baseline** — the baseline is the user's current version of the idea (pasted text or a file). If none was given, ask for it.

## Cost check

Sub-agent calls = **N pitches + 5 × (N − 1) match calls**, plus 1 with `--baseline`. (4 → 19, 8 → 43, 16 → 91.)

Before starting, say in one line: field size, number of rounds, and the call count. If N > 8, wait for the user's go-ahead.

## Run folder

All files go under `~/.council/arena/<run-id>/` — `~` is the user's home directory (`%USERPROFILE%` on Windows, `$HOME` elsewhere), resolved when the run starts and used as a full path everywhere (sub-agent briefs get the resolved path). `run-id` = local time `YYYYMMDD-HHMMSS`; if that folder already exists, append `-2`, `-3`, …. Never write into or edit the user's project or the current directory, and never write anywhere else. If the folder can't be created or written, say why and stop — never fall back to the current directory.

```text
~/.council/arena/<run-id>/
├── brief.md                      — the one brief every competitor gets
├── deal.md                       — competitor → card (only the main session and competitors read it; judges never do)
├── baseline.md                   — the user's version (--baseline only)
├── pitches/cNN.md                — each competitor's current pitch (revised in place after each match)
├── rounds/rR/mM/
│   ├── attacks-on-cNN.md         — one per side
│   ├── defense-cNN.md            — one per side
│   └── judgment.md
├── baseline-judgment.md          — (--baseline only)
└── state.md                      — bracket, results, next step
```

Use absolute paths in every sub-agent prompt.

**Keep the main session lean:** hold only paths, competitor ids and the one-line results sub-agents return. Do not read pitch, attack or defense files until the final output.

**Resume:** `state.md` is the source of truth. After a context compaction, or if interrupted, re-read `state.md` and continue from the first unfinished step. A step is finished when its output file exists.

## Process

### 1. Brief

Write `brief.md`:

```markdown
# Arena brief
## The idea
<the user's idea, in their words, plus any context they gave>
## Goal
<what success looks like>
## Audience
<who it is for>
## Constraints
<budget, time, people, technology, rules — "none stated" if none>
## A good pitch
Follows the pitch format in this brief, stays under about 700 words (revisions included — tighten rather than append), is concrete enough to start next week, and is judged on value (30), feasibility (25), robustness to attack (20), specificity (15) and originality (10).
## Pitch format
# <one-line pitch>
## How it works
## Who it serves
## Why now
## Cost and effort
## Top risks
## First three steps
```

Fill Goal, Audience and Constraints only from what the user said or what is plainly implied; write "not stated" otherwise. Every competitor gets this file unchanged.

### 2. Deal

Read `cards.md` (this skill's folder). Number the competitors `c01` … `cNN` and deal cards by its dealing rule. Write `deal.md` as a table: id, lens, shape, bias, each with its one-line instruction. Write `state.md` with the competitor list, the planned rounds, and "Next: pitches".

### 3. Pitch

One sub-agent per competitor, in waves of at most 8 in parallel:

> You are competitor `<id>` in an idea tournament. Read the brief at `<brief.md>`. Your strategy card:
> - Lens — <name>: <instruction>
> - Shape — <name>: <instruction>
> - Bias — <name>: <instruction>
>
> Write your version of the idea, shaped by your card, to `<pitches/id.md>` in exactly the brief's pitch format. Be concrete: name the audience, the mechanism, the cost and the first steps. Do not mention your card, lens, shape or bias anywhere in the file — a judge must not be able to tell which card produced it. Write nothing else. Reply with one line: `<id> pitched: <the one-line pitch>`.

Update `state.md`.

### 4. Rounds

Repeat until one competitor remains. Total matches = N − 1.

**Pairing.** Take the competitors still in, in id order.
- If the count is odd, the bye goes to the highest-numbered competitor who has not had a bye yet (if all have, the highest-numbered). It advances without a match.
- Pair the rest in order: 1st v 2nd, 3rd v 4th, …
- If a pair shares a lens, swap its second member with the next pair's second member (the previous pair's, if it is the last pair).

Record the round's matches and bye in `state.md` before running them. Matches are `rR/mM`, numbered from 1 within each round.

Each round runs in three waves (at most 8 sub-agents in parallel; split larger waves):

**a. Attack** — two sub-agents per match, one per side:

> You are competitor `<attacker>` in an idea tournament. Your strategy card: <lens / shape / bias with instructions>. Read the brief at `<brief.md>`, your own pitch at `<pitches/attacker.md>`, and your opponent's pitch at `<pitches/defender.md>`.
>
> Write up to five attacks on your opponent's pitch to `<rounds/rR/mM/attacks-on-defender.md>`, strongest first. Each: a number, a severity label — FATAL (the idea cannot deliver its goal at all), MAJOR (it loses much of its value or needs a large redesign) or MINOR (a small fix closes it) — and a concrete failure scenario. No vague worries; if you find nothing serious, say so and list only what you found. Do not mention your card. Reply with one line: `<attacker> → <defender>: <count> attacks (<F> fatal, <M> major)`.

**b. Defend and revise** — two sub-agents per match, one per side:

> You are competitor `<defender>` in an idea tournament. Your strategy card: <lens / shape / bias with instructions>. Read the brief at `<brief.md>`, your pitch at `<pitches/defender.md>`, and the attacks on it at `<rounds/rR/mM/attacks-on-defender.md>`.
>
> 1. Write `<rounds/rR/mM/defense-defender.md>`: for each attack, by number, either **Concede** (and say what you changed) or **Rebut** (with evidence or reasoning — not just disagreement). Concede only what is actually true of your pitch; rebut attacks that misread it, lack a concrete scenario, or overstate their severity — conceding everything is as wrong as rebutting everything.
> 2. Overwrite `<pitches/defender.md>` with your revised pitch, same format, fixing what you conceded. Keep what works; do not water the idea down to dodge attacks. Do not mention your card.
>
> Reply with one line: `<defender> defended: <conceded> conceded, <rebutted> rebutted`.

**c. Judge** — one sub-agent per match. It never gets `deal.md` or any card:

> You are the judge of match `<rR/mM>` in an idea tournament. Read the rubric at `<this skill's rubric.md>` and the brief at `<brief.md>`. Then read, for each side `<A>` and `<B>`: the revised pitch `<pitches/X.md>`, the attacks on it `<rounds/rR/mM/attacks-on-X.md>`, and its defense `<rounds/rR/mM/defense-X.md>`.
>
> Verify every attack (Holds / Answered / Unfounded), score both revised pitches on the rubric, apply the fatal-flaw rule, and write `<rounds/rR/mM/judgment.md>` in the rubric's judgment format. Read only the files named here. Judge only what is written; ignore which side argues more confidently. Reply with exactly one line: `WINNER <id> | <A> <total> fatal:<yes/no> | <B> <total> fatal:<yes/no>`.

Record each winner, both totals, and the loser's elimination round in `state.md`.

### 5. Baseline (only with `--baseline`)

Write the user's version to `baseline.md`. One sub-agent, given the two files under neutral names — randomly assign the champion and the baseline to "Version 1" and "Version 2", and note the assignment in `state.md` only:

> You are a blind judge. Read the rubric at `<rubric.md>` and the brief at `<brief.md>`. Version 1 is at `<path>`, Version 2 at `<path>`. Neither has been attacked yet: for each, write the three strongest attacks yourself with severity labels and decide whether each holds. Then score both on the rubric, apply the fatal-flaw rule, and write `<baseline-judgment.md>` in the rubric's judgment format, using "Version 1" and "Version 2" as ids. Reply with exactly one line: `WINNER Version <n> | Version 1 <total> | Version 2 <total>`.

Report the result even if the baseline wins.

### 6. Result

Mark the run complete in `state.md`. Now read the champion's pitch, its attacks, defenses and judgments, and the eliminated competitors' final pitches, then write the output.

## Output structure

## Arena Result

One line: field size, rounds, the run folder path (the user can delete it), and that the champion is the strongest idea found, not a guarantee it is right.

### Champion — `<id>`

The champion's final pitch, as written. Then its card (lens / shape / bias) and the rounds it won, with each match's score.

### Attacks it withstood

| Round | From | Severity | Attack | How it was answered |
|-------|------|----------|--------|---------------------|

Only attacks the judges marked **Answered**.

### Salvage

Up to five strong ideas from eliminated pitches worth grafting onto the champion — each one sentence, with its source competitor and a one-line note on how it fits. Do not pad: if fewer are worth it, list fewer; if none, say so.

### Open risks

Attacks on the champion that a judge marked **Holds**, or that it conceded without fully fixing — each with the concrete next step that would close it. If none, say so.

### Baseline *(with `--baseline` only)*

Champion and baseline totals, the winner, and one sentence on why.

### Next step

One line. When the champion is a business or technical proposal, suggest writing it up and running `/council:business` or `/council:it` on it.
