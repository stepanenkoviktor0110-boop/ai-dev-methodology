---
name: design-retrospective
description: |
  Analyze design session feedback, extract aesthetic lessons into
  .design-system/lessons-learned.md, promote recurring patterns to
  design-principles.md, write taste-profile and cross-project experience,
  generate context-free next-session prompt.

  Use when: "дизайн ретроспектива", "design retrospective",
  "уроки дизайна", "что улучшить в дизайне", "design lessons learned",
  "ретроспектива дизайн-сессии", "design feedback analysis"
---

# Design Retrospective

Evaluate the completed design session, extract aesthetic lessons from user feedback and corrections, embed them into the project's design system knowledge.

**Input:** session history (user feedback, corrections), `.design-system/` files
**Output:** entries in `.design-system/lessons-learned.md`, promotions to `.design-system/design-principles.md`, `.design-system/taste-profile.md`, experience entries in [designer-experience.md](../../shared/design-references/designer-experience.md), next-session prompt
**Language:** lessons and communication in Russian

## Phase 1: Collect Evidence

1. Check that `.design-system/` directory exists in the project.
   - If missing — stop and suggest: "Директория `.design-system/` не найдена. Запустите `/design-system-init` для создания дизайн-системы."
2. Ask user which design session to analyze (if not obvious from conversation context).
3. Read `.design-system/` structure: `tokens.json`, `components/`, `pages/` — note what was created or modified during the session.
4. Collect user feedback from the session:
   - Color corrections requested ("слишком яркий", "сделай теплее")
   - Font/typography changes ("шрифт не подходит", "заголовок крупнее")
   - Spacing adjustments ("слишком тесно", "больше воздуха")
   - Layout reworks ("переделай структуру", "поменяй расположение")
   - Component modifications ("кнопка не та", "карточка слишком широкая")
   - Elements rejected entirely ("убери это", "не нужен этот блок")
5. List all files changed during the session (components, pages, tokens).

**Checkpoint:** `.design-system/` confirmed, session feedback collected, changed files listed.

## Phase 2: Identify Patterns

1. Categorize collected corrections into types:

| Category | Examples |
|----------|----------|
| Color corrections | Palette too cold/warm, contrast issues, accent color wrong |
| Typography changes | Wrong font pair, sizes off, weight mismatch |
| Spacing adjustments | Too tight/loose, inconsistent gaps, padding issues |
| Layout reworks | Structure changed, grid reorganized, section order swapped |
| Component modifications | Shape/size/style of specific components adjusted |

2. Look for repetitions within the session — same type of correction appearing 2+ times signals a pattern.
3. Look for repetitions across sessions — compare with existing `.design-system/lessons-learned.md` entries (if file exists).
4. If no corrections were made and no patterns detected — report to user: "Сессия прошла без коррекций, паттернов не выявлено." Skip to Phase 5.

**Checkpoint:** corrections categorized, patterns identified (or confirmed absent).

## Phase 3: Write Lessons

1. Check if `.design-system/lessons-learned.md` exists.
   - If no — create with header:
     ```markdown
     # Design Lessons Learned

     Accumulated lessons from design sessions. Each entry records a problem,
     its cause, how it was resolved, and the rule to follow in the future.
     ```
   - If yes — read existing content.

2. For each identified pattern, check for duplicates:
   - Read existing entries in `lessons-learned.md`.
   - If the same problem is already recorded (matching root cause) — skip, do not duplicate.

3. Append new entries in this format. Каждый урок описывать двухслойно: сначала понятным языком (что и почему — для человека), затем технические детали (конкретные значения токенов, CSS-свойства, hex-коды — для агента).

```markdown
### {YYYY-MM-DD}: {pattern title}

**Problem:** {what went wrong — 1 sentence, human-readable}
**Cause:** {why it happened — 1 sentence, human-readable}
**Solution:** {how it was fixed — 1 sentence, human-readable}
**Technical:** {concrete values — tokens, CSS properties, hex codes}
**Rule:** {what to do in the future — actionable instruction}
```

