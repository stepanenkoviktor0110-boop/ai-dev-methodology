# Patterns & Conventions

Coding conventions, development workflow, and project-specific practices.

---

## Project-Specific Conventions

**Skill files:** Each skill lives in `{skill-name}/SKILL.md`. Name is kebab-case. Instructions are in Markdown, written for Claude to follow. No code — only prose instructions.

**Multi-phase procedural skills (moneymaker pattern):** Skills with file I/O and multi-step user interaction are structured as numbered Phases (Phase 1: Validation → Phase 2: ... → Phase N: ...). Each phase ends with a gate before proceeding. The skill ends with a `## Self-Verification` checklist and a "Next: /{skill-name}" chaining hint. Max 500 lines per SKILL.md.

**Agent files:** `agents/{agent-name}.md`. In Claude version, the parent skill reads the agent file inline and follows its instructions (e.g. `sketch-interviewer.md`). In Codex, agent files are spawned directly via `spawn_agent`.

**Templates:** Files in `shared/work-templates/` end with `.template` suffix and contain placeholders in `{curly-braces}`. Never edit templates in place — always copy first.

**Work artifacts:** All per-feature work goes in `work/{feature-name}/`. This directory is local only (in `.gitignore` or committed per feature). Source of truth for active feature work.

**Knowledge system:** Patterns go to `quick-learning/references/reasoning-patterns.md` as triads (Goal / Context / Decision). Promoted to skills when `Seen >= 4`. Never write patterns directly into skills without the quick-learning promotion cycle.

---

## Git Workflow

### Branch Structure

- **`master`** — single branch, all work committed directly. No staging branch.

### Branch Decision Criteria

Direct to `master`: all changes. No feature branches used in this project.

### Commit Convention

Free-form commit messages. Common prefixes observed: `feat:`, `fix:`, `docs:`, `learn()`, `chore()`.

---

## Testing & Verification

### Test Infrastructure

No automated tests. The "tests" are functional: invoke a skill, observe Claude's behavior, verify output matches intent.

### Verification Methods

**Skill change:** Read the updated SKILL.md, mentally trace through a typical invocation scenario. Optionally invoke the skill in a test project.

**Template change:** Copy template to a temp location, fill placeholders manually, verify structure is correct.

**Knowledge system change:** Check `triad-index.md` for duplicates after adding a new pattern.

---

## Business Rules

### Methodology Pipeline Order

**Full pipeline:** User Spec → Tech Spec → Tasks → Code. Each stage requires explicit user approval before proceeding. No skipping gates.

**Sketch Mode (lightweight path):** `/sketch` → 3–5 question interview → `sketch.md` (confirmed by user) → code in one session (no validators) → decision gate: develop (`/new-user-spec`) or archive (`/done`). Used when idea needs prototyping before committing to full pipeline.

### Skill Promotion Rule

Reasoning pattern promoted from `reasoning-patterns.md` into a skill's body only after `Seen >= 4` (appeared in 4 independent sessions). Lower threshold allowed for critical safety patterns.

### Codex Adaptation Rule

When porting a skill to Codex, apply the platform differences described in architecture.md — Platform Differences section. Logic stays identical; only platform-specific references change.

### Single Source of Truth Rule

`~/.claude/skills/` is the canonical source. Codex repo (`C:/tmp/ai-dev-methodology-codex/`) is a derived artifact — changes flow from Claude version to Codex, never the reverse (except Codex-specific features like `clean-delivery`).
