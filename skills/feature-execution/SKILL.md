---
name: feature-execution
description: |
  Orchestrate feature delivery as team lead: spawn agents by wave,
  manage review cycles, commit per wave.

  Use when: "выполни фичу", "do feature", "execute feature", "запусти фичу",
  "выполни все задачи", "execute all tasks"
---

# Feature Execution

> After each generated artifact, stop: list the controversial points, explain them simply, wait for the user's decision. Generating a second artifact before that decision arrives is a defect.

Team lead orchestrates feature delivery. You are a dispatcher: spawn agents, track progress, commit code, escalate issues. Delegate all code reading, diff analysis, and report review to spawned agents. Your only inputs are status messages from teammates ("Task complete") and escalation requests.

Delegation is this skill's job, but it is not free. A wave's tasks are independent by
construction — that is what makes spawning them worth it. Do not spawn an agent for work you
could finish in a handful of tool calls, do not split one task across several agents, and
never spawn an agent to check another agent's output; that is what the reviewer pass is for.
One agent per task, one reviewer per selected dimension.

Your context is compacted automatically as it fills, so you can keep working across the whole
feature. Do not wrap up a wave early over token budget: write the checkpoint, let the context
refresh, continue from it.

Before starting, read [quick-ref-feature-execution.md](../quick-learning/references/quick-ref-feature-execution.md) — top reasoning patterns for this skill (if file exists and non-empty).

## Phase 1: Initialization

0. Check `work/{feature}/logs/checkpoint.yml`:
   - **`status: awaiting_user` → STOP barrier (session boundary reached, waiting for user).**
     This state means the previous session ended cleanly and the next session must be user-initiated.
     Do not auto-continue into the next wave — that is exactly the bug this barrier prevents
     (a truncated session-boundary message must never roll forward into Phase 2).
     - If the user's current input **explicitly** names the next session or its waves/tasks
       (e.g. "Session 2", "waves 3–6", pasted next-session prompt) → treat as explicit start:
       clear `status` (set to `running`), then proceed with the resume logic below from `next_wave`.
     - Otherwise (empty re-entry, auto-resume after compaction/output truncation) → do not proceed.
       Output: "Предыдущая сессия завершена на границе. Промт следующей сессии:
       `work/{feature}/logs/next-session-prompt.md`. Подтвердите запуск следующей сессии." and END.
   - `last_completed_wave > 0` → this is a resume after context compaction.
     Read checkpoint, then read `work/{feature}/decisions.md` to confirm what was actually completed.
     For tasks in the resumed wave: if a task has a decisions.md entry, it completed — update its
     frontmatter to `done` and skip it. Only re-execute tasks without a decisions.md entry.
     No roster to restore — agents live only for their wave, and a resume re-spawns them from the
     task files of `next_wave`. State lives on disk: checkpoint.yml, task frontmatter, decisions.md,
     wave commits. Skip to Phase 2 starting from `next_wave`.
     Read session-plan.md to determine which session the next_wave belongs to. Update current_session accordingly.
     Report to user: "Resuming from wave {N} (session {S}). Waves 1-{N-1} completed."
   - `last_completed_wave: 0` → fresh start, proceed below.

1. Read `work/{feature}/tech-spec.md` and `work/{feature}/user-spec.md`
1.5. Read `work/{feature}/logs/session-plan.md` if it exists. Parse session boundaries: which waves belong to which session. If file does not exist — treat all waves as one session (backward compatibility).
1.6. **Track isolation (parallel projects only).** If the project runs features in parallel
   (the `parallel-tracks` skill applies / `scripts/train.py` exists), the feature must be
   worked on its own branch+worktree, never on `dev` directly. If not already isolated
   (current branch is `dev`/`main`), load the `parallel-tracks` skill and run its Part A
   (`python scripts/train.py start <slice> --touches <zones>`), then continue from inside
   the worktree. Relay any `COLLISION:` line to the user in plain language. Projects that
   do not use parallel-tracks skip this step (unchanged behavior).
