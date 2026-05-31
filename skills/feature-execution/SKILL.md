---
name: feature-execution
description: |
  Orchestrate feature delivery as team lead: spawn agents by wave,
  manage review cycles (max 3 rounds), commit per wave.

  Use when: "выполни фичу", "do feature", "execute feature", "запусти фичу",
  "выполни все задачи", "execute all tasks"
---

# Feature Execution

> **CRITICAL:** NEVER generate multiple artifacts without stopping. After EACH artifact: list controversial points, explain simply, WAIT for user decision. Only then proceed.

Team lead orchestrates feature delivery. You are a dispatcher: spawn agents, track progress, commit code, escalate issues. Delegate all code reading, diff analysis, and report review to spawned agents. Your only inputs are status messages from teammates ("Task complete") and escalation requests.

Before starting, read [quick-ref-feature-execution.md](../quick-learning/references/quick-ref-feature-execution.md) — top reasoning patterns for this skill (if file exists and non-empty).

## Phase 1: Initialization

0. Check `work/{feature}/logs/checkpoint.yml`:
   - `last_completed_wave > 0` → this is a resume after context compaction.
     Read checkpoint, then read `work/{feature}/decisions.md` to confirm what was actually completed.
     For tasks in the resumed wave: if a task has a decisions.md entry, it completed — update its
     frontmatter to `done` and skip it. Only re-execute tasks without a decisions.md entry.
     Check if `~/.claude/teams/{team_name}/config.json` exists: if yes, team is alive; if no,
     recreate via TeamCreate. Skip to Phase 2 starting from `next_wave`.
     Read session-plan.md to determine which session the next_wave belongs to. Update current_session accordingly.
     Report to user: "Resuming from wave {N} (session {S}). Waves 1-{N-1} completed."
   - `last_completed_wave: 0` → fresh start, proceed below.

1. Read `work/{feature}/tech-spec.md` and `work/{feature}/user-spec.md`
1.5. Read `work/{feature}/logs/session-plan.md` if it exists. Parse session boundaries: which waves belong to which session. If file does not exist — treat all waves as one session (backward compatibility).
2. Read frontmatter of all task files in `work/{feature}/tasks/` — extract fields:

   | Field | Purpose |
   |-------|---------|
   | `status` | planned → in_progress → done |
   | `wave` | Parallel execution group number |
   | `depends_on` | Task numbers that must be done first |
   | `skills` | Skills the teammate loads |
   | `reviewers` | Reviewer agents to spawn (source of truth) |
   | `teammate_name` | Agent name for team spawning (optional) |
   | `verify` | Verification types: [smoke], [user], [smoke, user], or [] (optional) |

   Build waves: group tasks by `wave` field. Within a wave, all tasks run in parallel.

3. Build execution plan following template at `~/.claude/shared/work-templates/execution-plan.md.template`
4. Save to `work/{feature}/logs/execution-plan.md`
5. Show plan to user, wait for approval
6. Create team via TeamCreate
7. Update `work/{feature}/logs/checkpoint.yml`: set `total_waves` from the execution plan.
8. If session-plan.md was found (step 1.5): write `current_session` and `total_sessions` to checkpoint.yml.

**Checkpoint:** execution plan approved, team created, checkpoint initialized.

## Phase 2: Execute Wave

1. Find tasks for current wave: `status: planned`, all `depends_on` tasks are `done`
2. Update frontmatter: `status: planned` → `status: in_progress`

3. For each task, spawn **teammate + reviewers** using prompt templates from [prompt-templates.md](references/prompt-templates.md).
   Read that file once at Phase 2 start, then use templates for all tasks in the wave.

4. All agents work in parallel. Lead waits for teammates to report "Task complete."

### Audit Wave tasks

Audit Wave tasks (Code Audit, Security Audit, Test Audit) have `reviewers: none` — each auditor teammate IS the review. Spawn them as standard teammates (general-purpose, opus), each loads its methodology skill.

Each auditor:
- Reads decisions.md to understand what was done in each task
- Reads all source files listed in tech-spec "Files to modify" across all implementation tasks
- Reviews the final state of code holistically (full files, not diffs)
- Writes report to `{feature_dir}/logs/working/audit/{auditor-name}.json`
- Writes decisions.md entry, reports to lead

After all 3 reports:
- All clean → proceed to Final Wave
- Issues found → spawn a fixer teammate (ad-hoc, code-writing skill), assign the auditors who found issues as reviewers, standard review protocol (max 3 rounds). After approval → proceed to Final Wave. If unresolved after 3 rounds → escalate (see Escalation).

### Ad-hoc agents

When lead spawns an agent outside the original execution plan (to fix audit findings, handle escalations, complete missing work):

1. Lead assigns a skill and reviewers matching the type of work:
   - Code changes → skill: `code-writing`, reviewers: code-reviewer, security-auditor, test-reviewer
   - Prompt changes → skill: `prompt-master`, reviewers: prompt-reviewer
   - Skill changes → skill: `skill-master`, reviewers: skill-checker
   - Deploy/CI changes → skill: `deploy-pipeline`, reviewers: deploy-reviewer
   - Infrastructure changes → skill: `infrastructure-setup`, reviewers: infrastructure-reviewer, security-auditor
   - Other tasks (research, config, manual steps) → no skill, no reviewers. Agent follows lead's instructions directly.
