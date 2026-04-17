---
name: stack-research
description: |
  Explicit-call only. Invoked by project-planning and tech-spec-planning as a
  gate before stack decisions, or manually via /stack-research. Not
  auto-triggered by keywords. Researches stack elements (libraries, APIs,
  services) against official documentation via parallel subagents, produces
  comparison tables, and maintains a stack registry in project knowledge.
---

# Stack Research

> **CRITICAL:** Research is a FACT-GATHERING step, not a decision step. This skill returns data. The calling skill (project-planning or tech-spec-planning) decides based on the data.

Orchestrate parallel documentation research for one or more stack candidates. Produce focused reports, optional comparison table, and update the stack registry. Uses a version-based cache: if the element is already in the registry at the same version, only NEW focus questions trigger research.

**Input (from caller):**
- `decision_context`: one sentence — what is being decided (e.g., "AI API for img2img in PDF illustrations")
- `candidates`: list of 1..N elements. Each: `{ name, type: external-api|library|service|tool }`
- `depth`: `shallow` (comparing) or `deep` (chosen element, deep study)
- `project_context`: 2-3 sentences — what the project needs from this element in its constraints (Russia-accessible, free tier, etc.)
- `feature_path`: absolute path to the feature folder (for per-feature reports)

**Output:**
- Per-candidate report in `{feature_path}/logs/stack-research/{slug}.md` (merges cached answers + new answers into one file)
- If `candidates.length > 1` → `stack-comparison-{slug}.md` in `.claude/skills/project-knowledge/references/`
- If `depth=deep` → registry entry updated in `.claude/skills/project-knowledge/references/stack-research.md`
- Return summary to caller: paths + 3-line digest per candidate

## Phase 1: Trigger Check

For each candidate, consult [stable-libraries-whitelist.md](references/stable-libraries-whitelist.md).

- **On whitelist + caller didn't explicitly request** → skip research for that candidate. Write one line to the caller: "{name} is on the stable whitelist, skipping auto-research. Request explicitly if needed."
- **Not on whitelist OR caller explicitly requested** → proceed.

External APIs, services, and paid/niche tools are NEVER whitelisted — always researched.

## Phase 2: Formulate Focus Questions

For each candidate, derive 4-8 focus questions **grounded in `project_context`** — not generic. Examples:

- Project needs img2img with small input images → "Supports img2img? Min/max input image size? Accepted formats? Returns direct URL or base64?"
- Project deploys from Russia without VPN → "Available from Russia without proxy? Auth via Russian phone/email?"
- Project is free-tier only → "Free tier quota? Rate limits on free? Payment methods accepted?"

Questions MUST be answerable from official docs. Do not ask opinions or predictions.

## Phase 3: Cache Check (version-based)

For each candidate, look up the existing entry in `.claude/skills/project-knowledge/references/stack-research.md` (registry) by `name`.

**Resolve current version** (cheap check — one request, no deep doc reading):
- `library` (npm) → fetch latest stable from `https://registry.npmjs.org/{pkg}/latest` via WebFetch, or Context7 `resolve-library-id` metadata.
- `external-api` / `service` without semver → read changelog/landing page date via WebFetch. Use date as pseudo-version.
- `tool` with GitHub releases → fetch latest release tag.

**Compare against registry version:**

| Registry state | Current version check | Action |
|---|---|---|
| No entry | — | `effective_focus` = all focus questions. Full research. |
| Same version | Matches | Load cached answers. `effective_focus` = ONLY focus questions NOT answered in cache. If empty → skip subagent entirely. |
| Different version | Changed | Cache invalid. `effective_focus` = all focus questions. Full re-research. |
| Same element, no version available, registry older than 30 days | — | Treat as stale. `effective_focus` = all focus questions. Full re-research. |

Store `cached_answers` (the answers that survive) and `effective_focus` (what still needs research) per candidate for Phase 4.

## Phase 4: Parallel Research

For each candidate with non-empty `effective_focus`, spawn a `stack-researcher` subagent with:
- `element`: candidate name + detected current version
- `element_type`: from input
- `focus`: `effective_focus` (new questions only)
- `depth`: from input
- `project_context`: from input
- `output_path`: `{feature_path}/logs/stack-research/{slug}.partial.md`

Spawn ALL non-cached candidates in parallel (one message, multiple Agent tool calls). Do not serialize.

Candidates with empty `effective_focus` (full cache hit) — skip subagent. They proceed directly to Phase 5 with `cached_answers` only.

## Phase 5: Merge Reports

For each candidate, assemble the final report at `{feature_path}/logs/stack-research/{slug}.md`:

- Header: name, type, depth, version, checked-date (today), sources.
- Focus Answers section: `cached_answers` + new answers from `{slug}.partial.md` merged in original focus order. Mark each answer with source tag: `[cached from {registry-date}]` or `[fresh]`.
- Key Facts / Breaking Changes / Gotchas: if full research ran, use subagent output. If full cache hit, copy from registry entry.
- Not Answered: union of both sets.

Delete the `.partial.md` file after merge — only the final report remains.

## Phase 6: Comparison Table (only if candidates.length > 1)

Create or update `.claude/skills/project-knowledge/references/stack-comparison-{slug}.md` where `{slug}` is derived from `decision_context` (e.g., `img2img-api`).

Use [stack-comparison-template.md](references/stack-comparison-template.md). Fill with:
- Row per focus question + key facts (version, auth, pricing, principal limits)
- Column per candidate
- Values copied from reports, not paraphrased
- Footer: `Checked: {YYYY-MM-DD}` + list of source report paths + note about which values were cached vs fresh

If the file exists — update in place, bump the `Checked` date. Do not create duplicates.

## Phase 7: Registry Update (only if depth=deep)

Update `.claude/skills/project-knowledge/references/stack-research.md` using [stack-research-template.md](references/stack-research-template.md).

For each candidate with `depth=deep`:
- If entry exists and version unchanged → append new focus-question answers to the entry, refresh `checked` date.
- If entry exists and version changed → replace entry entirely.
- If no entry → create new entry.

Fields: name, type, version, checked-date, auth, principal limits, gotchas, source URL, focus-answers accumulated across projects.

## Phase 8: Return to Caller

Return short summary:

```
Stack research complete.
- kandinsky-5 (external-api, shallow): work/{feature}/logs/stack-research/kandinsky-5.md
  [fresh] Supports img2img ✓, free tier 100 req/day, max input 2048px.
- paged-js (library, deep): work/{feature}/logs/stack-research/paged-js.md
  [cached, v0.4 unchanged] Skipped re-research. 2 new focus questions answered fresh.
- study-ai (service, shallow): work/{feature}/logs/stack-research/study-ai.md
  [fresh] Web-only, no public API as of 2026-04-18.

Comparison: .claude/skills/project-knowledge/references/stack-comparison-img2img-api.md
Registry updated: paged-js (deep)
```

The caller reads the comparison / registry and decides.

## Idempotency

- Version check ensures no redundant research across sessions/projects.
- Per-candidate reports overwrite previous run (single atomic Write).
- Comparison file updated in place.
- Registry entries keyed by name — replaced if version changed, extended if version same.

## What This Skill Does NOT Do

- Does NOT make recommendations. Caller decides.
- Does NOT fill missing info from memory. If docs don't cover it, it stays as `Not found in official docs`.
- Does NOT research whitelisted libraries unless caller explicitly asks.
- Does NOT evaluate architectural fit — only documentation facts.
- Does NOT re-research an element at an unchanged version, except for new focus questions.
