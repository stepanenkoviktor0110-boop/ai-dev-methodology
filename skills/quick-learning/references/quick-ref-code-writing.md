# Quick Reference — Code Writing

1. Передача файла на удалённый хост через SSH — stdin pipe вместо heredoc, unbuffered output флаг (Seen: 3)
2. Маскировка секретов в команде (`sed`, `grep -c`) — никогда не выводить .env целиком (Seen: 2)
3. Assertions на output-формат, не на input-атрибуты (Seen: 2)
4. Валидация файловых путей из внешних данных — против allowlist (Seen: 2)
5. Finally-блок с except Exception — использовать BaseException как trigger (Seen: 2)
6. Дорогостоящая инициализация в цикле — вынести init за цикл (Seen: 2)
7. Unit-тесты с моками — провести минимум 1 live smoke-прогон перед QA passed (Seen: 2)
8. Задача требует повторного чтения файла, файл не менялся → читать один раз в начале (Seen: 2)
9. Делегирование write-задачи sandboxed-инструменту → проверить write permissions тестовой операцией до промта (Seen: 2)
10. Генерация конфига с enum-полями → проверить допустимые значения из схемы/docs (Seen: 2)
