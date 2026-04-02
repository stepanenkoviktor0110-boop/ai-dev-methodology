---
name: moneymaker-setup
description: |
  Onboarding wizard for the moneymaker pricing pipeline. Collects rates,
  hosting tiers, agent costs, billing info, and service catalog through
  a guided interview, then writes ~/.moneymaker/config.yml.

  Use when: "настрой moneymaker", "moneymaker setup", "/moneymaker-setup",
  "настрой ценообразование", "setup pricing config", "обнови тарифы moneymaker",
  "создай config.yml для moneymaker", "moneymaker онбординг"
---

# Moneymaker Setup

> Guided interview that produces `~/.moneymaker/config.yml` — the shared
> config read by all other moneymaker skills. Run once for initial setup
> or again to update specific fields.

## Phase 0: Config Check

1. Check if `~/.moneymaker/config.yml` exists (use Read tool; an error means
   the file is absent).
2. **File exists** → announce: "Обнаружен существующий config.yml. Перехожу
   в режим обновления." → skip to the Update Mode section below.
3. **File absent** → announce: "Начинаем первичную настройку moneymaker."
   → proceed to Phase 1.

---

## Phase 1: Rates

1. Ask: "Какая ваша почасовая ставка разработки? (RUB/час, например 2000)"
2. Store the answer as `hourly_rate` (integer).

**Checkpoint:** "Ставка: {hourly_rate} ₽/час. Верно? Готовы перейти к хостинг-тирам?"

Wait for confirmation before proceeding.

---

## Phase 2: Hosting Tiers

Explain to the user:
> Хостинг-тиры описывают варианты серверов, которые вы предлагаете клиентам.
> Для каждого тира нужны два числа:
> - **cost** — ваша себестоимость (сколько вы платите хостеру)
> - **markup** — цена для клиента (сколько платит клиент)

1. Suggest starting examples:
   ```
   vps_small:  cost 800 / markup 1150
   vps_medium: cost 1500 / markup 2200
   ```
2. Ask: "Добавить эти тиры или хотите свои? Можете перечислить любое количество
   тиров в формате: название, cost, markup."
3. Collect all tiers. Each tier needs: key (snake_case), cost (integer), markup (integer).
4. Allow the user to add more tiers or remove suggested ones.

**Checkpoint:** Show collected tiers as a table. "Хостинг-тиры готовы. Переходим к себестоимости агентов?"

Wait for confirmation before proceeding.

---

## Phase 3: Agent Costs

Explain:
> Себестоимость AI-агентов — ежемесячные расходы на API, которые учитываются
> при расчёте маржи.

1. Ask: "Сколько в месяц уходит на Claude API? (RUB/мес, например 300)"
2. Store as `agent_costs.claude_api` (integer).

**Checkpoint:** "Claude API: {claude_api} ₽/мес. Верно? Переходим к реквизитам?"

Wait for confirmation before proceeding.

---

## Phase 4: Billing Info

Tell the user:
> Реквизиты используются при генерации коммерческих предложений.
> Данные хранятся локально в `~/.moneymaker/` и не попадают в git-репозиторий.

1. Ask for `name` — название юрлица или ИП (например "ИП Иванов Иван Иванович").
2. Ask for `inn` — ИНН.
3. Ask for `bank` — банковские реквизиты (название банка, БИК, р/с — одной строкой или несколькими).

**Checkpoint:** Show collected billing info. "Реквизиты собраны. Переходим к каталогу типовых блоков?"

Wait for confirmation before proceeding.

---

## Phase 5: Catalog

Explain:
> Каталог типовых блоков — список услуг/модулей, которые вы предлагаете клиентам.
> Используется в `/moneymaker-expand` для ценообразования апсейл-позиций.
>
> Каждый блок имеет:
> - **key** — уникальный идентификатор (kebab-case)
> - **hours** — норма часов на реализацию (или null для фиксированной цены)
> - **description** — название для клиента
>
> Для блоков с фиксированной ценой (hours: null) дополнительно:
> - **price_fixed** — цена для клиента
> - **cost_fixed** — ваша себестоимость (или null если нет прямых расходов)

1. Suggest starting catalog:
   ```
   email-notifications: 2h — "Email-уведомления"
   telegram-bot:        4h — "Telegram-бот для уведомлений"
   backup:              1h — "Резервное копирование"
   support-monthly:     фикс. цена 3000₽ — "Сопровождение (абонентская плата)"
   ```