2. The ad-hoc agent writes a decisions.md entry (same template as planned tasks)
3. Standard review protocol: agent commits → sends diff to reviewers → fix → max 3 rounds
4. Lead verifies decisions.md entry exists before considering ad-hoc work complete

**Checkpoint:** all teammates reported "Task complete", decisions.md entries written.

## Phase 3: Wave Transition

0. **Build check (mandatory).** Run full production build (`npm run build` or equivalent) after each wave completes. Unit tests don't catch server/client boundary violations, callback type mismatches, or runtime-only import errors — only build does. If build fails, fix before proceeding.
1. Verify decisions.md entries exist and match template (`~/.claude/shared/work-templates/decisions.md.template`)
2. If task had Smoke/User verification steps — confirm decisions.md Verification section includes results. Missing results without explanation → ask user whether to proceed.
3. Update task frontmatter: `status: in_progress` → `status: done` (or `done_with_concerns` if teammate reported concerns — preserve the `concerns:` field from decisions.md entry into task frontmatter)
4. Git commit: `chore: complete wave {N} — update task statuses and decisions`. Code is already committed by teammates.
5. Update `work/{feature}/logs/checkpoint.yml`: set `last_completed_wave`, update task statuses, set `next_wave`.
   At session boundary: explicitly commit checkpoint.yml even if no code changed in the last wave — next session must start with accurate state.
6. **Session boundary check** (skip if session-plan.md does not exist):
   Read session-plan.md. If current wave is the **last wave of current_session**:
   a00. **Update project-knowledge** (before generating the next-session prompt): check if roles, architecture, or business rules changed during this session — update the relevant `.claude/skills/project-knowledge/` docs so the next session does not re-ask what was already discussed.
   a0. **Quick Learning (subagent, background).** Spawn a subagent to run [quick-learning](../quick-learning/SKILL.md). Pass it: feature path, current session number, path to decisions.md. The subagent runs in the **background** while you proceed with the session report. When it finishes, show the user its one-line summary. Do NOT read the quick-learning SKILL.md yourself — the subagent loads it independently in its own context.
   a. Increment `current_session` in checkpoint.yml.
   b. Generate next-session prompt from template `~/.claude/shared/work-templates/session-prompt.md.template`:
      - Fill: feature name, description (first line of tech-spec Description), completed sessions/waves, next session's waves and tasks, context files from session-plan.md.
      - Apply prompt-master principles to the generated prompt before saving: make it concrete (specific files, wave numbers, task names), remove filler phrases, lead with the goal, not the context.
   c. Save prompt to `work/{feature}/logs/next-session-prompt.md` (overwrite each time).
   d. Present to user:
      ```
      Сессия {N} из {total} завершена.

      Рекомендую начать новую сессию Claude Code и вставить этот промт:

      ---
      {generated prompt content}
      ---
      ```
   e. **STOP execution.** Do not proceed to next wave. End the session here.

   If current wave is NOT a session boundary → proceed to Phase 2 for next wave.
7. Next wave → Phase 2

**Checkpoint:** all wave tasks done, committed, checkpoint updated.

## Phase 4: User Review

All waves done including Final Wave (QA, deploy if applicable, post-deploy verification if applicable).

1. Show results: what was built, key decisions, QA report summary
2. Describe what to check manually (from execution plan "user checks" section)
3. Issues found → fix → review → commit (max 3 rounds). If unresolved → escalate (see Escalation).
4. All ok → finalize, shutdown team, delete `work/{feature}/logs/checkpoint.yml`
5. Prompt user: "Фича завершена. Запусти `/done` для архивации и обновления документации."

## Escalation

Call user when:
- 3 review/fix iterations exhausted with remaining findings
- Teammate reports blocker or ambiguous requirement
- Task depends on unavailable MCP tool or external service

When escalating:
1. Stop all work on the blocked task/wave
2. Report to user: what failed, what was tried (all 3 attempts), what remains unresolved
3. Write decisions.md entry: summary of attempts + unresolved findings
4. Git commit: `chore: escalate task {N} — unresolved after 3 fix rounds`
5. Wait for user decision before continuing

## Promoted Patterns

- **Спорные решения ДО генерации:** Артефакт > 200 строк → сначала список решений с вариантами → утверждение → генерация. Один раунд вместо серии переделок.
- **Субагент не завершил → выполни напрямую:** Не ретраить субагент при внешней блокировке (права, permission). Lead делает сам через Write/Edit.
- **Верифицируй результат в реальной среде** (Seen: 4): После деплоя — curl/лог/проверка. Не объявлять "готово" без подтверждения работы. Для cron — лог через 5 мин. При READY/200 OK — дополнительно grep уникальный маркер или component name из нового коммита, чтобы убедиться что платформа промоутила именно новую сборку.

## Self-Verification

- [ ] Execution plan created and approved
- [ ] All tasks executed, reviewed where applicable (max 3 iterations each), decisions.md filled
- [ ] All waves committed (including Final Wave)
- [ ] User reviewed and approved

## Learned Patterns

**Lazy load:** Full orchestrator patterns in [orchestrator-patterns.md](references/orchestrator-patterns.md).
Read at Phase 2 start when executing waves. Audit agents use [learned-patterns.md](references/learned-patterns.md) separately.
