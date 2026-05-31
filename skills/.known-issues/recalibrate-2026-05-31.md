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

## Phase 0.5 — Memory retention

## Phase 1 — Skill discovery
| Skill | Lines | references/ | Status |

## Phase 2 — Audit findings (skipped)

## Phase 3 — Manual fix needed
