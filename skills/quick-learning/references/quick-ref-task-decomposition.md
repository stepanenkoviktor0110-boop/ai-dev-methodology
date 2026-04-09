# Quick Reference — Task Decomposition

1. Scope задач разных волн для одного файла: "только X" в ранней, "добавить Y" в поздней (Seen: 3)
2. Wave ordering: wave(B) > wave(A) для каждой пары зависимостей (Seen: 3)
3. Verify all cross-references: file paths через `test -e`, depends_on — подтверждать артефакт (Seen: 2)
4. Тест на стыке задач — добавить явно в spec/AC задачи-владельца (Seen: 2)
5. Wave поля — числа, не метки: "audit"/"final" не проходят schema-validation (Seen: 2)
6. String-output assertions — ограничивай scope: regex/split → значение внутри секции (Seen: 2)
7. No-op stubs — явно добавить шаг "замени stub на реализацию" в каждый бриф (Seen: 2)
8. Две задачи описывают поведение для одного edge case → cross-check описаний на консистентность до коммита (Seen: 1)
9. AC для markdown-only фич: через наличие конкретных артефактов, не описаний (Seen: 1)
10. Client state (useState) в server component → явно предписать client wrapper pattern, запретить "use client" на layout (Seen: 1)
