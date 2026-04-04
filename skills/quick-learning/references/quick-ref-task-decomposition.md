# Quick Reference — Task Decomposition

1. Wave ordering — последовательные задачи внутри одной "названной волны": если задачи зависят друг от друга (A→B→C) — каждая получает своё число wave; проверять wave(B) > wave(A) для каждой пары зависимостей (Seen: 3)
2. Verify all cross-references after task generation: file paths через `test -e`, decision numbers по счёту в tech-spec, depends_on по факту что dependency производит нужный артефакт (Seen: 2)
3. Тест на стыке задач — добавить явно в spec/AC: если при выполнении Task N обнаруживается тест из scope Task M — добавить его явно в AC или TDD Anchor задачи M (Seen: 2)
4. Wave поля Audit/Final Wave — числа, не метки: если имплементационных волн N — audit = N+1, final = N+2; строки "audit"/"final" не проходят frontmatter schema-validation (Seen: 2)
5. String-output assertions — ограничивай scope: для тестов структурированного string-output извлекай нужную секцию (regex/split), затем проверяй значение внутри неё (Seen: 2)
6. Scope задач разных волн для одного файла: если задача A создаёт файл а задача B расширяет — явно ограничить scope A, в бриф B включить "файл уже существует с X, Y. Добавить только Z" (Seen: 2)
7. Когда задача меняет обязательный параметр публичной функции — явно указать новую сигнатуру в брифе downstream задачи, чтобы избежать молчаливого TypeError из gap между задачами (Seen: 1)
