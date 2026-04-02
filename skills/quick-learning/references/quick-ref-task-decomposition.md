# Quick Reference — Task Decomposition

1. **Check file paths via `test -e`, decision numbers by counting in tech-spec, depends_on by confirming the dependency actually produces the referenced artifact. Agents generate references by analogy/assumption, not by verification.** — Тест на стыке задач — добавить явно в spec/AC (Seen: 2) (Seen: 2)
2. **Если при выполнении Task N обнаруживается тест, относящийся к scope Task M — добавить его явно в AC или TDD Anchor задачи M. Записи в decisions.md недостаточно: агент Task M decisions.md предыдущих задач не читает.** — Wave поля Audit/Final Wave — числа, не метки (Seen: 2) (Seen: 2)
3. **Если имплементационных волн N — audit = N+1, final = N+2. Передавать task-creator числа явно. Строки "audit"/"final" не проходят frontmatter schema-validation.** — String-output assertions — ограничивай scope (Seen: 2) (Seen: 2)
4. **Для тестов структурированного string-output (markdown, отчёты) недостаточно проверять наличие значения — добавь assertion на scope: извлекай нужную секцию (regex/split), затем проверяй значение внутри неё. Это отличает "значение есть" от "значение в нужном месте".** — Scope задач разных волн для одного файла (Seen: 2) (Seen: 2)
5. **Если задача A создаёт файл а задача B в позднейшей волне его расширяет — явно ограничить scope A ("только save/load — нужны в wave 1"), и в бриф B включить: "файл уже существует с функциями X, Y. Добавить только Z." Параллельные task-creator'ы не общаются — scope должен быть однозначен в каждом брифе.** — Wave ordering: последовательные задачи внутри одной "названной волны" (Seen: 2) (Seen: 2)
6. When writing AC for CI/CD pipeline tasks (Seen: 1)
7. When writing AC for markdown-only features (Seen: 1)
8. When a task in a wave references another task result (Seen: 1)
9. When creating a deletion task (remove feature/constant/field) (Seen: 1)
10. When designing algorithms that distribute records into capacity-capped buckets - (Seen: 1)
