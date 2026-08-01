---
name: task-decomposition
description: |
  Decompose approved tech-spec into atomic task files with parallel creation and validation.

  Use when: "разбей на задачи", "декомпозиция", "decompose tech-spec",
  "создай задачи из техспека", "/decompose-tech-spec"
---

# Task Decomposition

> **CRITICAL:** NEVER generate multiple artifacts without stopping. After EACH artifact: list controversial points, explain simply, WAIT for user decision. Only then proceed.

Decompose tech-spec Implementation Tasks into individual task files with parallel creation and validation.

Before starting, read [quick-ref-task-decomposition.md](../quick-learning/references/quick-ref-task-decomposition.md) — top reasoning patterns for this skill (if file exists and non-empty).

**Input:** `work/{feature}/tech-spec.md` (status: approved)
**Output:** `work/{feature}/tasks/*.md` (validated)
**Language:** Task files in English, communication in Russian

## Phase 0: Scope Estimation

Before creating tasks, present the user a structural plan:

1. Read tech-spec Implementation Tasks section.
2. Estimate total lines of code for the feature.
3. **Break down into blocks of ~1200 lines (±300)**, each block into **steps of ~300 lines (±100)**.
4. Present the plan as a table: blocks → steps with line estimates. Add a **Complexity** column:
   - **L1** (trivial) — estimated_loc < 50 AND task description contains none of: auth, login, password, token, session, input validation, upload, file input, database query, SQL, API endpoint, CORS, RBAC, permission, PII, personal data, export fields
   - **Standard** — everything else

   L1 tasks get `reviewers: [code-reviewer]` only (security-auditor and test-reviewer skipped). Audit Wave covers security holistically at feature level regardless.

5. Get user confirmation before proceeding to task creation.

This ensures predictable scope, manageable task sizes, and clear progress tracking. Each "step" typically maps to one task file. Each "block" maps to a wave or a group of related tasks.

**Important:** Save LOC estimates per task — they will be used in Phase 4 (Session Planning). Pass `estimated_loc` to each task-creator in Phase 1.

## Phase 1: Create Tasks

1. Ask user for feature name if not provided.

2. Read `work/{feature}/tech-spec.md`. Check frontmatter `status: approved`.
   If not approved — tell user: "tech-spec не утверждён. Сначала запусти `/new-tech-spec` и доведи до approved." Stop.

3. Read `work/{feature}/user-spec.md`.

4. Note the task template path: `~/.claude/shared/work-templates/tasks/task.md.template`

5. Read skills/reviewers catalog from [skills-and-reviewers.md](~/.claude/skills/tech-spec-planning/references/skills-and-reviewers.md) — for passing correct skills/reviewers to task-creators.

6. For each task in Implementation Tasks — launch [`task-creator`](~/.claude/agents/task-creator.md) subagent in parallel.
   Pass each task-creator:
   - feature_path, task_number, task_name
   - template_path: `~/.claude/shared/work-templates/tasks/task.md.template`
   - files_to_modify, files_to_read (from tech-spec)
   - depends_on, wave, skills, verify (from tech-spec)
   - reviewers: if task was classified **L1** in Phase 0 → pass `[code-reviewer]`; otherwise pass reviewers from tech-spec
   - teammate_name (if specified in tech-spec, optional)
   Each task-creator copies the template to `tasks/{N}.md` first, then edits each section in place. This ensures no sections are skipped.

7. Confirm each task-creator returned a file path. Skip reading task content — preserve context budget for validation phase.
8. Git commit: `draft(tasks): create {N} tasks from tech-spec for {feature}`

**Checkpoint:**
- [ ] All `tasks/*.md` files created
- [ ] Each task-creator returned file path
- [ ] Draft committed

## Phase 2: Validation (loop while it converges)

Tech-spec was already validated by 5 validators. This phase checks only: (1) task-creator correctly expanded tasks by template, (2) no mismatches with real code appeared during detailing.

### Validators

Launch both in parallel:

[`task-validator`](~/.claude/agents/task-validator.md) — Template Compliance + AC/TDD carry-forward:
- Batch: 5 tasks per call
- Pass: feature_path, task_numbers array, batch_number, iteration
- Report: `logs/tasks/template-batch{N}-review.json`

[`reality-checker`](~/.claude/agents/reality-checker.md) — Reality & Adequacy:
- Batch: 3 tasks per call
- Pass: feature_path, task_numbers array, batch_number, iteration
- Report: `logs/tasks/reality-batch{N}-review.json`

### Process

1. Launch both validators in parallel (task-validator in batches of 5, reality-checker in batches of 3).
2. Read JSON reports, collect findings.
3. If issues found — for each task with issues, launch [`task-creator`](~/.claude/agents/task-creator.md) in fix mode:
   - Pass: same inputs as creation + `mode: fix` + `findings` from validators
   - task-creator reads existing task, applies fixes, overwrites file
4. After each validation round, git commit: `chore(tasks): validation round {N} — {summary}`
5. Re-validate fixed tasks (repeat 1-4) while each round leaves strictly fewer open findings than the one before. The first round that does not reduce them, stop and escalate to the user with what remains.
6. If problems remain after 3rd iteration — show user: "Вот что осталось — давай решим вместе."

