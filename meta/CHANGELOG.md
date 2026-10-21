# Changelog

## 🚧 Unreleased

- Skills are now organized by area with an expert flag: `/council:it` and `/council:business` run every expert in the area and a reconciled verdict, while `--security`, `--standards`, `--efficiency`, `--infra`, `--ops`, `--finance`, `--strategy` and `--legal` run only the chosen experts (TODO #1).
- Breaking: removed `/council:all`, the per-expert skills (`council:it-security`, `council:it-standards`, `council:it-efficiency`, `council:it-infra`, `council:bu-ops`, `council:bu-finance`, `council:bu-strategy`, `council:bu-legal`), and renamed `council:bu` to `council:business` (TODO #1).
- Expert definitions moved to `skills/<area>/experts/<expert>.md` and are no longer skills; `references/shared-context.md` and the README describe the new flag rules (TODO #1).
