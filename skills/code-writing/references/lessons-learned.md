# Lessons Learned: code-writing

### 2026-03-26 shift-confirmation: Build не запущен после изменения сигнатуры callback

**Problem:** Изменение сигнатуры `applyFilters()` (добавлен optional параметр) сломало production build — функция использовалась как `onClick` handler, TypeScript не принял `MouseEvent` как `"list" | "grid"`.
**Cause:** Vitest не проверяет JSX type compatibility — только `npm run build` ловит такие ошибки. Агент запустил vitest (все тесты прошли), но не запустил build.
**Solution:** Обернул вызов в arrow function `() => applyFilters()`, запустил build, передеплоил.
**Rule:** После изменения сигнатуры функции, которая используется как event handler или callback — ОБЯЗАТЕЛЬНО запустить `npm run build` до коммита. Vitest не проверяет JSX-совместимость типов.
