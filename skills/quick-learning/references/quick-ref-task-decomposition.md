# Quick Reference — Task Decomposition

1. Wave numbers, not labels — передавать task-creator явные числа; для каждой пары depends_on проверять wave(consumer) > wave(producer) (Seen: 3)
2. Constraint-enforcement scope — извлекай enforcing-регион (restricting/predicate-часть), ищи токен только там; токен в output/labels/metadata не засчитывается (Seen: 3)
3. Verify all cross-references after task generation — file paths via `test -e`, decision numbers, depends_on artifacts (Seen: 2)
4. Тест на стыке задач — добавить явно в AC/TDD задачи-владельца; decisions.md соседние агенты не читают (Seen: 2)
5. Scope задач разных волн для одного файла — явно ограничить scope A; в бриф B: "файл уже есть с X, Y. Добавить только Z." (Seen: 2)
6. CI/CD AC — явно включать concurrency/idempotency guards (cancel-in-progress, дубли запусков) в AC (Seen: 1)
7. Markdown-only фичи — формулировать AC через наличие структурных артефактов (секции, ссылки, guard-блоки), не keywords (Seen: 1)
8. Inter-task dependency — заменять чтением из shared source of truth, чтобы сохранить параллелизм волны без read-after-write (Seen: 1)
9. Deletion task — добавить AC на dead variables, stale comments, дубли тестов до ревью (Seen: 1)
10. Capacity-capped buckets — определить overflow policy до реализации, чтобы не терять записи при переполнении (Seen: 1)