2. Read frontmatter of all task files in `work/{feature}/tasks/` — extract fields:

   | Field | Purpose |
   |-------|---------|
   | `status` | planned → in_progress → done |
   | `wave` | Parallel execution group number |
   | `depends_on` | Task numbers that must be done first |
   | `skills` | Skills the teammate loads |
   | `reviewers` | Reviewer agents to spawn (source of truth) |
   | `teammate_name` | Name given to the spawned agent in its prompt (optional) |
   | `verify` | Verification types: [smoke], [user], [smoke, user], or [] (optional) |

   Build waves: group tasks by `wave` field. Within a wave, all tasks run in parallel.

3. Build execution plan following template at `~/.claude/shared/work-templates/execution-plan.md.template`
4. Save to `work/{feature}/logs/execution-plan.md`
5. Show plan to user, wait for approval
6. Update `work/{feature}/logs/checkpoint.yml`: set `total_waves` from the execution plan.
7. If session-plan.md was found (step 1.5): write `current_session` and `total_sessions` to checkpoint.yml.

No team object is created: agents are spawned per wave in Phase 2 with the Agent tool
(`general-purpose` for teammates, the named reviewer agent for reviewers) and end with their wave.

**Checkpoint:** execution plan approved, checkpoint initialized.

## Phase 2: Execute Wave

1. Find tasks for current wave: `status: planned`, all `depends_on` tasks are `done`
2. Update frontmatter: `status: planned` → `status: in_progress`

3. For each task, spawn **teammate + reviewers** using prompt templates from [prompt-templates.md](references/prompt-templates.md).
   Read that file once at Phase 2 start, then use templates for all tasks in the wave.
   Reviewers come from the task's `reviewers` field; when it is empty, select by what the task
   will change, per [skills-and-reviewers.md](../tech-spec-planning/references/skills-and-reviewers.md).

4. All agents work in parallel. Lead waits for teammates to report "Task complete."

### Audit Wave tasks

Audit Wave tasks (Code Audit, Security Audit, Test Audit) have `reviewers: none` — each auditor teammate IS the review. Spawn them as standard teammates (`general-purpose`), each loads its methodology skill.

Each auditor:
- Reads decisions.md to understand what was done in each task
- Reads all source files listed in tech-spec "Files to modify" across all implementation tasks
- Reviews the final state of code holistically (full files, not diffs)
- Writes report to `{feature_dir}/logs/working/audit/{auditor-name}.json`
- Writes decisions.md entry, reports to lead

After all 3 reports:
- All clean → proceed to Final Wave
- Issues found → spawn a fixer teammate (ad-hoc, code-writing skill), assign the auditors who found issues as reviewers, standard review protocol. After approval → proceed to Final Wave. If the loop stops converging → escalate (see Escalation).

### Ad-hoc agents

When lead spawns an agent outside the original execution plan (to fix audit findings, handle escalations, complete missing work):

1. Lead assigns a skill and reviewers matching the type of work:
   - Code changes → skill: `code-writing`, reviewers per the diff (see skills-and-reviewers.md)
   - Prompt changes → skill: `prompt-master`, reviewers: prompt-reviewer
   - Skill or agent changes → no skill; follow the skill-authoring conventions, reviewers: skill-checker
   - Deploy/CI changes → skill: `deploy-pipeline`, reviewers: deploy-reviewer
   - Infrastructure changes → skill: `infrastructure-setup`, reviewers: infrastructure-reviewer, security-auditor
   - Other tasks (research, config, manual steps) → no skill, no reviewers. Agent follows lead's instructions directly.
2. The ad-hoc agent writes a decisions.md entry (same template as planned tasks)
3. Standard review protocol: agent commits → sends diff to reviewers → fix → repeat while each round leaves strictly fewer open findings
4. Lead verifies decisions.md entry exists before considering ad-hoc work complete

**Checkpoint:** all teammates reported "Task complete", decisions.md entries written.

## Phase 3: Wave Transition

