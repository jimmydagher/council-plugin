# Changelog

## 🚧 Unreleased

- Skills are now organized by area with an expert flag: `/council:it` and `/council:business` run every expert in the area and a reconciled verdict, while `--security`, `--standards`, `--efficiency`, `--infra`, `--ops`, `--finance`, `--strategy` and `--legal` run only the chosen experts (TODO #1).
- Breaking: removed `/council:all`, the per-expert skills (`council:it-security`, `council:it-standards`, `council:it-efficiency`, `council:it-infra`, `council:bu-ops`, `council:bu-finance`, `council:bu-strategy`, `council:bu-legal`), and renamed `council:bu` to `council:business` (TODO #1).
- New `/council:arena` skill: brainstorms the strongest version of an idea through a judged tournament of strategy-carded sub-agents (pitch, attack, defend, blind judge), with `--quick`, `--field N` and `--baseline` (TODO #2).
- New `/council:court` skill: puts an idea on trial — prosecution charges, defense, an independent jury voting on each charge and overall, and a judge's verdict with the conditions for acquittal; `--quick` and `--jury N` (TODO #3).
- New `/council:conclave` skill: a panel of differently-minded lenses forms positions blind, cross-examines and takes final stances, and a chair reports what is unresolved, where the panel split and converged, and a recommendation with kill criteria; `--quick` and `--seats N` (TTD004).
- New `--peer` mode for `/council:it` and `/council:business`: the selected experts review independently as sub-agents, check each other's findings anonymously (HOLDS / OVERSTATED / WRONG), a mechanical tally marks each finding upheld, contested or unchecked, and a chair writes the verdict with a Peer-contested line; lessons from Karpathy's llm-council (TODO #5).
- Changed: every skill's working files (arena, court, conclave, and `--peer` runs) now go to `~/.council/<skill>/<run-id>/` in your home folder instead of a dot-folder in the current project; the project is never written to (TODO #6, TTD006).
- Expert definitions moved to `skills/<area>/experts/<expert>.md` and are no longer skills; `references/shared-context.md` and the README describe the new flag rules (TODO #1).
