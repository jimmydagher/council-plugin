# Council — Plan

## ⛏️ In progress

**TTD006 / TODO #6 — All skills write their run files outside the project.** Behavior is in `SPEC.md › Run files`. (TTD005's finished steps below are merged into the plan body on the next pass; they stay here until then.)

### Decision: where run files go

The owner's correction: "outside the project" means the user's **profile**, not the project. Options:

1. **`~/.council/<skill>/<run-id>/`** — **chosen.** One discoverable root, per-skill subfolders, survives across projects, never inside a repo so it can't be committed or leak into a diff. Keeps the existing `<run-id>` and `state.md` resume scheme.
2. OS temp dir (`%TEMP%`, `/tmp`) — rejected: cleaned unpredictably, so a resume after compaction or a later inspection can fail, and paths differ per OS.
3. Keep per-project dot-folders and add them to `.gitignore` — rejected: still writes into the project, which is the thing being forbidden.

### Steps

1. Replace the four path rules (each states "current directory") in `skills/arena/SKILL.md`, `skills/court/SKILL.md`, `skills/conclave/SKILL.md` and `references/peer-review.md` with the SPEC rule: root `~/.council/<skill>/<run-id>/` (`<area>` for `--peer`), resolve `~` at run time, `-2` suffix on collision, stop with the reason if the folder can't be written (never fall back to the project). Update their layout trees and closing "run files" lines to print the full resolved path. Read each file's other path mentions first. **STOP** if a skill writes a file the SPEC's list doesn't cover.
2. `skills/it/SKILL.md`, `skills/business/SKILL.md`, `references/shared-context.md`: check for path or "never edit the project" wording; align it and name the shared rule once in `shared-context.md`. Check how sub-agent prompts reference run paths (briefs pass `<…>` file paths, so they must be the resolved absolute path).
3. `README.md`: replace the four "in the current folder (delete when done)" sentences with the profile path; mention it once in a short "Where files go" note. Add a `meta/CHANGELOG.md` entry under 🚧 Unreleased citing `TODO #6` (TTD006).
4. Extend the tests (stdlib `unittest`, same style): every `SKILL.md` and `peer-review.md` names `~/.council/<…>/<run-id>`; no file under `skills/` or `references/` still contains `.arena/`, `.court/`, `.conclave/`, a bare `.council/<run-id>` or "current directory/folder" as a write location. Add the new tests first and confirm they fail on the current text, then make them pass.
5. Verify: `python -m unittest discover -s tests` passes; grep the repo for stale paths; one live run (e.g. `council:court --quick` on a sample idea) confirming files land only under the home `.council/court/<run-id>/` and the working directory is unchanged (`git status` clean). If no live multi-agent session is available, say so and leave it for validate. Report what wasn't covered (e.g. Windows vs POSIX path resolution tested on one OS only).

### Risks and notes

- Folders accumulate in the profile; nothing auto-deletes. The result names the path for the user to delete. A cleanup command is out of scope.
- Pasted or sensitive idea text now persists in the user's home rather than the project; the output line says so.
- Existing `.arena/`, `.court/`, `.conclave/`, `.council/` folders in projects from earlier runs are not migrated or removed.
- Unchanged: run-id format, file names inside a run, resume via `state.md`, every skill's process and output.

---

### Previous change (merged on next pass)
**TTD005 / TODO #5 — Apply llm-council's lessons: `--peer` mode for `council:it` and `council:business`.** Behavior is in `SPEC.md › Peer review`.

### Decision: where llm-council's lessons go

llm-council's core is: independent answers → anonymized peer ranking with a parseable block and a mechanical aggregate → a chair who writes the answer from both. Options considered:

1. **New skill (`council:ask`) that answers any question llm-council-style** — rejected: it overlaps `arena` (competing takes, blind judges) and `conclave` (independent positions, chair), and it pulls the plugin away from reviewing documents and ideas toward general Q&A.
2. **Retrofit anonymized peer review into arena / court / conclave** — rejected: they already have blind first positions, blind judges or juries, and mechanical counts. Conclave's cross-examination needs to know who is speaking (it aims at the counterweight), so anonymizing it would break it.
3. **Cross-model diversity (mixing opus / sonnet / haiku sub-agents)** — rejected for now: same-family tiers give little real diversity and the weaker tier lowers review quality. The output states the correlation caveat instead.
4. **Opt-in `--peer` mode on the area skills** — **chosen.** This is where the gap is: today every expert review runs in one context and the same session reconciles its own findings. With `--peer`, the experts review independently, check each other's findings anonymously (never their own), a mechanical tally marks each finding upheld / contested / unchecked, and a separate chair writes the verdict. The default single-session mode is untouched (no cost change).

Resulting layout:

```text
references/
├── shared-context.md  — argument rules gain the --peer mode flag (one paragraph)
└── peer-review.md     — NEW: the --peer procedure, run folder, briefs, tally rules (read only when --peer is set)
skills/it/SKILL.md, skills/business/SKILL.md — --peer row, process branch, Peer Review + Peer-contested output
```

### Steps