0. **Build check (mandatory).** Run full production build (`npm run build` or equivalent) after each wave completes. Unit tests don't catch server/client boundary violations, callback type mismatches, or runtime-only import errors — only build does. If build fails, fix before proceeding.
1. Verify decisions.md entries exist and match template (`~/.claude/shared/work-templates/decisions.md.template`)
2. If task had Smoke/User verification steps — confirm decisions.md Verification section includes results. Missing results without explanation → ask user whether to proceed.
3. Update task frontmatter: `status: in_progress` → `status: done` (or `done_with_concerns` if teammate reported concerns — preserve the `concerns:` field from decisions.md entry into task frontmatter)
4. Git commit: `chore: complete wave {N} — update task statuses and decisions`. Code is already committed by teammates.
5. Update `work/{feature}/logs/checkpoint.yml`: set `last_completed_wave`, update task statuses, set `next_wave`.
   At session boundary: also set `status: awaiting_user` (the stop barrier read by Phase 1 step 0) so a
   truncated boundary message can never auto-roll into the next wave. For a non-boundary wave keep
   `status: running`. Explicitly commit checkpoint.yml even if no code changed in the last wave — next
   session must start with accurate state including the barrier flag.
5b. **Project tracker sync (if the project has one).** If the project's CLAUDE.md / project-knowledge
   defines a dev-board or external tracker (a CRM/kanban card per feature/slice), sync it NOW to reflect
   this wave's reality. The trigger is a **lifecycle-state change**, not a specific command: a deploy wave →
   move the card to the live-test/verification stage; acceptance blocked or scope pivot → update the card
   description. Do this proactively at the transition — the named command points (do-feature start, `/done`)
   are a minimum, not the full set. Relying on memory instead of this explicit step is the known failure
   mode that leaves the board stale and forces the owner to remind you.
