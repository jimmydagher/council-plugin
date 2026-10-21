---
name: business
description: >
  Use to "convene the business council", "have leadership review this",
  "run all business experts on this document", "operations review",
  "finance review", "strategy review", "legal review", or
  "/council:business". Runs the Operations, Finance, Strategy, and Legal
  experts on a proposal. With no flag, runs all four and converges one
  reconciled Business verdict; with flags (--ops, --finance, --strategy,
  --legal) runs only those experts.
---

Before anything else, read `../../references/shared-context.md`, including its argument rules.

## Experts

In this order (the canonical order, whatever order the flags came in):

| Flag | Alias | Review title | Definition |
|------|-------|--------------|------------|
| `--ops` | `--operations` | Operations Review | `experts/ops.md` |
| `--finance` | | Finance Review | `experts/finance.md` |
| `--strategy` | | Strategy Review | `experts/strategy.md` |
| `--legal` | | Legal Review | `experts/legal.md` |

## Process

1. Select the experts from the arguments as `shared-context.md` describes. On a bad flag, give the error it specifies and stop.
2. Identify the proposal or document under review. If genuinely unclear, ask before proceeding.
3. Read only the selected expert definitions. Review the proposal once per selected expert, applying its checklist and output format exactly. Keep each review self-contained.
4. One expert selected: output that review and stop — no verdict. Two or more: close with a **Business Verdict** that reconciles the selected reviews — the most important part of the output, not a shallow summary.

## Output structure

Present the selected reviews first, each under its own heading from the table, in canonical order, each following its own definition's format exactly.

Then, when two or more ran, close with:

---

## Business Verdict

**Where they agree:** findings two or more experts independently flagged, or issues that reinforce each other (e.g. an Operations accountability gap and a Finance unquantified-savings flag are both symptoms of a plan that isn't rigorous enough yet).

**Where they conflict:** name the specific tensions explicitly — often near-term cost/efficiency (Operations, Finance) vs. an investment needed for long-term position (Strategy), or a commercial term Legal flags as risky that Finance is counting on for the savings case. State both sides of each tension in one sentence each.

**Resolution:** for each conflict, make an actual call. Defaults when nothing in the document says otherwise: a Legal finding with "Needs counsel: Yes" on real financial/regulatory/liability exposure outranks a near-term cost or efficiency win — that exposure compounds and is expensive to unwind later. Beyond that, a well-justified savings or efficiency gain from Operations or Finance outranks a vague, unquantified Strategy concern.

**Single verdict:** one of `Not ready — leadership concerns to resolve first`, `Ready with required changes`, `Ready with optional follow-ups`, or `Ready to move forward` — plus a short numbered list of the specific changes required, ordered by priority. If nothing is required, say so.

Keep the Business Verdict tight — a leadership team's summary after reading all the takes, not a repeat of the findings tables. When only a subset ran, reconcile just those and say which experts were not run.
