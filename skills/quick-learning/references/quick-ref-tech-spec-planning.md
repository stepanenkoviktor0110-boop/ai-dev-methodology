# Quick Reference — Tech-Spec Planning

1. Верифицируй API response shapes live-вызовом: при интеграции с внешним API — перенести в спек ВСЕ коды ответа, формат данных, edge cases; live call до включения response shapes из code-research (Seen: 2)
2. Верифицируй целевые файлы перед описанием операции: grep по каждому файлу перед фиксацией типа операции (add vs replace) — файл без X требует add, не replace (Seen: 2)
3. Верифицируй файловые пути через ls/glob: перед записью путей в tech-spec — проверить через ls/glob, не из памяти или architecture docs; grep по имени функции перед записью call sites в Files to modify (Seen: 2)
4. When spec narrows a criterion from user-spec (A or B → only A): add to Technical Decisions "decided NOT to include B, because…" to avoid extra validation rounds (Seen: 1)
5. When completing Implementation Tasks: check for Files-to-modify overlap within each wave to prevent merge conflicts during parallel execution (Seen: 1)
6. When a stakeholder names a specific technical component as a requirement: verify it against current project documentation before fixing it in the spec, to avoid accepting statements as truth without verification (Seen: 1)
7. When moving a task from one execution environment to another: enumerate all implicit environment dependencies (env vars, filesystem, network, runtime, auth model) before migrating (Seen: 1)
8. When assigning a value to a named configuration field: trace how the consuming system actually reads and uses that value, to avoid conflating the field label with the machine contract (Seen: 1)
9. When an external document names positional attributes for an existing data structure: verify actual positions in code before accepting them into the spec (Seen: 1)
10. When spec defines narrower access on an endpoint where an existing guard allows broader roles: explicitly describe creation of a new guard in the task to prevent auth gaps discovered only at security audit (Seen: 1)
