# Quick Reference — Code Writing

1. Маскировка секретов в команде (`sed`, `grep -c`) — никогда не выводить .env целиком (Seen: 2)
2. Assertions на output-формат, не на input-атрибуты (Seen: 2)
3. Валидация файловых путей из внешних данных — против allowlist (Seen: 2)
4. Finally-блок с except Exception — использовать BaseException как trigger (Seen: 2)
5. Дорогостоящая инициализация в цикле — вынести init за цикл (Seen: 2)
6. Задача требует написания кода → написать sketch.md и делегировать Codex ДО начала писать вручную (Seen: 1)
7. JS in-memory state + POST мутирует один элемент → обновить state синхронно после успешного POST (Seen: 1)
8. Batch endpoint → "skip unknowns, return known" вместо 400 на весь batch (Seen: 1)
9. Одноимённая колонка в двух таблицах как JOIN-ключ → проверить семантику до объединения (Seen: 1)
10. Overflow-x-auto + sticky колонка → не ставить div между scroll-контейнером и table (Safari) (Seen: 1)
