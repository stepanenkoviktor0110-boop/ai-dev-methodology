# Before/After Collage Workflow

> Triggered when the user confirms the final variant ("да", "этот", "утверждаю", "go", "approved").

## Capture "Before"

- If replacing an existing page → take a screenshot of the current version (or ask user to paste one)
- If designing from scratch → use a solid `var(--color-neutral-200)` rectangle with centered text "No previous design"

## Build collage

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

## Save

1. Validate name: `/^[a-z0-9-]+$/`
2. Save to `.design-system/collages/{page-name}-collage.html`
3. Tell the user: "Collage saved to `.design-system/collages/{page-name}-collage.html` — open in browser to see the diagonal before/after comparison."

## Cleanup

After the collage is saved, delete intermediate artifacts:

1. Remove all iteration SVGs: `.design-system/pages/{name}.svg`, `{name}-mobile.svg`, etc.
2. Remove intermediate HTML previews if the final version has been applied to the actual codebase
3. Keep only:
   - `.design-system/collages/{page-name}-collage.html` (before/after comparison)
   - `.design-system/pages/{name}.html` (final approved version — as reference)
4. Ask the user: "Промежуточные файлы (SVG, черновики) удалены. Оставлен финальный HTML и коллаж до/после. Ок?"
