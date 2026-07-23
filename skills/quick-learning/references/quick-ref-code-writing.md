# Quick Reference — Code Writing

1. Mask secrets BEFORE executing a command — embed sed-masking or grep -c instead of printing .env. (Seen: 2)
2. Assertions on output format, not input attributes — for format-conversion functions read a real output example before writing the test. (Seen: 2)
3. Building a file path from any external value — validate each value against an allowlist before use. (Seen: 2)
4. Extract magic numbers to named constants before first review, to avoid a predictable hardcoded-value finding. (Seen: 1)
5. Unit tests with mocks for an external process/API — run at least 1 live smoke pass before declaring QA passed. (Seen: 1)
6. HTTP API-key auth — include timing-safe comparison and an explicit body size limit in the initial implementation. (Seen: 1)
7. Operation with multiple auth levels — test with the least-privileged real user first, so a 500 for the primary consumer surfaces early (triad #428). (Seen: 1)
8. When a dispatcher's fall-through default IS the primary consequential action — invert it: require an affirmative positive match, route unrecognized input to a safe handler (triad #442). (Seen: 1)
9. Set the idempotency sentinel BEFORE the mutation (optimistic lock), not after, to close the duplicate-mutation race window (triad #436). (Seen: 1)
10. Emit downstream commands in the host's actual shell syntax — do not propagate the upstream-spec's Unix dialect verbatim (triad #461). (Seen: 1)

## Visual/Layout QA (перед сдачей UI — проверять РЕНДЕР замером, не глазами)

A. **Равные высоты.** Соседние блоки/карточки/ячейки/nav-пункты в одной зоне — одной высоты. Многострочный контент (перенос заголовка, RU длиннее EN) РЕЗЕРВИРУЕТ место: `min-height` под N строк (+`line-clamp`), чтобы 1-строчный == 2-строчный. Done: все `getBoundingClientRect().height` равны.
B. **Равные ширины.** Кнопки/бейджи/инпуты в одной колонке/группе — одной ширины (по самому широкому): `min-width`+`box-sizing`+`text-align:center`. Проверять ВСЕ ветки статусов (pending/approved/rejected дают разный набор кнопок). Done: один `width`.
C. **Один ряд.** Однотипные элементы в РАЗНЫХ соседних контейнерах/таблицах — выровнять по общей кромке; если ширина колонок разная — `text-align:right` к общему правому краю. Done: один `.right` у всех.
D. **Никаких стыков.** Контейнер с >1 интерактивным/визуальным потомком → `flex`+`gap`. Никогда встык: кнопки, инпут+кнопка, формы подряд, бейдж у текста.
E. **Шрифт под язык + оптический размер.** Латинский дисплей-шрифт может НЕ иметь кириллицы — нужен компаньон `@font-face`+`unicode-range U+0400-04FF` (иначе кириллица молча падает в serif-фолбэк типа Georgia). Пример PASYAKIN: Luxerie→Tenor Sans, Maven Pro→Manrope (см. `app/assets/stylesheets/tailwind.css`). Для self-contained HTML компаньон встроить тоже (base64). **Мало подключить — компаньон должен быть ОПТИЧЕСКИ РАВЕН основному:** замерить cap-height (заголовки) / x-height (body) обоих при одном font-size; если расходятся — `size-adjust:<%>` на @font-face компаньона (PASYAKIN: Tenor Sans cap-height 133 vs Luxerie 111 → `size-adjust:83%`). Иначе RU-текст рядом с EN выглядит крупнее/мельче. Done: cap-height/x-height совпадают замером.
F. **Цифры в дисплей-шрифте.** Некоторые дисплей-шрифты не содержат глифов цифр (PASYAKIN: Luxerie — цифры невидимы). Любой числовой контент (счётчики, индексы, даты, года, статистика) — текстовым шрифтом (Maven Pro). Симптом «пропали цифры/пустая сетка» → первый подозреваемый.
G. **Ширина съёмки/верстки фикс-канваса.** Фикс-ширинный макет (напр. Figma-канвас 1440) смотреть/снимать при ширине ≥ канваса — иначе horizontal overflow + всплывает оверлей-слой (серая полоса) и режется контент.

Done = каждый пункт подтверждён замером на реальном рендере (Playwright `getBoundingClientRect`), а не на глаз.
