---
name: design-generate
description: |
  Generates HTML/CSS pages and static SVG mockups from text descriptions using
  a project's design system. Selects from 15 layout patterns (5 basic + 10 advanced
  grids), assembles components, applies tokens, supports iteration via screenshots.
  After approval, generates diagonal before/after collage.

  Use when: "сделай макет", "generate design", "сгенерируй страницу", "create mockup",
  "макет страницы", "generate a page", "собери страницу", "покажи страницу",
  "design page", "сверстай макет"
---

# Design Generate

Generate HTML+SVG page mockups from text descriptions using the project's design system.

```
User description → Parse → Select Layout → Assemble Components → HTML + SVG
                                                                      ↓
                                                              User feedback (screenshot)
                                                                      ↓
                                                                  Iterate
                                                                      ↓
                                                              User approves final
                                                                      ↓
                                                          Before/After Collage
```

## Phase 0: Readiness Check

1. Check that `.design-system/tokens.json` exists in the project root
   - If missing → stop and tell the user: "Design system not found. Run `/design-system-init` to create one."
   - If the file exists, read it and validate that it is valid JSON
   - If JSON is malformed → stop and tell the user: "tokens.json is corrupted. Run `/design-system-init` to recreate the design system."

2. Parse tokens into CSS custom properties for use in generated pages (following the mapping pattern from [design-tokens.md](../../shared/design-references/design-tokens.md))

3. Проверить наличие `.design-system/taste-profile.md`:
   - Если файл существует и не пуст — прочитать и извлечь предпочтения:
     - **Цветовые предпочтения** — температура, насыщенность, конкретные предпочтения
     - **Типографика** — стиль заголовков, предпочтения по шрифтам
     - **Стиль и смелость** — уровень (conservative / balanced / bold / experimental)
     - **Антипаттерны** — что было отклонено пользователем в прошлых сессиях
   - Если файла нет или он пуст — продолжить без него (первая сессия, профиль ещё не создан)
   - Передать загруженные предпочтения как контекст в Phase 2 (выбор лейаута) и Phase 3 (сборка)

**Checkpoint:** tokens.json exists, parses as valid JSON, contains colors/typography/spacing sections. Taste-profile прочитан (если существует) или пропущен с graceful degradation.

## Phase 1: Parse Request

1. Identify from the user's description:
   - **Page type** — what kind of page (login, dashboard, landing, catalog, settings, etc.)
   - **Components needed** — buttons, cards, inputs, tables, navigation, etc.
   - **Layout structure** — sidebar? grid? hero section? split view?
   - **Content** — real content provided, or use realistic placeholders?

2. If the description is ambiguous, propose a specific interpretation:
   - "I'll create a login page with Split Screen layout: brand image on the left, login form (email + password + submit button) on the right. Sound good?"
   - Wait for confirmation before proceeding

3. List components that are in `.design-system/components/`. For missing ones:
   - Simple components (badge, alert, divider) → create on the fly following patterns from [component-patterns.md](references/component-patterns.md)
   - Complex components (carousel, data-table, calendar) → inform the user this needs a separate session via `/design-system-init` to add the component properly

**Checkpoint:** page type identified, component list ready, layout direction chosen, ambiguities resolved.

## Phase 2: Select Layout

1. Choose a layout from 15 available patterns using the selection table in [generation-guide.md](references/generation-guide.md) (layout patterns, selection criteria, CSS implementation)

2. For **basic layouts** (Single Column, Sidebar+Content, Grid, Hero+Sections, Split Screen):
   - Use the built-in CSS from generation-guide.md directly

3. For **advanced layouts** (Golden Ratio, Fibonacci, Broken Grid, Van de Graaf, Ratio Grid, Optical Margin, Diagonal, Typographic Grid, Bento, Swiss Grid):
   - Apply the CSS technique from [grid-techniques.md](references/grid-techniques.md) for the chosen pattern
   - Advanced layouts are appropriate when the user asks for visual impact, editorial feel, or premium aesthetics

