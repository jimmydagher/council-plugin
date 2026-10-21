> Read by `council:it` and `council:business` only when `--peer` is set. The area skill supplies the area name, the selected experts, the document, its verdict format and its precedence default; this file supplies everything else. Don't copy it into an area skill.

# Peer review (`--peer`)

With `--peer`, the selected experts don't share one context. Each one reviews the document as an **independent sub-agent**, then checks the **other experts' findings anonymously** (never its own), the main session tallies the marks mechanically, and a separate **chair** writes the area verdict from the reviews and the tally. The question it answers: which findings hold up when the other specialists look at them?

## Preconditions

- Two or more experts selected. `--peer` with one expert is an error: say "peer review needs two or more experts; add an expert flag or drop --peer" and stop.
- The document is identified (shared process, step 1). If it's unclear, ask before spending any sub-agent calls.

## Cost check

Sub-agent calls = **2N + 1** (N reviews, N peer checks, 1 chair): 2 → 5, 3 → 7, 4 → 9. Fewer when an expert has no findings to check (see Stage 2). Plus one per file re-requested for a missing closing block. Before starting, say in one line: the experts, the mode and the call count. No confirmation step.

## Run folder

All files go under `.council/<run-id>/` in the current directory, `run-id` = local time `YYYYMMDD-HHMMSS`. Never write anywhere else and never edit the user's project.

```text
.council/<run-id>/
├── brief.md                 — area, experts, document path (or the pasted text)
├── reviews/<expert>.md      — Stage 1 reviews
├── findings.md              — every finding, anonymized as F1, F2, …
├── labels.md                — F number → expert (never given to a peer)
├── peer/<expert>-input.md   — findings.md without that expert's own findings
├── peer/<expert>.md         — Stage 2 peer checks
├── tally.md                 — written by the main session
├── VERDICT.md               — written by the chair
└── state.md                 — steps done, next step
```

Use absolute paths in every sub-agent prompt. `<expert>` is the flag name without dashes (`security`, `finance`, …).

**Keep the main session lean:** hold only paths, the parsed closing-block lines and the one-line replies. It never reviews, marks a finding, or edits the tally or the verdict.

**Resume:** `state.md` is the source of truth. After a context compaction, or if interrupted, re-read it and continue from the first unfinished step. A step is finished when its output files exist.

## Process

### 1. Brief

Write `brief.md`: the area, the selected experts in canonical order with their expert file paths, the document's path (or the pasted text in full, verbatim), and any instructions the user gave about it. Write `state.md` with "Next: stage 1".

### 2. Stage 1 — independent reviews

One sub-agent per selected expert, all in parallel:

> You are the <Review title> expert on the <area> council. Read the brief at `<brief.md>`, the document it names, and your expert definition at `<experts/<expert>.md>`. Read only those files; you will not see any other expert's review.
>
> Review the document exactly as your expert definition says, in its exact output format, following the shared process: don't manufacture findings, and give every finding a concrete fix. Write it to `<reviews/<expert>.md>`, then end the file with a closing block listing every finding from your review, one per line:
>
> ```text
> FINDINGS:
> - High | <the finding in one line> | <the concrete fix in one line>
> - Low | <the finding in one line> | <the concrete fix in one line>
> ```
>
> Severity is `Critical`, `High`, `Medium` or `Low`: use your definition's own severity if it has one, otherwise rate the finding's impact on the document's goal. If you found nothing of concern, end with the single line `FINDINGS: none`. Reply with one line: `<expert>: <count> findings`.

Check each file for a `FINDINGS:` line, followed by finding lines or `none`. Re-run a file without one once with the same prompt; if it is still malformed or the sub-agent failed, record that expert as **not run** (no findings, no peer check). With fewer than two reviews left, stop: say peer review couldn't run and offer `/council:<area>` without `--peer`. Update `state.md`.

### 3. Anonymize

Mechanical; the main session judges nothing here.

- Take every finding line from every review. Order them round-robin across experts, starting with the **last** expert in canonical order: its first finding, then the previous expert's first finding, and so on, then everyone's second findings, skipping experts that ran out. Number them `F1`, `F2`, … in that order.
- Write `findings.md`: one line per finding, `F<n> | <severity> | <finding> | <fix>`. No expert names.
- Write `labels.md`: `F<n> → <expert>`, one per line.
- For each expert, write `peer/<expert>-input.md`: `findings.md` without that expert's own lines. The numbers stay as they are.

Update `state.md`.

### 4. Stage 2 — peer check

One sub-agent per expert that has a review and a non-empty `peer/<expert>-input.md`, all in parallel. An expert whose input is empty (every other expert wrote `FINDINGS: none`) gets no peer check and no call; the tally says so. If no expert found anything, skip stages 2 and 5 and give the chair `tally.md` reading "No findings to check".

