# Recalibrate-all run 2026-05-31

## Phase 0.1 — Orphan map
| File | Line | Match | Doomed skill | Replacement |
| skill-trainer/SKILL.md | 33 | design-taste row | design-system-init | row removed (category orphaned) |
| skill-trainer/SKILL.md | 34 | design-process row | design-generate | row removed (category orphaned) |
| quick-learning/SKILL.md | 10 | "called by ... design-generate" | design-generate | strip from list |
| photo-crop/SKILL.md | 17 | "use after /design-generate" | design-generate | replace with frontend-design:frontend-design |
| user-spec-planning/SKILL.md | 145 | design-plan + design-spec workflow | design-plan, design-spec | UNREPLACEABLE (planning workflow) → skip deletion |
| quick-learning/references/triad-index.md | many | Adapted column provenance | design-generate, design-system-init | RETAINED as historical metadata, not active workflow |
| quick-learning/references/reasoning-patterns.md | many | historical context | design-generate, design-system-init, design-retrospective, design-task-decompose | RETAINED as historical context |

## Phase 0.2 — Skipped deletions
- design-plan: referenced by user-spec-planning/SKILL.md:145 as active workflow step — no plugin equivalent (planning skill)
- design-spec: referenced by user-spec-planning/SKILL.md:145 as active workflow step — no plugin equivalent (planning skill)

## Phase 0.3 — Codex retention (generic delegation kept)
- feature-execution/references/orchestrator-patterns.md:14 — rule kept, "Codex" stripped → "внешний агент"
- code-writing/SKILL.md — Codex-only Phase 2 block deleted; rule line 170 deleted (Codex-only delegation)
- feature-execution/SKILL.md — Codex mode block (1.6), Codex-First Routing block, 2 Codex bullets in Promoted Patterns deleted
- feature-execution/references/codex-routing.md — entire file deleted (Codex-specific)
- feature-execution/references/orchestrator-patterns.md:79 — pattern 25 deleted (Codex-specific)
- do-task/skill.md — Codex-First Path deleted; Claude Path renamed to plain execute
- quick-learning/references/quick-ref-feature-execution.md — 2 Codex bullets removed, list renumbered

## Phase 0.4 — Triad retention
- triad-index #226 v1 (codex delegation reflex): deleted (Codex-specific, no coherent rule without it)
- triad-index #226 v2 (full diff after delegation): kept, "(Codex)" stripped
- triad-index #241 (audit/review): deleted (Codex-specific)
- reasoning-patterns.md: triad #226 v1 block deleted, triad #226 v2 rewritten generic
- Historical Context paragraphs mentioning Codex left intact (frozen reasoning records, not active rules)

## Phase 0.5 — Memory retention
Deleted (5 files, positive/operational Codex usage):
- d-----6/memory/feedback_codex-for-execution.md
- d-----9/memory/feedback_codex_delegation.md
- d-----9/memory/feedback_codex_agent_status.md
- SuperJob/memory/feedback_codex_delegation.md
- d-----14/memory/feedback_codex_default.md

Retained (5 files, prohibitions or unrelated business knowledge):
- d-----8/memory/feedback_delegate_code_to_codex.md — meta-cancellation of codex rule
- d-----10/memory/feedback_no_codex.md — "Codex отключён навсегда"
- d-----12/memory/feedback_no_codex_delegation.md — "Никогда не делегировать Codex"
- d-----6/memory/feedback_never_use_codex.md — "Никогда не использовать Codex"
- d-----6/memory/project_codex_pipeline_product.md — business knowledge (user's product named "Codex pipeline", body is about ChatGPT add-on, not Codex tool usage)

## Phase 1 — Skill discovery
| Skill | Lines | references/ | Status |
| framer-motion | 270 | no | FAIL |
| methodology | 212 | no | WARN |
| ui-styling | 256 | yes | DELETED (Phase 0.2 follow-up) |
| ui-ux-pro-max | 531 | no | DELETED (Phase 0.2 follow-up) |
| design | 223 | yes | DELETED (Phase 0.2 follow-up) |
All other 45 skills: <200 lines, OK.

Scope for Phase 2: framer-motion, methodology (2 skills, single wave).

## Phase 2 — Audit findings (skipped)

## Phase 3 — Manual fix needed