Example entry:
```markdown
### 2026-03-15: Слишком холодная палитра для уютного бренда

**Problem:** Сгенерированная палитра воспринималась холодной и отстранённой для сайта спа-салона.
**Cause:** Выбраны чистые синие оттенки без тёплого подтона — не соответствует настроению "уют, расслабление".
**Solution:** Заменены на приглушённые тёплые оттенки (sage, warm beige, muted terracotta).
**Technical:** hsl(210, 60%, 50%) → hsl(30, 40%, 85%) --color-bg-warm; hsl(15, 35%, 65%) --color-accent-warm
**Rule:** Для "уютных" и "расслабляющих" проектов использовать приглушённые тёплые тона, избегать чистых холодных оттенков.
```

**Checkpoint:** lessons written to `.design-system/lessons-learned.md`, duplicates skipped.

## Phase 4: Promote Principles

1. Read all entries in `.design-system/lessons-learned.md`.
2. Group entries by similar rules — same root cause type or same correction category.
3. Count occurrences in each group. If a rule appears 3+ times across all entries (not per session) — it qualifies for promotion.
4. Check if `.design-system/design-principles.md` exists.
   - If no — create with header:
     ```markdown
     # Design Principles

     Project-specific aesthetic rules derived from accumulated feedback.
     Each principle emerged from 3+ repeated lessons and reflects the
     project's taste profile.
     ```
   - If yes — read existing content.

5. For each qualifying rule:
   - Check if already present in `design-principles.md` — skip if exists.
   - Add new principle:
     ```markdown
     ## {principle title}

     **Rule:** {actionable instruction}
     **Rationale:** {why — derived from N lessons, dates: ...}
     **Category:** {color | typography | spacing | layout | component}
     ```

6. If no rules qualify for promotion — report: "Нет правил для промоушена (ни одно не появилось 3+ раз)."

**Checkpoint:** qualifying rules promoted to `design-principles.md`, or reported that none qualify.

## Phase 4.5: Write Taste Profile & Experience

Записать эстетические предпочтения из сессии в проектный taste-profile и кросс-проектную базу опыта.

### Taste-profile запись

1. Проверить наличие `.design-system/taste-profile.md`.
   - Отсутствует — создать по шаблону ниже.
   - Существует, но повреждён (отсутствуют обязательные секции `## Цветовые предпочтения`, `## Типографика`, `## Стиль и смелость`, `## Антипаттерны`, `## История изменений`) — пересоздать по шаблону, предупредить пользователя: "taste-profile.md был повреждён и пересоздан. Предыдущие записи утеряны."

2. Извлечь из сессии эстетические предпочтения:
   - Цветовые: температура (тёплые/холодные/нейтральные), насыщенность (приглушённые/яркие/смешанные), конкретные предпочтения.
   - Типографика: стиль заголовков (serif/sans-serif/mono), предпочтения по размерам и весам.
   - Стиль и смелость: уровень (conservative/balanced/bold/experimental), характер.
   - Антипаттерны: что отклонялось пользователем, сколько раз.

3. Записать извлечённые предпочтения в соответствующие секции `.design-system/taste-profile.md`. При конфликте с существующим предпочтением (например, тёплые тона → холодные тона) — применить latest-wins: обновить значение, пометить старое "пересмотрено {YYYY-MM-DD}" в секции `## История изменений`.

4. Если из сессии не удалось извлечь эстетических предпочтений — пропустить, не записывать пустые значения.

Шаблон taste-profile.md:
```markdown
# Taste Profile

## Цветовые предпочтения
- Температура: тёплые / холодные / нейтральные
- Насыщенность: приглушённые / яркие / смешанные
- Конкретные предпочтения:

## Типографика
- Стиль заголовков: serif / sans-serif / mono
- Предпочтения:

## Стиль и смелость
- Уровень: conservative / balanced / bold / experimental
- Характер:

## Антипаттерны
<!-- что отклонялось и сколько раз -->

## История изменений
<!-- dated entries, latest wins, overridden marked "пересмотрено" -->
```

