---
name: it
description: >
  Use to "convene IT", "have engineering review this", "run all IT
  experts on this document", "security review", "standards review",
  "efficiency review", "infrastructure review", or "/council:it".
  Runs the Security, Standards, Efficiency, and Infrastructure experts on
  a document. With no flag, runs all four and converges one reconciled IT
  verdict; with flags (--security, --standards, --efficiency, --infra)
  runs only those experts.
---

Before anything else, read `../../references/shared-context.md`, including its argument rules.

## Experts

In this order (the canonical order, whatever order the flags came in):

| Flag | Alias | Review title | Definition |
|------|-------|--------------|------------|
| `--security` | | Security Review | `experts/security.md` |
| `--standards` | | Standards Review | `experts/standards.md` |
| `--efficiency` | | Efficiency Review | `experts/efficiency.md` |
| `--infra` | `--infrastructure` | Infrastructure Review | `experts/infra.md` |

## Process

1. Select the experts from the arguments as `shared-context.md` describes. On a bad flag, give the error it specifies and stop.
2. Identify the document under review. If genuinely unclear, ask before proceeding.
3. Read only the selected expert definitions. Review the document once per selected expert, applying its checklist and output format exactly. Keep each review self-contained.
4. One expert selected: output that review and stop — no verdict. Two or more: close with an **IT Verdict** that reconciles the selected reviews — the most important part of the output, not a shallow summary.

## Output structure

Present the selected reviews first, each under its own heading from the table, in canonical order, each following its own definition's format exactly.

Then, when two or more ran, close with:

---

## IT Verdict

**Where they agree:** findings two or more experts independently flagged, or issues that reinforce each other (e.g. a missing auth check from Security and a missing audit-log retention plan from Infrastructure are related).

**Where they conflict:** name the specific tensions explicitly — usually some version of security/robustness vs. simplicity, or polish/completeness vs. cost/lean infrastructure. State both sides of each tension in one sentence each.

**Resolution:** for each conflict, make an actual call rather than presenting both sides and stopping. Default: unresolved *Critical* or *High* findings from Security always outrank the others and must be addressed regardless of what the other experts say. Beyond that, prioritize by concrete impact/likelihood, not by which expert raised it.

**Single verdict:** one of `Not ready — blocking issues to resolve first`, `Ready with required changes`, `Ready with optional follow-ups`, or `Ready to ship` — plus a short numbered list of the specific changes required, ordered by priority. If nothing is required, say so.

Keep the IT Verdict tight — a lead reviewer's summary after reading all the takes, not a repeat of the findings tables. When only a subset ran, reconcile just those and say which experts were not run.
