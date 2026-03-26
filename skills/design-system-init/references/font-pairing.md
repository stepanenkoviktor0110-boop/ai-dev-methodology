# Font Pairing Reference

## Pairing Principles

### Contrast Pairing

Combine fonts from different classes: sans-serif heading + serif body, or serif heading + sans-serif body. Creates visual tension and clear hierarchy. Best for editorial, marketing, and content-heavy layouts where heading must stand apart from body text.

Advantages: strong visual hierarchy, easy to distinguish roles, works at any scale.
Limitation: requires careful x-height matching — pair fonts with similar x-heights to avoid visual discord.

### Concordance Pairing

Both fonts from the same family (e.g., Roboto + Roboto Slab) or same classification (two geometric sans-serifs). Creates harmony and consistency. Best for dashboards, SaaS products, documentation, and technical interfaces where uniformity matters more than drama.

Advantages: inherently harmonious, fewer visual conflicts, simpler to maintain.
Limitation: hierarchy relies entirely on weight and size — needs strong weight contrast (200+ units).

**When to choose:**
- Marketing / editorial / portfolio → contrast pairing
- SaaS / dashboard / documentation / technical → concordance pairing
- Uncertain → start with concordance (safer default), switch to contrast if hierarchy feels flat

## Weight Hierarchy

- **Heading:** semibold (600) or bold (700). Use 700 for impact, 600 for professional tone.
- **Body:** regular (400) or medium (500). Use 400 for long-form, 500 for UI text.
- Minimum 200-unit difference between heading and body weights for visible hierarchy.
- Verify chosen weights are available for the specific Google Font.

## Typographic Scale Ratios

Each ratio generates a set of sizes from a base of 16px. Smaller ratios produce tighter scales suited for dense UIs; larger ratios create dramatic scales for editorial layouts.

### Minor Third (1.200) — dashboards, admin panels, dense UIs
Sizes at base 16px: xs 11, sm 13, base 16, lg 19, xl 23, 2xl 28, 3xl 33, 4xl 40

### Major Third (1.250) — general-purpose web apps, marketing sites
Sizes at base 16px: xs 10, sm 13, base 16, lg 20, xl 25, 2xl 31, 3xl 39, 4xl 49

### Perfect Fourth (1.333) — editorial content, blogs, clear heading hierarchy
Sizes at base 16px: xs 9, sm 12, base 16, lg 21, xl 28, 2xl 38, 3xl 50, 4xl 67

### Golden Ratio (1.618) — hero sections, portfolios. Too wide for dense UIs
Sizes at base 16px: sm 10, base 16, lg 26, xl 42, 2xl 68

## Classic Combinations

Each entry is self-contained — read it and write directly to tokens.json.

### 1. Inter + Lora
- **Type:** contrast (sans + serif)
- **Mood:** modern, professional
- **Heading:** Inter, weights: 600, 700
- **Body:** Lora, weights: 400, 500
- **Use-case:** SaaS products, fintech, corporate sites
- **tokens.json:**
  - `typography.families.heading`: `"Inter, system-ui, sans-serif"`
  - `typography.families.body`: `"Lora, Georgia, serif"`

### 2. Playfair Display + Source Sans 3
- **Type:** contrast (serif + sans)
- **Mood:** elegant, editorial
- **Heading:** Playfair Display, weights: 600, 700
- **Body:** Source Sans 3, weights: 400, 500
- **Use-case:** fashion, luxury brands, magazines, portfolios
- **tokens.json:**
  - `typography.families.heading`: `"Playfair Display, Georgia, serif"`
  - `typography.families.body`: `"Source Sans 3, system-ui, sans-serif"`

### 3. Roboto + Roboto Slab
- **Type:** concordance (same superfamily)
- **Mood:** modern, technical
- **Heading:** Roboto Slab, weights: 600, 700
- **Body:** Roboto, weights: 400, 500
- **Use-case:** documentation, developer tools, technical blogs
- **tokens.json:**
  - `typography.families.heading`: `"Roboto Slab, Georgia, serif"`
  - `typography.families.body`: `"Roboto, system-ui, sans-serif"`

### 4. Montserrat + Merriweather
- **Type:** contrast (sans + serif)
- **Mood:** friendly, warm
- **Heading:** Montserrat, weights: 600, 700
- **Body:** Merriweather, weights: 400, 500
- **Use-case:** blogs, education platforms, non-profits, community sites
- **tokens.json:**
  - `typography.families.heading`: `"Montserrat, system-ui, sans-serif"`
  - `typography.families.body`: `"Merriweather, Georgia, serif"`

