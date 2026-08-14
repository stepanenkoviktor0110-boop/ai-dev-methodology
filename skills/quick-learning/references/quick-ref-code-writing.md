# Quick Reference — Code Writing

1. Unit tests mock an external process/API — run at least 1 live smoke pass before declaring QA passed. (Seen: 4)
2. Delegating to an agent/tool with unknown limits — probe capability (write permissions, resources) with a test operation before the full prompt. (Seen: 3)
3. File transfer to a remote host over a complex SSH command drops the connection — pass the file as an stdin pipe instead of heredoc/SCP. (Seen: 3)
4. Mask secrets BEFORE the command runs — embed sed-masking or `grep -c` instead of printing `.env` whole. (Seen: 2)
5. Assert on the output format, not on input attributes — read a real output sample before writing assertions for a format-conversion function. (Seen: 2)
6. Building a file path from any external value — validate each value against an allowlist first. (Seen: 2)
7. A subprocess must outlive the current agent turn — spawn it at OS level (detached, output to file), not as an agent-managed background task. (Seen: 2)
8. "No references found" used as a precondition for an irreversible action — first search for a case known to match and confirm it is found. (Seen: 2)
9. Adding error handling to a reusable component — separate transient (propagate) from permanent (mark failed); do not swallow both through a generic `Exception`. (Seen: 2)
10. A resource is reachable by several paths (external and internal, sync test path vs async prod path) — enumerate every path and verify each independently. (Seen: 2)

## Visual/Layout QA (перед сдачей UI — проверять РЕНДЕР замером, не глазами)

A. **Равные высоты.** Соседние блоки/карточки/ячейки/nav-пункты в одной зоне — одной высоты. Многострочный контент (перенос заголовка, RU длиннее EN) РЕЗЕРВИРУЕТ место: `min-height` под N строк (+`line-clamp`), чтобы 1-строчный == 2-строчный. Done: все `getBoundingClientRect().height` равны.
B. **Равные ширины.** Кнопки/бейджи/инпуты в одной колонке/группе — одной ширины (по самому широкому): `min-width`+`box-sizing`+`text-align:center`. Проверять ВСЕ ветки статусов (pending/approved/rejected дают разный набор кнопок). Done: один `width`.
C. **Один ряд.** Однотипные элементы в РАЗНЫХ соседних контейнерах/таблицах — выровнять по общей кромке; если ширина колонок разная — `text-align:right` к общему правому краю. Done: один `.right` у всех.
D. **Никаких стыков.** Контейнер с >1 интерактивным/визуальным потомком → `flex`+`gap`. Никогда встык: кнопки, инпут+кнопка, формы подряд, бейдж у текста.
E. **Шрифт под язык + оптический размер.** Латинский дисплей-шрифт может НЕ иметь кириллицы — нужен компаньон `@font-face`+`unicode-range U+0400-04FF` (иначе кириллица молча падает в serif-фолбэк типа Georgia). Пример PASYAKIN: Luxerie→Tenor Sans, Maven Pro→Manrope (см. `app/assets/stylesheets/tailwind.css`). Для self-contained HTML компаньон встроить тоже (base64). **Мало подключить — компаньон должен быть ОПТИЧЕСКИ РАВЕН основному:** замерить cap-height (заголовки) / x-height (body) обоих при одном font-size; если расходятся — `size-adjust:<%>` на @font-face компаньона (PASYAKIN: Tenor Sans cap-height 133 vs Luxerie 111 → `size-adjust:83%`). Иначе RU-текст рядом с EN выглядит крупнее/мельче. Done: cap-height/x-height совпадают замером.
F. **Цифры в дисплей-шрифте.** Некоторые дисплей-шрифты не содержат глифов цифр (PASYAKIN: Luxerie — цифры невидимы). Любой числовой контент (счётчики, индексы, даты, года, статистика) — текстовым шрифтом (Maven Pro). Симптом «пропали цифры/пустая сетка» → первый подозреваемый.
G. **Ширина съёмки/верстки фикс-канваса.** Фикс-ширинный макет (напр. Figma-канвас 1440) смотреть/снимать при ширине ≥ канваса — иначе horizontal overflow + всплывает оверлей-слой (серая полоса) и режется контент.

Done = каждый пункт подтверждён замером на реальном рендере (Playwright `getBoundingClientRect`), а не на глаз.