6. **Session boundary check** (skip if session-plan.md does not exist):
   Read session-plan.md. If current wave is the **last wave of current_session**:
   a00. **Update project-knowledge** (before generating the next-session prompt): check if roles, architecture, or business rules changed during this session — update the relevant `.claude/skills/project-knowledge/` docs so the next session does not re-ask what was already discussed.
   a0. **Quick Learning (subagent, background).** Spawn a subagent to run [quick-learning](../quick-learning/SKILL.md). Pass it: feature path, current session number, path to decisions.md. The subagent runs in the **background** while you proceed with the session report. When it finishes, show the user its one-line summary. Do not read the quick-learning SKILL.md yourself — the subagent loads it independently in its own context.
   a. Set `status: awaiting_user` in checkpoint.yml first (before anything below), then increment
      `current_session`. Make the increment **idempotent**: only increment if `current_session` still
      equals the session that just finished — a re-entry that finds the barrier already set must not
      increment again. Order matters: the barrier is written before the prompt is generated, so even if
      generation or the final message is truncated, the stop state is already durable on disk.
   b. Generate next-session prompt from template `~/.claude/shared/work-templates/session-prompt.md.template`:
      - Fill: feature name, description (first line of tech-spec Description), completed sessions/waves, next session's waves and tasks, context files from session-plan.md.
      - Apply prompt-master principles to the generated prompt before saving: make it concrete (specific files, wave numbers, task names), remove filler phrases, lead with the goal, not the context.
   b2. **Executor-calibration pass (mandatory, before saving).** Re-read the generated prompt as the executor who will run the next session *from* it — not as its author. Answer three questions explicitly:
      - **What already works** — keep it.
      - **What is missing for effective work** — gaps that would force the next session to re-ask, re-derive, or guess: unresolved technical forks, infra/dependency risks (a named tool that isn't installed yet, RAM/latency budget on shared infra), test strategy when local infra is partial (no DB/vector store/external service locally), a concrete definition-of-done acceptance anchor, reusable primitives/files to point at instead of reinventing.
      - **What is excess / confusing / contradictory / over-constraining** — deploy mechanics front-loaded at spec-start (belongs to the deploy wave), parameters locked that the spec itself should decide, irrelevant remarks, duplication.
      Then **revise the draft** to close the gaps and cut the noise. **Resolve any technical fork surfaced here autonomously** (simplicity / efficiency / growth) — do not defer it into the prompt as an open question for the user; only genuinely process/irreversible/scope items get escalated. Keep the decision-patterns block intact. The saved prompt is the post-calibration version, not the first draft.
   c. Save prompt to `work/{feature}/logs/next-session-prompt.md` (overwrite each time).
   d. Present to user — **do not paste the full prompt inline** (a long inline prompt is what gets
      truncated mid-text). Keep the final message SHORT and point to the saved file:
      ```
      Сессия {N} из {total} завершена. Барьер выставлен — следующая волна автоматически не стартует.

      Промт следующей сессии сохранён целиком: `work/{feature}/logs/next-session-prompt.md`
      Открой файл, скопируй промт и вставь в новую сессию Claude Code.
      ```
      (If the user explicitly asks to see the prompt in chat, only then print it — but the file is the
      source of truth, never a half-typed chat block.)
   e. **Stop execution.** Do not proceed to next wave. End the session here. The barrier (`status:
      awaiting_user`, step a) is the durable guarantee — this text instruction alone is not relied upon.

   If current wave is not a session boundary → proceed to Phase 2 for next wave.
7. Next wave → Phase 2

**Checkpoint:** all wave tasks done, committed, checkpoint updated.

## Phase 4: User Review

All waves done including Final Wave (QA, deploy if applicable, post-deploy verification if applicable).

1. Show results: what was built, key decisions, QA report summary. Lead with the outcome — the first sentence answers what happened — and put supporting detail after it.
2. Describe what to check manually (from execution plan "user checks" section)
3. Issues found → fix → review → commit, while each round leaves strictly fewer open issues. Stops converging → escalate (see Escalation).
4. All ok → finalize, delete `work/{feature}/logs/checkpoint.yml` (agents already ended with their waves)
5. **Integration (parallel projects only).** If the project uses `parallel-tracks` and the
   feature was worked on a `feature/<slice>` branch, it is not yet in `dev`. Load the
   `parallel-tracks` skill and run its Part B (integration train) + Part C (per-service
   deploy) — one word from the user, "собери", triggers this. Only after the track is
   merged+deployed proceed to `/done`. Non-parallel projects skip this (feature is already
   on the mainline).
6. Prompt user: "Фича завершена. Запусти `/done` для архивации и обновления документации."

## Escalation

Call user when:
- A fix/review loop stops reducing open findings
- Teammate reports blocker or ambiguous requirement
- Task depends on unavailable MCP tool or external service

When escalating:
1. Stop all work on the blocked task/wave
2. Report to user: what failed, what was tried in each round, what remains unresolved
3. Write decisions.md entry: summary of attempts + unresolved findings
4. Git commit: `chore: escalate task {N} — loop stopped converging`
5. Wait for user decision before continuing

## Checks against state

```bash
# 1. execution plan was written and approved before waves started
rg -c . work/{feature}/logs/execution-plan.md

# 2. every task in the completed wave has a decisions.md entry
rg -c "^## Task " work/{feature}/decisions.md

# 3. the wave was committed, checkpoint included
git log --oneline -5 --grep "wave {N}"

# 4. the barrier is durable on disk at a session boundary
rg -n "^status:|^current_session:|^next_wave:" work/{feature}/logs/checkpoint.yml

# 5. the capture instrument a procedure names really produces a durable artifact —
#    run the capture once on a throwaway input BEFORE the expensive run
ls -l {capture_path} && rg -c . {capture_path}
```

Check 1 must return a non-zero count before the first agent of wave 1 is spawned; a missing file or
0 means waves started without an approved plan. Check 2 must equal the number of tasks in the wave.
Check 3 must list a commit naming the wave just finished; empty means the wave was never committed
and the next session resumes from a checkpoint that does not match the tree. Check 4 at a session
boundary must read
`status: awaiting_user` — if it does not, the barrier never landed and the next entry will roll
straight into the following wave. Check 5 must list the file and return a non-zero line count
**after the producing process has exited**; an empty or missing path means the named instrument
never captured anything, so switch the procedure to a source written to durable state (a file, a
commit, a table row) instead of a value that lives only inside the run that produced it. Authorship
of the procedure by the requester is not evidence that the instrument was ever exercised. (triad #484)

## Learned Patterns

**Lazy load:** Full orchestrator patterns, including the promoted ones, in [orchestrator-patterns.md](references/orchestrator-patterns.md). Read at Phase 2 start when executing waves. Audit agents use [learned-patterns.md](references/learned-patterns.md) separately.
