# Component Patterns

## Component File Structure

Each `.design-system/components/{name}.html` is a self-contained showcase:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{ComponentName} — Design System</title>
  <style>
    /* 1. Import tokens as CSS custom properties */
    :root { /* ... generated from tokens.json ... */ }

    /* 2. Component styles */
    .btn { /* ... */ }
    .btn--primary { /* ... */ }
    .btn--sm { /* ... */ }

    /* 3. Showcase layout (not part of the component) */
    .showcase { padding: 32px; font-family: var(--font-body); }
    .showcase__section { margin-bottom: 24px; }
    .showcase__label { font-size: 12px; color: var(--color-text-secondary); margin-bottom: 8px; }
    .showcase__row { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
  </style>
</head>
<body>
  <div class="showcase">
    <h1>{ComponentName}</h1>

    <div class="showcase__section">
      <div class="showcase__label">Variants</div>
      <div class="showcase__row">
        <!-- All variants shown here -->
      </div>
    </div>

    <div class="showcase__section">
      <div class="showcase__label">Sizes</div>
      <div class="showcase__row">
        <!-- All sizes shown here -->
      </div>
    </div>
  </div>
</body>
</html>
```

## Core Components

### Button
Variants: primary, secondary, outline, ghost, destructive
Sizes: sm, md, lg
States: default, hover, disabled

```css
.btn {
  display: inline-flex; align-items: center; justify-content: center;
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-weight: var(--font-weight-medium);
  cursor: pointer; border: 1px solid transparent;
  transition: background 0.15s, border-color 0.15s;
}
.btn--sm { padding: var(--space-1) var(--space-3); font-size: var(--font-size-sm); }
.btn--md { padding: var(--space-2) var(--space-4); font-size: var(--font-size-base); }
.btn--lg { padding: var(--space-3) var(--space-6); font-size: var(--font-size-lg); }
.btn--primary { background: var(--color-primary-500); color: var(--color-text-inverse); }
.btn--secondary { background: var(--color-neutral-100); color: var(--color-text-primary); }
.btn--outline { border-color: var(--color-neutral-300); color: var(--color-text-primary); background: transparent; }
.btn--ghost { background: transparent; color: var(--color-text-primary); }
.btn--destructive { background: var(--color-semantic-error); color: var(--color-text-inverse); }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }
```

### Input
Variants: default, error, disabled
Sizes: sm, md, lg
Extras: with label, with helper text, with icon

### Card
Variants: default, elevated, outlined
Slots: header, body, footer, media (image top)

### Badge
Variants: primary, secondary, success, warning, error
Sizes: sm, md

### Alert
Variants: info, success, warning, error
Slots: icon, title, description, action

### Avatar
Variants: image, initials, fallback
Sizes: sm, md, lg, xl
Shape: circle, rounded

### Navigation (Nav)
Variants: horizontal, vertical, tabs
Items: with icon, active state, disabled

### Table
Features: header, rows, striped, hoverable
Slots: cell content, actions column

## Creating New Components

When user requests a component not in the core list:

1. Identify the closest core component pattern
2. Define variants based on use cases
3. Define sizes if applicable
4. Define states (default, hover, active, disabled, error)
5. Use design tokens for all visual properties
6. Include all variants in the showcase file

## Variant System

Use BEM-like class naming:
- Block: `.component`
- Variant: `.component--variant`
- Size: `.component--size`
- State: `.component--state` or `:disabled`, `:hover`
- Child: `.component__child`

Example: `.card`, `.card--elevated`, `.card--sm`, `.card__header`, `.card__body`

## Slot Pattern

Components with variable content use semantic sections:

```html
<div class="card">
  <div class="card__media"><!-- image, video, or empty --></div>
  <div class="card__header"><!-- title + subtitle --></div>
  <div class="card__body"><!-- main content --></div>
  <div class="card__footer"><!-- actions --></div>
</div>
```

Slots can be omitted — component renders correctly without optional slots.