### 5. Poppins + Inter
- **Type:** concordance (two geometric sans)
- **Mood:** modern, friendly
- **Heading:** Poppins, weights: 600, 700
- **Body:** Inter, weights: 400, 500
- **Use-case:** startups, mobile-first apps, modern dashboards
- **tokens.json:**
  - `typography.families.heading`: `"Poppins, system-ui, sans-serif"`
  - `typography.families.body`: `"Inter, system-ui, sans-serif"`

### 6. Raleway + Open Sans
- **Type:** concordance (two sans-serif)
- **Mood:** clean, formal
- **Heading:** Raleway, weights: 600, 700
- **Body:** Open Sans, weights: 400, 500
- **Use-case:** corporate sites, consulting, government, B2B
- **tokens.json:**
  - `typography.families.heading`: `"Raleway, system-ui, sans-serif"`
  - `typography.families.body`: `"Open Sans, system-ui, sans-serif"`

### 7. DM Serif Display + DM Sans
- **Type:** contrast (serif + sans, same superfamily)
- **Mood:** elegant, modern
- **Heading:** DM Serif Display, weights: 400 (only weight available)
- **Body:** DM Sans, weights: 400, 500
- **Use-case:** creative agencies, lifestyle brands, restaurants
- **tokens.json:**
  - `typography.families.heading`: `"DM Serif Display, Georgia, serif"`
  - `typography.families.body`: `"DM Sans, system-ui, sans-serif"`

### 8. Space Grotesk + IBM Plex Sans
- **Type:** concordance (two sans-serif, both technical)
- **Mood:** technical, futuristic
- **Heading:** Space Grotesk, weights: 600, 700
- **Body:** IBM Plex Sans, weights: 400, 500
- **Use-case:** dev tools, crypto/web3, engineering platforms
- **tokens.json:**
  - `typography.families.heading`: `"Space Grotesk, system-ui, sans-serif"`
  - `typography.families.body`: `"IBM Plex Sans, system-ui, sans-serif"`

### 9. Nunito + Libre Baskerville
- **Type:** contrast (rounded sans + serif)
- **Mood:** friendly, approachable
- **Heading:** Nunito, weights: 600, 700
- **Body:** Libre Baskerville, weights: 400
- **Use-case:** education, children's platforms, healthcare
- **tokens.json:**
  - `typography.families.heading`: `"Nunito, system-ui, sans-serif"`
  - `typography.families.body`: `"Libre Baskerville, Georgia, serif"`

### 10. Oswald + Source Serif 4
- **Type:** contrast (condensed sans + serif)
- **Mood:** bold, editorial
- **Heading:** Oswald, weights: 600, 700
- **Body:** Source Serif 4, weights: 400, 500
- **Use-case:** news sites, sports, media, event pages
- **tokens.json:**
  - `typography.families.heading`: `"Oswald, system-ui, sans-serif"`
  - `typography.families.body`: `"Source Serif 4, Georgia, serif"`

## Alignment with tokens.json

Font values map to `typography.families` in tokens.json as plain strings with fallback stacks:

```json
{
  "typography": {
    "families": {
      "heading": "Font Name, fallback-stack",
      "body": "Font Name, fallback-stack",
      "mono": "JetBrains Mono, monospace"
    }
  }
}
```

Fallback stacks by classification:
- **Sans-serif:** `system-ui, sans-serif`
- **Serif:** `Georgia, serif`
- **Monospace:** `monospace` (not covered by font pairing — keep default)

The `mono` family is not affected by font pairing — it stays as `"JetBrains Mono, monospace"` unless user explicitly changes it.

Scale ratios map to `typography.sizes`. Pick a ratio from the Typographic Scale Ratios section, round values to whole pixels, and write them as:

```json
{
  "typography": {
    "sizes": {
      "xs": "11px", "sm": "13px", "base": "16px", "lg": "19px",
      "xl": "23px", "2xl": "28px", "3xl": "33px", "4xl": "40px"
    }
  }
}
```

Weights map to `typography.weights` — keep the standard four tokens:

```json
{
  "typography": {
    "weights": { "regular": 400, "medium": 500, "semibold": 600, "bold": 700 }
  }
}
```
