# Quick Reference — Reasoning Patterns

Top universal patterns promoted from session analysis. Loaded at session start.

<!-- Auto-generated. Max 7 entries. Regenerated on each universal pattern promotion. -->

1. **Build после каждой волны** — unit-тесты не ловят server/client boundary violations, callback type mismatches, runtime-only import errors. Только production build ловит.
2. **Live call до включения API shapes в спек** — code-research может содержать неточный формат (JSON вместо XML, другая структура). Один реальный вызов дешевле propagation миража через весь pipeline.
