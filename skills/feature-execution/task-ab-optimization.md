---
type: methodology-improvement
status: ready
created: 2026-04-21
feature: feature-execution skill
---

# Task: A+B Agent Prompt Optimization

## Problem

Субагенты в feature-execution тратят 150–200k токенов на задачу из-за двух паттернов:

**A. Агент сам читает весь контекст через tool calls** — каждый агент получает "read task file, read tech-spec, read user-spec, read 5 context files, read project-knowledge", делает 15–20 Read вызовов перед тем как написать первую строку кода.

**B. Загрузка code-writing SKILL.md** — 164-строчный документ с полным TDD-процессом, review-протоколом, design tokens и т.д. Большая часть нерелевантна для конкретной задачи.

Эффект: task 19 — 200k токенов, 67 tool uses, 735 сек.

## Solution (already implemented)

`~/.claude/skills/feature-execution/references/prompt-templates.md` обновлён:

**A — Оркестратор pre-читает и инлайнит контекст:**
- Читает task файл, source-файлы которые нужно изменить, decisions.md (только depends_on)
- Вставляет нужный контекст текстом прямо в промт агента
- Агент не делает Read calls для изучения контекста — только для работы с кодом

**B — Inline coding rules вместо skill loading:**
- Убрано "Load skill: code-writing/SKILL.md"
- В промт агента вставлены только релевантные правила (8 строк вместо 164)

## What to do in this session

1. **Verify** — прочитать обновлённый `prompt-templates.md` и убедиться что он корректен
2. **Apply** — запустить task 20 (mvp-booking-flow, D:/МОИ ПРОЕКТЫ/КульмИИнатор) используя НОВЫЙ подход:
   - Оркестратор сам читает task 20, conftest.py из task 19, key source files
   - Инлайнит в промт агента
   - НЕ пишет "Load skill" и "Read task file"
3. **Measure** — сравнить token usage с предыдущими задачами (baseline: ~150k)
4. **Commit** — закоммитить обновлённый prompt-templates.md в ~/.claude/skills

## Task 20 context (to inline)

Task 20: `D:/МОИ ПРОЕКТЫ/КульмИИнатор/work/mvp-booking-flow/tasks/20.md`
- Integration tests: /cancel mid-flow, /start mid-flow restart prompt, session_timeout (15 min), fsm_restore across restart
- Extends `tests/integration/conftest.py` from task 19 (add only what's missing)
- Uses file-based SQLite (tmp_path), not :memory:
- freezegun already in dev-dependencies

Key source files to inline for task 20:
- `tests/integration/conftest.py` (existing fixtures from task 19)
- `src/kulminiator/storage/fsm_storage.py` (SqlAlchemyFsmStorage — the persistence layer under test)
- `src/kulminiator/bot/routers/cancel.py` (the cancel router being tested)

## Acceptance Criteria

- [ ] task 20 выполнена, все тесты зелёные
- [ ] Агент для task 20 не делал Read calls на task file / skill / tech-spec / project-knowledge
- [ ] Token usage task 20 < 120k (цель: -35% от baseline)
- [ ] prompt-templates.md закоммичен в ~/.claude/skills
