# Quick Reference — Task Decomposition

Top patterns relevant to task-decomposition. Max 10 entries, sorted by Seen (highest first).

<!-- Auto-generated from reasoning-patterns.md. Regenerated on each write/promotion by quick-learning. -->

1. **Проверяй пути в сгенерированных задачах** (Seen: 1) — После генерации задач проверяй каждый путь к файлу через `test -e`. Валидируй depends_on: зависимость должна создавать артефакт, который зависимая задача читает.
2. **Заменяй межзадачную зависимость на общий source of truth** (Seen: 1) — При декомпозиции на параллельные задачи — если задача читает результат другой в той же волне, заменить зависимость на чтение общего документа. depends_on + same wave = гонка данных.
3. **Wave поля Audit/Final Wave — числа, не метки** (Seen: 2) — Если имплементационных волн N — audit = N+1, final = N+2. Передавать task-creator числа явно. Строки "audit"/"final" не проходят frontmatter schema-validation.
