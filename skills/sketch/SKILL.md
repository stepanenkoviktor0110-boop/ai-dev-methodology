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

> Fills the gap between the full pipeline and nothing at all: a working prototype in one
> session, no validators, no reviewers. Afterwards either develop it through `/new-user-spec`
> or archive it through `/done`.

Talk to the user in Russian throughout — the prompts below are the wording to use.

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

**Design context (UI sketches only).** Skip entirely for CLI tools, scripts and backend logic.
A sketch is new-from-scratch by definition, so for a UI sketch invoke `Skill(design-ultimate)`
before writing markup — it is the single entry point for design and pulls in its own
dependencies. Do not call `impeccable`, `frontend-design` or the taste overlays directly.
If the project already carries a `DESIGN.md`, read it and follow it instead of re-deriving a
direction. Keep the outcome in working context — no file, no report to the user.

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

## Checks against state

```bash
# 1. sketch.md exists — the compass the code was supposed to follow
rg -c . work/{sketch-name}/sketch.md

# 2. the prototype was committed
git log --oneline -5 --grep "sketch({sketch-name})"
```
