---
name: design-review
description: |
  Lightweight review of UI code against project design tokens.
  Reads .design-system/tokens.json and scans changed UI files for hardcoded values,
  outputs 2-3 concrete token-based recommendations.

  Use when: "design review", "review styles", "check tokens", "проверь стили",
  "проверь токены", "проверь дизайн-систему", "check design system compliance"
---

# Design Review

Scan changed UI files against project design tokens. Output concrete recommendations to replace hardcoded values with token references. Minimal overhead: read only `tokens.json`, check only changed files.

## When to Activate

**Activate** if both conditions are true:
- `.design-system/tokens.json` exists in the project root
- The current task changed at least one UI file (`.tsx`, `.vue`, `.html`, `.css`, `.scss`)

**Skip silently** if either condition fails. No error, no message — just proceed with the rest of the workflow.

### Decision Framework

| Condition | Action |
|-----------|--------|
| tokens.json exists AND UI files changed | Run review |
| tokens.json exists, no UI files changed | Skip silently |
| No tokens.json, UI files changed | Skip silently |
| No tokens.json, no UI files changed | Skip silently |

## What to Read

Read only `.design-system/tokens.json` from the project. This gives you:
- `colors` — primary, secondary, neutral (shade scales), semantic, background, text
- `typography` — families, sizes, weights, lineHeights
- `spacing` — numeric scale (4px–64px)
- `radii`, `shadows`, `breakpoints`

Do not read component HTML files, design-principles.md, lessons-learned.md, or any other DS artifacts. Token economy: keep overhead at ~500-1000 tokens.

For token schema details and CSS custom property naming, apply conventions from [design-tokens.md](../../shared/design-references/design-tokens.md) — naming patterns, CSS variable generation rules (`--{category}-{path}`).

## What to Check

Scan each changed UI file for these categories of hardcoded values:

### Colors
- Hex values (`#3b82f6`, `#fff`, `#111827`) not defined as CSS custom properties from tokens
- `rgb()`/`rgba()`/`hsl()` values that match or approximate a token color
- Inline `color`, `background-color`, `border-color` with literal values

**Match strategy:** Compare hardcoded hex against token color values. Case-insensitive. For approximate matches (e.g., `#3a82f5` vs token `#3b82f6`), recommend the closest token.

For color matching nuance, apply principles from [color-principles.md](../../shared/design-references/color-principles.md) — temperature awareness, saturation context when evaluating "close enough" matches.

### Spacing
- `px` values in `margin`, `padding`, `gap`, `top`, `right`, `bottom`, `left` that don't correspond to the spacing scale
- Check against spacing tokens: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px (default scale)

### Typography
- `font-family` declarations not matching `families.heading`, `families.body`, or `families.mono`
- `font-size` values not in the sizes scale (xs through 4xl)
- `font-weight` numeric values not matching weights tokens (400, 500, 600, 700)

### Non-DS Custom Properties
- CSS custom properties (`--some-var`) that duplicate token semantics but use different names

## How to Report

### Findings present (1+ issues)

Output 2-3 most impactful recommendations. Format each as:

```
found {what} in {file}:{line} -> use {token CSS variable}
```

Examples:
- `found color #3B82F6 in Button.tsx:14 -> use --color-primary-500`
- `found gap: 8px in Card.vue:32 -> use --space-2 (8px) or consider --space-4 (16px) for component spacing`
- `found font-family: Arial in Header.css:5 -> use --font-heading (Inter, system-ui, sans-serif)`

**Non-obvious matches** (token is not an exact value match): add a brief two-layer explanation after the `->` line — first why the token fits (human-readable), then the technical detail. Example:
```
found color #3a82f5 in Card.tsx:9 -> use --color-primary-500
  why: closest brand primary color (off by 1 in R channel)
  detail: token value #3b82f6, deltaE < 1
```
Skip the explanation when the match is exact.

Prioritization when more than 3 findings:
1. Colors — highest visual impact
2. Typography — brand consistency
3. Spacing — layout consistency

Cap at 3 recommendations. If more exist, add: "N more findings — run `/design-review` for full report."

### No findings

Report: **"Styles match DS"** — stop. No iterations, no suggestions, no further analysis.

## Scope Guard

This skill does the following and nothing else:
- Reads tokens.json
- Scans changed UI files for hardcoded values
- Outputs concrete token replacement recommendations

This skill does not:
- Run the full design pipeline
- Generate mockups, pages, or SVG
- Conduct design interviews or ask about mood/preferences
- Create new components or modify existing ones
- Run design-retrospective or collect feedback
- Modify any files (it only reports — the caller decides whether to apply fixes)
- Validate token correctness or contrast ratios (that is design-system-init's job)
- Check layout structure, responsiveness, or accessibility
