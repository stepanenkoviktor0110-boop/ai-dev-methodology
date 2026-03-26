---
name: design-system-init
description: |
  Creates a project design system through scan and interview. Generates
  .design-system/tokens.json + standalone HTML components with CSS custom properties.
  Covers palette (by mood), typography (font pairs), spacing (golden ratio/Fibonacci),
  radii, shadows, breakpoints.

  Use when: "создай дизайн-систему", "инициализируй дизайн", "design system init",
  "create design system", "настрой дизайн", "initialize design", "сделай дизайн-токены"
---

# Design System Init

Create a design system for a web project through scanning existing styles and structured interview. Output: `.design-system/tokens.json` + component HTML files, each opening standalone in a browser.

## Phase 0: Project Readiness

1. Verify the project is web-based — look for HTML, CSS, SCSS, JS, TS, JSX, TSX, Vue, or Svelte files. If none found — stop and explain: "This skill works with web projects only (HTML/CSS/JS/TS/React/Vue/Svelte). Your project does not appear to be a web project."
2. Check if `.design-system/` directory already exists:
   - If yes — ask user: **(a)** update existing tokens, **(b)** recreate from scratch, **(c)** cancel
   - If "update" — load existing `tokens.json` and use as defaults in interview. Also read `.design-system/taste-profile.md` (if exists) — use saved preferences (liked/disliked decisions, style tendencies) as context for proposing updates. If file is missing — continue without it.
   - If "recreate" — proceed as if no DS exists
   - If "cancel" — stop

**Checkpoint:** Project is web-based. `.design-system/` conflict resolved (or absent). Proceed to Phase 1.

## Phase 1: Project Scan

Scan the project for existing design values before asking anything. Priority order for sources:

1. **Tailwind config** (`tailwind.config.*`) — `theme.extend.colors`, `theme.extend.spacing`, `theme.extend.fontFamily`
2. **CSS custom properties** — `:root` or `html` declarations with `--` prefix
3. **SCSS variables** — `$color-*`, `$font-*`, `$spacing-*` patterns
4. **Hardcoded values** — repeated hex colors, px/rem values in component files

Also detect:
- Tech stack (React, Vue, Svelte, plain HTML)
- Existing component patterns (buttons, cards, inputs, navbars)
- Google Fonts imports or `@font-face` declarations

**If conflicting values exist** between sources (e.g., Tailwind says primary is blue, CSS vars say green) — present both to user and ask which takes priority.

Present findings: "I found these design patterns in your project: {list}. I'll use them as a starting point for the interview."

**If no styles found** — report "No existing styles detected. We'll build everything from scratch." and proceed.

**Checkpoint:** Scan complete. Existing values collected (or noted as absent). Present summary to user. Proceed to Phase 2.

## Phase 2: Interview

Propose-first approach: suggest concrete values based on scan results, user confirms or adjusts. One topic at a time.

### 2.1 Project Context and Mood

1. Определить категорию проекта (landing / webapp / admin / portfolio) и прочитать соответствующую секцию `## {Category}` из [designer-experience.md](../../shared/design-references/designer-experience.md) — учесть накопленные предпочтения, удачные решения и антипаттерны при формулировке предложений. Если секция пуста или файл отсутствует — продолжить без неё.

2. Ask: "Who is this project for? What feeling should it evoke?" Offer examples: professional, playful, calm, bold, luxurious, minimal.

3. Based on user's answer, propose a color mood using the emotional color map from [color-psychology.md](../../shared/design-references/color-psychology.md) — match the described emotion to a color combination from the summary table (e.g., "calm spa" → dusty rose + warm beige + terracotta; "fintech" → dark navy + warm white + copper).

4. После определения настроения — прочитать только соответствующую секцию из [style-profiles.md](../../shared/design-references/style-profiles.md): найти профиль по совпадению mood + category (использовать Quick Lookup таблицу для матчинга), загрузить только эту секцию. Использовать рецепты профиля (типографика, палитра, spacing, характерные приёмы) при формировании предложений в следующих шагах интервью. Если точного совпадения нет — выбрать ближайший подходящий профиль.

### 2.2 Color Palette

Using the mood from 2.1, propose specific hex values for:
- **Primary** (shades 50–900) — the brand color
- **Secondary** (shades 50–900) — complementary accent
- **Neutral** (0–1000) — grayscale with appropriate temperature
- **Semantic** — success (green), warning (amber), error (red), info (blue)
- **Background** — default, surface, elevated
- **Text** — primary, secondary, disabled, inverse

Apply color combination principles from [color-principles.md](../../shared/design-references/color-principles.md) when building the palette — temperature contrast (principle 1), 60-30-10 ratio (principle 2), grège treatment for depth (principle 6), asymmetric saturation (principle 8).

Present the palette. User confirms or adjusts individual colors.

### 2.3 Typography

Select heading + body font pair following pairing rules from [font-pairing.md](references/font-pairing.md) — pick a classic combination matching the project mood, apply weight hierarchy and typographic scale ratio.

Propose:
- **Heading font** — name, weights (600/700)
- **Body font** — name, weights (400/500)
- **Mono font** — default: JetBrains Mono, monospace
- **Size scale** — based on chosen ratio (Minor Third for dense UIs, Major Third for general, Perfect Fourth for editorial)
- **Line heights** — tight: 1.25, normal: 1.5, relaxed: 1.75

