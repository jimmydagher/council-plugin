---
name: eli5
description: >
  Use to "eli5 this", "explain this like I'm five", "ask the kid", "does this
  make sense to a beginner", "find the jargon in this", or "/council:eli5".
  The kid: one sub-agent that has only the text, nothing else, explains the
  document or idea back in plain words a five-year-old would follow, then
  lists every place it got lost — jargon, missing reasons, steps that jump —
  with a plainer rewrite for each. A clarity check, not a review of the
  content. No flags.
---

Before anything else, read the "What this council reviews" and "Shared process, every expert" sections of `../../references/shared-context.md`. The area/expert argument rules there do not apply to this skill.

This skill **tests whether a document or idea can be understood by someone with no background**. It does not judge whether the content is right: for that use `council:it` or `council:business` (review), `council:court` (verdict) or `council:conclave` (what am I missing).

## Arguments

None. Everything the user typed is the document or idea. If a flag-like word (`--quick`, `--peer`, ...) is given, say this skill has no flags and stop. If nothing to explain can be identified, ask which file, text or idea before spending the sub-agent call.

## Process

1. **Prepare the text.** Take the document or idea exactly as written (read the file if one is named). Do not summarize, simplify or add context: the kid must see only what a real reader would.
2. **One sub-agent call, text only.** Brief it with the text and nothing else — no project, no goal, no your-own-notes — and this instruction: *You are a curious five-year-old who is very good at listening. Explain back what this is about in a few short sentences using only words a five-year-old knows, and use one everyday comparison. Then answer honestly: where did you get lost?* It returns the two sections below, labeled.
3. **Don't edit the kid's answer.** Print it under the output structure below. The main session adds only the closing line.

## Output

**The kid's version** — three to six short sentences and one everyday comparison. If the kid could not explain it at all, it says so here instead of guessing.

**Where the kid got lost** — a table, in reading order:

| # | Quote | Why it lost the kid | Plainer version |
|---|-------|---------------------|-----------------|

Why is one of: jargon or acronym · missing reason (says what, not why) · step that jumps · assumes something unsaid · too many ideas at once. Every row carries a concrete rewrite, not "make it clearer". If nothing lost the kid, say so in one line and name what was checked.

Close with one line: how many rows, and whether the idea's core survived the translation. No run files are written; the skill never touches the user's project.

This is a readability check by a model standing in for a beginner; it shows where text is hard to follow, not that real beginners would follow the rewrite.
