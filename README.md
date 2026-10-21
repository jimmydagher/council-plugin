# Council

A council of contractor-style reviewer experts for **documentation, designs, plans, and business proposals**. Each expert is named for what it does, not who it is — nothing to memorize to invoke the right one. For **source code**, use the separate `code-reviewer` plugin instead; that's a different job with its own process (intake → catalog → strategy → execute → validate), and this plugin deliberately doesn't overlap with it.

This plugin supersedes the earlier `council-of-claude` plugin, which named each lens after a person (Tom, Mike, Pedro, Hector, Emma, John, Natalie).

## Structure

```text
council
├── council:it        — Security, Standards, Efficiency, Infrastructure
├── council:business  — Operations, Finance, Strategy, Legal
├── council:arena     — idea tournament: find the strongest version of an idea
├── council:court     — idea trial: a jury's verdict on an idea as stated
└── council:conclave  — idea panel: differently-minded lenses map what you're missing
```

One skill per area. Pick experts within an area with a flag; with no flag, every expert in the area runs and one reconciled verdict closes the review.

## IT (`council:it`)

For reviewing documentation, designs, or architecture proposals.

| Flag | Focus |
|------|-------|
| `--security` | Security gaps, auditability, logging |
| `--standards` | Standards, naming, structure, readability |
| `--efficiency` | Performance, resource use, KISS/simplicity |
| `--infra` (or `--infrastructure`) | Tech/infra fit, cost, uptime, performance balance |

## Business (`council:business`)

For reviewing business proposals, plans, budgets, or initiatives.

| Flag | Focus |
|------|-------|
| `--ops` (or `--operations`) | Operational efficiency, ownership, process discipline |
| `--finance` | Cost trajectory, bottom-line soundness, savings quality |
| `--strategy` | Long-term fit, systems maturity, scalability, dependency risk |
| `--legal` | Contract, regulatory, IP, and data-privacy exposure |

## Flags

| Command | Result |
|---------|--------|
| `/council:it` | All IT experts, then an IT Verdict |
| `/council:it --security` | Security only, no verdict |
| `/council:it --security --infra` | Those two, then a verdict over just them |
| `/council:business --finance` | Finance only, no verdict |
| `/council:it --peer` | All IT experts, independently, cross-checked, then a verdict (see below) |

Flags work in any order and the experts always run in the table's order. A flag that isn't one of the area's experts (such as `/council:it --finance`) is an error that lists the valid flags. There is no all-areas command: run `council:it` and `council:business` separately.

## Peer review (`--peer`)

Add `--peer` to either area when the findings matter enough to cross-check. Without it, every expert reviews in one shared context and the same session reconciles its own findings. With it:

1. Each selected expert reviews the document as an **independent sub-agent**, seeing no other review.
2. The findings are pooled, renumbered `F1`, `F2`, … and stripped of expert names.
3. Each expert marks every *other* expert's finding HOLDS, OVERSTATED, WRONG or OUT OF LANE, picks its top three, and may add up to two findings nobody raised.
4. A mechanical tally marks each finding **upheld**, **contested** or **unchecked**.
5. A separate chair writes the area verdict from the reviews and the tally, never drops a contested finding, and lists each one with the check that would settle it.

| Command | Experts | Sub-agent calls |
|---------|---------|-----------------|
| `/council:it --peer` | 4 | 9 |
| `/council:business --peer --finance --legal` | 2 | 5 |

The cost is at most 2N + 1 calls (fewer when an expert has nothing to check), stated before the run. `--peer` needs at least two experts. Working files go to `.council/<run-id>/` in the current folder (delete when done), so you can check every raw review, peer mark and the tally. The sub-agents are all one model family, so their agreement is correlated evidence, not independent proof.

Inspired by Karpathy's [llm-council](https://github.com/karpathy/llm-council), which answers a question with several models, has them rank each other's anonymized answers, and has a chairman synthesize the result. This mode applies those ideas to expert document review: nothing is copied, a reviewer never judges its own findings, and findings are checked one by one instead of whole answers being ranked.

## Arena (`council:arena`)

For **generating** ideas, not reviewing them. Give it a rough idea or open question; it returns the strongest version it can find.

