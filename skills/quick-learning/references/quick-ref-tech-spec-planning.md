# Quick Reference — Tech Spec Planning

1. При интеграции с внешним API — перенести в спек ВСЕ коды ответа, формат данных и edge cases; live API call для проверки (Seen: 3)
2. Верифицировать values/methods против реальной документации — не принимать на веру память (Seen: 3)
3. Файловые пути через ls/glob + grep по имени функции перед записью call sites в Files to modify (Seen: 3)
4. Запуск task-creator агентов → проверить runner (jest/vitest/pytest) и тест-директории, передать явно (Seen: 3)
5. Верифицируй целевые файлы перед описанием операции: grep по каждому файлу перед фиксацией типа (Seen: 2)
6. Требования к формату поступают итеративно → согласовать полную структуру до кода (Seen: 2)
7. AC checklist: перед написанием Solution пройти все AC user-spec, отметить каждый в черновике (Seen: 1)
8. Security checklist для публичного POST: CSRF/Origin, sanitization, IP source, rate-limit, headers (Seen: 1)
9. Compatibility constraint в брифе → явно указать разрешённые API с примером из кода (Seen: 1)
10. Агрегация по колонке из ALTER TABLE → проверить заполненность исторических строк (Seen: 1)
