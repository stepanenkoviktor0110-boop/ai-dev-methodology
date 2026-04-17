# Stack Research Registry

Registry of researched stack elements for this project. Each entry is the latest state of an element as of its `checked` date. Used by `stack-research` skill as a cache (version match → skip re-research).

**Maintained by:** `stack-research` skill (automated).
**Scope:** Only elements researched with `depth=deep`. Shallow comparisons are NOT persisted here — they live in `stack-comparison-*.md` files.

---

## Template for each entry

```markdown
## {element-name}

- **Type:** external-api | library | service | tool
- **Version:** {version or pseudo-version, e.g. "changelog 2026-03-12"}
- **Checked:** {YYYY-MM-DD}
- **Source:** {URL or list of URLs}
- **Auth:** {one line or N/A}
- **Pricing:** {one line or "free"}
- **Principal limits:**
  - {limit 1}
  - {limit 2}
- **Gotchas:**
  - {gotcha with source ref}
- **Breaking changes (last 12 months):**
  - {date} — {change}
- **Focus answers (accumulated across projects):**
  - Q: {question} — A: {answer} (checked {date})
  - Q: {question} — A: {answer} (checked {date})
- **Not answered:**
  - {focus question official docs don't cover}
```

---

## Entries

<!-- Entries appended/replaced by stack-research skill. Keep alphabetical by element-name. -->
