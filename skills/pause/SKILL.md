---
name: pause
description: |
  Stops current work on user request, captures full session state to project docs,
  and generates a resume prompt so the next session can continue without loss.

  Use when: "пауза", "стоп", "остановись", "stop", "pause", "подожди",
  "притормози", "сохрани прогресс", "прервись", "halt"
---

# Pause — Save State and Stop

Capture current session state and prepare a resume prompt. After this skill activates, stop all ongoing work and output only the checkpoint and resume prompt.

## Step 1: Locate Feature Context

Scan `work/` for an active feature directory:
- Check `work/*/logs/checkpoint.yml` — if `last_completed_wave` > 0 or tasks are `in_progress` → this is the active feature
- If multiple candidates → pick the one with the most recent file modification

If no feature found → ad-hoc mode (no `work/` structure). Skip to Step 3.

## Step 2: Read Project Documentation

Read these files from the feature directory (they are the authoritative source of state):

1. `work/{feature}/logs/checkpoint.yml` — current wave, session, next_wave
2. `work/{feature}/tasks/*.md` (frontmatter only) — task statuses: `planned` / `in_progress` / `done` / `done_with_concerns`
3. `work/{feature}/decisions.md` — what was actually completed and committed
4. `work/{feature}/logs/session-plan.md` (if exists) — session boundaries

From these files derive:
- **Completed tasks:** status `done` or `done_with_concerns`, has decisions.md entry
- **In-flight tasks:** status `in_progress`, no decisions.md entry yet (subagent working or interrupted)
- **Remaining tasks:** status `planned`
- **Current wave and session**

Run `git status --short` to get uncommitted files.

**Checkpoint:** Active feature directory identified (or ad-hoc mode confirmed). checkpoint.yml, task statuses, decisions.md read. Git status captured.

## Step 3: Handle Subagents (if feature-execution was active)

In-flight tasks (status `in_progress`, no decisions.md entry) mean subagents may still be running. These agents will commit their work and write decisions.md when done — or they won't if interrupted.

Report to user:
> Задачи {N, M} в статусе `in_progress` без записи в decisions.md — субагенты могли быть прерваны.
> При возобновлении feature-execution прочитает checkpoint.yml и decisions.md и сам определит, что переделать.

This is the reliable approach: `feature-execution` Phase 1 already handles resume from checkpoint by checking decisions.md for each in-progress task.

## Step 4: Determine Save Path

- Feature found → `work/{feature}/logs/pause-checkpoint.md`
- Ad-hoc → `.claude/pause-checkpoint.md`

## Step 5: Write Checkpoint

```markdown
# Pause Checkpoint

**Date:** {YYYY-MM-DD HH:MM}
**Skill running:** {skill-name or "ad-hoc"}
**Feature:** {feature path or "none"}

## State from Project Docs

**Checkpoint:** wave {N} of {total}, session {S} of {total_sessions}
**Tasks done:** {list task numbers with titles}
**Tasks in-flight:** {list task numbers — subagents may be running or interrupted}
**Tasks remaining:** {list task numbers with titles}

## Uncommitted Changes

{output of git status --short, or "none"}

## Active Step (ad-hoc only)

{If no feature context: what was being done, specific file/action}

## Open Questions

{Unresolved decisions or ambiguities for next session. "None" if clean.}

## Resume Prompt

{see Step 6 — paste verbatim}
```

**Checkpoint:** pause-checkpoint.md written with all sections filled. Resume prompt section is present.

## Step 6: Generate Resume Prompt

Write a concrete, copy-paste-ready prompt. Lead with the goal, include specific file paths, skip filler.

**For feature-execution resume:**
```
Продолжаем фичу {feature-name}.

Прогресс: волна {last_completed_wave} из {total} завершена. Задачи {done list} готовы.
Задачи {in_progress list} прерваны — feature-execution проверит decisions.md и определит что переделать.
Следующая волна: {next_wave}, задачи {task list}.

Запусти: /do-feature work/{feature}/
```

**For do-task resume:**
```
Продолжаем задачу {N} — {task title}.

Прогресс: {what's in decisions.md}
Следующий шаг: {exact step from do-task workflow — Phase X / Step Y}
Файлы с изменениями: {list from git status or "нет"}

Запусти: /do-task work/{feature}/tasks/{N}.md
```

**For ad-hoc resume:**
```
Продолжаем работу: {what was being done in one sentence}.
Сделано: {what's done}
Следующий шаг: {specific action — file, function, command}
Открытые вопросы: {pending decisions or "нет"}
```

## Step 7: Report to User

1. Confirm: "Прогресс сохранён → {path}"
2. Print the resume prompt in a code block
3. "Можешь закрыть сессию. При возобновлении вставь промт выше."

## Self-Verification

- [ ] Feature context found (or ad-hoc mode confirmed)
- [ ] checkpoint.yml, task statuses, decisions.md read (or ad-hoc: conversation reviewed)
- [ ] In-flight tasks reported to user with explanation
- [ ] Checkpoint written with all sections (no empty fields — write "none" explicitly)
- [ ] Resume prompt is specific: wave numbers, task numbers, next command
- [ ] User shown save path and resume prompt
