# Quick Reference — Task Decomposition

Top patterns relevant to task-decomposition. Max 10 entries, sorted by Seen (highest first).

<!-- Auto-generated from reasoning-patterns.md. Regenerated on each write/promotion by quick-learning. -->

1. **Проверяй пути в сгенерированных задачах** (Seen: 1) — После генерации задач проверяй каждый путь к файлу через `test -e`. Валидируй depends_on: зависимость должна создавать артефакт, который зависимая задача читает.
2. **Тест на стыке задач — добавить явно в spec/AC** (Seen: 2) — Если при выполнении Task N найден тест для Task M — добавить явно в AC/TDD Anchor задачи M. Записи в decisions.md недостаточно: агент M не читает decisions предыдущих задач.
3. **Заменяй межзадачную зависимость на общий source of truth** (Seen: 1) — При декомпозиции на параллельные задачи — если задача читает результат другой в той же волне, заменить зависимость на чтение общего документа. depends_on + same wave = гонка данных.
4. **Wave поля Audit/Final Wave — числа, не метки** (Seen: 2) — Если имплементационных волн N — audit = N+1, final = N+2. Передавать task-creator числа явно. Строки "audit"/"final" не проходят frontmatter schema-validation.
5. **String-output assertions — ограничивай scope** (Seen: 2) — Для тестов markdown/отчётов: assertion на наличие недостаточно — извлекай нужную секцию (regex/split), затем проверяй внутри неё.
6. **Scope задач разных волн для одного файла** (Seen: 2) — Если задача A создаёт файл, задача B его расширяет — ограничить scope A нуждами её волны; в бриф B явно написать "файл уже существует с X, добавить Y".
7. **Wave ordering: последовательные задачи внутри одной "названной волны"** (Seen: 2) — "Final Wave" — семантическая метка, не число. Если задачи A→B→C зависят друг от друга — назначить A=N, B=N+1, C=N+2. Проверять: wave(задача) > max(wave(depends_on)).
8. **Именованные экспорты для cross-wave тестов** (Seen: 1) — Если Task B тестирует функции из файла Task A — добавить сигнатуры в What to do Task A. Функция без объявленного владельца рискует быть пропущена.