### Experience запись

1. Определить категорию текущего проекта: landing, webapp, admin, portfolio. Определять по типу проекта из контекста сессии (структура страниц, назначение, целевая аудитория).

2. Проверить наличие [designer-experience.md](../../shared/design-references/designer-experience.md).
   - Отсутствует — создать с базовой структурой: 4 категории (Landing, Webapp, Admin, Portfolio), в каждой 3 подсекции (Предпочтения, Что работало, Антипаттерны).
   - Секция нужной категории отсутствует — создать секцию с 3 подсекциями.

3. Из уроков текущей сессии выбрать обобщаемые (применимые не только к этому проекту, но к категории в целом). Проектно-специфичные детали (конкретные hex-коды, имена компонентов) обобщить до уровня категории.

4. Append обобщённые уроки в конец соответствующих подсекций категории в `designer-experience.md`. Формат записи:
```markdown
- {YYYY-MM-DD}: {обобщённый урок — 1-2 предложения}
```

Записи добавляются строго в конец подсекции (append-only). Существующие записи не редактируются и не удаляются.

**Checkpoint:** taste-profile.md записан/обновлён (или пропущен если нет данных), experience записи добавлены в designer-experience.md (append-only).

## Phase 4.9: Quick Learning (background)

Before generating the next-session prompt, spawn a subagent to run [quick-learning](../quick-learning/SKILL.md). Pass it: "design retrospective", session corrections summary (from Phase 1-2), lessons extracted count. The subagent runs in the **background** — proceed to Phase 5 immediately. When it finishes, show the user its one-line summary. Do NOT read quick-learning SKILL.md yourself.

## Phase 5: Generate Next-Session Prompt

Generate a self-contained prompt for continuing design work in a new session. The prompt requires zero prior conversation context to be useful.

Prompt structure:
```
## Контекст проекта
{Project name, purpose, target audience — from tokens.json metadata or session context}

## Текущее состояние дизайн-системы
{List of tokens.json sections: palette mood, font pair, spacing scale}
{List of existing components and pages}

## Накопленные принципы
{List rules from design-principles.md, or "Принципов пока нет" if empty/missing}

## Вкусовой профиль
{Краткое резюме из .design-system/taste-profile.md: цветовая температура, насыщенность, типографика, уровень смелости. Или "Вкусовой профиль пока не сформирован" если файл отсутствует/пуст}

## Что было сделано в последней сессии
{Summary of session work: what was created/modified, key decisions}

## Что делать дальше
{Suggested next steps: new pages, component refinements, areas needing attention}

## Как запустить
{Concrete command: /design-generate for new pages, /design-system-init for token updates}
```

Present the prompt to user in a code block for easy copy-paste.

**Checkpoint:** next-session prompt generated and shown to user.

## Self-Verification

Before finishing, verify:
- [ ] `.design-system/` existence checked (refused if missing)
- [ ] Session feedback collected and categorized
- [ ] Each lesson has all 5 fields (Problem, Cause, Solution, Technical, Rule)
- [ ] No duplicate lessons added
- [ ] Rules are actionable (not vague advice like "делать лучше")
- [ ] Promotion count is across all entries, not per session
- [ ] Already-promoted rules not duplicated in `design-principles.md`
- [ ] Next-session prompt is self-contained (no references to "this conversation")
- [ ] Next-session prompt includes taste-profile summary (or "не сформирован" if missing)
- [ ] taste-profile.md содержит все обязательные секции (Цветовые предпочтения, Типографика, Стиль и смелость, Антипаттерны, История изменений)
- [ ] Experience запись добавлена append-only (существующие записи в designer-experience.md не перезаписаны)
- [ ] Конфликтующие предпочтения помечены "пересмотрено" с датой в Истории изменений
- [ ] Edge cases обработаны: missing/corrupted taste-profile, missing designer-experience, missing category section
- [ ] All file writes target `.design-system/` in the project (not skill directory), experience writes target `shared/design-references/`
