---
name: do-task
description: |
  Execute task from tasks/*.md with quality gates.

  Use when: "выполни задачу", "сделай таску", "do task", "execute task", "запусти задачу"
---

# Do Task

> **CRITICAL:** NEVER generate multiple artifacts without stopping. After EACH artifact: list controversial points, explain simply, WAIT for user decision. Only then proceed.

Execute a spec-driven task with validation and status tracking.

Deliver the task at the scope the task file states. Make routine judgement calls yourself;
check in only where two readings would produce materially different work. Do not widen the
task with adjacent cleanup, extra configurability, or defensive code for cases that cannot
occur. Delegate only the reviewer pass described below — never spawn an agent to re-check
work you just did yourself.

Before starting, read [quick-ref-do-task.md](../quick-learning/references/quick-ref-do-task.md) — top reasoning patterns for this skill (if file exists and non-empty).

## Step 1: Read Task

1. Read task file (user provides path or task number)
   - If user didn't specify → ask: "Which task to execute?"
2. Verify task status is `planned` (if not → ask user before proceeding)
3. Update task frontmatter: `status: planned` → `status: in_progress`
4. Read every file listed in the task's "Context Files" section

## Step 2: Execute

1. Load each skill listed in the task (frontmatter `skills: [...]` and "Required Skills" section)
   - If a skill is not found → warn user, continue with remaining skills
   - If task has no skill (frontmatter `skills: []` or absent) → read the task, execute "What to do" and "Verification Steps" directly. For tasks with user instructions → show the instruction to user, wait for confirmation.
2. Follow loaded skill workflow
3. Git commit implementation (code + tests pass): `feat|fix|refactor: task {N} — {brief description}`
4. Reviewers:
   - The task's "Reviewers" section wins when present.
   - When it is absent, select by what the diff contains, per the table in
     [skills-and-reviewers.md](../tech-spec-planning/references/skills-and-reviewers.md).
     A trivial edit — a typo, a renamed local, a version bump — gets no reviewer at all.
   - For each selected reviewer: spawn subagent via Task tool (subagent_type = reviewer name),
     pass the git diff, the task file, the tech-spec and the user-spec. The reviewer loads its
     own skill via its agent frontmatter.
   - Read the report. Findings → fix, re-run tests, commit `fix: address review round {N} for task {N}`, re-run the reviewers that raised them.
   - **Stop on progress, not on a counter:** continue while each round leaves strictly fewer open findings than the one before. The first round that ends with the same or more open findings, stop and report — a loop that stopped converging will not converge next pass.

## Step 3: Verify

1. Check each acceptance criterion from task file
2. If task has "Verification Steps → Smoke" → execute each smoke command, record results in decisions.md Verification section
3. If task has "Verification Steps → User" → ask user to verify, wait for confirmation
4. If any verification fails → fix → re-run tests → re-run reviewers (new round) → re-verify.
   Same stop condition as Step 2. When it trips, stop, report the failures to the user and keep status `in_progress`.
   - Tool unavailable → document, suggest manual check

## Step 4: Complete

1. Read template `~/.claude/shared/work-templates/decisions.md.template` and write a concise execution report to `work/{feature}/decisions.md`. Follow template format strictly — no extra sections. Use Planned/Actual/Deviation structure. Match the length to the substance: no filler sections, no restated summaries.
2. Update task frontmatter: `status: in_progress` → `status: done` (or `done_with_concerns` + fill `concerns:` field if something worries you — performance risk, edge case not covered, code smell that passed review, tech debt introduced). Use `done_with_concerns` when the task works but you have reservations.
3. Update tech-spec: `- [ ] Task N` → `- [x] Task N`
4. Git commit: `chore: complete task {N} — update status and decisions`
5. **Session boundary check** (skip if `work/{feature}/logs/session-plan.md` does not exist):
   Read session-plan.md. Find which session this task belongs to.
   - If this task is the **last task of current session** (all session's tasks are now `done`):
     **Quick Learning (subagent, background).** Spawn a subagent to run [quick-learning](../quick-learning/SKILL.md). Pass it: feature path, current session number, path to decisions.md. The subagent runs in the **background** while you proceed. When it finishes, show the user its one-line summary. Do NOT read the quick-learning SKILL.md yourself — the subagent loads it independently.
     Generate next-session prompt from `~/.claude/shared/work-templates/session-prompt.md.template`.
     Save to `work/{feature}/logs/next-session-prompt.md`.
     Present to user:
     ```
     Сессия {N} из {total} завершена.

     Рекомендую начать новую сессию Claude Code и вставить этот промт:

     ---
     {generated prompt content}
     ---
     ```
   - If tasks remain in current session: inform user which tasks are left in this session.
   - If `session-plan.md` does not exist and all tasks in `work/{feature}/tasks/` are `done` → prompt user: "Все задачи выполнены. Запусти `/done` для архивации, затем `/quick-learning` для фиксации уроков."

## Checks against state

```bash
# 1. task frontmatter reached a terminal status
rg -n "^status:" work/{feature}/tasks/task-{N}*.md

# 2. tech-spec checkbox for this task is ticked
rg -n "\[x\] Task {N}\b" work/{feature}/tech-spec.md

# 3. decisions.md carries an entry for this task
rg -n "Task {N}\b" work/{feature}/decisions.md

# 4. a commit references this task
git log --oneline -10 --grep "task {N}"
```

Any line returning nothing means that step did not happen — go do it, rather than recording the task as complete.