Each competitor is a sub-agent that gets the same brief plus one strategy card (a lens such as *inversion* or *customer's eyes*, a shape such as *phased rollout* or *platform*, and a bias such as *cheapest* or *lowest risk*). Each pitches its own version; pitches then meet in single-elimination matches — attack, defend and revise, then a blind judge scores both on a fixed rubric (value, feasibility, robustness, specificity, originality). A pitch with a fatal flaw that holds always loses.

| Command | Field | Sub-agent calls |
|---------|-------|-----------------|
| `/council:arena <idea>` | 8 | 43 |
| `/council:arena --quick <idea>` | 4 | 19 |
| `/council:arena --field N <idea>` | 2–16 | N + 5 × (N − 1) |
| add `--baseline` | — | +1: also judges the champion blind against your current version |

The result is the champion pitch, the attacks it withstood, ideas worth salvaging from the losers, and its open risks. It states the cost before starting and asks first for fields over 8. Working files go to `.arena/<run-id>/` in the current folder (delete when done); it never edits your project. Strategy cards and the rubric are editable in `skills/arena/cards.md` and `skills/arena/rubric.md`.

Inspired by [arena-skill](https://github.com/Jakeschincariol/arena-skill) (MIT), which runs up to 100 competitors on tasks; this one is a smaller, markdown-only take aimed at ideas.

## Court (`council:court`)

For a **verdict** on an idea or decision as you stated it — should you do this, and what sinks it? Use the arena to improve an idea; use the court to test one before you commit.

A prosecutor files up to five numbered charges, the defense answers each (conceding only what is true), and a jury of sub-agents — each a different perspective (cost accountant, first-time customer, engineer, compliance officer, investor, frontline employee, …) — votes on every charge and on the idea overall without seeing each other's votes. A judge then writes the verdict and the **conditions for acquittal**: the changes that would flip the most votes. Ties are reported as hung, never forced.

| Command | Jury | Sub-agent calls |
|---------|------|-----------------|
| `/council:court <idea>` | 9 | 14 |
| `/council:court --quick <idea>` | 5 | 10 |
| `/council:court --jury N <idea>` | 3–12 | N + 5 |

Give it the specifics (numbers, audience, what you've tried, the alternative): the jury judges only what the case file states. Working files go to `.court/<run-id>/` in the current folder (delete when done); it never edits your project. The jury pool is editable in `skills/court/jurors.md`. The verdict is a structured second opinion, not legal, financial or professional advice.

Inspired by [court-skill](https://github.com/alexyc9381/court-skill) (MIT); this one is markdown-only, votes on each charge, and uses a business/IT jury pool.

## Conclave (`council:conclave`)

For **exploring** an idea: what am I not seeing? The arena finds the best version, the court rules on one, the conclave maps it. Use it early, before you know which version to build or whether to commit.

A panel of sub-agents, each a different lens (customer advocate, unit economist, systems thinker, pragmatic builder, skeptic, downside guardian, daily operator, trust steward, …), forms a position **blind**. Each then cross-examines the others, starting with its **counterweight** (the lens aimed at its blind spot), and takes a final stance. A chair reports what is unresolved first, where the panel split (kept as a split, never smoothed over), where it converged, options nobody had stated, and a recommendation with kill criteria and one next step. Claims are labeled FACT / INFERENCE / ASSUMPTION / UNKNOWN, and a short ledger records the prediction and review date.

| Command | Panel | Sub-agent calls |
|---------|-------|-----------------|
| `/council:conclave <idea>` | 6 | 19 |
| `/council:conclave --quick <idea>` | 4, blind positions only | 5 |
| `/council:conclave --seats N <idea>` | 3–12 | 3N + 1 |

It states the cost before starting and asks first when a run is over 20 calls. If you have already decided and want approval, or the question is a plain lookup, it says so and suggests a better tool. Working files go to `.conclave/<run-id>/` in the current folder (delete when done); it never edits your project. The lens pool is editable in `skills/conclave/lenses.md`. The report is a set of perspectives from language models, not professional advice, and a panel agreeing is not proof.

Inspired by [council-of-high-intelligence](https://github.com/0xnyk/council-of-high-intelligence), a separate general-purpose multi-host skill that this one does not replace; this one is markdown-only, uses business/IT lenses instead of historical personas, and has a smaller, cost-bounded panel.

## Setup

No configuration, environment variables, or external connectors required — every skill runs on its own using only the document you give it.

## Usage

1. Attach or paste the document (or point Claude at a file) in your message.
2. Run an area (`/council:it` or `/council:business`) for every expert in it and one reconciled verdict, or add flags (`/council:it --security`) for specific experts.
3. Plain language works too — each skill's description lists the phrases it responds to ("security review", "have leadership review this").

## Legal disclaimer

The `--legal` expert's output is a risk-flagging pass, not legal advice — it's meant to tell you what to send to an actual attorney, not to replace one.

## Install

Published through the `jtag-claude-marketplace` marketplace:

```text
/plugin marketplace add jimmydagher/jtag-claude-marketplace
/plugin install council@jtag-claude-marketplace
```

## Customization

Want another expert, or another area? Just ask. Want different arena strategies? Edit `skills/arena/cards.md`. Different jurors? Edit `skills/court/jurors.md`. Different panel lenses? Edit `skills/conclave/lenses.md`. A new expert is one markdown file in its area's `experts/` folder plus one row in that area's skill; a new area is one new skill folder with its own `experts/`.
