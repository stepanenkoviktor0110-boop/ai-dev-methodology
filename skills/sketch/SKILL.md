---
disable-model-invocation: true
name: sketch
description: |
  Lightweight prototyping mode: collect requirements in 3–5 questions,
  write code directly without validators, then decide whether to develop
  further or archive.

  Use when: "сделай скетч", "набросай прототип", "/sketch",
  "хочу быстро попробовать", "sketch mode"
---

# Sketch Mode

> Sketch Mode закрывает gap: между "полным pipeline" и "ничего".
> За одну сессию — рабочий прототип. Без validators, без code-reviewer.
> После: развивать через `/new-user-spec` или архивировать через `/done`.

## Phase 1: Entry

When the user invokes `/sketch`:

1. Ask: "Как назовём скетч? (будет именем директории `work/{sketch-name}/`)"
   - Accept kebab-case or derive from the user's answer automatically.
2. Create working directory: `work/{sketch-name}/`
3. Check if any other non-completed feature exists in `work/`:
   - If yes → warn: "В `work/` уже есть активная фича. Sketch Mode изолирован
     в своей директории — конфликтов быть не должно. Продолжить?"
   - Wait for user confirmation before proceeding.
   - If no → proceed silently.
4. Proceed to Phase 2.

## Phase 2: Interview

Read [skills/agents/sketch-interviewer.md](../agents/sketch-interviewer.md) and
follow the interview protocol defined there.

- If the user interrupts at any point (says "стоп", "отмена", "не надо" or
  equivalent) → stop immediately. Do NOT create sketch.md.
  Report: "Интервью прервано. sketch.md не создан."
- If all answers collected → proceed to Phase 3.

## Phase 3: Create sketch.md

Using the answers from Phase 2, fill `shared/work-templates/sketch.md`:
- Replace `{name}` with the sketch name from Phase 1.
- Fill each section with the corresponding interview answer.

Save the result as `work/{sketch-name}/sketch.md`.

Show the filled document to the user.

Proceed to Phase 4.

## Phase 4: Confirmation

Wait for user approval of sketch.md.

- **Approved** → proceed to Phase 5.
- **Rejected / change requested** → apply targeted edits to the affected
  section(s), show updated sketch.md again. No iteration limit.
  Repeat until approved.

Start coding only after the user explicitly approves sketch.md.

## Phase 5: Code

**Design Context (UI sketches only).** If the sketch involves UI (component/page/visual prototype), run before writing markup. Skip for non-UI sketches (CLI tools, scripts, backend logic). Keep output in working context only — no file, no user report.

- **CIP brief.** Run PowerShell: `& "C:\Users\natel\AppData\Local\Python\bin\python.exe" "C:\Users\natel\.claude\plugins\cache\ui-ux-pro-max-skill\ui-ux-pro-max\2.5.0\.claude\skills\design\scripts\cip\search.py" "<industry/context>" --cip-brief -b "<sketch-name>"`. Output (palette/typography/style/anti-patterns) informs implementation.
- **Execution principles.** Invoke `Skill(frontend-design:frontend-design)` before writing markup — sketches are new-from-scratch by definition, so this is unconditional for UI sketches.

Write code directly into `work/{sketch-name}/`.

Rules for this phase:
- No validators (no code-reviewer, no security-auditor, no test-reviewer).
- No tests required.
- No tech-spec, no tasks decomposition.
- Use sketch.md as the sole compass: implement exactly "What must work" and
  nothing beyond it.
- Commit when the prototype runs: `feat(sketch): {sketch-name} — initial prototype`

When the prototype is working (the "What must work" slice is demonstrable),
proceed to Phase 6.

## Phase 6: Decision Gate

Ask the user:

> "Прототип готов. Что дальше?
> - **Развиваем** → запускаю `/new-user-spec` и передаю `work/{sketch-name}/sketch.md` как стартовый контекст.
> - **Архивируем** → запускаю `/done` для `work/{sketch-name}/`."

- **"Развиваем"** → invoke `/new-user-spec` and explicitly pass the path
  `work/{sketch-name}/sketch.md` as pre-filled context for the interview.
- **"Архивируем"** → invoke `/done` to archive `work/{sketch-name}/`.

## Self-Verification

- [ ] `work/{sketch-name}/sketch.md` created and approved by user
- [ ] Design Context loaded for UI sketches (CIP brief + frontend-design)
- [ ] Code implements exactly the "What must work" slice — nothing more
- [ ] Prototype committed
- [ ] Decision gate reached: user chose develop or archive
