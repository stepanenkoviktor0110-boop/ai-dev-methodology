---
name: moneymaker-finalize
description: |
  Finalizes a project quote by reading expand-output.md, optionally applying
  a per-project rate override, selecting upsell positions, validating margins,
  and generating a markdown KP table saved as kp-{timestamp}.md.

  Use when: "/moneymaker-finalize", "сформируй КП", "финализируй смету",
  "финальное КП", "finalize quote", "moneymaker finalize", "сгенерируй смету",
  "создай коммерческое предложение", "собери КП", "оформи КП"
argument-hint: "{project}"
---

# moneymaker-finalize

Leads the user through finalizing a commercial proposal: displays both quote
blocks, handles rate override, lets the user select upsell positions, validates
margins, and writes the final `kp-{timestamp}.md` file.

## Phase 1: Validation

1. Check that `~/.moneymaker/config.yml` exists:

   ```bash
   test -f ~/.moneymaker/config.yml && echo "EXISTS" || echo "MISSING"
   ```

   If MISSING → "Конфиг не найден. Запустите `/moneymaker-setup`." Stop.

2. Check that `expand-output.md` exists for this project:

   ```bash
   test -f ~/.moneymaker/projects/{project}/expand-output.md && echo "EXISTS" || echo "MISSING"
   ```

   If MISSING → "Файл expand-output.md не найден. Запустите `/moneymaker-expand {project}` сначала." Stop.

3. Check that `expand-output.md` is not empty and contains both section markers:

   Read the file. If it lacks both `[Договорились]` and `[Можно предложить]` → "Файл expand-output.md повреждён или пуст. Перезапустите `/moneymaker-expand {project}`." Stop.

**Checkpoint:** Config and expand-output.md present and valid. Proceed to display.

---

## Phase 2: Display & Rate Override

1. Read `~/.moneymaker/config.yml` — extract `hourly_rate` and `catalog`.

2. Check if `~/.moneymaker/projects/{project}/overrides.yml` exists. If yes, read it and use its `hourly_rate` as the active rate for this project.

3. Show both blocks from `expand-output.md` to the user.

4. Ask: "Используем ставку {active_rate} руб/час для этого проекта. Хотите задать другую ставку для '{project}'? (введите число или нажмите Enter чтобы продолжить)"

5. If the user enters a number:
   - Show: "Установить ставку {new_rate} руб/час для проекта '{project}'? (да / нет)"
   - Wait for confirmation.
   - On confirmation: write `~/.moneymaker/projects/{project}/overrides.yml` with content:
     ```yaml
     hourly_rate: {new_rate}   # Overrides global rate for this project only
     ```
   - Update active rate to `new_rate`.
   - Note: `config.yml` is not modified.

**Checkpoint:** Active rate confirmed, override written if requested. Proceed to position selection.

---

## Phase 3: Position Selection

1. Positions from `[Договорились]` are included automatically — inform the user.

2. Present the `[Можно предложить]` block and ask the user to select positions to include:

   "Выберите позиции из блока 'Можно предложить' (через запятую введите номера или названия, или 'все' / 'нет'):"

3. Wait for user response. Accept flexible formats: numbers, names, "все", "нет", empty.

4. Build the final position list: all Договорились items + selected Можно предложить items.

**Checkpoint:** Final position list assembled. Proceed to margin validation.

---

## Phase 4: Margin Validation

For each position in the final list, calculate margin using the active rate:

- **Hourly labor** (has `hours` in catalog): `margin = price - (hours × active_rate)`
- **Price-fixed** (`price_fixed` in catalog, `hours: null`): `margin = price_fixed - cost_fixed`
  - If `cost_fixed: null` → margin = "не определена" (not a blocker)
- **Hosting**: `margin = markup - cost` (from config.yml hosting section)
- **No catalog match**: margin shown as from expand-output.md

If any position has negative margin:

1. Show the warning immediately:

   ```
   ⚠️ Убыточная позиция: {name}
   Себестоимость: {cost} руб
   Предложенная цена: {price} руб
   Минимальная безубыточная цена: {cost} руб
   ```

2. Ask: "Что сделать? [1] Включить с текущей ценой  [2] Изменить цену  [3] Исключить позицию"

3. Wait for user decision before proceeding to the next position.

**Checkpoint:** All positions validated, negative margins resolved. Proceed to KP generation.

---

## Phase 5: KP Generation

1. Separate positions into two groups:
   - **Разовые работы**: type = "one-time"
   - **Ежемесячные платежи**: type = "monthly"

2. Build the KP markdown using this exact format:

   ```markdown
   # Коммерческое предложение: {project}

   ## Разовые работы

   | Позиция | Стоимость | Маржа |
   |---------|-----------|-------|
   | {name} | {price} руб | {margin} руб |
   | **Итого разовые** | **{total} руб** | **{total_margin} руб** |

   ## Ежемесячные платежи

   | Позиция | Стоимость/мес | Маржа/мес |
   |---------|--------------|-----------|
   | {name} | {price} руб | {margin} руб |
   | **Итого ежемесячные** | **{total} руб** | — |

   ## Итог

   | | |
   |--|--|
   | Чистая прибыль (разовые) | {total_margin_one_time} руб |
   | Чистая прибыль (ежемесячные) | {total_margin_monthly} руб/мес |
   ```

   Rules for totals:
   - If any margin in a group is "не определена" → show "—" in the group's итого margin cell.
   - If a position was kept despite negative margin → add `⚠️ убыток` note in its margin cell.
   - If ежемесячные group is empty → omit that section entirely.

3. Generate timestamp in format `YYYY-MM-DD-HHmmss`.

4. Write the file to `~/.moneymaker/projects/{project}/kp-{timestamp}.md` using Write tool.

5. Show the full KP to the user.

6. Show tip: "КП сохранено: kp-{timestamp}.md. Скопируйте таблицу для отправки клиенту."

**Checkpoint:** KP file written, content shown to user, tip displayed.

---

## Self-Verification

- [ ] Validation stops with specific error + hint command when config.yml or expand-output.md missing
- [ ] Damaged expand-output.md (missing section markers) → error, not crash
- [ ] overrides.yml written on rate override; config.yml left unchanged
- [ ] overrides.yml already exists → show current value, ask to update
- [ ] Договорились positions included automatically; user selects from Можно предложить only
- [ ] Negative margin → ⚠️ warning with breakeven price in RUB, user chooses before proceeding
- [ ] price_fixed with cost_fixed: null → margin "не определена", generation continues
- [ ] KP table split into Разовые / Ежемесячные; empty group omitted
- [ ] Group итого margin shows "—" if any item in the group has undefined margin
- [ ] kp-{timestamp}.md written in YYYY-MM-DD-HHmmss format, not appended
- [ ] Tip shown after save