### Cross-Task Integration Check

After individual validation passes, run a final cross-task check:

1. Launch both validators on ALL tasks in a single batch (not split into smaller batches):
   - `task-validator` — focus: shared resource ownership (one owner, consumers depend_on owner), no competing instances in same wave
   - `reality-checker` — focus: duplicate heavy resource init, hidden dependencies, inconsistent approaches across tasks

2. If issues found → launch `task-creator` in fix mode for affected tasks. Re-validate fixed tasks.

3. Max 2 iterations for cross-task check (on top of the 3 individual iterations).

**Checkpoint:**
- [ ] Both validators: status=approved OR user resolved remaining issues
- [ ] Cross-task integration check: no cross-task conflicts

## Phase 3: Present to User

1. Summary: task count, waves, dependencies, validation results (iterations, issues found/fixed).
2. Wait for user approval.
3. Git commit: `chore(tasks): task decomposition approved for {feature}`

**Checkpoint:**
- [ ] Summary presented to user
- [ ] User approved task decomposition
- [ ] Approval committed

## Phase 4: Session Planning

After user approves task decomposition, calculate session grouping for predictable execution.

1. Read all task files, collect per task: `wave`, `estimated_loc`, Context Files list. Read the tech-spec frontmatter `branch:` — the implementation branch for this feature.
2. Group waves into sessions using LOC budget:
   a. **Session LOC budget = ~1200 lines (±300)** — matches Phase 0 block size.
   b. Walk waves in order. For each wave, sum `estimated_loc` of its tasks.
   c. Accumulate wave LOC into current session. If adding next wave exceeds budget → start new session.
   d. **Never split a wave across sessions.**
   e. **Audit Wave + Final Wave → always the last session** (fixed, no LOC budget — these are review & deploy).
   f. If a single wave > budget → it gets its own session (warn user: "Wave N exceeds session budget").
3. For each session, collect unique Context Files from all tasks in that session (deduplicate).
4. Give each session a short descriptive title based on its tasks' descriptions.
5. Generate `work/{feature}/logs/session-plan.md` from template `~/.claude/shared/work-templates/session-plan.md.template`. Include prompts for ALL sessions in the file (for reference). Fill the **Branch** field (header + every session block) from the tech-spec `branch:`, applying the template's Branch-discipline rule (isolated `feature/{name}` + worktree for a multi-session/multi-component feature or when the default branch is prod; merge back to the default branch only in the final session after green QA). **Every session prompt MUST open with a `Ветка/Branch:` line** stating the working branch + isolation rule — never leave the branch implicit (big repos have many branches).
6. Present session plan to user as a table: session number, title, waves, tasks, estimated LOC.
7. Git commit: `chore(tasks): session plan for {feature} — {N} sessions`
8. Show ONLY the prompt for Session 1. Do NOT show prompts for later sessions — they are in session-plan.md and will be delivered by feature-execution at the end of each session.

**Checkpoint:**
- [ ] session-plan.md created and committed
- [ ] User saw session grouping

## Final Check

- [ ] All phases completed (tasks created, validation passed)
- [ ] All tasks match template (frontmatter: status, depends_on, wave, skills, reviewers, teammate_name)
- [ ] Validation: both validators passed or user confirmed remaining issues

## Promoted Patterns

**Verify all cross-references after task generation (Seen: 2):** Check file paths via `test -e`, decision numbers by counting in tech-spec, depends_on by confirming the dependency actually produces the referenced artifact. Agents generate references by analogy/assumption, not by verification.

**A test that straddles two tasks goes into the spec/AC explicitly (Seen: 2):** if while executing task N you find a test belonging to task M's scope, add it to task M's acceptance criteria or TDD Anchor. A note in decisions.md is not enough — the agent running task M does not read earlier tasks' decisions.

**Wave numbers, not labels (Seen: 3):** semantic labels ("Audit Wave", "Final Wave", any named wave) are not numbers. Pass task-creator explicit integers: with N implementation waves, audit is N+1 and final is N+2. When tasks inside one label depend on each other (A→B→C) each gets its own number (A=N, B=N+1, C=N+2). After generation, validate every depends_on pair: wave(consumer) > wave(producer).

**Constraint enforcement — check only inside the enforcing region (Seen: 3):** for tests over structured string output (markdown, reports) it is not enough that a value is present — extract the relevant section first (regex/split), then check the value inside it. Generally: when checking that a structure ENFORCES a constraint through the presence of a token, identify the region that actually enforces it (the restricting/predicate part) and search only there; the same token in a non-enforcing region (output, ordering, labels, metadata) must not count (non-restricting presence bias). This separates "the value exists" from "the value is in the place that binds". (triad #384)

**Scope of same-file tasks across waves (Seen: 2):** when task A creates a file and task B in a later wave extends it, bound A explicitly ("save/load only — needed in wave 1") and put into B's brief: "the file already exists with functions X and Y; add only Z". Parallel task-creators do not talk to each other, so the scope must be unambiguous in every brief.

## Learned Patterns

Full pattern history: [references/learned-patterns.md](references/learned-patterns.md)
Load only for audit wave and retrospective — not during task decomposition.
