---
name: design-task-decompose
description: |
  Decompose approved design-plan.md into atomic design task files (1 screen = 1 task).
  Parses Screen Plan blocks, fills design-task.md.template, validates inline, plans sessions.

  Use when: "разбей дизайн на задачи", "декомпозиция дизайн-плана", "decompose design plan",
  "создай дизайн-задачи", "design task decompose", "разбей экраны на задачи",
  "break design into tasks", "split screens into tasks"
---

# Design Task Decompose

Decompose an approved design plan into individual design task files — one task per screen.

**Input:** `work/{feature}/design-plan.md` (status: approved)
**Optional input:** `work/{feature}/design-spec.md` (graceful degradation if missing)
**Output:** `work/{feature}/tasks/*.md` (from design-task.md.template)
**Language:** Task files in English, communication in Russian

## Phase 0: Load Context

1. Ask user for feature name if not provided.

2. Read `work/{feature}/design-plan.md`.
   - If file missing — stop: "design-plan.md не найден. Сначала запусти `/design-plan`."
   - Check frontmatter `status: approved`. If not approved — stop: "design-plan.md не утверждён (status: {actual}). Сначала доведи до approved."

3. Read `work/{feature}/design-spec.md`.
   - If missing — continue without it. Use design-plan.md data only. Log: "design-spec.md не найден — продолжаю только по design-plan.md."

4. Parse Screen Plan blocks — find all `### Screen: [name]` headings.
   Extract from each block:
   - Screen name
   - Layout Pattern
   - Responsive Strategy
   - Visual Hierarchy (ordered list)
   - Component List (bullet list)
   - Notes

5. Count screens found.
   - **0 screens** — stop: "No Screen Plan blocks found in design-plan.md. Expected `### Screen: [name]` headings in Screen Plans section."
   - **Corrupted / malformed / invalid** plan (no Screen Plans section, broken markdown structure, missing required fields in blocks) — stop with error describing the specific issue.
   - **1 screen** — create the single task (Phase 1), skip session planning (Phase 4), suggest `/design-execute` directly after approval.

**Checkpoint:**
- [ ] design-plan.md loaded, status: approved confirmed
- [ ] design-spec.md loaded or gracefully skipped
- [ ] Screen Plan blocks parsed, screen count known
- [ ] Edge cases (0 screens, corrupted, 1 screen) handled

## Phase 1: Create Tasks

1. Read the task template: [design-task.md.template](~/.claude/shared/work-templates/tasks/design-task.md.template)

2. For each Screen Plan block, create one task file `tasks/{N}.md`:
   - Read the template
   - Fill frontmatter:
     - `screen:` screen name from `### Screen:` heading
     - `page_type:` infer from screen name and design-spec context (login, dashboard, landing, catalog, settings, etc.)
     - `layout:` Layout Pattern value from the block
     - `complexity: high` if the screen is a dashboard with 3+ widget sections or similarly complex; otherwise `complexity: normal`
     - `depends_on:` based on user flow order from design-plan or design-spec (empty for first screens)
     - `wave:` group independent screens into same wave for parallel execution
   - Fill sections from Screen Plan block data:
     - **Description** — screen purpose, role in product flow (use design-spec if available)
     - **What to Generate** — page purpose, key interactions, navigation context (where user comes from / goes next)
     - **Visual Hierarchy** — copy from Screen Plan block's Visual Hierarchy list
     - **Components** — convert Component List to `component:variant` format
     - **Content** — realistic content descriptions (use design-spec data if available, otherwise describe placeholders)
     - **Layout Details** — expand Layout Pattern into structure, grid, spacing, alignment
     - **Responsive Notes** — expand Responsive Strategy into breakpoint-specific behavior
     - **Acceptance Criteria** — HTML + SVG generation, tokens applied, hierarchy matches, components present
   - Complex screens (complexity: high) get extra detail in Description and Details sections

3. Git commit: `draft(tasks): create {N} design tasks from design-plan for {feature}`

**Checkpoint:**
- [ ] All `tasks/*.md` files created (1 per screen)
- [ ] Each task has filled frontmatter: screen, page_type, layout, complexity, wave
- [ ] design-generate Phase 1 fields covered: page type, components, layout structure, content

## Phase 2: Validate (inline, max 2 passes)

Run two validation checks inline (no subagents — design plans have 3-10 screens):

**Template compliance:**
- All required sections present in each task file
- Frontmatter fields filled (no empty required fields)
- component:variant format used in Components section
- Visual Hierarchy has primary/secondary/tertiary

**Plan traceability:**
- Every screen in design-plan.md has exactly one task
- No orphan tasks (tasks without matching Screen Plan block)
- Wave assignments consistent with depends_on

Fix issues inline. If problems remain after 2 passes — show user: "Вот что осталось — давай решим вместе."

**Checkpoint:**
- [ ] Template compliance passed for all tasks
- [ ] Plan traceability: screen count == task count, no orphans

## Phase 3: Present to User + Approval

1. Present summary:
   - Screen count and task count
   - Task list with: number, screen name, layout, complexity flag, wave
   - Any complexity: high screens highlighted with reason

2. Wait for user approval.

3. After approval — git commit: `chore(tasks): design task decomposition approved for {feature}`

**Checkpoint:**
- [ ] Summary presented
- [ ] User approved
- [ ] Approval committed

## Phase 4: Session Planning

Triggers only if screen count > 3. For 1-3 screens — skip, suggest `/design-execute` directly.

1. Group screens into sessions by count: ~3-5 screens per session.
   - Keep screens from same wave together when possible.
   - Respect depends_on order — dependent screens in same or later session.

2. Generate `work/{feature}/session-plan.md`:
   - For each session: title, screen list, task numbers
   - Include prompts for all sessions (not just the first)

3. Present session plan to user.

4. Git commit: `chore(tasks): session plan for {feature} — {N} sessions`

5. Suggest `/design-execute` as next step. The file contains all session prompts; show the user only the Session 1 prompt to copy.

**Checkpoint:**
- [ ] session-plan.md created (if >3 screens)
- [ ] User saw session grouping
- [ ] `/design-execute` suggested as next step

## Final Check

- [ ] All phases completed (tasks created, validated, approved)
- [ ] Each task matches design-task.md.template (frontmatter + all sections filled)
- [ ] Plan traceability: every screen has a task, no orphans
- [ ] Complex screens flagged with complexity: high
- [ ] design-spec.md used if available, gracefully skipped if not
- [ ] Session plan generated (if >3 screens)
- [ ] 1-screen shortcut: Phase 4 skipped, `/design-execute` suggested directly
- [ ] `/design-execute` referenced as next step