4. Если taste-profile загружен — учитывать стиль и уровень смелости при выборе лейаута:
   - conservative/balanced → предпочитать basic layouts
   - bold/experimental → рассматривать advanced layouts (Broken Grid, Diagonal, Bento)
   - Антипаттерны из taste-profile → исключить лейауты, которые пользователь отклонял ранее

5. Present the chosen layout to the user:
   - "For your login page, I'll use Split Screen layout — brand visual on the left half, form on the right."
   - If the user disagrees → select a different pattern

**Checkpoint:** layout pattern selected and confirmed, CSS approach determined.

## Phase 3: Assemble & Generate

### 3.1 Assemble page

1. Build the page structure using the selected layout CSS
2. Place components into layout regions following patterns from [component-patterns.md](references/component-patterns.md) (BEM naming, variant system, slot pattern)
3. Inject design tokens as CSS custom properties in `:root`
4. Add content — real if provided, realistic placeholders otherwise (per generation-guide.md placeholder rules: diverse names, meaningful text, colored rectangles for images, realistic numbers)
5. Если taste-profile загружен — применить предпочтения при сборке:
   - Цветовые предпочтения → корректировать выбор цветовых токенов (тёплые/холодные, насыщенность)
   - Типографика → учитывать предпочтения по стилю заголовков (serif/sans-serif)
   - Антипаттерны → избегать паттернов, которые пользователь отклонял ранее

### 3.2 Generate HTML

1. Use [preview-template.html](assets/preview-template.html) as the base template
2. Replace `{{PAGE_TITLE}}` with the page name
3. Replace `{{PAGE_STYLES}}` with component styles + layout CSS
4. Replace `{{PAGE_CONTENT}}` with assembled page HTML
5. Replace placeholder tokens in `:root` with actual values from tokens.json

### 3.3 Generate SVG

1. Convert the same layout to static SVG (per generation-guide.md SVG rules)
2. Desktop viewport: `viewBox="0 0 1440 900"`
3. Mobile viewport (if requested): `viewBox="0 0 390 844"`
4. Convert layouts to absolute-positioned shapes, embed colors directly (no CSS variables in SVG)

### 3.4 Save files

1. Validate file names: only lowercase letters, digits, and hyphens allowed (`/^[a-z0-9-]+$/`). Reason: prevents path traversal when writing to `.design-system/pages/`
2. Save HTML to `.design-system/pages/{name}.html`
3. Save SVG to `.design-system/pages/{name}.svg`
4. If device variants requested: `{name}-mobile.html`, `{name}-desktop.html`

**Checkpoint:** HTML file uses template + tokens (no hardcoded values), SVG renders the same layout, file names validated, files saved to `.design-system/pages/`.

## Phase 4: Present & Iterate

### 4.1 Present result

1. Tell the user where files were saved
2. Suggest opening the HTML file in a browser: "Open `.design-system/pages/{name}.html` in your browser to see the interactive preview."
3. Ask: "Send a screenshot if you'd like adjustments, or describe what to change."

### 4.2 Two-layer description

После генерации страницы создать двухуровневое описание и сохранить в `.design-system/pages/{name}.description.md`:
- **Layer 1 (краткое):** тип страницы и выбранный лейаут — одно предложение. Пример: "Landing page на Split Screen лейауте с hero-секцией слева и формой справа."
- **Layer 2 (детальное):** компоненты, использованные цветовые токены, типографика, отступы, адаптивность — техническая спецификация для будущих итераций.

### 4.3 Iterate on feedback

When the user provides feedback (screenshot or text):
- "Bigger" / "smaller" → adjust spacing and font sizes
- "More contrast" → darken text, increase color differences
- "Simpler" → reduce components, increase whitespace
- "More detail" → add secondary info, icons, metadata
- Specific feedback → apply the requested change

Regenerate both HTML and SVG after each iteration.

### 4.4 Handle context exhaustion

If the conversation context is running low and further iterations are needed:
1. **Quick Learning (background).** Spawn a subagent to run [quick-learning](../quick-learning/SKILL.md). Pass it: "design session", iteration count, user corrections summary. Do NOT read quick-learning SKILL.md yourself.
2. Save the current state of all generated files
3. Generate a continuation prompt the user can paste into a new session:

