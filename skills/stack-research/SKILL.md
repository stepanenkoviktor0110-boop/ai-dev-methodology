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

> **CONTEXT BUDGET:** subagents do all heavy reading. The orchestrator never loads individual reports into its own context — only aggregator output and short DONE lines.

Orchestrate parallel documentation research for one or more stack candidates. Produce focused reports, optional comparison table, and update the stack registry. Version-based cache avoids redundant research.

**Input (from caller):**
- `decision_context`: one sentence — what is being decided
- `candidates`: list of 1..N elements. Each: `{ name, type: external-api|library|service|tool }`
- `depth`: `shallow` | `deep`
- `project_context`: 2-3 sentences — what the project needs from this element
- `feature_path`: absolute path to feature folder (per-feature reports live under `{feature_path}/logs/stack-research/`)

**Output:**
- Per-candidate report at `{feature_path}/logs/stack-research/{slug}.md` (written by `stack-researcher`)
- If `candidates.length > 1` → `stack-comparison-{slug}.md` in PK (written by `stack-aggregator`)
- If `depth=deep` → registry entry in `stack-research.md` in PK (written by `stack-aggregator`)
- Short summary returned to caller (paths + DONE digest)

## Context Protocol

1. The orchestrator (this skill) NEVER reads per-candidate reports — only the aggregator does.
2. Every subagent returns exactly one DONE line. The orchestrator stores those lines as its record of Phase 4 and Phase 5.
3. After aggregation, the caller may read `stack-comparison-{slug}.md` — it is the single consolidated artifact.
4. Target: total main-context cost per `/stack-research` invocation ≤ 2–3k tokens regardless of candidate count.

## Phase 1: Trigger Check

For each candidate, consult [stable-libraries-whitelist.md](references/stable-libraries-whitelist.md).

- On whitelist + caller didn't explicitly request → skip that candidate. Note in return summary.
- Not on whitelist OR caller explicitly requested → proceed.

External APIs, services, paid/niche tools are NEVER whitelisted.

## Phase 2: Formulate Focus Questions

Derive 4–8 focus questions per candidate, grounded in `project_context`. Must be answerable from official docs. Do not ask opinions.

Examples:
- img2img with small inputs → "Supports img2img? Min/max input image size? Accepted formats?"
- deploy from Russia → "Available without proxy? Auth via Russian phone/email?"
- free tier only → "Free tier quota? Rate limits on free tier?"

## Phase 3: Cache Check (version-based)

For each candidate, look up `stack-research.md` registry by `name`.

Resolve current version cheaply (one request — do NOT read full docs):
- `library` (npm) → `https://registry.npmjs.org/{pkg}/latest` via WebFetch, or Context7 `resolve-library-id` metadata
- `external-api` / `service` / `tool` → changelog/landing page date via WebFetch (pseudo-version)

| Registry state | Current version | Action |
|---|---|---|
| No entry | — | `effective_focus` = all focus questions. Full research. |
| Same version | Matches | `effective_focus` = ONLY new focus questions not in cache. If empty → skip subagent entirely, record "cached" in return summary. |
| Different version | Changed | `effective_focus` = all focus questions. Full re-research. |
| No version available, registry older than 30 days | — | `effective_focus` = all focus questions. |

## Phase 4: Parallel Research

For each candidate with non-empty `effective_focus`, spawn a `stack-researcher` subagent (ONE message, multiple Agent calls — parallel).

Per-subagent input:
- `element`, `element_type`, `focus` (= `effective_focus`), `depth`, `project_context`
- `output_path`: `{feature_path}/logs/stack-research/{slug}.md`

Each subagent returns one `DONE element=...` line. The orchestrator collects these lines and proceeds — it does NOT read the `output_path` files.

Candidates with empty `effective_focus` (full cache hit) skip Phase 4 entirely.

## Phase 5: Aggregation

Spawn ONE `stack-aggregator` subagent with:
- `reports`: list of all `output_path`s (from Phase 4) + registry-cached candidates marked with `cached=true`
- `depth`: from input
- `decision_context`: from input
- `slug`: derived from `decision_context` (e.g. `img2img-api`)
- `project_root`: absolute path to current project
- `comparison_path`: `{project_root}/.claude/skills/project-knowledge/references/stack-comparison-{slug}.md` if `candidates.length > 1`, else `null`
- `registry_path`: `{project_root}/.claude/skills/project-knowledge/references/stack-research.md`

The aggregator reads every report in its isolated context, writes comparison + registry, returns one `DONE comparison=... registry_updated=... candidates=N digest=...` line.

The orchestrator NEVER reads the individual reports. The aggregator is the firewall.

## Phase 6: Return to Caller

Return a short summary composed from DONE lines only:

```
Stack research complete.
- kandinsky-5 (external-api, shallow): fresh [answered=7/7]
- paged-js (library, deep): cached (v0.4 unchanged)
- study-ai (service, shallow): fresh [answered=3/5, notfound=2]

Comparison: .claude/skills/project-knowledge/references/stack-comparison-img2img-api.md
Registry updated: paged-js
```

The caller opens `stack-comparison-{slug}.md` when it needs to compare candidates, or reads specific registry entries when writing Decisions. The orchestrator itself has seen NONE of the content.

## Practical Limits

- 2–5 candidates per invocation is optimal. 6+ starts straining Agent-tool parallelism and produces comparison tables too wide to read.
- If more than 5 candidates need review, split into two rounds: hard-filter to a shortlist, then research the shortlist.

## Idempotency

- Version check prevents redundant research across sessions/projects.
- Per-candidate reports overwrite previous runs.
- Comparison file updated in place.
- Registry entries keyed by name — replaced on version change, extended on version match.

## What This Skill Does NOT Do

- Does NOT make recommendations. Caller decides.
- Does NOT fill missing info from memory. Docs-only.
- Does NOT load report contents into the orchestrator's context. That is the aggregator's job.
- Does NOT research whitelisted libraries unless caller explicitly asks.
- Does NOT re-research an element at an unchanged version, except for new focus questions.