1. [x] Write `references/peer-review.md`: when it applies, the 2N + 1 cost line, the `.council/<run-id>/` layout and `state.md` resume rule, verbatim briefs for Stage 1 review (expert format + `FINDINGS:` block), Stage 2 peer check (`F<n>:` marks, `TOP:`, `MISSED:`) and the chair; the anonymize step (round-robin `F` numbers starting with the last expert, `labels.md` withheld, own findings removed); the tally rules (counts without OUT OF LANE, 3/2/1 points, upheld / contested / unchecked, unreviewed MISSED); graceful degradation (one re-request, "not run", stop below two reviews, chair failure); the closing correlation line. Both areas use it; area-specific bits (verdict title, precedence default) come from the area SKILL.
2. [x] Update `references/shared-context.md`: in `## Arguments`, add `--peer` as the only mode flag (selects no expert, needs two or more experts, error text), point to `peer-review.md`, and name the files read only in that mode. Upstream credit stays in the README.
3. [x] Update `skills/it/SKILL.md` and `skills/business/SKILL.md`: frontmatter triggers ("have the experts check each other", "peer review", "independent review"); a `--peer` line under the expert table; a process branch "if `--peer`: follow `../../references/peer-review.md`"; the Peer Review table and the **Peer-contested** verdict line in the output structure. Wording stays the same in both except area names, verdict labels and the precedence default.
4. [x] Update `README.md` (a Peer review section with an example, the 2N + 1 cost, when to use it vs the default, credit to Karpathy's llm-council as inspiration) and `.claude-plugin/plugin.json` description and keywords (`peer-review`). Leave `version` to the release hooks.
5. [x] Add a note under `## 🚧 Unreleased` in `meta/CHANGELOG.md` citing `TODO #5` (TTD005).
6. [x] Add `tests/test_peer.py` (stdlib `unittest`, same style as `test_conclave.py`):
   - `peer-review.md`'s Stage 1 `FINDINGS` line, Stage 2 `F<n>:` / `TOP:` / `MISSED:` examples match their regexes;
   - its call count text matches 2N + 1 for N = 2–4;
   - a reference tally function over sample peer files gives upheld / contested / unchecked as the SPEC says (majority holds, tie → contested, all OUT OF LANE → unchecked), points 3/2/1, and ignores a mark on an unshown or own finding;
   - both area SKILLs list `--peer`, point to `peer-review.md` and have a Peer-contested line; `shared-context.md` names `--peer` as the one mode flag.
7. [x] Verify:
   - `python -m unittest discover -s tests` passes (arena, court, conclave, peer).
   - Trace the error cases from the text: `--peer --security` (one expert), `--peer --finance` on `council:it` (bad flag still wins), `--PEER` repeated, and a run with no flags (unchanged single-session path).
   - One real `council:it --peer` run on a sample design doc: only `.council/` is written, Stage 1 agents read no other review, Stage 2 inputs exclude each expert's own findings and no expert names, the tally matches the `F<n>:` lines, and the verdict keeps contested findings. If no live multi-agent session is available, say so in the step and leave it for validate.
   - Done: `python -m unittest discover -s tests` passes, 50 tests (arena, court, conclave, peer 16). Error cases traced from the text: `--peer --security` hits the two-expert error; `council:it --peer --finance` hits the bad-flag error first; `--PEER` twice counts once; no flags takes the unchanged single-session path.
   - Live run of `council:it --peer --security --efficiency` on a sample design (`C:/tmp/peertest/`), main session following `peer-review.md` by hand: 2 reviews, 4 peer checks (one re-run after a brief fix) and 1 chair, all written only under `.council/<run-id>/`. Both closing blocks parsed, findings anonymized round-robin into F1–F13, and the tally matched the `F<n>:` lines with nothing ignored. The verdict kept the contested Critical (F6) blocking by precedence, kept the unchecked Criticals, and ended with a Peer-contested line.
   - Fixed from the run: (1) peers re-raised their own hidden findings as MISSED, so Stage 2 now reads its own review and MISSED must be new; the re-run confirmed it. (2) The efficiency peer marked a Critical PII exposure OVERSTATED on cost grounds, so OUT OF LANE now covers the main risk and forbids downgrading a side the peer can't judge. Re-run of the efficiency peer check after fix (2): F6 is now OUT OF LANE with the storage-cost part noted in the reason, and no security finding was marked OVERSTATED or WRONG. It is more conservative, though: F12, which it upheld before, is now OUT OF LANE too.
   - Observed limit: with two experts each finding gets at most one in-lane mark, and cross-specialty findings are mostly unchecked. The table shows this, and the chair treated unchecked Criticals as blocking.

### Risks and notes

- Cost: 2N + 1 sub-agent calls (max 9) vs 0 today; opt-in only, stated before every run.
- Anonymity is partial: a finding's subject often reveals its specialty (a Security finding reads like one). The point is to remove name-based deference and self-judgment, not to hide the domain; the SPEC says so.
- Peer marks come from one model family, so agreement is correlated; the output says so. Revisit cross-model mixing only if the owner wants it (option 3).
- `.council/` lands in the user's working directory; the output names it for deletion. Not added to any `.gitignore` automatically.
- Unchanged: each expert's checklist and output format, the default (no `--peer`) behavior, and arena / court / conclave.

## ✅ Done

- **TTD004 / TODO #4** — Added `council:conclave`: blind positions from a counterweighted lens panel, cross-examination, final stances, mechanical count, chair report with unresolved items first, kill criteria and an outcome ledger; `tests/test_conclave.py` guards the pool, formats and counts.
- **TTD003 / TODO #3** — Added `council:court`: idea trial with numbered charges, honest prosecution/defense, blind jury per charge, tally, conditions for acquittal; `tests/test_court.py` guards the pool, ballot format and counts.
- **TTD002 / TODO #2** — Added `council:arena`: idea tournament with dealt strategy cards, attack/defend/blind-judge matches, salvage list; `tests/test_arena.py` guards dealing, bracket and call counts.
- **TTD001 / TODO #1** — Consolidated skills into `council:it` and `council:business` with expert flags; experts moved to `skills/<area>/experts/`.