```
Continue design iteration for `.design-system/pages/{name}.html`.
Design system: `.design-system/tokens.json`.
Layout: {layout pattern used}.
Last feedback: "{user's last feedback}".
Open the HTML file, apply the feedback, regenerate HTML+SVG.
```

3. Tell the user: "Context is getting long. Start a new session with `/design-generate` and paste this prompt: {prompt above}"

**Checkpoint:** result presented, user feedback addressed (or continuation prompt generated).

## Phase 5: Before/After Collage

Triggers when the user confirms the final variant ("да", "этот", "утверждаю", "go", "approved").

### 5.1 Capture "Before"

- If replacing an existing page → take a screenshot of the current version (or ask user to paste one)
- If designing from scratch → use a solid `var(--color-neutral-200)` rectangle with centered text "No previous design"

### 5.2 Build collage

Generate a single HTML file with diagonal split overlay:

```html
<div class="collage" style="position:relative; width:100%; max-width:1440px; aspect-ratio:16/9; overflow:hidden">
  <!-- Bottom layer: After -->
  <img src="{after-screenshot}" style="width:100%; height:100%; object-fit:cover">
  <!-- Top layer: Before, clipped diagonally -->
  <img src="{before-screenshot}" style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover; clip-path:polygon(0 0,100% 0,0 100%)">
  <!-- Diagonal line -->
  <div style="position:absolute; inset:0; background:linear-gradient(to bottom right,transparent calc(50% - 1px),white calc(50% - 1px),white calc(50% + 1px),transparent calc(50% + 1px)); pointer-events:none"></div>
  <!-- Labels -->
  <span style="position:absolute; top:12%; left:8%; background:rgba(0,0,0,.6); color:#fff; padding:6px 18px; border-radius:4px; font:600 14px/1 system-ui">До</span>
  <span style="position:absolute; bottom:12%; right:8%; background:rgba(0,0,0,.6); color:#fff; padding:6px 18px; border-radius:4px; font:600 14px/1 system-ui">После</span>
</div>
```

Images: embed as base64 data URIs (self-contained file, no external dependencies).

### 5.3 Save

1. Validate name: `/^[a-z0-9-]+$/`
2. Save to `.design-system/collages/{page-name}-collage.html`
3. Tell the user: "Collage saved to `.design-system/collages/{page-name}-collage.html` — open in browser to see the diagonal before/after comparison."

**Checkpoint:** collage generated with diagonal clip-path, both images embedded, labels overlaid, file saved.

### 5.4 Cleanup

After the collage is saved, delete intermediate artifacts that were used only for demonstration and iteration:

1. Remove all iteration SVGs: `.design-system/pages/{name}.svg`, `{name}-mobile.svg`, etc.
2. Remove intermediate HTML previews if the final version has been applied to the actual codebase
3. Keep only:
   - `.design-system/collages/{page-name}-collage.html` (before/after comparison)
   - `.design-system/pages/{name}.html` (final approved version — as reference)
4. Ask the user: "Промежуточные файлы (SVG, черновики) удалены. Оставлен финальный HTML и коллаж до/после. Ок?"

**Checkpoint:** intermediate artifacts removed, only final HTML + collage remain.

## Final Check

Before finishing, verify:
- [ ] All generated HTML files use design tokens from tokens.json (no hardcoded color/spacing values)
- [ ] HTML files use preview-template.html as base (includes CSP meta tag)
- [ ] SVG files render the same layout as HTML with embedded colors
- [ ] File names match `/^[a-z0-9-]+$/` pattern
- [ ] `.design-system/pages/` directory contains the generated files
- [ ] User has been shown where to find the files
- [ ] Before/after collage saved to `.design-system/collages/` (if user confirmed final variant)
- [ ] Intermediate artifacts (SVGs, draft HTMLs) cleaned up — only final HTML + collage remain
- [ ] Taste-profile прочитан (если `.design-system/taste-profile.md` существует) и предпочтения применены в Phase 2 и Phase 3
- [ ] Two-layer description сгенерировано и сохранено в `.design-system/pages/{name}.description.md`
