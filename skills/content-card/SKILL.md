---
name: content-card
description: |
  Generates HTML/CSS social media content cards (1080×1350px) in two modes:
  personal-brand (editorial, atmospheric) and marketplace (product, selling).
  Selects card format based on content, applies design techniques,
  uses local photo paths. Supports iteration after preview.

  Use when: "сделай карточку", "content-card", "/card", "карточка для соцсетей",
  "сделай пост-карточку", "карточка для инстаграма", "карточка для телеграма",
  "make a card", "создай карточку"
---

# Content Card

Generates social media cards as self-contained HTML files (1080×1350px).
Output opens in browser, ready to screenshot and post.

## Phase 1: Determine Mode

- **personal-brand** — личный блог, экспертный контент, кейсы
- **marketplace** — карточка товара для маркетплейса или продающего поста

If content makes mode obvious — propose without asking.

**Checkpoint:** mode confirmed.

## Phase 2: Gather Content

### personal-brand

Ask in one message:
1. Тема / заголовок
2. Текст (буллеты, цитата, описание)
3. Фото: путь к файлу (`D:/photos/photo.jpg`) или "без фото"
4. Фирменные цвета (если есть)
5. Название канала/бренда для подписи (если нужно)

Propose format from [personal-brand.md](references/personal-brand.md).

### marketplace

Ask in one message:
1. Название товара + характеристики (3–7 пунктов)
2. Фото товара: путь к файлу
3. Цветовая тема (или "подобрать под товар")
4. Цена / скидка (если нужно)

**Checkpoint:** контент собран, формат предложен и подтверждён.

## Phase 3: Generate Card

1. Apply techniques from [personal-brand.md](references/personal-brand.md)
   or [marketplace.md](references/marketplace.md)

2. Generate self-contained HTML file:
   - Size: `1080px × 1350px`, fixed
   - All CSS in `<style>` block
   - Photo via `<img src="{path}">` with `object-fit: cover`
   - Fonts via Google Fonts CDN (default: Inter / Playfair Display)
   - No external dependencies except fonts

3. Ask user where to save the file before writing.

4. После генерации — назвать 2–3 спорных дизайн-решения, объяснить кратко.
   Ждать фидбэка.

**Checkpoint:** HTML создан, пользователь посмотрел.

## Phase 4: Iterate

Принять фидбэк, применить правки. Типичные итерации:
- Размер/вес шрифта
- Позиция кадрирования фото (`object-position`)
- Цветовые тона
- Расположение текста