2. Ask: "Добавить эти блоки как стартовый набор? Можете изменить, удалить
   или добавить свои."
3. For each block with `hours: null`, collect `price_fixed` and `cost_fixed`.
4. Allow iterative adding until the user says "готово" or "хватит".

**Checkpoint:** Show the full catalog as a list. "Каталог готов. Переходим к финальной сборке?"

Wait for confirmation before proceeding.

---

## Phase 6: Write

1. Assemble the full YAML from all collected data following this structure:

   ```yaml
   hourly_rate: {value}
   hosting:
     {tier_key}:
       cost: {value}
       markup: {value}
   agent_costs:
     claude_api: {value}
   billing:
     name: "{value}"
     inn: "{value}"
     bank: "{value}"
   catalog:
     {block_key}:
       hours: {value_or_null}
       description: "{value}"
       # for fixed-price blocks only:
       price_fixed: {value}
       cost_fixed: {value_or_null}
   ```

2. Show a summary to the user (do NOT display billing section contents — inn, bank, name — in chat):
   - "hourly_rate: {value}"
   - "hosting: {tiers summary}"
   - "catalog: {N} позиций"
   - "billing: [данные сохранены]"
   - "agent_costs: claude_api: {value}"
3. Wait for explicit approval: "Записать этот файл в `~/.moneymaker/config.yml`?"

**Checkpoint:** YAML reviewed and approved by user. Proceed to write.

4. On approval:
   - Create `~/.moneymaker/` directory if it does not exist (use Bash: `mkdir -p`).
   - Write the file using Write tool to `~/.moneymaker/config.yml`.
5. Set file permissions:
   ```bash
   chmod 600 ~/.moneymaker/config.yml && chmod 700 ~/.moneymaker/
   ```
6. Confirm: "Файл записан."
7. Show tip: "Готово. Следующий шаг: `/moneymaker-new {project-name}`"

---

## Update Mode

Triggered from Phase 0 when `~/.moneymaker/config.yml` already exists.

1. Read existing `config.yml` via Read tool.
2. Parse and display current values grouped by section (do NOT display billing section contents — inn, bank, name — in chat):
   - Ставка: `hourly_rate`
   - Хостинг: list of tiers with cost/markup
   - Агенты: `claude_api`
   - Реквизиты: "[данные сохранены]"
   - Каталог: list of blocks
3. Ask: "Какие разделы хотите обновить? (ставка, хостинг, агенты, реквизиты, каталог — или 'всё')"
4. For each section the user wants to change:
   - Show current value(s).
   - Collect new value(s) using the same prompts as the corresponding phase.
   - For every changed field, show confirmation:
     "Обновить {field} с {old_value} на {new_value}?"
   - Wait for explicit "да" before accepting the change.
   - If the user says "нет" → keep the old value for that field.
5. After all changes confirmed:
   - Show a summary of the updated config (do NOT display billing section contents in chat; show "billing: [данные сохранены]" instead).
   - Wait for final approval: "Перезаписать config.yml?"

   **Checkpoint:** Updated YAML reviewed and approved. Proceed to write.

   - On approval → write via Write tool.
6. Set file permissions:
   ```bash
   chmod 600 ~/.moneymaker/config.yml && chmod 700 ~/.moneymaker/
   ```
7. Confirm: "Config обновлён."
8. Show tip: "Готово. Следующий шаг: `/moneymaker-new {project-name}`"

---

## Self-Verification

After completing setup or update, verify:

- [ ] `~/.moneymaker/config.yml` exists and is valid YAML
- [ ] File contains all top-level keys: `hourly_rate`, `hosting`, `agent_costs`, `billing`, `catalog`
- [ ] `hourly_rate` is a positive integer
- [ ] Each hosting tier has both `cost` and `markup` as positive integers
- [ ] `agent_costs.claude_api` is a positive integer
- [ ] `billing` contains `name`, `inn`, `bank` — all non-empty strings
- [ ] Each catalog entry has `hours` (positive integer or null) and `description` (non-empty string)
- [ ] Catalog entries with `hours: null` have `price_fixed` defined
- [ ] In update mode: only explicitly confirmed changes were applied
- [ ] User received the "Следующий шаг" tip
