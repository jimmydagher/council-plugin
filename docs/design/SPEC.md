# Council — Specification

Behavior of the `council` plugin after TODO #1 / TTD001 (skill restructure). Council reviews documentation, designs, plans, and business proposals — never source code (see `code-reviewer`).

## Invocation

One skill per **area**. A flag narrows it to specific **experts** (lenses) within that area.

| Command | Result |
|---------|--------|
| `/council:it` | All IT experts, plus a reconciled **IT Verdict** |
| `/council:it --security` | Only the Security expert; no verdict |
| `/council:it --security --infra` | Only those experts, plus a verdict reconciling just them |
| `/council:business` | All business experts, plus a reconciled **Business Verdict** |
| `/council:business --finance` | Only the Finance expert; no verdict |

Rules:

- The area skill is the only entry point. Plain-language triggers ("security review", "finance review") still route to the area skill with the matching expert.
- Flags are `--<expert>`, case-insensitive, any order, repeatable. No flag means every expert in the area.
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