### 2.4 Spacing

Propose three spacing scale options:
- **Golden Ratio** (1.618x): 4, 6, 10, 17, 27, 43, 70, 113 px
- **Fibonacci**: 4, 4, 8, 12, 20, 32, 52, 84 px
- **Standard**: 4, 8, 12, 16, 24, 32, 48, 64 px (most predictable, widely used)

User picks one. Default recommendation: Standard (safest for general use).

### 2.5 Radii, Shadows, Breakpoints

Propose defaults:
- **Radii:** sm 4px, md 8px, lg 12px, full 9999px
- **Shadows:** sm `0 1px 2px rgba(0,0,0,0.05)`, md `0 4px 6px rgba(0,0,0,0.07)`, lg `0 10px 15px rgba(0,0,0,0.1)`
- **Breakpoints:** sm 640px, md 768px, lg 1024px, xl 1280px

User confirms or adjusts.

### 2.6 Components

Based on scan results and project type, propose a component list. Common set: button, card, input, badge, alert, navbar. User selects which to include in v1.

After every 2-3 topics — briefly summarize decisions so far.

### Двухслойные описания

При предложении любых решений во время интервью — описывать двумя слоями:
1. **Человеко-понятный** — образное описание на языке ощущений («тёплая уютная палитра с акцентом на натуральные тона», «чистая геометричная типографика с ощущением лёгкости»).
2. **Технический** — конкретные значения (hex-коды, font-family, font-weight, px/rem).

Сначала всегда человеко-понятное описание, затем техническое. Это помогает пользователю сначала оценить общее ощущение, а потом проверить детали.

**Checkpoint:** All topics covered: mood, palette, typography, spacing, radii/shadows/breakpoints, components. User confirmed choices. Proceed to Phase 3.

## Phase 3: Build

### 3.1 Generate tokens.json

Create `.design-system/tokens.json` following the schema from [design-tokens.md](../../shared/design-references/design-tokens.md) — colors (primary/secondary/neutral/semantic/background/text), typography (families/sizes/weights/lineHeights), spacing, radii, shadows, breakpoints.

Validate file name segments used in paths: component and page names follow `/^[a-z0-9-]+$/` — alphanumeric and hyphens only. Reject names with path separators or special characters.

### 3.2 Generate CSS Custom Properties

Convert tokens to CSS variables following the pattern `--{category}-{path}`:
- `--color-primary-500`, `--color-text-primary`
- `--font-heading`, `--font-size-base`, `--font-weight-medium`
- `--space-4`, `--radius-md`, `--shadow-md`

### 3.3 Generate Components

For each approved component, create `.design-system/components/{name}.html`:

Each file is self-contained:
- `<!DOCTYPE html>` with full HTML structure
- `<style>` block with `:root` CSS custom properties (all tokens) + component styles using only `var(--token-name)` — zero hardcoded color/spacing/font values
- Component markup showing all variants (sizes, states, colors)
- Opens standalone in browser — no build step needed

Google Fonts loaded via `<link>` tag for chosen heading and body fonts.

### 3.4 Generate README

Create `.design-system/README.md` with:
- Token overview (color names, type scale, spacing scale)
- Component list with file paths
- "Open any `.html` file in a browser to preview"

**Checkpoint:** `tokens.json` created with all interview values. Components generated using CSS custom properties. README generated. Proceed to Phase 4.

## Phase 4: Verify

1. **JSON validation** — parse `tokens.json`, verify it contains all required sections: colors, typography, spacing, radii, shadows, breakpoints
2. **CSS custom properties check** — scan each component HTML for hardcoded hex colors (`#[0-9a-fA-F]{3,8}`), hardcoded px values outside of token definitions, or hardcoded font names in component styles. All values use `var(--*)` references
3. **Contrast ratio check** — for these text/background pairs from tokens:
   - `text.primary` on `background.default` — target >= 4.5:1
   - `text.secondary` on `background.default` — target >= 4.5:1
   - `text.inverse` on `colors.primary.500` — target >= 4.5:1
   - If any pair fails, adjust the color and update tokens.json
4. **File name check** — verify all files in `.design-system/components/` match `/^[a-z0-9-]+\.html$/`

Report results. Fix any failures before finishing.

**Checkpoint:** All verifications passed. Design system is ready.

## Final Check

Before finishing, verify:
- [ ] All 4 phases completed
- [ ] `tokens.json` is valid JSON with colors, typography, spacing, radii, shadows, breakpoints
- [ ] Every component HTML uses CSS custom properties (no hardcoded values)
- [ ] Contrast ratios >= 4.5:1 for all text/background pairs
- [ ] All file names in `.design-system/` match `/^[a-z0-9-]+$/` (excluding extensions)
- [ ] `.design-system/README.md` reflects actual contents
- [ ] User confirmed palette, typography, spacing choices during interview
- [ ] designer-experience.md был прочитан по категории проекта (или отмечено как пустой/отсутствующий)
- [ ] style-profile использован: предложения по палитре и типографике учитывают рецепты из соответствующего профиля
- [ ] taste-profile.md прочитан при update-сценарии (или отмечен как отсутствующий)
- [ ] Все описания решений двухслойные: сначала образное, затем техническое
