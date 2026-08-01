# Patterns & Conventions

Coding conventions, development workflow, and project-specific practices.

---

## Project-Specific Conventions

**Skill files:** Each skill lives in `{skill-name}/SKILL.md`. Name is kebab-case. Instructions are in Markdown, written for Claude to follow. No code — only prose instructions.

**Multi-phase procedural skills:** Skills with file I/O and multi-step user interaction are structured as numbered Phases (Phase 1: Validation → Phase 2: ... → Phase N: ...). Each phase ends with a gate before proceeding. The skill ends with a `## Checks against state` block and a "Next: /{skill-name}" chaining hint. Max 500 lines per SKILL.md.

**Checks against state, not self-verification checklists.** A closing block lists commands that read state off disk — a file that must exist, a frontmatter field that must be set, a commit that must reference the task — together with the delta expected from each. It does not list tick-boxes asking the executor whether it did its work well: the executor already checks that, and a rule restated as a tick-box catches nothing, because whoever broke the rule in the body will not catch themselves with a copy of it. If nothing on disk can answer the question, say plainly that it is a user check rather than dressing it as one.

**Agent files:** `agents/{agent-name}.md`. The parent skill reads the agent file inline and follows its instructions (e.g. `sketch-interviewer.md`). Validators are separate: launched via the built-in `Agent` tool with `subagent_type`.

**Templates:** Files in `shared/work-templates/` end with `.template` suffix and contain placeholders in `{curly-braces}`. Never edit templates in place — always copy first.

**Work artifacts:** All per-feature work goes in `work/{feature-name}/`. This directory is local only (in `.gitignore` or committed per feature). Source of truth for active feature work.

**Knowledge system:** Patterns added via `/quick-learning` only — never write directly into skills, bypass breaks the promotion cycle (see architecture.md → Key Components → Quick-learning system for the buffer/promotion mechanics).

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

Promotion threshold is `Seen >= 4` (see architecture.md → Quick-learning system). Lower threshold allowed only for critical safety patterns.

### Single Source of Truth Rule

`~/.claude/skills/` is the canonical source. There is no derived copy to keep in sync.

### No Model or Effort in a Skill Body

A skill says what an agent does, never which model runs it or how hard it thinks. Both are
configuration — set in the harness and in each agent's frontmatter — and a skill that pins either
one overrides a deliberate setting and goes stale with it. The same applies to explaining a rule by
the behaviour of a named model: the next reader is a different model and will take the description
as a statement about itself. The reason for a change belongs in the git commit, not in the skill.

### English Body

Skill bodies, headings, tables and patterns are written in English. Russian stays only where the
language is the content: trigger phrases in `description` (they are matched against what the owner
types), strings the skill prints to the owner, Russian text used as data (infostyle stop-word lists,
legal templates for Russian regulators), and generated deliverables the owner reads.
