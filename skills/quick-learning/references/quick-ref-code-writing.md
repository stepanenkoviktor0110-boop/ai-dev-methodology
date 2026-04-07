# Quick Reference — Code Writing

1. Маскировка секретов в команде (`sed`, `grep -c`) — никогда не выводить .env целиком (Seen: 2)
2. Assertions на output-формат, не на input-атрибуты — иначе тест не ловит баги конвертации (Seen: 2)
3. Валидация файловых путей из внешних данных — против allowlist (Seen: 2)
4. Finally-блок с except Exception — использовать BaseException как trigger (Seen: 2)
5. Дорогостоящая инициализация в цикле — вынести init за цикл (Seen: 2)
6. Overflow-x-auto + sticky колонка → не ставить div между scroll-контейнером и table (Safari) (Seen: 1)
7. Делегирование AI-агенту → "пиши файлы по одному, не все разом" (Seen: 1)
8. d3 `.each()` на React SVG → lookup по data-* атрибутам вместо bound data (Seen: 1)
9. Write-задача sandboxed-инструменту → проверить permissions тестовой операцией до промта (Seen: 1)
10. VPS нужен публичный URL → проверить outbound connectivity (HTTPS? SSH?) перед выбором tunnel (Seen: 1)
