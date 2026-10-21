# Council — Specification

Behavior of the `council` plugin after TODO #1 / TTD001 (skill restructure), TODO #2 / TTD002 (arena), TODO #3 / TTD003 (court), TODO #4 / TTD004 (conclave) and TODO #5 / TTD005 (peer review for the area skills). The `it` and `business` areas review documentation, designs, plans, and business proposals; `arena` generates and stress-tests ideas; `court` tries one idea and returns a verdict; `conclave` has a panel of differently-minded lenses deliberate an idea and maps where they agree, split and don't know. None of them review source code (see `code-reviewer`).

## Invocation

One skill per **area**. A flag narrows it to specific **experts** (lenses) within that area.

| Command | Result |
|---------|--------|
| `/council:it` | All IT experts, plus a reconciled **IT Verdict** |
| `/council:it --security` | Only the Security expert; no verdict |
| `/council:it --security --infra` | Only those experts, plus a verdict reconciling just them |
| `/council:business` | All business experts, plus a reconciled **Business Verdict** |
| `/council:business --finance` | Only the Finance expert; no verdict |
| `/council:it --peer` | All IT experts as independent sub-agents, an anonymized peer check of their findings, and a verdict built on it (see **Peer review**) |

Rules:

- The area skill is the only entry point. Plain-language triggers ("security review", "finance review") still route to the area skill with the matching expert.
- Flags are `--<expert>`, case-insensitive, any order, repeatable. No flag means every expert in the area. The one mode flag, `--peer`, is valid in both areas and selects no expert (see **Peer review**).
- A flag that is not an expert of that area (including another area's expert, e.g. `/council:it --finance`) is an error: state the valid flags for the area and stop. Never guess or silently drop it.
- One flag: the single expert's review in its own format, no verdict. Two or more flags: the selected reviews in canonical order, then the area verdict over only those.
- Experts always run in canonical order, regardless of flag order.
- The document under review is identified as before; if unclear, ask.

## Areas and experts

| Area | Skill | Experts (flag) |
|------|-------|----------------|
| IT | `council:it` | `--security`, `--standards`, `--efficiency`, `--infra` (alias `--infrastructure`) |
| Business | `council:business` | `--ops` (alias `--operations`), `--finance`, `--strategy`, `--legal` |

More areas are planned; each adds one skill and one expert folder, with no change to existing areas.

## Where the experts live

Experts are not skills and have no command of their own. Each is one markdown file under its area skill, `skills/<area>/experts/<expert>.md`, read only when selected. The area skill's expert table maps each flag to its file. Adding an expert means adding a file and a table row.

## Shared context

`references/shared-context.md` is rewritten to match; it is read first by every area skill and is the single place for these rules:

- Lenses are invoked as an area plus an expert flag, never by a per-expert skill name.
- The argument rules above (flags, aliases, canonical order, errors, verdict only for two or more experts).
- The structure tree shows the two areas and their `experts/` files, with no `council:all`.
- Expert files own their checklist and output format; area skills own the verdict.
- Unchanged: scope (documents, designs, plans, proposals, not code), the `code-reviewer` redirect, and the four shared-process rules.

## Removed

- `council:all` (company-wide verdict across every area). Run each area separately.
- Per-expert skills (`council:it-security`, `council:it-standards`, `council:it-efficiency`, `council:it-infra`, `council:bu-ops`, `council:bu-finance`, `council:bu-strategy`, `council:bu-legal`). Replaced by flags.
- `council:bu`. Renamed `council:business`.

## Unchanged

- Each expert's checklist, output table, and verdict wording.
- Area verdict rules (agree / conflict / resolution / single verdict). When a subset runs, they apply to the selected experts only.
- Shared process and scope in `references/shared-context.md`.
- `bu-legal`'s output remains a risk-flagging pass, not legal advice.

## Arena (`council:arena`) — TODO #2

A **generative** skill: it takes a rough idea or open question and returns the strongest version of it, found by making several differently-reasoned takes compete. It does not review an existing document (that is `council:it` / `council:business`) and does not deliberate as a panel (`council:conclave`) or try a case (`council:court`).

Lessons taken from the upstream `arena-skill` (MIT; nothing copied verbatim): one identical brief for every competitor, diversity by dealt strategy cards rather than by asking for "different" answers, concrete attack → defend → revise rounds, a blind judge with a weighted rubric where a verified fatal flaw always loses, state kept on disk so the main session tracks receipts and survives compaction, and an honest final comparison against the user's own baseline. Deliberately different: it is about **ideas** (product, business, process, design concepts), not solving a task; the field is small (cost-bounded); it is pure markdown (no Python); and the output keeps the best ideas from eliminated competitors as a salvage list instead of discarding them.

### Invocation

| Command | Result |
|---------|--------|
| `/council:arena <idea>` | Field of 8 competitors, single-elimination, champion dossier |
| `/council:arena --quick <idea>` | Field of 4 |
| `/council:arena --field N <idea>` | Field of N, 2 ≤ N ≤ 16 |
| `/council:arena --baseline <idea>` | Also judges the champion against the user's current version (pasted text or a file) |

- Flags are case-insensitive, any order. `--quick` and `--field` together, `--field` outside 2–16 or non-numeric, or any other flag: error listing the valid flags, then stop.
- Plain-language triggers: "arena this idea", "make versions of this idea fight", "stress-test this idea", "brainstorm the best version of …".
- No idea given, or the idea is too vague to brief (no goal or no audience inferable): ask one round of clarifying questions before spending any sub-agent calls.
- Before a run, state the field size and approximate sub-agent call count in one line; for N > 8 ask for confirmation.

### Flow

1. **Brief.** Write one brief — the idea, goal, constraints, and what a good answer contains — to `.arena/<run-id>/brief.md`. Every competitor receives it byte-for-byte. Pitches stay under about 700 words, revisions included.
2. **Deal.** Each competitor gets one strategy card from `skills/arena/cards.md`: a **lens** (e.g. first principles, inversion, customer's eyes, constraint-first, analogy from another industry, minimum viable, 10× version, contrarian), a **shape** (e.g. phased rollout, platform, service, partnership, automation, kill-or-pivot) and a **bias** (e.g. cheapest, fastest to market, lowest risk, most defensible, simplest to run). Cards are dealt without repeats, spreading each part as evenly as possible.
3. **Pitch.** Each competitor (fresh sub-agent) writes its version of the idea to `pitches/<id>.md` in the fixed pitch format: one-line pitch, how it works, who it serves, why now, cost/effort, top risks, first three steps.
4. **Match** (repeated per round). Pair competitors, avoiding same-lens pairs; an odd field gives one bye, never twice to the same competitor while others wait.
   - **Attack:** each side writes up to five attacks on the other, each labeled FATAL / MAJOR / MINOR with a concrete failure scenario.
   - **Defend:** each side concedes or rebuts each attack — conceding only what is true, rebutting attacks that misread the pitch, lack a concrete scenario or overstate severity — then revises its pitch (revision overwrites its pitch file; the attacks it faced are kept).
   - **Judge:** a separate sub-agent that never sees the cards (it is told to read only the files it is given, and is never given `deal.md`) verifies each attack and scores both revised pitches on the rubric. The higher total advances; a pitch with a verified FATAL attack cannot beat one without.
5. **Champion.** The last survivor wins. With `--baseline`, a final blind judge scores champion vs baseline and the result is reported even if the baseline wins.

### Rubric (`skills/arena/rubric.md`)

| Criterion | Weight |
|-----------|--------|
| Value — solves a real problem for a named audience | 30 |
| Feasibility — buildable with stated effort and resources | 25 |
| Robustness — how well it survived the attacks | 20 |
| Specificity — concrete enough to act on next week | 15 |
| Originality — not the obvious first answer | 10 |

### Output

An **Arena Result** in chat:

- **Champion** — the final pitch, its card, rounds won, and the attacks it withstood (with how each was answered).
- **Salvage** — up to five strong ideas from eliminated pitches worth grafting onto the champion, each with its source competitor.
- **Open risks** — attacks the champion conceded or only partly answered.
- **Baseline** (with `--baseline`) — scores for both and one sentence on why.
- **Next step** — optionally suggest `/council:business` or `/council:it` to review the champion once it is written up.

### Rules

- Never edits the user's project. The only files written are under `.arena/<run-id>/` in the current directory (`run-id` = `YYYYMMDD-HHMMSS`); the result names that folder so the user can delete it.
- The main session holds only file paths and scores, not pitch text, until the final output; a run can be resumed from `.arena/<run-id>/state.md` after compaction.
- Sub-agents run in waves of at most 8 in parallel.
- The champion is the strongest idea found, not a guarantee it is right; the output says so in one line.
- The four shared-process rules in `references/shared-context.md` (no manufactured findings, concrete fixes) apply to attacks and judgments.

## Court (`council:court`) — TODO #3

A **verdict** skill: it puts one idea or decision on trial *as the user stated it* and returns whether it holds up, which specific charges against it stick, and the changes that would flip the verdict. It does not improve the idea (that is `council:arena`) and does not review a written document lens by lens (that is `council:it` / `council:business`).

Lessons taken from the upstream `court-skill` (MIT; nothing copied verbatim): adversarial roles that must argue *honestly* (strongest true case against, strongest true case for), a jury of distinct perspectives that vote **independently** so no one follows the room, a judge who summarizes but never changes the vote, the main session that never argues, votes or edits the verdict, deterministic vote counting, "conditions for acquittal" (the changes that would flip the most votes), state on disk, a `--quick` mode and a cost line before every run, and the "second opinion, not professional advice" caveat. Deliberately different: pure markdown (no Python), a jury pool built for business/IT decisions, the prosecutor files **numbered charges** and jurors rule on **each charge** as well as overall (so the output says *what* fails, not only *that* it fails), a hung result on ties instead of a forced verdict, and a hand-off to `council:arena` when the idea is convicted.

### Invocation

| Command | Result |
|---------|--------|
| `/council:court <idea>` | Trial with a jury of 9 |
| `/council:court --quick <idea>` | Jury of 5 |
| `/council:court --jury N <idea>` | Jury of N, 3 ≤ N ≤ 12 |

- Flags are case-insensitive, any order. `--quick` and `--jury` together, `--jury` with no value, a non-number or a number outside 3–12, or any other flag: error listing the valid flags, then stop.
- Plain-language triggers: "put this idea on trial", "court this idea", "should I do this — make the case for and against", "jury this decision", "find the holes before I commit".
- The idea should include the specifics the jury will judge on (numbers, audience, what's been tried, the alternative). No idea given, or no goal or decision inferable: ask one round of clarifying questions, each with a suggested answer, before spending any sub-agent calls.
- Before a run, state jury size and sub-agent call count (**N + 5**: 2 openings, 2 rebuttals, N jurors, 1 judge; 5 → 10, 9 → 14, 12 → 17) in one line. No confirmation needed (bounded at 17, plus at most one re-run per malformed ballot).

### Jury pool (`skills/court/jurors.md`)

Twelve jurors, each a one-paragraph perspective with what they weigh and what would convince them, spread over four seats: **money** (e.g. CFO-minded accountant, investor), **people** (e.g. first-time customer, frontline employee who must run it), **delivery** (e.g. engineer, project manager, operations lead), **risk** (e.g. security/compliance officer, competitor, skeptical outsider). The pool is listed in a fixed seating order that rotates through the four seats, so the first N jurors are always balanced; a jury of N sits the first N. Editing the pool means editing that file.

### Flow

1. **Case file.** Write the idea, goal, decision being made, and stated facts to `.court/<run-id>/case.md`. Every sub-agent gets it byte-for-byte; nobody may invent facts the case file doesn't state (an unstated fact is argued as unknown, not assumed).
2. **Openings** (2 in parallel).
   - **Prosecution:** the strongest honest case that the idea fails as described, as 1–5 numbered **charges**, each with the claim, the fact from the case file it rests on, and a concrete failure scenario. No charge it does not believe holds.
   - **Defense:** the strongest honest case that it works: why, for whom, and what evidence in the case file supports it.
3. **Rebuttals** (2 in parallel, each reads both openings).
   - **Prosecution** answers the defense's claims and may withdraw a charge the defense shows is wrong (never add one). Withdrawn charges keep their number and are not voted on; if every charge is withdrawn, jurors vote on the overall verdict only.
   - **Defense** answers each charge by number: concede (only what is true) or rebut (misreads the case, no concrete scenario, or overstated).
4. **Jury** (N in parallel, waves of at most 8). Each juror reads only the case file, the four filings and its own persona — never the other jurors' votes or personas. It writes a fixed-format ballot: per charge **PROVEN / NOT PROVEN** with a one-line reason; an overall **GUILTY** (the idea fails as described) / **NOT GUILTY**; a one-line overall reason; and the fewest changes that would flip its vote (all of them needed).
5. **Tally** (main session, mechanical). Count the ballot lines only. A charge is **sustained** with a strict majority of PROVEN, otherwise **dismissed**; an exact tie is **hung** on that charge. The overall verdict is the strict majority; a tie is a **hung jury**. The main session writes the tally to `tally.md` and never changes it.
6. **Judgment** (1). The judge reads the case file, filings, ballots and `tally.md` and writes `VERDICT.md`: the tally as given, the charges that stuck, what the defense got right, and the **conditions for acquittal** — the changes named by GUILTY jurors, grouped across jurors and ranked by how many ask for each, then which combination of changes flips which votes (a vote flips only when every change on that juror's FLIP line is made). The judge cannot alter the tally.

### Output

A **Court Verdict** in chat (also `.court/<run-id>/VERDICT.md`):

- **Verdict** — GUILTY / NOT GUILTY / HUNG, with the count ("GUILTY, 7 to 2") and the jury size.
- **Charges** — each with sustained / dismissed / hung, its count, and one line on why.
- **What the defense got right** — the strengths that held.
- **Jurors** — one line per juror: perspective, vote, reason.
- **Conditions for acquittal** — ranked changes (from GUILTY jurors) with the jurors asking for each, then which combination of changes flips which votes.
- **What must not change** — changes that would turn NOT GUILTY jurors, with counts; omitted when no juror voted NOT GUILTY.
- **Next step** — GUILTY or HUNG: suggest `/council:arena` to find a stronger version; NOT GUILTY: suggest `/council:business` or `/council:it` once it is written up.
- One closing line: the verdict is a structured second opinion from language models, not legal, financial or professional advice.

### Rules

- Never edits the user's project. The only files written are under `.court/<run-id>/` in the current directory (`run-id` = `YYYYMMDD-HHMMSS`): `case.md`, `jury.md`, `filings/{prosecution,defense}-{opening,rebuttal}.md`, `ballots/jNN.md`, `tally.md`, `VERDICT.md`, `state.md`. The result names that folder so the user can delete it.
- The main session never argues a side, never votes and never edits the verdict; it holds only paths, one-line returns and the ballots' vote lines (for the tally) until the judgment, and a run can resume from `state.md` after compaction.
- A ballot missing a vote line for a charge, the overall verdict or the FLIP line is re-requested once from the same juror; if still malformed, that juror is recorded as **abstained** and the count says so.
- The four shared-process rules in `references/shared-context.md` (no manufactured findings, concrete fixes) apply to charges, rebuttals and ballots.

## Conclave (`council:conclave`) — TODO #4

A **deliberation** skill: it seats a panel of differently-minded **lenses**, has each form a position blind, makes them challenge each other, and returns a map of the idea — where the panel converged, where it split, what nobody knows, and what to do next. It neither improves the idea into a winner (`council:arena`), nor rules guilty / not guilty on it (`council:court`), nor reviews a written document (`council:it` / `council:business`). Use it when the question is "what do I not see about this?" rather than "which version wins?" or "does it hold?".

Lessons taken from the upstream `council-of-high-intelligence` (nothing copied verbatim; it is a separate, general-purpose, multi-host skill and this one does not replace or compete with it): independent first positions before anyone sees anyone else, members chosen as analytical lenses each paired with a **counterweight** aimed at its blind spot, forced direct cross-examination, a final stance after being challenged, dissent and unresolved questions kept as deliverables (a split panel is reported as split, never smoothed into a consensus paragraph), claims labeled **FACT / INFERENCE / ASSUMPTION / UNKNOWN**, recommendations that carry acceptable compromises, **kill criteria** and one concrete next step, a short **outcome ledger** entry (prediction, review date, what would change the answer), `--quick` mode, and a guard against using a panel to decorate a decision already made. Deliberately different: pure markdown with a plugin-native orchestration (no Python, no multi-host mirrors, no provider routing, no 18-persona roster), lenses built for business/IT ideas rather than historical figures, and a bounded cost line with a smaller default panel.

### Invocation

| Command | Result |
|---------|--------|
| `/council:conclave <idea>` | Panel of 6, three rounds, Conclave Report |
| `/council:conclave --quick <idea>` | Panel of 4, blind positions then report (no cross-examination) |
| `/council:conclave --seats N <idea>` | Panel of N, 3 ≤ N ≤ 12, three rounds |

- Flags are case-insensitive, any order. `--quick` and `--seats` together, `--seats` with no value, a non-number or a number outside 3–12, or any other flag: error listing the valid flags, then stop.
- Plain-language triggers: "convene the conclave", "brainstorm this idea with a panel", "what am I missing about this idea", "get different perspectives on …", "/council:conclave".
- No idea given, or no goal or decision inferable: ask one round of clarifying questions, each with a suggested answer, before spending any sub-agent calls.
- **Decoration guard.** If the user has plainly already decided and wants approval, say so in one line and offer `council:court` instead. If the question is a factual lookup or a cheap reversible choice, say a direct answer or a small experiment fits better and ask whether to run anyway. Otherwise proceed.
- Before a run, state panel size and sub-agent call count in one line. Full run: **3N + 1** (N blind positions, N cross-examinations, N final stances, 1 chair): 3 → 10, 6 → 19, 12 → 37. Quick run: **N + 1**: 3 → 4, 4 → 5. Ask for confirmation when the count exceeds 20; plus at most one re-run per malformed file.

### Lens pool (`skills/conclave/lenses.md`)

Twelve lenses in six counterweight pairs, listed in a fixed seating order so the first N always form as many whole pairs as possible (a panel of N seats the first N; an odd N leaves one lens without its counterweight, and the chair notes it). Each lens has a one-paragraph method, a **blind spot**, and the question it must answer. Pairs: customer advocate ↔ unit economist; systems thinker ↔ pragmatic builder; skeptic ↔ first-principles rebuilder; downside guardian ↔ cost-of-inaction advocate; daily operator ↔ market strategist; trust steward ↔ long-horizon futurist. Lenses are viewpoints, not impersonations. Editing the pool means editing that file.

### Flow

1. **Field notes.** Write to `.conclave/<run-id>/notes.md`: the idea, the decision, the goal, **Facts stated** (only what the user said), **Assumptions** being made, **Unknowns** that could change the answer, reversibility, and deadline (each "not stated" if absent). Every sub-agent gets it byte-for-byte; no one may invent facts it doesn't state. Seat the panel and write `panel.md`.
2. **Round 1 — blind positions** (N in parallel, waves of at most 8). Each lens reads only the notes and its own lens card, never another position, and writes `r1/<id>.md` in the fixed position format: a `POSITION:` one-liner, 3–6 numbered claims each labeled FACT / INFERENCE / ASSUMPTION / UNKNOWN, `BLIND SPOT:` (where its own lens could mislead it here), and `ASK:` (the one thing it would want answered). Under about 400 words.
3. **Round 2 — cross-examination** (N in parallel; skipped in `--quick`). Each lens reads all Round 1 positions and writes `r2/<id>.md`: a direct challenge to its counterweight (or, with no counterweight seated, to the position it most disagrees with) and one more challenge to another lens, each quoting the claim it attacks and the evidence or gap it exposes; and, for each other position, **AGREE** (naming what agreement costs the idea), **DISAGREE** or **NO VIEW**. Blanket agreement or a challenge with no quoted claim is invalid. Under about 400 words.
4. **Round 3 — final stance** (N in parallel; skipped in `--quick`). Each lens reads the notes, all Round 1 positions and all Round 2 cross-examinations (especially those aimed at it) and writes `r3/<id>.md`: `STANCE: BACK | BACK IF | OPPOSE — <reason>` (`BACK IF` names its condition), `MOVED: YES | NO — <what changed its mind, or what it held against which challenge>`, `COMPROMISE:` (what it could accept), `KILL:` (the evidence that would make it drop its stance). Under about 300 words.
5. **Count** (main session, mechanical). Read only the `STANCE` and `MOVED` lines of the Round 3 files (in `--quick`, Round 1 has no `STANCE` line, so there is no count and the report says so). Write `count.md`: BACK / BACK IF / OPPOSE totals and each lens's stance and whether it moved. A strict majority of BACK plus BACK IF is **leaning yes**; a strict majority of OPPOSE is **leaning no**; anything else is **split**. This is a signal, not a verdict; the main session never changes it.
6. **Chair** (1). A separate sub-agent that never casts a stance reads the notes and every file and writes `REPORT.md`. It must not average the panel into a middle position, must keep minority stances with their strongest reason, and must flag suspicious agreement (every blind position alike, or no lens `MOVED` nor held against a concrete challenge) as weak evidence rather than strength.

### Output

A **Conclave Report** in chat (also `.conclave/<run-id>/REPORT.md`), in this order:

- **Panel** — size, mode, run folder path, and any unpaired lens.
- **Unresolved first** — open questions and UNKNOWNs that could change the answer, each with the lens that raised it and a cheap way to check it.
- **Where the panel splits** — each live disagreement: the positions, who holds each, the strongest reason for each side, and what evidence would settle it. Never merged into a compromise paragraph.
- **Where it converged** — points held by a strict majority after challenge, labeled FACT / INFERENCE / ASSUMPTION, and how hard they were challenged.
- **Options surfaced** — directions raised by any lens that the user had not stated, each with its source lens (not ranked into a winner).
- **Count** — the mechanical count from `count.md` and its reading (leaning yes / leaning no / split); in `--quick`, "not counted".
- **Recommendation** — the chair's recommendation with acceptable compromises, **kill criteria**, and one concrete next step doable this week. If the panel is split, the recommendation is the test or question that would break the tie, not a pick.
- **Ledger** — prediction, owner (the user), review date (the user's, or "to be set"), and what evidence would change the answer. Written as `ledger.md`; a later session may mark it confirmed / revised / reversed / inconclusive without rewriting the original.
- **Next step** — a hand-off: `/council:arena` to build stronger versions of an option, `/council:court` to try the leading version, `/council:business` or `/council:it` once it is written up.
- One closing line: the report is a structured set of perspectives from language models, not professional advice, and a panel agreeing is not proof.

### Rules

- Never edits the user's project. The only files written are under `.conclave/<run-id>/` in the current directory (`run-id` = `YYYYMMDD-HHMMSS`): `notes.md`, `panel.md`, `r1/`, `r2/`, `r3/`, `count.md`, `REPORT.md`, `ledger.md`, `state.md`. The result names that folder so the user can delete it.
- Independence: in Round 1 no sub-agent sees another position; every later round names exactly which files a sub-agent may read.
- The main session never argues, takes a stance or edits the report; it holds only paths, one-line returns and the `STANCE` / `MOVED` lines until the end, and a run can resume from `state.md` after compaction.
- A file missing a required line is re-requested once from the same lens; if still malformed, that lens is recorded as **abstained** and the count says so. Required lines: Round 1 `POSITION`, at least one `CLAIM`, `BLIND SPOT`, `ASK`; Round 3 `STANCE`, `MOVED`, `COMPROMISE`, `KILL`. Round 2 files are not machine-checked; the chair treats a challenge with no quoted claim, or an AGREE that names no cost, as invalid. A lens abstained in Round 1 sits out the later rounds and is not counted.
- Sub-agents run in waves of at most 8 in parallel.
- The four shared-process rules in `references/shared-context.md` (no manufactured findings, concrete fixes) apply to every claim and challenge.

## Peer review (`--peer` on `council:it` / `council:business`) — TODO #5

An opt-in mode for the two area skills. Without `--peer` they behave exactly as above (one session, no sub-agents). With it, each selected expert reviews the document as an **independent sub-agent**, each expert then checks the **other experts' findings anonymously**, and a separate chair writes the verdict from those checks. It answers "which findings hold up when the other specialists look at them?". The single-session review can't answer that: every review shares one context, and the session that wrote the findings also reconciles them.

Lessons taken from Karpathy's `llm-council` (nothing copied; it is a three-stage web app that sends one question to several provider models):

- independent first answers, collected in parallel;
- a peer stage where answers carry neutral labels (`Response A`, `Response B`) so a reviewer can't favor a source;
- a strict, machine-parseable closing block, with the aggregate (average rank) computed mechanically outside the models;
- a chair that writes the final answer from the answers **and** the peer results;
- carrying on with the answers that came back when one member fails;
- every raw answer and parsed result kept on disk so the user can check the parsing.

Deliberately different:

- Diversity comes from the experts' lenses, not from different model vendors. Sub-agents here are one model family, so the output says peer agreement is correlated evidence, not independent proof.
- A reviewer never judges its own findings (upstream lets a model rank its own answer).
- Findings are judged one by one (HOLDS / OVERSTATED / WRONG) instead of ranking whole answers, because an area review is a set of findings, not one answer.
- It is a mode of the existing area skills, not a new skill: `arena`, `court` and `conclave` already cover competing takes, verdicts and deliberation on ideas, and the gap llm-council fills here is independence and cross-checking in document review.

### Invocation

| Command | Result |
|---------|--------|
| `/council:it --peer` | Four IT experts, peer review, IT Verdict |
| `/council:business --peer --finance --legal` | Those two experts, peer review, Business Verdict over them |

- `--peer` is case-insensitive, may appear anywhere among the flags, and repeats are ignored. It needs at least two selected experts. `--peer` with one expert flag is an error ("peer review needs two or more experts; add an expert flag or drop --peer"), then stop. Other flag errors are unchanged.
- Plain-language triggers: "have the experts check each other", "peer review this with IT / the business council", "independent IT review".
- Before a run, state the expert count and sub-agent call count in one line: **2N + 1** (N reviews, N peer checks, 1 chair), so 2 → 5, 3 → 7, 4 → 9, fewer when an expert has nothing to check, plus at most one re-run per malformed file. No confirmation step (the maximum is 9).

### Flow

1. **Brief.** Write `.council/<run-id>/brief.md`: the area, the selected experts, and the document's path (or the pasted text in full). Every sub-agent reads this and only the files its brief names.
2. **Stage 1: independent reviews** (N in parallel). Each expert sub-agent reads the brief, the document and its own expert file, never another review. It writes `reviews/<expert>.md` in its expert file's exact format, followed by a closing block: `FINDINGS:`, then one line per finding, `- <severity> | <one-line claim> | <fix>`, with severity `Critical`, `High`, `Medium` or `Low` (Security's own scale; the other experts rate the finding's impact on the document's goal). An expert with nothing of concern writes `FINDINGS: none` (shared-process rule 3).
3. **Anonymize** (main session, mechanical). Collect every `FINDINGS` line into `findings.md`, numbered `F1`, `F2`, … in a fixed interleaved order (round-robin across experts, starting with the last in canonical order, so findings aren't grouped by expert), with the expert name removed and the severity kept. `labels.md` maps each number to its expert and is never given to a Stage 2 sub-agent.
4. **Stage 2: peer check** (up to N in parallel). An expert whose input would be empty (every other expert wrote `FINDINGS: none`) gets no peer check and no call; if nobody found anything, Stage 2 and the tally are skipped and the chair is told there were no findings to check. Each expert reads the brief, the document, its own expert file, its own review and a copy of `findings.md` with its own findings removed (`peer/<expert>-input.md`), and writes `peer/<expert>.md`:
   - for each finding shown, `F<n>: HOLDS | OVERSTATED | WRONG | OUT OF LANE — <reason>` (OVERSTATED names the severity it should have; OUT OF LANE means its specialty can't judge the finding's main risk, with any in-lane part noted in the reason; a peer never marks OVERSTATED or WRONG because of a side it can't judge);
   - `TOP: F<a>, F<b>, F<c>`, the three it thinks matter most, best first (fewer if fewer were shown);
   - `MISSED:` at most two findings in neither its own review nor the findings shown, in the Stage 1 line format, or `none`. (Reading its own review stops it re-raising its own findings as missed; the live trial showed that happening.)
5. **Tally** (main session, mechanical). Parse only the `F<n>:`, `TOP:` and `MISSED:` lines and write `tally.md`. For each finding: its expert, severity, HOLDS / OVERSTATED / WRONG counts (OUT OF LANE excluded), TOP points (3 for first, 2 for second, 1 for third), and a status:
   - **upheld**: HOLDS is a strict majority of the in-lane marks;
   - **contested**: at least one in-lane mark, and OVERSTATED + WRONG is at least HOLDS;
   - **unchecked**: no in-lane marks.
   Rows are ordered by status (upheld, contested, unchecked), then points. `MISSED` items are listed separately as **unreviewed**, with who raised them. The main session never edits the tally.
6. **Chair** (1). A separate sub-agent that wrote no review reads the brief, the document, every review, `tally.md`, `labels.md` and the area SKILL (for its verdict format and precedence default), and writes `VERDICT.md` in the area skill's verdict format (agree / conflict / resolution / single verdict). In addition it:
   - uses the tally as evidence, and never drops a contested finding (it says what check would settle it);
   - keeps the area's precedence default: an unresolved Critical/High Security finding (IT) or a "Needs counsel: Yes" Legal finding (Business) still outranks the others when contested, until the user checks it;
   - flags suspicious agreement (every finding upheld, with reasons that only restate the claim) as weak evidence.

### Output

In chat, in this order:

- The selected reviews in canonical order, each in its expert's exact format (the `FINDINGS` block is left out of the chat copy).
- **Peer Review**: one table from `tally.md` (finding, expert, severity, holds / overstated / wrong, points, status), then the unreviewed `MISSED` items with who raised them.
- The area **Verdict** from `VERDICT.md`, with one added line, **Peer-contested:** the contested and unchecked findings and how to settle each, or "none".
- One closing line naming `.council/<run-id>/` (raw reviews, peer files, tally) so the user can check the parsing or delete it, and saying that agreement among sub-agents of one model family is correlated evidence, not independent confirmation.

### Rules

- Never edits the user's project. The only files written are under `.council/<run-id>/` in the current directory (`run-id` = `YYYYMMDD-HHMMSS`): `brief.md`, `reviews/`, `findings.md`, `labels.md`, `peer/`, `tally.md`, `VERDICT.md`, `state.md`. A run can resume from `state.md` after compaction.
- The main session never reviews, judges or edits the verdict; it holds paths, the parsed lines and one-line returns.
- Graceful degradation. A file missing its closing block (Stage 1 `FINDINGS`; Stage 2 at least one `F<n>:` line and `TOP`) is re-requested once from the same expert. If it is still malformed or the sub-agent fails, that expert is **not run** for that stage: with no review it has no findings and does no peer check; with no peer check its marks are absent. The run continues while at least two reviews exist; with fewer it stops and names the single-session mode (`/council:<area>` without `--peer`) as the fallback. If the chair fails, the output gives the reviews and the Peer Review table and says the verdict wasn't produced.
- A `F<n>:` line or `TOP` entry naming a number the expert wasn't shown (including its own finding), or a second mark on the same number from the same expert, is ignored and noted in the tally.
- The four shared-process rules apply to every finding and every peer mark.
