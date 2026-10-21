# Council — Plan

## ⛏️ In progress

**TTD001 / TODO #1 — Consolidate skills into area skills with expert flags.** Behavior is in `SPEC.md`.

### Decision: where the experts live

Options considered:

1. **Stay as skills** — rejected: that is the structure being removed, and each would still show up as its own `/council:*` command.
2. **Under `references/`** — workable, but the experts belong to one area, and `references/` is for what every skill shares.
3. **One file per area holding all experts** — rejected: a `--finance` run would load all four experts, and the file grows with every expert added.
4. **One file per expert inside its area skill folder** — **chosen.** `skills/it/experts/security.md`, and so on. A run reads only the selected expert files; adding an expert is one new file plus one row in the area's table; `references/` stays for truly shared content.

Resulting layout:

```text
skills/
├── it/
│   ├── SKILL.md              — parse flags, run experts, IT Verdict
│   └── experts/{security,standards,efficiency,infra}.md
└── business/
    ├── SKILL.md              — parse flags, run experts, Business Verdict
    └── experts/{ops,finance,strategy,legal}.md
references/shared-context.md  — shared rules for every area and expert
```

Expert files are plain markdown with no frontmatter, so they are not registered as skills. Their body (checklist, output format, verdict wording) is moved unchanged.

### Steps

1. [x] `git mv` the eight expert definitions into `skills/it/experts/` and `skills/business/experts/`; drop only the frontmatter and the line "Before anything else, read shared-context" (the area skill now does that once).
2. [x] Rewrite `skills/it/SKILL.md`: frontmatter description covering the plain-language triggers of the old expert skills, argument parsing (flags, aliases, unknown/cross-area flag error listing valid flags, no flag = all), an expert table (flag → file), read only the selected expert files, one expert = no verdict, subset = verdict over the subset.
3. [x] Create `skills/business/SKILL.md` the same way from `skills/bu` ("Business Verdict"); delete `skills/bu`.
4. [x] Delete `skills/all` and the eight old expert skill folders.
5. [x] Rewrite `references/shared-context.md` (see SPEC › Shared context). It currently tells the model that each lens is invoked by its own skill name and lists the old tree, so every one of these changes:
   - Intro paragraph: lenses are called as an area plus a flag (`council:it --security`), not as skills named `it-security`.
   - "Structure" tree: replace with the two areas and their `experts/` files; drop `council:all`.
   - "Bucket skills" section → "Area skills": parse flags, run the selected experts in canonical order, each in its expert file's exact format, then close with the verdict only when two or more ran.
   - "Individual lens skills" section → "Expert files": each defines its own checklist and output table, lives under its area's `experts/` folder, and is not invocable on its own.
   - Add the argument rules (flags, aliases, errors) once here so both area skills point to it instead of repeating them.
   - Keep unchanged: what the council does and doesn't review, the `code-reviewer` redirect, and the four shared-process rules.
6. [x] Update `README.md` (structure, tables, usage with flag examples, legal disclaimer, customization: how to add an expert or an area) and `.claude-plugin/plugin.json` description and keywords. Leave `version` to the release hooks.
7. [x] Add notes under `## 🚧 Unreleased` in `meta/CHANGELOG.md` (create if missing) citing `TODO #1`, with the breaking removals listed.
8. [x] Verify:
   - grep for stale references: `council:all`, `it-security`, `it-standards`, `it-efficiency`, `it-infra`, `bu-`, `council:bu`, "individual lens skills".
   - `git diff -M` shows the eight expert files as renames with only the frontmatter and read-first line removed.
   - Trace one run per case: area only, single flag, two flags out of order, alias, unknown flag, cross-area flag.

### Risks and notes

- Breaking change for anyone using `council:it-security` and similar, or `council:all`; called out in the changelog. Version bump is for the owner and the release hooks.
- No automated test harness exists (markdown-only plugin); verification is the checks in step 8.
- Out of scope: the `eli5` expert and arena concept (TODO #2, #3). The layout is meant to make adding them cheap.

## ✅ Done

(none)
