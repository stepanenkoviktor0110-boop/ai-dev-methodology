---
name: moneymaker-pattern
description: |
  Creates and manages progression chain patterns in ~/.moneymaker/patterns/.
  A pattern describes the natural evolution of a project archetype as named steps.
  Referenced by cases (pattern_key + chain_position) and used by moneymaker-expand
  to identify where a current project sits in a chain and what comes next.

  Use when: "/moneymaker-pattern", "создай паттерн", "добавь цепочку прогрессии",
  "редактируй паттерн", "покажи паттерны", "moneymaker pattern",
  "какие паттерны есть", "обнови цепочку"
argument-hint: "{create|edit|list} {pattern-key?}"
---

# moneymaker-pattern

Manages archetypal progression chains. A pattern captures the logical sequence
of steps a project naturally evolves through, so `moneymaker-expand` can
identify the current position and suggest what comes next.

## Pattern file format

Each pattern lives at `~/.moneymaker/patterns/{pattern-key}.md`:

```markdown
---
pattern_key: {pattern-key}
name: {human-readable name}
task_types: [{comma-separated task type labels matching cases}]
---

# {name}

## Chain

### {step-key}
**Название:** {short name shown in expand output}
**Описание:** {what this step delivers}
**Типичные триггеры:** {conditions that make a client agree to this step}

### {next-step-key}
...
```

Step keys are kebab-case, stable identifiers. They are referenced in case files
as `chain_position`. Never rename a step key — it would break existing case links.
Add new steps at the end or insert with a new key.

---

## Actions

### list

Show all existing patterns:

```bash
find ~/.moneymaker/patterns -name "*.md" -type f 2>/dev/null
```

If none found → "Паттернов пока нет. Создайте первый: `/moneymaker-pattern create {key}`"

For each found file → read it and display: `{pattern_key}: {name} ({N} шагов)` with step keys listed inline.

---

### create {pattern-key}

1. Validate `{pattern-key}` matches `^[a-z0-9-]+$`. If not → "Ключ паттерна — только строчные буквы, цифры и дефис." Stop.

2. Check if file already exists:
   ```bash
   test -f ~/.moneymaker/patterns/{pattern-key}.md && echo "EXISTS" || echo "MISSING"
   ```
   If EXISTS → "Паттерн `{pattern-key}` уже существует. Используйте `edit` для изменения." Stop.

3. Create directory:
   ```bash
   mkdir -p ~/.moneymaker/patterns
   ```

4. Interview — collect pattern metadata:

   - Ask: "Как называется этот тип проекта? (например: 'Личный кабинет с ролевой моделью')"
   - Ask: "Какие метки task_type соответствуют этому паттерну? (через запятую, например: личный кабинет, веб-кабинет, портал)"

5. Interview — collect chain steps:

   Tell the user:
   > Теперь опишем шаги цепочки — от базового заказа до максимального развития.
   > Для каждого шага нужны: ключ (kebab-case), название, описание, типичные триггеры.
   > Начните с первого шага (то, с чего обычно начинается проект).

   Collect steps iteratively:
   - For each step ask: "Ключ шага (kebab-case):", "Название:", "Описание:", "Типичные триггеры:"
   - After each step: "Добавить следующий шаг? (да/нет)"
   - Continue until user says "нет".

   Minimum 2 steps required. If user stops at 1 → "Цепочка должна содержать минимум 2 шага. Добавьте хотя бы один следующий шаг."

6. Show assembled pattern for review:

   ```
   Паттерн: {pattern_key}
   Название: {name}
   task_types: {list}

   Цепочка:
   {step_key} → {название}
     Описание: {описание}
     Триггеры: {триггеры}
   {step_key} → ...
   ```

   Ask: "Записать паттерн? (да / нет / исправить)"

   - "исправить" → ask what to change, show updated version again, repeat.
   - "нет" → "Отменено."
   - "да" → write file.

7. Write file using Write tool.

8. Confirm: "Паттерн `{pattern-key}` записан: `~/.moneymaker/patterns/{pattern-key}.md`"

9. Show hint: "Теперь при записи кейса (`/moneymaker-case`) можно указать этот паттерн."

---

### edit {pattern-key}

1. Check file exists:
   ```bash
   test -f ~/.moneymaker/patterns/{pattern-key}.md && echo "EXISTS" || echo "MISSING"
   ```
   If MISSING → "Паттерн `{pattern-key}` не найден. Список: `/moneymaker-pattern list`" Stop.

2. Read and display the current pattern in full.

3. Ask: "Что изменить? (название / task_types / добавить шаг / изменить шаг / удалить шаг)"

4. Apply the requested change:

   - **название / task_types**: collect new value, show diff, confirm.
   - **добавить шаг**: ask position ("после какого шага?"), collect step fields, insert.
   - **изменить шаг**: ask which step key, show current values, collect new values per field.
   - **удалить шаг**: ask which step key → warn: "Удаление шага сломает кейсы с chain_position: {key}. Точно удалить?" → require explicit "да".

5. Show full updated pattern. Ask: "Перезаписать? (да/нет)"

6. On "да" → overwrite file with Write tool. Confirm: "Паттерн обновлён."

---

## Self-Verification

- [ ] pattern_key validated: `^[a-z0-9-]+$`
- [ ] list action reads actual files, not hardcoded
- [ ] create: minimum 2 steps enforced
- [ ] create: full pattern shown to user before writing
- [ ] edit: step deletion shows warning about case breakage before proceeding
- [ ] step keys are kebab-case — enforced in both create and edit
- [ ] files written with Write tool (not Bash echo)
- [ ] hint to use pattern in moneymaker-case shown after create
