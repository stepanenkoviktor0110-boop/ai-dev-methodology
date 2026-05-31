# Skill Quality Checklist (post-embedding)

Run after Phase 6 (quick-ref regen), before Phase 7 (commit).
Per each modified skill — one parallel agent.

## Two-layer check

1. **General skill compliance** — delegated to existing `skill-checker` agent (size, structure, references, checkpoints, self-verification). Don't re-implement.
2. **Skill-trainer-specific** (rule-level) — items below. These check the NEW applied rules, not the whole skill.

## Agent prompt

```
You audit a skill after skill-trainer embedded new rules.

Skill: {skill-name}
SKILL.md path: $AGENTS_HOME/skills/{skill-name}/SKILL.md
Write target (where new rules went): {write_target}
Newly applied rule IDs: {applied_ids}

STEP 1 — General skill health (delegate via Task tool):
Invoke skill-checker agent on this skill. Capture its findings.

STEP 2 — Read SKILL.md and write_target. Check these skill-trainer-specific items
against the NEW applied rules (identifiable by `(triad #N)` suffix or recent diff):

### Size discipline
- [ ] **A1.** SKILL.md body ≤ 250 строк (мягкий лимит).
      - 200-250 → WARN "приближается, время выносить блоки в references/"
      - >250 → FAIL с конкретным предложением: какие секции вынести
- [ ] **A2.** write_target (references/*.md) ≤ 500 строк
- [ ] **A3.** Если SKILL.md > 250 — тело осталось координацией (карта файлов,
      порядок чтения, gate-вопросы), а не партитурой (длинные процедуры в теле)

### Rule quality (новые правила only)
- [ ] **B1.** Логический уровень: нет имён проектов, файлов из памяти, сессий.
      Имена инструментов (pdfplumber, BigQuery, Prisma) — допустимо.
      Имена внутренних артефактов (mvp-booking-flow, school-stol) — недопустимо.
- [ ] **B2.** Каждое новое правило имеет триаду trigger→action→goal в одной строке
- [ ] **B3.** Каждое новое правило ссылается на исходную триаду через `(triad #N)`
      для трассировки
- [ ] **B4.** Новое правило не дублирует существующее по trigger+goal
      (проверить grep'ом write_target до новых правил)
- [ ] **B5.** Trigger конкретный (узнаваемая ситуация: "when X happens",
      "before doing Y"), не generic ("when writing code", "when working with files")
- [ ] **B6.** Action императивный и проверяемый ("grep X", "enumerate Y",
      "verify against Z"), не размытый ("be careful", "consider", "think about")

## Output JSON

```json
{
  "skill": "{name}",
  "skill_checker_findings": [...],
  "trainer_specific": {
    "passed": ["A1", "B1", ...],
    "failed": [{"item": "A1", "evidence": "SKILL.md 312 строк", "fix": "вынести Phase 3+4 в references/phases.md"}],
    "warned": [{"item": "A1", "note": "248 строк, близко к границе"}]
  }
}
```

## Gate behaviour (мягкий)

After all agents return — main context aggregates:
- Если все pass → silent, proceed to Phase 7
- Если есть failed → показать пользователю компактную сводку:
  ```
  Quality issues found:
  - {skill-name}: A1 (SKILL.md 312 строк), B4 (rule duplicates existing)
  - {skill-name}: B1 (rule mentions project name)

  Действия:
  [починить] — спавню fix-агентов по каждому failed item
  [записать в known-issues] — фиксирую в $AGENTS_HOME/skills/{skill}/known-issues.md
  [игнорировать] — commit без починки
  ```
- Если только warned → одна строка в финальном Report, без блокировки

Жёсткий gate не используем: мягкий даёт пользователю контроль и не блокирует
быстрые проходы при незначительных отклонениях.