> You are the <Review title> expert on the <area> council. Read the brief at `<brief.md>`, the document it names, your expert definition at `<experts/<expert>.md>`, your own review at `<reviews/<expert>.md>`, and the findings at `<peer/<expert>-input.md>`. Read only those files. The findings came from the other experts; you don't know which one wrote which, and your own findings have been left out.
>
> Check each finding against the document from your specialty. Write `<peer/<expert>.md>` in exactly this format, one item per line:
>
> ```text
> F3: HOLDS — <why the document shows this is a real problem>
> F7: OVERSTATED — should be Low: <why the severity is too high>
> F1: WRONG — <what in the document contradicts it>
> F5: OUT OF LANE — <why your specialty can't judge it>
> TOP: F7, F3, F1
> MISSED:
> - Medium | <a finding nobody raised> | <its concrete fix>
> ```
>
> One `F<n>:` line for every finding shown, in number order. HOLDS: the problem is real at that severity. OVERSTATED: real, but lower; name the severity it should have. WRONG: the document doesn't support it, or the fix would make things worse. OUT OF LANE: your specialty can't judge the finding's main risk — say so rather than guess, and note any in-lane part in the reason. Never mark OVERSTATED or WRONG because of a side of the finding you can't judge. `TOP` lists the three findings that matter most to the document, best first (fewer if fewer were shown). Under `MISSED`, at most two findings that are in neither your own review nor the findings shown, in the same line format, or write `MISSED: none`. Mark only what you believe; agreeing by default is not a check. Keep reasons to one line. Reply with one line: `<expert>: <holds>/<overstated>/<wrong> marked`.

Check each file for at least one `F<n>:` line and a `TOP:` line. Re-run once if malformed; if still malformed or failed, record that expert's peer check as **not run** (its marks are absent). Update `state.md`.

### 5. Tally

The main session counts; it does not judge. From each peer file read only the lines matching:

- `^F(\d+): (HOLDS|OVERSTATED|WRONG|OUT OF LANE) — .+$`
- `^TOP: F\d+(, F\d+){0,2}$`
- `^- (Critical|High|Medium|Low) \| .+ \| .+$` after `MISSED:`

Rules:

- Ignore, and note under **Ignored** in the tally, any mark or `TOP` entry on a number that wasn't in that expert's input (including its own findings), and any second mark on the same number from the same expert.
- **In-lane marks** = HOLDS + OVERSTATED + WRONG; OUT OF LANE is not counted.
- **Points**: 3 for each first place in a `TOP` line, 2 for second, 1 for third.
- **Status**: **upheld** if HOLDS is a strict majority of the in-lane marks; **contested** if there is at least one in-lane mark and OVERSTATED + WRONG is at least HOLDS; **unchecked** if there are no in-lane marks.
- `MISSED` findings are **unreviewed**: listed with who raised them, never counted.

Examples: 3 peers, HOLDS / HOLDS / WRONG → upheld. HOLDS / OVERSTATED → contested (tie). OUT OF LANE / OUT OF LANE → unchecked.

Write `tally.md`:

```markdown
# Peer tally
Experts: <N> reviewed, <P> peer-checked, not run: <list or none>
| Finding | Expert | Severity | Holds | Overstated | Wrong | Points | Status |
|---------|--------|----------|-------|------------|-------|--------|--------|
| F3 | <expert> | High | 2 | 0 | 1 | 5 | upheld |
## Unreviewed (MISSED)
- <severity> | <finding> | <fix> — raised by <expert>
## Ignored
- <expert>: <the line and why, or "none">
```

Rows are ordered by status (upheld, contested, unchecked), then points, highest first. Update `state.md`.

### 6. Chair

One sub-agent that wrote no review:

> You chair the <area> council's peer review. Read the brief at `<brief.md>`, the document it names, every review in `<reviews/>`, the tally at `<tally.md>`, the labels at `<labels.md>`, and the area skill at `<skills/<area>/SKILL.md>` for the verdict format and its precedence default. Read only those files. You did not review the document and you cast no marks.
>
> Write `<VERDICT.md>` in the area skill's verdict format (where they agree, where they conflict, resolution, single verdict), using the tally as evidence:
> - An upheld finding with high points weighs more than one raised by a single expert. A contested finding is never dropped: say what check in the document or with the user would settle it.
> - Keep the area's precedence default even when the finding is contested, until the user checks it.
> - Treat unreviewed `MISSED` findings as leads, not findings: include one only if the document plainly supports it, and say it wasn't peer-checked.
> - If every finding is upheld and the peer reasons only restate the claims, say the agreement is weak evidence.
>
> End with a line **Peer-contested:** listing each contested and unchecked finding and how to settle it, or "none". Reply with one line: `<the single verdict>`.

If the chair fails, don't write a verdict yourself: give the reviews and the Peer Review table and say the verdict wasn't produced. Update `state.md`.

## Output

In chat, in this order:

1. The selected reviews in canonical order, each under its heading from the area's expert table, in its expert's exact format, read from `reviews/` with the `FINDINGS` block left out.
2. **Peer Review** — the table from `tally.md` with each finding's text, then the unreviewed `MISSED` items with who raised them, and any experts not run.
3. The area verdict from `VERDICT.md`, including its **Peer-contested** line.
4. One closing line: `Run files: .council/<run-id>/ (reviews, peer checks, tally) — delete when done. Peer agreement among sub-agents of one model family is correlated evidence, not independent confirmation.`
