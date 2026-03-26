# Design Generation Guide

## Table of Contents

- [Page Assembly Process](#page-assembly-process)
- [Layout Selection Guide](#layout-selection-guide)
- [Basic Layout Patterns](#basic-layout-patterns)
- [Advanced Grid Patterns](#advanced-grid-patterns)
- [Responsive Behavior](#responsive-behavior)
- [Placeholder Content](#placeholder-content)
- [HTML Generation](#html-generation)
- [SVG Generation](#svg-generation)
- [Device Frames](#device-frames)
- [Iterating on Designs](#iterating-on-designs)

## Page Assembly Process

1. **Parse request** — identify page type, sections, components needed
2. **Select layout** — choose layout pattern based on page type
3. **Place components** — fill layout regions with design system components
4. **Add content** — use real content if provided, realistic placeholders otherwise
5. **Generate HTML** — assemble into preview-ready HTML file
6. **Generate SVG** — convert the same layout to static SVG

## Layout Selection Guide

15 layout patterns available: 5 basic (built-in CSS) and 10 advanced (from grid-techniques.md).

### When to use basic vs advanced

Use **basic layouts** when the request is straightforward, content-driven, or conventional — dashboards, forms, catalogs, standard landing pages. They load faster in context and produce predictable results.

Use **advanced layouts** when the user explicitly asks for visual impact, editorial feel, premium aesthetics, or unconventional structure. Also use when the project's design principles favor bold composition.

### Selection table

| Request type | Recommended pattern | Category |
|---|---|---|
| Article, blog post, settings page, form | Single Column | basic |
| Dashboard, admin panel, CRM, email client | Sidebar + Content | basic |
| Product catalog, gallery, card list, team page | Grid | basic |
| Landing page, marketing page, homepage | Hero + Sections | basic |
| Auth page (login/signup), onboarding, comparison | Split Screen | basic |
| Portfolio, editorial spread, magazine layout | Golden Ratio | advanced |
| Design system showcase, component library page | Fibonacci Sequence | advanced |
| Fashion, agency, creative studio, art portfolio | Broken Grid | advanced |
| Long-form reading, documentation, book-style layout | Van de Graaf | advanced |
| Media gallery, mixed-content grid, photo portfolio | Ratio Grid | advanced |
| Typography-heavy page, quote sections, icon nav | Optical Margin Alignment | advanced |
| Startup landing, sports brand, aggressive editorial | Diagonal Layout | advanced |
| Blog, publishing, content-first design | Typographic Grid | advanced |
| Product features (Apple-style), SaaS features, about page | Bento Grid | advanced |
| Branding page, cultural institution, design agency | Swiss Grid | advanced |

## Basic Layout Patterns

### Single Column (articles, forms, settings)
```
┌──────────────────────────┐
│         Header           │
├──────────────────────────┤
│                          │
│     Content (max-w)      │
│                          │
├──────────────────────────┤
│         Footer           │
└──────────────────────────┘
```
CSS: `max-width: 768px; margin: 0 auto;`

### Sidebar + Content (dashboards, admin panels)
```
┌────────┬─────────────────┐
│        │     Header      │
│  Side  ├─────────────────┤
│  bar   │                 │
│        │    Content      │
│  240px │                 │
└────────┴─────────────────┘
```
CSS: `display: grid; grid-template-columns: 240px 1fr;`

### Grid (catalogs, galleries, card lists)
```
┌──────┬──────┬──────┐
│ Card │ Card │ Card │
├──────┼──────┼──────┤
│ Card │ Card │ Card │
└──────┴──────┴──────┘
```
CSS: `display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: var(--space-6);`

### Hero + Sections (landing pages)
```
┌──────────────────────────┐
│         Hero             │
├──────────────────────────┤
│     Feature Grid         │
├──────────────────────────┤
│     Testimonials         │
├──────────────────────────┤
│     CTA Section          │
├──────────────────────────┤
│         Footer           │
└──────────────────────────┘
```

### Split Screen (auth, onboarding)
```
┌────────────┬─────────────┐
│            │             │
│   Image/   │   Form/     │
│   Brand    │   Content   │
│            │             │
└────────────┴─────────────┘
```
CSS: `display: grid; grid-template-columns: 1fr 1fr; min-height: 100vh;`

## Advanced Grid Patterns

For advanced layouts, apply techniques from [grid-techniques.md](grid-techniques.md) — 10 non-standard grid systems with CSS examples, each with rationale and best-use scenarios.

Summary of available techniques:

1. **Golden Ratio** — page divided by φ=1.618, recursive proportions. Portfolios, editorial.
2. **Fibonacci Sequence** — spacing/sizing scale based on 3-5-8-13-21-34. Design systems, type scales.
3. **Broken Grid** — strict grid with 1-2 intentional violations. Creative, fashion, agencies.
4. **Van de Graaf** — medieval book margins (1:1.5:2:3), text block = 4/9 page. Long-form, book-style.
5. **Ratio Grid** — aspect-ratio based cards (16:9, 4:3, 1:1, 3:4). Galleries, media sites.
6. **Optical Margin Alignment** — visual corrections beyond mathematical alignment. Typography, icons.
7. **Diagonal Layout** — diagonal section boundaries via clip-path. Tech startups, sports.
8. **Typographic Grid** — all dimensions derived from line-height. Content sites, publishing.
9. **Bento Grid** — asymmetric multi-size blocks (Apple-style). Product features, SaaS.
10. **Swiss Grid** — strict 12-column grid with color fields. Branding, cultural institutions.

## Responsive Behavior

When page needs responsiveness:

```css
/* Mobile-first base */
.layout { display: flex; flex-direction: column; }

/* Desktop */
@media (min-width: 768px) {
  .layout { display: grid; grid-template-columns: 240px 1fr; }
}
```

Sidebar collapses to top nav on mobile. Grid goes to single column. Split screen stacks vertically.

## Placeholder Content

When real content not provided, use realistic placeholders:

- **Names**: Alex Johnson, Maria Chen, David Kim (diverse, realistic)
- **Text**: Short meaningful sentences, not lorem ipsum
- **Images**: Colored rectangles with labels (`<div style="background: var(--color-neutral-200); aspect-ratio: 16/9; display: grid; place-items: center; color: var(--color-text-secondary);">Product Image</div>`)
- **Numbers**: Realistic ranges ($29.99, 4.8 stars, 1,234 users)
- **Dates**: Relative to current date

## HTML Generation

Structure of generated page file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{Page Name} — Preview</title>
  <style>
    /* Reset */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    /* Tokens (from tokens.json) */
    :root { /* ... */ }

    /* Component styles (from used components) */
    /* ... */

    /* Page layout */
    /* ... */
  </style>
</head>
<body>
  <!-- Page content assembled from components -->
</body>
</html>
```

Include only styles for components actually used on the page.

## SVG Generation

Convert the HTML layout to SVG:

1. Set SVG viewBox to page dimensions (1440x900 for desktop, 390x844 for mobile)
2. Convert layout to absolute-positioned rectangles
3. Use `<text>` for all text content with proper font attributes
4. Use `<rect>` for backgrounds, cards, buttons
5. Use `<line>` or `<rect>` for borders and dividers
6. Embed colors directly (no CSS variables in SVG)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900">
  <!-- Background -->
  <rect width="1440" height="900" fill="#ffffff"/>

  <!-- Header -->
  <rect x="0" y="0" width="1440" height="64" fill="#f9fafb"/>
  <text x="24" y="40" font-family="Inter" font-size="20" font-weight="600" fill="#111827">Logo</text>

  <!-- Content -->
  <!-- ... -->
</svg>
```

## Device Frames

When user asks "show how it looks on phone/tablet":

- **Mobile**: 390x844 viewport, render in phone frame
- **Tablet**: 768x1024 viewport
- **Desktop**: 1440x900 viewport

Generate separate files: `{name}-mobile.html`, `{name}-desktop.html`.

## Iterating on Designs

After presenting the initial result:
- "Bigger" / "smaller" — adjust spacing and font sizes
- "More contrast" — darken text, increase color differences
- "Simpler" — reduce components, whitespace up
- "More detail" — add secondary info, icons, metadata
- Apply change → regenerate both HTML and SVG
