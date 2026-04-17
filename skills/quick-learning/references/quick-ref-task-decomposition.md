# Quick Reference — Task Decomposition

1. Wave ordering: wave(B) > wave(A) для каждой пары зависимостей; sequential tasks inside a named wave get their own numbers (A=N, B=N+1, C=N+2) (Seen: 3)
2. Scope задач разных волн для одного файла: явно ограничить scope A ("только X"), в бриф B включить "файл уже существует с X, Y. Добавить только Z." (Seen: 2)
3. Verify all cross-references after task generation: file paths via `test -e`, decision numbers by counting in tech-spec, depends_on by confirming dependency produces referenced artifact (Seen: 2)
4. Тест на стыке задач — добавить явно в spec/AC задачи-владельца; decisions.md агент не читает (Seen: 2)
5. Wave поля Audit/Final Wave — числа, не метки: audit = N+1, final = N+2; строки "audit"/"final" не проходят frontmatter schema-validation (Seen: 2)
6. String-output assertions — ограничивай scope: извлекай нужную секцию (regex/split), затем проверяй значение внутри неё (Seen: 2)
7. No-op stubs — явно добавить шаг "замени stub на реализацию" в каждый зависимый бриф (Seen: 2)
8. Mass-generating tasks from template for the first time — generate 1 pilot task, validate, then scale to avoid 30+ fixes on first run (Seen: 1)
9. CI/CD pipeline tasks — explicitly include concurrency/idempotency guards (cancel-in-progress, prevent duplicate runs) in AC (Seen: 1)
10. Inter-task dependency on another task's result — replace with reading from shared source of truth to preserve wave parallelism without read-after-write risks (Seen: 1)
