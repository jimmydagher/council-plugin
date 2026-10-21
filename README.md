# Council

A council of contractor-style reviewer experts for **documentation, designs, plans, and business proposals**. Each expert is named for what it does, not who it is — nothing to memorize to invoke the right one. For **source code**, use the separate `code-reviewer` plugin instead; that's a different job with its own process (intake → catalog → strategy → execute → validate), and this plugin deliberately doesn't overlap with it.

This plugin supersedes the earlier `council-of-claude` plugin, which named each lens after a person (Tom, Mike, Pedro, Hector, Emma, John, Natalie).

## Structure

```text
council
├── council:it        — Security, Standards, Efficiency, Infrastructure
└── council:business  — Operations, Finance, Strategy, Legal
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

Flags work in any order and the experts always run in the table's order. A flag that isn't one of the area's experts (such as `/council:it --finance`) is an error that lists the valid flags. There is no all-areas command: run `council:it` and `council:business` separately.

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

Want another expert, or another area? Just ask. A new expert is one markdown file in its area's `experts/` folder plus one row in that area's skill; a new area is one new skill folder with its own `experts/`.
