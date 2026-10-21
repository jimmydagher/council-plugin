> Read by every `council:arena` judge. The judge never sees the competitors' cards.

# Arena rubric

## Attack severity

| Label | Meaning |
|-------|---------|
| **FATAL** | If true, the idea cannot deliver its stated goal for its stated audience at all (it is illegal, impossible with the stated resources, solves a problem nobody has, or is already done and free). |
| **MAJOR** | If true, the idea still works but loses a large part of its value or needs a substantial redesign. |
| **MINOR** | If true, a gap that a small change fixes. |

Every attack must name a concrete failure scenario ("a customer with two accounts gets billed twice"), not a vague worry ("billing might be an issue").

## Verifying attacks

For each attack, after reading the defense and the revised pitch, decide:

- **Holds** — the attack is true of the revised pitch.
- **Answered** — the revision fixes it, or the rebuttal shows with evidence or reasoning that it was never true.
- **Unfounded** — the attack misread the pitch or has no concrete scenario.

Only attacks that **hold** count against a pitch.

## Criteria

Score each revised pitch 0–10 per criterion, then multiply by the weight and divide by 10. Totals are out of 100.

| Criterion | Weight | 0 | 5 | 10 |
|-----------|--------|---|---|----|
| **Value** | 30 | No real problem or no named audience | Real problem, vague audience or payoff | Named audience, clear pain, clear payoff |
| **Feasibility** | 25 | Cannot be done with what it states | Doable, but effort or resources are hand-waved | Effort, resources and dependencies stated and credible |
| **Robustness** | 20 | A FATAL or several MAJOR attacks hold | One MAJOR attack holds | No MAJOR or FATAL attack holds |
| **Specificity** | 15 | Slogan-level | Some concrete parts, first steps unclear | Someone could start the first step next week |
| **Originality** | 10 | The obvious first answer | A sensible twist on the obvious | A non-obvious angle that still holds up |

## Fatal-flaw rule

A pitch with a FATAL attack that **holds** cannot beat a pitch without one, whatever the totals. If both have one, the higher total wins. On an exact tie, the pitch with fewer MAJOR attacks holding wins; if still tied, the one with the higher Feasibility score.

## Judgment format

Write the judgment file in exactly this shape:

```markdown
# Judgment — <match id>

## Attacks on <id A>
| # | Severity | Status (Holds / Answered / Unfounded) | Why |

## Attacks on <id B>
| # | Severity | Status | Why |

## Scores
| Criterion | <id A> | <id B> |
|-----------|--------|--------|
| Value (30) | | |
| Feasibility (25) | | |
| Robustness (20) | | |
| Specificity (15) | | |
| Originality (10) | | |
| **Total** | | |

**Fatal flaw holding:** <id A>: yes/no · <id B>: yes/no
**Winner:** <id> — one sentence on the deciding difference.
```
