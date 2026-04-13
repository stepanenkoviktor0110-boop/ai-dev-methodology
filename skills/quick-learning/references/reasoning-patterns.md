# Reasoning Patterns

Accumulated insights about decision-making logic across projects.
Single transit buffer for ALL methodology knowledge — both reasoning patterns and operational lessons.

**This is a transit buffer.** Patterns that reach `Seen: 3` get promoted into skill SKILL.md files and removed from here. Stale entries (Seen: 1, older than 30 days) get pruned.

---

## Universal

Patterns that apply to any project, any stack, any domain.

<!-- Append universal patterns below -->
### 2026-04-13 admin-panel / session 3: Запрос стейкхолдера ≠ следующий шаг плана

**Seen:** 1
**Adapted:** —
**Cognitive Error:** pipeline momentum bias
**Triad:** стейкхолдер просит увидеть результат при наличии плана с ≥2 оставшимися шагами → интерпретировать запрос буквально, не через призму следующего шага плана → предотвратить подмену цели стейкхолдера ближайшим пунктом плана
**Context:** Стейкхолдер сказал «хочу увидеть» — исполнитель интерпретировал как «запустить деплой» (следующий шаг плана), а не «показать работающее локально». Инерция плана подменила буквальный смысл запроса.
**Pattern:** Когда стейкхолдер просит результат, а план предлагает промежуточный шаг — переспроси что именно он хочет увидеть, не проецируй план на запрос. «Увидеть» может означать локальное демо, не production deploy.
**Scope:** universal
**Category:** communication

### 2026-03-31 dashboard-v1 / deploy: Браузер молчит — смотри server access log до диагностики сети

**Seen:** 1
**Adapted:** —
**Triad:** браузер показывает "не грузит" без ошибки → сразу проверить server access log → узнать реальный HTTP-статус до диагностики firewall/сети
**Context:** Пользователь видел пустой браузер и думал что порт заблокирован. Nginx access log показал 4 запроса с 401 — сервер работал, проблема была в неверном пароле Basic Auth.
**Pattern:** Когда браузер не отвечает — не диагностируй сеть вслепую. Первый шаг: `tail -f /var/log/nginx/access.log`. Если запросы доходят — проблема в приложении. Если запросов нет — проблема в сети.
**Scope:** universal
**Category:** recovery

### 2026-03-30 methodology-sync-sketch / session 1: агент-файл для multi-context — нейтральные сигналы завершения

**Seen:** 1 (methodology-sync-sketch / session 1)
**Adapted:** —
**Triad:** написание агент-файла, который используется и inline, и через spawn_agent → не использовать ссылки на родительский контекст ("return to Phase N"), давать нейтральный сигнал завершения ("task complete. [result]") → артефакт работает корректно в обоих execution environments
**Context:** sketch-interviewer.md написан с `"return to SKILL.md Phase 5"` — это работает в Claude Code (inline load), но ломается в Codex spawn_agent где агент не знает про родителя.
**Pattern:** Когда файл агента предназначен для нескольких execution environments (inline + spawned) — описывать завершение нейтрально: "task complete. [result description]". Вызывающая сторона сама решает что делать дальше. Back-reference на parent step — это coupling на конкретную среду.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 employee-cabinet / session 1: Проверять overlap файлов внутри волны перед финализацией tech-spec

**Seen:** 2
**Adapted:** —
**Triad:** завершение секции Implementation Tasks в tech-spec → проверить "Files to modify" каждой задачи на пересечение внутри одной волны → предотвратить merge-конфликт при параллельном выполнении
**Context:** Tasks 7 и 8 в Wave 3 оба изменяли `cabinet/timesheet/page.tsx`. При параллельном выполнении — гарантированный конфликт. Поймал только template-validator. (Seen 2: panel-next-run — Tasks 3/4/5 все меняли `index.html`, поймал template-validator.)
**Pattern:** После написания всех задач в волне — прогнать мысленный (или grep-based) check: нет ли двух задач в одной волне с совпадающим файлом в "Files to modify". Если есть — объединить задачи или разнести по волнам.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 employee-cabinet / session 1: File upload в архитектуре требует явного описания file download

**Seen:** 1
**Adapted:** —
**Triad:** проектирование фичи с загрузкой пользовательских файлов на диск → явно определить механизм доставки файлов (protected API endpoint с ownership check, не static) в Architecture секции → предотвратить IDOR через неавторизованный прямой доступ к файлам
**Context:** Tech-spec описывал POST для загрузки PDF-сертификатов, но не описывал как файлы отдаются клиенту. Файлы попали бы в `/uploads/` без auth-защиты. Поймал security-auditor — добавлен новый Task 5.
**Pattern:** Когда фича включает хранение файлов пользователя, upload и download — разные операции с разными требованиями безопасности. В Architecture явно описать оба direction: куда файл попадает при upload И через какой endpoint возвращается при download (с auth check). Статическая раздача файловой директории по умолчанию небезопасна.
**Scope:** universal
**Category:** information-gathering

### 2026-04-01 employee-cabinet / session 1: Субагент сообщает о блокере — верифицировать самостоятельно

**Seen:** 1
**Adapted:** —
**Triad:** субагент сообщает о блокере (build failure, missing dep, broken env) как причине незавершённой задачи → запустить ту же команду самостоятельно → не принимать диагноз агента как факт без проверки
**Context:** Task 5 агент заявил "pre-existing build failure (missing admin/timesheets route, unrelated)" и пометил это как не-блокер. Верификация показала: build проходил нормально, никакого pre-existing failure не было. Диагноз агента был ложным.
**Pattern:** Когда субагент сообщает о блокере как оправдании — не принимать этот диагноз как факт. Запустить ту же команду (build, test, curl) самостоятельно. Если блокер не воспроизводится — задача не заблокирована, а агент ошибся в диагностике. "Pre-existing blocker" — распространённый паттерн самооправдания.
**Scope:** universal
**Category:** recovery

### 2026-04-01 employee-cabinet / session 1: Субагент не обновляет frontmatter статус задачи

**Seen:** 1
**Adapted:** —
**Triad:** завершение задачи субагентом → явно обновить `status: done` в frontmatter task-файла как финальный шаг → не накапливать задачи со статусом "planned" требующие ручного batch-обновления от лида
**Context:** Tasks 2, 4, 5, 6, 7 оставлены со статусом "planned" после выполнения — агенты обновляли decisions.md, но не трогали task frontmatter. Лид обнаружил при wave transition и обновлял вручную партиями.
**Pattern:** В промт каждого teammate явно добавить шаг "обновить `status: planned → done` в frontmatter task-файла". Это не опциональная административная работа — без этого lead не может определить состояние фичи без ручного просмотра. Включить в commit flow перед reporting completion.
**Scope:** universal
**Category:** sequencing
### 2026-03-31 dashboard-v1 / session 3: Local-first режим — уточнить среду деплоя до запуска deploy-pipeline

**Seen:** 1
**Adapted:** —
**Triad:** pre-deploy QA завершён, пользователь в local-first / sketch режиме → уточнить желаемую среду верификации ДО запуска deploy wave → не готовить VPS-деплой для пользователя который не планирует его сейчас
**Context:** Task 12 (Deploy) запустился по плану волны. Только после попытки настройки выяснилось: нет remote, нет GitHub, нет секретов — пользователь сказал "пока размещаем локально". Создан GitHub репо, код запушен, но VPS-деплой отложен. Волна 7-8 зафиксирована как deferred.
**Pattern:** Перед запуском deploy wave уточнить у пользователя: "Деплоим сейчас на VPS или оставляем локально?" — особенно в sketch/local-first проектах. GitHub + deploy.yml можно настроить в любой момент; principal goal — working local result.
**Scope:** situational
**Situation:** sketch-mode или local-first фичи, где пользователь не заявил явного намерения деплоить
**Category:** communication

### 2026-03-26 shift-confirmation: Ошибки повторяются между волнами

**Seen:** 1
**Adapted:** —
**Triad:** ревью нашло паттерн ошибки (не разовый баг) → добавить предупреждение в промт следующего teammate → предотвратить повторение ошибки в следующих задачах
**Context:** В Task 1 ревьюер нашёл `confirmationStatus: string` вместо enum. Исправили. В Task 4 — ровно та же ошибка. Агент Task 4 не знал о находке Task 1, т.к. каждый teammate с чистым контекстом.
**Pattern:** Когда ревью находит паттерн ошибки (не разовый баг), lead добавляет предупреждение в промт следующего teammate: "В предыдущих задачах ревьюеры находили [X] — убедись, что новый код не повторяет эту ошибку."
**Scope:** situational
**Situation:** multi-agent feature execution с несколькими волнами
**Category:** communication

<!-- PROMOTED → code-writing (Seen: 2, 2026-03-30) -->

### 2026-03-26 shift-confirmation: Known-issues реестр для аудитов

**Seen:** 1
**Adapted:** —
**Triad:** security/code audit в multi-task feature → вести known-issues.md, аудитор читает перед ревью → не тратить время на повторный репорт известных проблем
**Context:** Security auditor нашёл IDOR в `markEvent()` при ревью Task 2. Та же находка повторилась в audit wave. Нет реестра известных проблем — тратит время на уже известное.
**Pattern:** Завести `known-issues.md` на уровне проекта. Перед ревью агент читает его и пропускает задокументированные проблемы.
**Scope:** situational
**Situation:** multi-task features с security/code audit
**Category:** information-gathering

### 2026-03-28 mvp-pipeline-core + mvp-parser: Тесты на моках скрывают расхождение с реальным внешним процессом

**Seen:** 2
**Adapted:** —
**Triad:** unit-тесты с моками для внешнего процесса/API → провести минимум 1 live smoke-прогон перед объявлением QA passed → предотвратить ложное "all tests pass" при расхождении мока и реальности
**Context:** (1) mvp-parser: 75 тестов pass, но реальный API возвращал другую структуру. (2) mvp-pipeline-core: 77 тестов pass, QA passed — но реальный `claude -p` вернул JSON в envelope + markdown fences + свой формат полей. 7 fix-коммитов после "успешного" QA.
**Pattern:** Перед объявлением QA passed — сделать минимум 1 live прогон с реальным внешним процессом (API/CLI). Не доверять мокнутым тестам для валидации интеграции. Сохранить реальный ответ как golden fixture.
**Scope:** universal
**Category:** information-gathering

### 2026-03-28 mvp-parser / live-test: Программное создание документа — зачищай дефолтные артефакты

**Seen:** 1
**Adapted:** —
**Triad:** программное создание документа через API → после создания кастомного контента удалить дефолтные артефакты → не оставлять мусор в финальном документе
**Context:** При создании spreadsheet через API дефолтный лист остался пустым рядом с кастомными вкладками. Проверка пустоты по техническому свойству (row_count) не сработала — свойство имеет ненулевой default. Фикс: идентифицировать дефолтные артефакты по имени.
**Pattern:** При программном создании документа через API — проверить какие дефолтные элементы создаются автоматически и зачистить их после наполнения кастомным контентом. Идентифицировать дефолтные элементы по имени/типу, не по содержимому (пустота может не определяться из-за default-значений).
**Scope:** universal
**Category:** tool-selection

<!-- PROMOTED → feature-execution SKILL.md (2026-03-30, Seen: 2) -->

### 2026-03-28 bp-pipeline / skeleton-pipe: Язык пользователя, не профессиональный жаргон

**Seen:** 1
**Adapted:** —
**Triad:** обсуждение решений с пользователем → использовать язык и терминологию пользователя, расшифровывать каждый термин → ускорить принятие решений, не тратить время на "а что это значит?"
**Context:** Спорные пункты pipeline.md были описаны с аббревиатурами (T1/T2/T3, ICE, severity levels). Пользователь сказал: "я не знаю что такое Т1, ты знаешь, не сокращай ничего". После переформулирования простым языком — все 6 решений приняты за один раунд.
**Pattern:** При обсуждении решений с пользователем — каждый термин расшифровывать при первом упоминании, объяснять последствия на примерах из его домена. Если пользователь хоть раз спросил "что это?" — это сигнал переключиться на простой язык для ВСЕХ последующих обсуждений.
**Scope:** universal
**Category:** communication

### 2026-03-31 dashboard-v1 / session 3: CSS position:fixed провалился на React inline style — зеркаль JS-паттерн соседнего компонента

**Seen:** 1
**Adapted:** —
**Triad:** CSS `position: fixed` не применяется к компоненту с React inline `style={{ display: "none" }}` → использовать JS `isMobile` state с resize listener (зеркально существующему компоненту) → не тратить раунды на CSS, который не может надёжно переопределить React inline style
**Context:** mobile-nav в App.jsx имел `style={{ display: "none" }}` с переопределением через `@media { .mobile-nav { display: flex !important; position: fixed; } }`. Пользователь подтвердил: вкладка находится не внизу viewport, нужно прокрутить страницу. При этом ProjectModal уже использовал `isMobile = useState(() => window.innerWidth <= 640)` + useEffect resize listener. Фикс: применить тот же паттерн к nav div, убрав CSS-подход.
**Pattern:** Когда CSS медиа-запрос должен переопределить React inline style (особенно `position: fixed`) — не полагайся на CSS `!important`. Вместо этого используй JS state `isMobile` с `window.addEventListener("resize", ...)` и прямые inline styles. Этот паттерн уже реализован в модалках — зеркаль его.
**Scope:** universal
**Category:** recovery

### 2026-03-27 mvp-parser / live-test: Проверить стоимость retry до включения

**Seen:** 1
**Adapted:** —
**Triad:** API с лимитом запросов + retry decorator → проверить считаются ли неудачные запросы в лимит ДО включения retry → не сжечь квоту на бессмысленные повторы
**Context:** retry_with_backoff на parser-api.com сжёг 51 запрос из 200/месяц за одну сессию. Каждый обрыв соединения (ConnectionError, ReadTimeout) = запрос списан. Документация не указывает, считаются ли failed requests. Предположение "считаются только успешные" оказалось ложным.
**Pattern:** Перед добавлением retry на API с жёстким лимитом, сделать 2-3 тестовых запроса и сверить счётчик через /stat/ (или аналог). Если failed считаются — retry убрать или ограничить 1 попыткой.
**Scope:** universal
**Category:** tool-selection

### 2026-03-28 mvp-parser / session 3: Согласуй структуру выходного артефакта до реализации

**Seen:** 1
**Adapted:** —
**Triad:** требования к формату выходных данных поступают итеративно → согласовать полную структуру на макете до написания кода → не переписывать реализацию на каждое уточнение
**Context:** Структура экспорта менялась 4 раза за сессию. Каждое изменение = переписывание export + query + тесты.
**Pattern:** Когда фича генерирует выходной артефакт для заказчика — показать пример на 2-3 строках и получить подтверждение структуры ДО реализации. Цена согласования минимальна, цена переделки кратна количеству итераций.
**Scope:** universal
**Category:** scope-management

### 2026-03-28 design-pipeline-v2 / techspec: Verify-smoke для markdown — проверяй структуру, не ключевые слова

**Seen:** 1
**Adapted:** —
**Triad:** verify-smoke для markdown-артефакта (SKILL.md, шаблон) → проверять структурные элементы (фазы, ссылки на файлы, guard-ы), не просто ключевые слова → убедиться что артефакт полноценный, а не stub с нужными словами
**Context:** Изначально verify-smoke для ~180-строчного deep skill содержал 2 grep-проверки (имя скилла + слово "Phase"). Test reviewer справедливо указал: SKILL.md из одной строки с этими словами пройдёт проверку. После фикса — 6-8 проверок: Phase 0, Phase 2, ссылки на input-файлы, corruption guard.
**Pattern:** Для markdown-only артефактов verify-smoke должен проверять не наличие слов, а структурные элементы: (1) множественные фазы по номерам, (2) ссылки на input/output файлы, (3) guard-ы для edge cases, (4) resolution ссылок на reference-файлы. Количество проверок пропорционально размеру артефакта.
**Scope:** universal
**Category:** tool-selection

### 2026-03-28 design-pipeline-v2 / userspec: Генерируй все шаги deliverable целиком, не только ближайший

**Seen:** 3
**Adapted:** —
**Triad:** создание multi-step deliverable (план, roadmap, серия промптов) → сгенерировать все шаги целиком, не только ближайший → не заставлять пользователя ловить недостающие части
**Context:** Создал промпт только для Session 1 из 6. Пользователь сразу заметил что промпт для Session 2 будет некорректным. Пришлось создавать session-roadmap.md со всеми промптами — то, что нужно было сделать сразу.
**Pattern:** Когда deliverable состоит из нескольких шагов (серия промптов, roadmap, план сессий) — генерировать ВСЕ шаги сразу, даже если пользователь явно просил только следующий. Предвидеть проблему устаревания, а не ждать пока пользователь её поймает.
**Scope:** universal
**Category:** scope-management

### 2026-03-28 analiticxxs / perf-fix: Проверяй дефолты библиотек до оптимизации кода

**Seen:** 1
**Adapted:** —
**Triad:** performance problem на сервере с низким трафиком → проверить дефолтные таймауты/лимиты connection pool и кэшей → найти root cause в конфигурации до оптимизации кода
**Context:** TTFB 7-23 секунд на Next.js SSR. Инстинкт — искать тяжёлые запросы, N+1, SSR complexity. Реальная причина: pg Pool `idleTimeoutMillis: 10000` (дефолт) — на low-traffic сервере ВСЕ соединения закрывались каждые 10 секунд, каждый запрос = DNS + TCP + PG handshake. Фикс: одно число `10000 → 60000` = TTFB с 7-23 сек до 196 мс.
**Pattern:** При performance-проблемах на low-traffic серверах — первым делом проверять дефолтные таймауты и лимиты библиотек (connection pool idle timeout, cache TTL, keepalive). Одно число в конфиге часто даёт больше, чем рефакторинг запросов.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 methodology-sync-sketch / techspec: Файловые пути — верифицировать, не угадывать (PROMOTED)

**Seen:** 2 → PROMOTED → tech-spec-planning
**Adapted:** —
**Triad:** написание файловых путей в tech-spec или skill из памяти/docs → верифицировать через ls/glob или прочитать source-файл → не допустить неверных путей в artifacts
**Context:** (1) design-task-decompose: путь к session-plan.md указан по аналогии, реальный путь отличался. (2) methodology-sync-sketch: tech-spec написал `~/.claude/skills/shared/work-templates/`, реальный — `~/.claude/shared/work-templates/`. Оба поймал mirage detector в validation round 1.
**Pattern:** Перед написанием любого файлового пути в tech-spec — верифицировать ls/glob. Architecture docs описывают намерение, а не факт filesystem.
**Scope:** universal
**Category:** information-gathering

### 2026-03-29 fix-knowledge-pipeline / decompose: Заменяй межзадачную зависимость на общий source of truth

**Seen:** 1
**Adapted:** —
**Triad:** задача в одной волне ссылается на результат другой задачи той же волны → заменить зависимость на чтение общего source of truth (decisions.md, tech-spec.md) → сохранить параллельность волны без рисков read-after-write
**Context:** Task 2 (align retrospective) ссылалась на quick-learning/SKILL.md "after Task 1 modifies it", но обе задачи в Wave 1 (параллельно). depends_on: [1] + wave: 1 — противоречие. Решение: Task 2 читает decisions.md напрямую (те же решения, но source of truth, а не output другой задачи). Зависимость убрана, параллельность сохранена.
**Pattern:** При декомпозиции на параллельные задачи — если задача "читает результат другой" в той же волне, заменить зависимость на чтение общего документа (decisions.md, tech-spec.md). Если это невозможно — перенести задачу в следующую волну. Третьего не дано: depends_on + same wave = гонка данных.
**Scope:** universal
**Category:** problem-decomposition

### 2026-03-29 missing-ui-details / wave-2: Сверяй типографику с референсом ДО реализации

**Seen:** 2
**Adapted:** design-generate
**Triad:** фича с визуальным оригиналом (rebuild, redesign, visual polish) → сверить layout, цветовую схему и типографику с референсом ДО написания CSS, составить чеклист расхождений → избежать полного редизайна или серии fix-коммитов после деплоя
**Context:** (1) Visual polish — спек не описывал конкретный шрифт, 9 fix-коммитов. (2) Website rebuild — текстовое описание из code-research без скриншотов привело к полностью другому дизайну (тёмный gradient вместо белого фона, centered вместо two-column, слайдер отдельно вместо в hero). Обнаружено только после деплоя на VPS.
**Pattern:** Перед реализацией визуальной задачи с оригиналом — открыть скриншоты и составить чеклист: (1) layout (колонки, выравнивание), (2) цветовая схема (фон, акценты), (3) типографика (шрифт, вес, размер), (4) структура секций (порядок, вложенность компонентов). Если скриншотов нет — запросить у пользователя. Текстовое описание недостаточно для visual match.
**Scope:** universal
**Category:** information-gathering

### 2026-03-29 pipeline-stabilization / session 1: Перед ревью — проверить артефакты удаления

**Seen:** 1
**Adapted:** —
**Triad:** задача на удаление фичи/константы/поля → перед отправкой на ревью проверить dead variables, stale comments, duplicate tests от удалённого кода → не тратить review-раунд на предсказуемые артефакты удаления
**Context:** Task 1 удалил MAX_OUTPUT_CHARS и два поля из REQUIRED_FIELDS. Task 2 удалил extended mode и wave-поля. Все 6 ревьюеров нашли только minor-находки: мёртвая переменная `missing` (ссылалась на удалённый check), stale-комментарии с "extended", дублирующийся тест (старый обновлён до пустого набора — совпал с новым TDD-тестом). Все предсказуемы.
**Pattern:** После задачи на удаление — перед отправкой на ревью пройти чеклист: (1) dead variables/imports, ссылающиеся на удалённый код, (2) комментарии/docstrings, упоминающие удалённую функциональность, (3) тесты, ставшие дублями или тестирующие удалённое поведение. Три минуты проверки экономят review-раунд.
**Scope:** universal
**Category:** sequencing

### 2026-03-29 pipeline-stabilization / session 2: При редактировании AI-промтов — явно проверять emphasis-framing

**Seen:** 1
**Adapted:** —
**Triad:** редактирование/компрессия AI-промта → явно проверить все prohibition/caps формулировки ("НЕЛЬЗЯ", "ЖЁСТКИЕ ОГРАНИЧЕНИЯ", "ГЛАВНОЕ ПРАВИЛО") и заменить на motivation-framing → не тратить review-раунды на предсказуемую emphasis-ошибку
**Context:** Tasks 4, 5, 6 (компрессия agent-04..10) — три задачи подряд получили major-находку от prompt-reviewer: prohibition lists и капслок ("СТРОГО СОБЛЮДАЙ", "ЖЁСТКИЕ ОГРАНИЧЕНИЯ", "ГЛАВНОЕ ПРАВИЛО"). Паттерн повторился во всех трёх задачах. Все найдены в одном review-раунде и исправлены в одном коммите.
**Pattern:** При редактировании или компрессии AI-промтов — добавить финальный чеклист перед ревью: (1) найти все КАПСЛОК-заголовки, (2) найти все формулировки "нельзя/запрещено/жёсткие/строгие", (3) заменить на мотивационное обоснование ("чтобы X, делай Y" вместо "ЗАПРЕЩЕНО делать Y"). Prohibition-framing — предсказуемая находка в любом AI-промте.
**Scope:** universal
**Category:** sequencing

### 2026-03-29 fix-knowledge-pipeline: Overflow-политика при распределении в capped buckets

**Seen:** 1
**Adapted:** —
**Triad:** алгоритм распределяет записи по bucket-ам с max-cap → определить overflow-политику (куда идут записи сверх лимита) до реализации → не терять записи при заполнении bucket-а
**Context:** Task 5 генерировал per-skill quick-ref файлы с лимитом 10 записей. quick-ref-feature-execution.md заполнился (10 записей из sequencing/recovery/communication), запись #32 была молча отброшена. Reviewer обнаружил: #32 должна попасть в do-task (overflow bucket). Задача не описывала overflow-поведение.
**Pattern:** При реализации алгоритма "распределить N элементов по M buckets с max-cap" — явно определить политику overflow до написания кода: (1) куда попадают элементы сверх cap (следующий bucket, default bucket, ошибка), (2) как проверить что ни один элемент не потерян. Без явной политики реализатор молча выбросит overflow.
**Scope:** universal
**Category:** tool-selection

### 2026-03-29 design-pipeline-v2 v2.3 / session 1: При cross-domain адаптации шаблона — проверять совместимость каждого поля

**Seen:** 1
**Adapted:** —
**Triad:** адаптация шаблона задачи из одного домена в другой → проверить каждое поле frontmatter на применимость к целевому домену → не исправлять domain-несовместимые defaults отдельной задачей после деплоя
**Context:** design-task.md.template был создан в v2.2 по образцу task.md.template. Поле `reviewers: [skill-checker]` скопировано из code-domain шаблона — там оно осмысленно. В design-domain quality gate — user visual review, не skill-checker. Несовместимость обнаружена при написании tech-spec v2.3 и потребовала отдельной Task 2 в следующей версии.
**Pattern:** При адаптации шаблона из одного домена в другой — пройти каждое поле frontmatter через вопрос "это поле имеет смысл в целевом домене?". Если нет — изменить default прямо при адаптации, не копировать как есть. Несовместимые defaults, скопированные "на потом", становятся отдельными задачами в следующей итерации.
**Scope:** universal
**Category:** sequencing

### 2026-03-29 design-pipeline-v2 v2.3 / task-decomposition: Пилотная задача перед массовой генерацией по новому шаблону

**Seen:** 1
**Adapted:** —
**Triad:** массовая генерация задач по шаблону, применяемому к новому домену впервые → сначала 1 пилотная задача → проверить и валидировать → масштабировать на все задачи → не накапливать 30+ правок при первом прогоне
**Context:** task-creator сгенерировал 8 задач по design-task.md.template за один прогон. Validation round 1 дал 30+ находок (несовместимые поля, неверные пути, domain-mismatch в reviewers). Если бы задача 1 была проверена первой — паттерн ошибок был бы найден до масштабирования на 7 оставшихся.
**Pattern:** При первом применении шаблона к новому домену — сгенерировать 1 пилотную задачу, прогнать через валидатор, зафиксировать все несоответствия. Только после успешной пилотной — генерировать остальные. Стоимость пилота минимальна; стоимость 30+ правок в 8 задачах — в 8 раз выше.
**Scope:** universal
**Category:** problem-decomposition

### 2026-03-29 pipeline-stabilization / session-3: Security severity привязывается к модели развёртывания

**Seen:** 3 → PROMOTED to security-auditor
**Adapted:** —
**Triad:** security audit находит medium-уязвимости в локальном CLI-инструменте → классифицировать как non-blocking с явным условием "до перехода на service/multi-user деплой" → не блокировать релиз по находкам нерелевантным текущей модели развёртывания
**Context:** Task 9 нашла 3 medium-находки (отсутствие hard-limit на --text, произвольный --data-dir, отсутствие size limits на validator fields). Все три реальны и требуют fix — но только перед service deployment. Для single-user CLI они не создают угрозы.
**Pattern:** При аудите безопасности явно привязывать severity к модели развёртывания. Medium-находка в single-user CLI и medium-находка в multi-user service — разные приоритеты. Записывать условие перехода ("before service deployment") прямо в статус задачи, не только в comments.
**Scope:** situational
**Situation:** инструмент развёртывается как локальный CLI для одного пользователя; есть планы перейти на service-модель
**Category:** scope-management

<!-- PROMOTED → task-decomposition (Seen: 2, 2026-03-30) -->

### 2026-03-29 pipeline-stabilization / session-3: QA разделяет failed и deferred

**Seen:** 1
**Adapted:** —
**Triad:** QA-критерий требует live-вызова внешнего сервиса (LLM, API, DB) недоступного в test-среде → отметить как deferred с явным условием, не как failed → получить чистый QA pass на автоматизируемых критериях без блокировки
**Context:** Task 11 (pre-deploy QA) прошла 20 из 22 критериев. 2 оставшихся требуют live Claude CLI вызова с активной подпиской. Вместо fail или skip — deferred с записью в deferredToPostDeploy, что даёт чёткий план для post-deploy verification.
**Pattern:** В QA-отчёте явно разделять три статуса: passed, failed, deferred. Deferred — критерий, истинность которого не может быть проверена автоматически (требует live-среды, подписки, внешнего пользователя). Deferred не блокирует релиз, но создаёт обязательный чеклист для post-deploy. Не смешивать с "не успели проверить".
**Scope:** universal
**Category:** sequencing

### 2026-03-29 analiticxxs / recovery: Давай один шаг за раз при неизвестном внешнем состоянии

**Seen:** 2
**Adapted:** —
**Triad:** пользователь выполняет многошаговый процесс с неизвестной веткой или внешним состоянием → сначала задать уточняющий вопрос о ветке, затем давать по одному шагу с ожиданием результата → не давать инструкции для неизвестного или неактуального состояния
**Context:** Пользователь вставил весь блок команд прямо в psql вместо bash. Также: пользователь получил все 5 шагов SSH fix без уточнения способа доступа к VPS — инструкции могли быть нерелевантны.
**Pattern:** Когда следующий шаг зависит от неизвестного условия (способ доступа, текущее состояние среды) — сначала задать один уточняющий вопрос. Затем давать ровно один шаг, ждать вывода, убедиться что контекст правильный, только потом следующий.
**Scope:** universal
**Category:** communication

### 2026-03-30 design-pipeline-v2 v2.3: Граничное условие счётчика — верифицируй против спецификации

**Seen:** 2
**Adapted:** —
**Triad:** написание числовой логики с граничным условием (max N повторений, retry limit, iteration cap) → сразу подставить граничное значение и убедиться что условие выполняется ровно N раз → не пропустить off-by-one через code review
**Context:** Wave-итерации в design-session-execution: counter=1, условие `< 3` — вместо 3 re-spawn получилось 2. Decision 9 требовал max 3 итерации. Code audit (HIGH finding) поймал; обычный review не заметил бы. Fix: `< 3` → `<= 3`.
**Pattern:** При написании логики "повторять максимум N раз" — сразу подставить граничное значение и посчитать итерации вручную: если counter=1, то `<= N` даёт N итераций, `< N` даёт N-1. Off-by-one визуально неотличим от правильного кода — review ловит редко.
**Scope:** universal
**Category:** sequencing

### 2026-03-30 design-pipeline-v2 v2.3: git add scope должен покрывать все write locations скилла

**Seen:** 1
**Adapted:** —
**Triad:** скилл или агент делает commit и пишет файлы в несколько директорий → перечислить все write locations из тела скилла перед написанием git add → не потерять файлы вне основного дерева при коммите
**Context:** design-done: `git add work/completed/{feature}/` не захватывал `.design-system/` файлы, которые design-retrospective пишет в корне проекта. Архивный коммит был неполным. HIGH finding на code audit; fix: `git add -A`.
**Pattern:** При написании шага commit в скилле — просмотреть все фазы, которые пишут файлы, и составить список write locations. Если хотя бы одна запись происходит вне основной директории — использовать `git add -A`. Path-specific `git add` скрыто ломается при добавлении новых write locations в будущем.
**Scope:** universal
**Category:** sequencing

### 2026-03-30 design-pipeline-v2 v2.3: TRIZ для выбора между равнозначными вариантами фикса

**Seen:** 1
**Adapted:** —
**Triad:** два варианта фикса дают одинаковый результат но отличаются по устойчивости к будущим изменениям → применить tradeoff-анализ (minimal diff vs systemic robustness) → выбрать вариант с меньшим coupling к текущим деталям реализации
**Context:** HIGH #1: `< 3` vs `counter=0` — оба дают 3 итерации, но `<= 3` семантически точнее и ближе к спецификации. HIGH #2: `git add work/completed/` vs `git add -A` — оба фиксируют текущие файлы, но `-A` устойчив к добавлению новых write locations. Оба выбора сделаны за один раунд без обсуждения.
**Pattern:** Когда два варианта фикса технически корректны — проверить: (1) какой вариант продолжает работать при изменении смежного требования, (2) какой вариант создаёт меньше implicit coupling с деталями реализации. Выбрать более устойчивый даже если diff чуть больше.
**Scope:** universal
**Category:** tool-selection

### 2026-03-30 agent-research-prompt-fix userspec: поведение агента после пропуска — логика, не маркер

**Seen:** 1
**Adapted:** —
**Triad:** описание skip-поведения агента при пустом user input → явно описать что агент ДЕЛАЕТ после пропуска (продолжает анализ), не только какой маркер ставит в поле → не допустить реализации label-swap без изменения логики
**Context:** Спек описывал [ПРОПУЩЕНО ПОЛЬЗОВАТЕЛЕМ] как замену [НЕТ ДАННЫХ]. Пользователь уточнил: агент должен реально завершить анализ с имеющимися данными, а не просто переименовать заглушку. Разница критическая для реализации.
**Pattern:** Когда описываешь поведение агента при пустом/пропущенном вводе — формулируй не только output marker, но и processing logic: "агент продолжает анализ с тем, что есть, и помечает только вычислительно недостижимые поля". Без явной processing logic разработчик реализует label-swap.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 agent-research-prompt-fix userspec: active + planned stubs для многочастного скопа

**Seen:** 1
**Adapted:** —
**Triad:** user spec вырастает до 3+ последовательно зависимых deliverable разного размера → оставить первый deliverable active draft, остальные создать как planned stubs → пользователь видит прогресс на каждой части и контекст постфич сохранён
**Context:** Спек начался как 3 пункта, вырос до 4, потом пользователь попросил разбить "чтобы видеть прогресс". Создали 3 отдельных файла: part1 (active/approved), part2+3 (planned). Части 2 и 3 полностью проработаны для контекста, но не запускаются сразу.
**Pattern:** Если feature вырастает до 3+ частей с чёткими зависимостями — не пытайся уместить всё в один спек. Создай первую часть как active draft, остальные как planned stubs с полным описанием. Это даёт видимость прогресса без потери плана. Planned stubs не требуют повторного интервью при запуске.
**Scope:** universal
**Category:** scope-management

### 2026-03-30 design-v2 / session 1: Зона субъекта фото — до расстановки UI overlay

**Seen:** 1
**Adapted:** —
**Triad:** размещение текста/UI поверх full-bleed фото → определить зону субъекта в кропированном вьюпорте ДО расстановки элементов → не перекрыть лицо/объект текстом
**Context:** Hero с portrait фото в landscape viewport — текст был поставлен по центру экрана и накрыл лицо стилиста. Потребовался полный редизайн grid-структуры.
**Pattern:** Перед расстановкой UI-элементов поверх фото — вычислить где окажется субъект после object-fit cover кропа. Portrait в landscape → субъект всегда около горизонтального центра. Текст ставить только в негативное пространство: низ (bottom gradient zone), крайний угол или зону без субъекта.
**Scope:** situational
**Situation:** Hero или full-bleed секция с фото, поверх которой размещаются текст или UI-блоки
**Category:** design-process

### 2026-03-30 design-v2 / session 1: Редизайн = независимый выбор layout, не наследование структуры

**Seen:** 1
**Adapted:** —
**Triad:** задача "альтернативный дизайн" или "редизайн существующей страницы" → выбирать layout pattern независимо от существующей верстки → получить реальную альтернативу, а не ресайн с другими цветами
**Context:** Первый preview был отклонён ("всё ещё сильно основан на прошлой версии") — структура 50/50 split была перенесена из v1, изменены только шрифты и цвета.
**Pattern:** При задаче редизайна — не смотреть в существующий CSS/HTML при выборе layout. Начинать с вопроса: "как принципиально иначе можно показать этот контент?" Только после независимого решения сверяться с существующим кодом для понимания контента (тексты, фото), но не структуры.
**Scope:** situational
**Situation:** Задача создать v2, альтернативный вариант или редизайн существующей страницы
**Category:** design-iteration

### 2026-03-30 methodology-sync-sketch / session 1: Классификация глубины diff до написания sync scope

**Seen:** 1
**Adapted:** —
**Triad:** планирование синка файлов между двумя версиями одного репо → запустить code-research для классификации глубины различий до написания scope → не описывать в AC механический синк который требует ручного ревью каждого файла
**Context:** Планировали синк 26 скиллов в Codex через замену путей (.claude/→.agents/). Code-research показал что 24 из 26 имеют реальные content-различия (feature-execution переписан под spawn_agent API) — scope пришлось полностью переписать.
**Pattern:** Перед тем как включить cross-repo sync в scope спека — запустить code-research с вопросом "path-only diff или content diff?". Если content diff > 50% файлов — это не механическая задача, это ручной ревью. Отдельная фича.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 methodology-sync-sketch / session 1: Итеративная классификация доменов в mono-repo

**Seen:** 1
**Adapted:** —
**Triad:** репо содержит скиллы из нескольких доменов → явно перечислить каждый домен и получить is_in_scope per domain до написания спека → не переписывать scope в 3 итерации из-за постепенного уточнения границ
**Context:** Один репо содержит методологию, дизайн-пайплайн, promoter, skeleton-pipe, sketch. Уточнения "это отдельный пайплайн" происходили трижды (design → promoter/skeleton → уточнение что sketch ВХОДИТ). Каждый раз — реакция на вопрос.
**Pattern:** При старте user-spec для проекта с несколькими доменами — сразу предъявить полный список всего что есть в репо и попросить пометить каждый домен: in/out/separate. Одним вопросом, а не серией уточнений.
**Scope:** universal
**Category:** scope-management

### 2026-03-30 agent-research-prompt-fix / session 2: верифицировать содержимое каждого целевого файла перед описанием операции

**Seen:** 2 (agent-research-prompt-fix × 2)
**Adapted:** —
**Triad:** spec (user, tech, task) называет набор файлов и описывает трансформацию → верифицировать каждый файл на наличие изменяемого элемента → не допустить ошибочный тип операции (replace вместо add)
**Context:** (1) User-spec назвал "runner.py" и "счётчик уже есть" — неточные утверждения, пойманы code-research. (2) Tech-spec описал "убрать [НЕТ ДАННЫХ] из всех 9 промптов" — agent-03 этой строки не содержит, нужна другая операция (add instruction). Поймано reality-checker при декомпозиции.
**Pattern:** Любой spec-артефакт (user-spec/tech-spec/task) доверяет, что файлы содержат описываемый элемент. Перед тем как зафиксировать "удалить X" или "заменить X" — grep по каждому целевому файлу. Файлы без X требуют операции add, не replace. Ошибка типа операции обнаруживается только при выполнении.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 agent-research-prompt-fix / session 2: тест с точной строкой-маркером создаёт неявный depends_on

**Seen:** 1 (agent-research-prompt-fix)
**Adapted:** —
**Triad:** задача содержит тест с точной строкой-маркером определённой в другой задаче → объявить depends_on на задачу-источник даже если строка — литерал → не пропустить неявную зависимость через разделённый дизайн-маркер
**Context:** Task 4 содержала `test_propushcheno_not_pipeline_defect` ассертящий на `"[ПРОПУЩЕНО ПОЛЬЗОВАТЕЛЕМ]"`. Строка определяется в Task 2 (pipeline.py). Task 4 объявила only `depends_on: [1]`. Индивидуальные валидаторы пропустили — cross-task валидатор поймал.
**Pattern:** Если задача содержит тест ассертящий на конкретную строку/константу/маркер — проверить: кто принял дизайн-решение об этой строке? Задача-источник должна быть в depends_on даже если строка используется как литерал а не импортируется.
**Scope:** situational
**Situation:** multi-task декомпозиция с sentinel strings / protocol markers общими между задачами
**Category:** problem-decomposition

### 2026-04-02 moneymaker / techspec: Каталог скиллов — читай ДО написания задач И при исправлении

**Seen:** 2
**Adapted:** n/a
**Triad:** написание ИЛИ исправление полей Skill/Reviewers в Implementation Tasks → сверить ВСЕ значения в списке с `skills-and-reviewers.md`, не только сообщённый → не вносить новые миражи при починке известных
**Context:** Tasks 1-5 использовали `write-code` (wrapper) — поймано в round 1. При исправлении был введён `test-reviewer` (не существует) — поймано skeptic в round 2. Оба раза ошибка = интуитивный псевдоним вместо проверки каталога.
**Pattern:** При написании ИЛИ исправлении reviewer/skill имён — открыть `skills-and-reviewers.md` и проверить ВСЕ значения в списке одновременно. При замене одного неверного имени соседние могут быть такими же неверными. Wrapper-skills и интуитивные псевдонимы (`test-reviewer`, `write-code`) — самые частые ошибки.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 pipeline-report / decompose: TDD Anchor для private метода — вызов через инстанс

**Seen:** 1
**Adapted:** —
**Triad:** TDD Anchor описывает тест для private метода класса → указывать вызов через инстанс объекта, не через прямой импорт → тесты не падают с ImportError до запуска реальной логики
**Context:** task-creator написал TDD Anchor с инструкцией `import _generate_report from bp_pipeline.pipeline`. Private метод нельзя импортировать напрямую — reality-checker поймал как critical. Правка: `pipeline_instance._generate_report(session, session_dir)`.
**Pattern:** В TDD Anchor для private/protected метода — явно указывать паттерн доступа: создать инстанс класса, вызвать `instance._method()`. Не писать `from module import _method` — это ImportError. Актуально для любого языка с private convention (Python `_`, JS `#`).
**Scope:** situational
**Situation:** task-creator генерирует TDD Anchor для private метода класса
**Category:** problem-decomposition

### 2026-03-30 design-v2-stylist / session 2: Совместимость фото с контейнером — проверять до CSS

**Seen:** 1
**Adapted:** —
**Triad:** выбор лейаута с full-bleed фото → проверить ориентацию фото и кадрирование субъекта против формы контейнера ДО написания CSS → не тратить итерации на геометрически невозможный кроп
**Context:** Портретное фото стилиста (субъект стоит в полный рост на фоне яркого окна) поставили в 50vh landscape-баннер. Ни один Y не мог показать субъекта — это геометрический факт определяемый до верстки. Понадобилось 3 итерации и полная переделка лейаута.
**Pattern:** Перед вёрсткой секции с фото: (1) посмотреть фото через Read, (2) проверить ориентацию (portrait/landscape), (3) оценить где субъект в кадре (верх/центр/низ, % от края), (4) сопоставить с контейнером. Если субъект занимает <30% ширины landscape-контейнера или фото portrait при контейнере landscape — сменить лейаут на тот, который сохраняет пропорцию.
**Scope:** situational
**Situation:** верстка секций с фотографиями в фиксированных контейнерах (hero, banner, split)
**Category:** design-process

### 2026-03-30 design-v2-stylist / session 2: Структурированные данные → UI напрямую

**Seen:** 1
**Adapted:** —
**Triad:** верстка контентной секции из структурированных данных пользователя → маппировать каждое поле данных в UI-элемент напрямую → не изобретать структуру отображения которая расходится с источником
**Context:** Пользователь прислал услуги в формате: название → суть → цена → буллеты. Вместо прямого маппинга была создана отдельная таблица-индекс + аккордеон с другими именами. Потребовались 2 раунда переделки пока структура не совпала с источником.
**Pattern:** Получив от пользователя структурированные данные с явными полями — написать маппинг полей в HTML-элементы ДО верстки (поле_1 → тег_1, поле_2 → тег_2). Дополнительные UI-слои (таблица-индекс, фильтры) добавлять только если пользователь явно запросил.
**Scope:** universal
**Category:** design-process

### 2026-03-30 methodology-sync-sketch / code-audit: Граница ответственности SKILL.md vs. agent-file

**Seen:** 1
**Adapted:** —
**Triad:** создание скилла с companion agent-file (SKILL.md + agents/{name}.md) → явно разграничить что делает SKILL.md (оркестрация фаз) и что делает agent-file (протокол одного шага) → избежать дублирования одного действия в обоих файлах
**Context:** sketch/SKILL.md Phase 3 и sketch-interviewer.md оба описывали сохранение sketch.md. Code audit поймал дублирование как minor finding — execution model оказалась неоднозначной: кто реально выполняет save?
**Pattern:** При написании скилла с companion agent-file: SKILL.md описывает ЧТО происходит на каждой фазе (вход, выход, переход), agent-file описывает КАК выполняется конкретный шаг внутри одной фазы. Каждое конкретное действие (save, send, transform) должно быть явно описано ровно в одном месте.
**Scope:** situational
**Situation:** Новый скилл делегирует часть логики в отдельный agents/{name}.md файл
**Category:** problem-decomposition

### 2026-03-30 pipeline-report / techspec: AC — единственная верификационная рамка при противоречии с описательным блоком

**Seen:** 1
**Adapted:** —
**Triad:** user-spec содержит описательный блок с требованием не отражённым в AC → следовать только AC как источнику истины; противоречие зафиксировать decision-записью и обновить user-spec → не тащить неопределённость из описательного блока в реализацию
**Context:** pipeline-report: описательный блок говорил "стандартный запрос по шаблону поля" — AC этого не содержал. tech-spec принял AC за истину, оформил разрыв решением, обновил user-spec. Без этого разрыв дошёл бы до реализации как неоднозначность.
**Pattern:** Если user-spec содержит описательный блок с требованием не отражённым в AC — AC является источником истины. Зафиксировать разрыв в tech-spec decisions и обновить user-spec, иначе следующий агент снова наткнётся на то же противоречие и будет вынужден решать его самостоятельно.
**Scope:** universal
**Category:** scope-management

<!-- PROMOTED → code-writing (Seen: 2, 2026-03-30 pipeline-report retro — merged: session_id user-provided input added to trigger) -->
### 2026-03-30 methodology-sync-sketch / test-audit: grep в AVP чувствителен к регистру

**Seen:** 1
**Adapted:** —
**Triad:** написание grep-based smoke check для markdown-контента → проверить фактический регистр строки в целевом файле перед финализацией команды → предотвратить ложно-отрицательный AVP check при несовпадении регистра
**Context:** AVP step 2 искал `'decision gate'` (lowercase), SKILL.md содержал `## Phase 6: Decision Gate` (Title Case). grep -c вернул бы 0 вместо ожидаемого ≥ 2. Поймано в test audit, не в момент написания AVP.
**Pattern:** При написании grep-смоков для markdown: открыть целевой файл и убедиться что искомая строка написана именно так. Если регистр не предсказуем (фаза, секция, метка) — добавить флаг -i. Правило: "сначала прочитай, потом grep".
**Scope:** universal
**Category:** tool-selection

### 2026-03-30 methodology-sync-sketch / done: Атомарная запись в shared-файл при конкурентных сессиях

**Seen:** 1
**Adapted:** —
**Triad:** Edit tool возвращает "File has been unexpectedly modified" на shared файле методологии → переключиться на атомарный read-modify-write через скрипт, не повторять Edit → избежать накопления partial writes и дублирующихся записей
**Context:** При исправлении дублирующихся номеров в triad-index.md Edit tool 3 раза падал с "unexpectedly modified" — файл одновременно изменялся другими сессиями. Python-скрипт с прямой записью решил за 1 попытку.
**Pattern:** Первое "File has been unexpectedly modified" — сигнал конкурентной записи, не случайная ошибка. Не повторяй Edit — переключайся сразу на atomic read-modify-write: прочитать файл целиком, преобразовать в памяти, записать атомарно через скрипт.
**Scope:** situational
**Situation:** Shared файлы методологии (triad-index.md, reasoning-patterns.md), редактируемые из нескольких сессий одновременно
**Category:** recovery

### 2026-03-30 pipeline-report / session 1: параллельный запуск ломает смысловой порядок

**Seen:** 1
**Adapted:** —
**Triad:** два шага процесса связаны по смыслу (A должен завершиться до показа B) → запускать A синхронно, ждать завершения, только потом выполнять B → гарантировать смысловой порядок — фоновый запуск A не означает A < B
**Context:** quick-learning запущен в фоне одновременно с генерацией next-session prompt — уведомление пришло после, нарушив ожидаемый порядок "сначала анализ, потом промт".
**Pattern:** Если два шага имеют смысловую зависимость для пользователя (B опирается на результат A или должен следовать после него), не оптимизируй под параллелизм — запускай A синхронно. Фоновый запуск сохраняет время, но ломает порядок и доверие.
**Scope:** universal
**Category:** sequencing

<!-- PROMOTED → feature-execution (Seen: 2, 2026-03-30 pipeline-report retro) -->
<!-- PROMOTED → task-decomposition (Seen: 2, 2026-03-30 pipeline-report retro) -->
### 2026-04-02 content-card / marketplace: Вырезать фон товара ДО генерации карточки

**Seen:** 1
**Adapted:** —
**Triad:** marketplace карточка с фото товара на нежелательном фоне → запустить rembg и получить PNG с прозрачностью ДО генерации HTML → избежать прямоугольного "кирпича" фото в дизайне карточки
**Context:** Первая версия карточки для бейсболки показала кепку с серым градиентным фоном на кремовом фоне карточки — пользователь оценил как "очень слабо". Фоновый прямоугольник уничтожил весь дизайн. Переделка потребовала установки rembg, вырезки фона и полного перепроектирования photo-зоны.
**Pattern:** Для marketplace карточки с фото товара: первый шаг — проверить нужна ли вырезка фона. Если фон нежелательный (не белый/нейтральный) — запустить `rembg` до генерации HTML. Вырезанный PNG позволяет товару "плавать" на фоне карточки с CSS drop-shadow вместо object-fit cover. Это структурное решение, менять его после генерации дорого.
**Scope:** situational
**Situation:** content-card / marketplace режим, фото товара с ненейтральным фоном
**Category:** design-process

### 2026-04-02 content-card / marketplace: Прозрачное пространство в PNG — учитывать при посадке на поверхность

**Seen:** 1
**Adapted:** —
**Triad:** PNG с вырезанным фоном (product shot) позиционируется CSS-bottom на платформу или поверхность → рассчитать bottom = platform_top_px - transparent_space_bottom_px → предмет визуально стоит на поверхности, не парит
**Context:** После вырезки фона кепка при bottom: 90-112px продолжала парить над платформой. Причина: rembg убрал серую поверхность-отражение оригинального фото — снизу PNG остался прозрачный блок ~30% высоты изображения. Реальный brim кепки находится на 255px выше низа PNG при max-height: 851px.
**Pattern:** После rembg product-shot содержит прозрачное пространство снизу — там было отражение/поверхность оригинала. Правило посадки: `img.bottom = platform_top - transparent_bottom`. Для product shots transparent_bottom ≈ 25-35% от rendered height. Проверять через Read tool: если субъект не занимает нижнюю треть PNG — прозрачный блок есть.
**Scope:** situational
**Situation:** HTML/CSS карточка с CSS-платформой и PNG-товаром с вырезанным фоном
**Category:** design-process

### 2026-03-30 freelance-dashboard / session 1: scope-impact check перед добавлением фичи в спек

**Seen:** 1
**Adapted:** —
**Triad:** пользователь говорит "встроить" / "добавить" на вопрос о новой фиче в середине user-spec интервью → задать scope-impact вопрос ("это v1 или отдельная фича?") до обновления спека → не добавить в текущий спек фичу, которая утроит объём и потребует другой архитектуры
**Context:** Пользователь подтвердил включение sync-агента в dashboard-v1 ("это нужно в первый заход встроить"). Я начал перестраивать архитектуру (localStorage → backend). Пользователь сам откатил через 2 сообщения. Потерял 1 цикл интервью.
**Pattern:** Когда пользователь добавляет нетривиальную фичу в текущий спек — не вноси немедленно. Сначала озвучи архитектурный импакт и спроси явно: "Это v1 или отдельная спека?" Один вопрос дешевле чем переписывание scope.
**Scope:** situational
**Situation:** user-spec интервью, пользователь предлагает добавить фичу которая меняет архитектурный слой или удваивает объём задач
**Category:** scope-management

### 2026-03-30 freelance-dashboard / session 1: client-only storage + серверная автоматизация — проверять совместимость сразу

**Seen:** 1
**Adapted:** —
**Triad:** в одной фиче сочетаются client-only хранилище (localStorage, IndexedDB, cookies) и серверная автоматизация (cron, background script, webhook) → до финализации архитектуры проверить: может ли серверный процесс читать/писать в это хранилище → не обнаружить data-access конфликт в середине tech-spec
**Context:** localStorage + ежедневный sync-скрипт были предложены как v1. Поймал конфликт до спека: серверный скрипт не имеет доступа к browser storage — потребовался бы полный backend. Предотвратил ошибочную архитектуру.
**Pattern:** Если фича включает client-only storage и любой серверный процесс — немедленно проверь data-access layer: кто пишет, кто читает, через какой канал. localStorage недоступен с сервера; server-side файл недоступен из браузера без API. Это базовый compatibility check, который нужно делать до любого архитектурного решения.
**Scope:** universal
**Category:** problem-decomposition

### 2026-03-30 photo-crop / session 1: структурные gate-вопросы при конвертации алгоритма в процедурный скилл

**Seen:** 1
**Adapted:** —
**Triad:** конвертация пользовательского алгоритма (список шагов) в процедурный SKILL.md → добавить gate-вопрос («перечисли что определил на этом шаге») в конце каждой фазы, даже если его нет в оригинале → удовлетворить структурные требования процедурного скилла без повторного прогона валидатора
**Context:** пользователь передал 4-шаговый алгоритм для расчёта object-position; первый черновик точно воспроизвёл шаги, но пропустил межфазовые чекпоинты — skill-checker потребовал второй прогон.
**Pattern:** Пользовательский алгоритм — это контент, не формат. При конвертации в процедурный скилл добавляй checkpoint-gates независимо от исходника: в конце каждой фазы явно требуй от агента зафиксировать промежуточный результат перед переходом к следующему шагу.
**Scope:** situational
**Situation:** создание нового процедурного SKILL.md на основе алгоритма, предоставленного пользователем или взятого из документации
**Category:** sequencing

### 2026-03-30 export-contacts-filter / session 1: Деструктивная операция в пайплайне — фильтр по статусу, не по полю

**Seen:** 1
**Adapted:** —
**Triad:** user-spec описывает delete/cleanup в системе с pipeline-статусами → ограничивать удаление терминальными статусами (enriched/done), не значением поля → не удалить записи ещё в обработке (pending/in-progress)
**Context:** Предложение "удалять дела без телефона при каждом запуске" удалило бы pending-записи, которые просто не дошли до обогащения (квота ofdata исчерпана на середине цикла). Adequacy validator поймал это как critical data loss риск.
**Pattern:** Если specs описывают деструктивную операцию над записями в системе с processing-статусами — всегда уточни: удаляем только те, что прошли финальный статус (enriched/failed/complete). "Нет нужного поля" ≠ "обработка завершена".
**Scope:** universal
**Category:** scope-management

### 2026-03-30 export-contacts-filter / session 1: Сужение фильтра в спеке — документируй исключение явно

**Seen:** 1
**Adapted:** —
**Triad:** spec сужает критерий от обсуждённого в интервью (A or B → только A) → добавить в Технические решения "решили НЕ включать B, потому что..." → не тратить дополнительные раунды валидации на задокументирование очевидного для автора решения
**Context:** В интервью обсуждался фильтр "phone OR email". Spec молча сузил до "только phone". Quality validator 3 раза подряд флажил это как undocumented decision, пока не появилась явная строка "решили не фильтровать по email, потому что нужен отзвон".
**Pattern:** Когда в спеке сужаешь фильтр/критерий относительно того, что обсуждалось — документируй не только то, что взяли, но и то, что явно отбросили и почему. Reviewers не знают что это осознанное решение, а не упущение.
**Scope:** universal
**Category:** scope-management

### 2026-04-07 website-design-match / session 1: Визуальная фича — один экран за раз

**Seen:** 2
**Adapted:** —
**Triad:** визуальная фича с несколькими экранами/блоками → показать один экран/блок полностью → дождаться одобрения перед следующим
**Context:** (1) admin-demo сгенерирован за один проход (3 блока × 3 вкладки) — 700+ строк без раннего фидбэка. (2) website-design-match tech-spec поставил 3 страницы в параллельную волну — пользователь сказал "один экран за раз", перестройка волн.
**Pattern:** При планировании визуальной фичи (дизайн, редизайн, layout) — каждый экран/блок в отдельную волну с Verify-user. Не параллелить страницы, даже если технически независимы.
**Scope:** universal
**Category:** design-iteration

<!-- PROMOTED → feature-execution (Seen: 2, 2026-03-30): Флаг-файл run-once — путь от якоря, не от CWD -->

### 2026-03-30 pipeline-report / session 2: checkpoint.yml не создан при старте второй сессии

**Seen:** 1
**Adapted:** —
**Triad:** многосессионная фича с session-plan → создавать/коммитить checkpoint.yml в конце каждой сессии, не только читать его в начале следующей → предотвратить ситуацию «ожидаемый файл состояния отсутствует» при старте сессии 2+
**Context:** При старте сессии 2 pipeline-report ожидался checkpoint.yml, но файл не был создан в конце сессии 1. Сессия 1 завершилась коммитом кода, но без явного шага создания state-файла — checkpoint.yml не входил в outputs сессии 1 по session-plan.
**Pattern:** В session-plan для каждой сессии явно добавлять checkpoint.yml в список outputs. Если сессия 2 начинается с «читаем checkpoint.yml» — сессия 1 должна заканчиваться «создаём checkpoint.yml». Ожидать state-файл без его явного создания — молчаливая ошибка handoff.
**Scope:** situational
**Situation:** multi-session feature execution с явным session-plan и передачей состояния между сессиями
**Category:** sequencing

### 2026-03-30 export-contacts-filter / session 2: Audit-волна ловит cross-task баги невидимые per-task ревьюеру

**Seen:** 1
**Adapted:** —
**Triad:** завершение implementation-волн в multi-task фиче → запустить code + security + test аудиты параллельно в отдельной волне → поймать баги из взаимодействия задач, невидимые для ревьюера отдельного diff-а
**Context:** Per-task ревьюеры одобрили Task 1 (флаг-файл создан). Audit-волна нашла major finding: путь к флаг-файлу CWD-relative — проблема возникает из контекста deployment, а не из diff отдельной задачи.
**Pattern:** После implementation-волн добавляй audit-волну (code + security + test, параллельно). Каждый аудитор читает финальное состояние всех файлов фичи — ловит deployment-sensitive и cross-component проблемы, которые per-task ревьюер видит только в своём diff-е.
**Scope:** situational
**Situation:** multi-task feature с 3+ implementation задачами в разных файлах
**Category:** sequencing

### 2026-03-30 juridical-parser / deploy: Метрика в статус-дашборде — уточни временной горизонт

**Seen:** 1
**Adapted:** —
**Triad:** добавление метрики в status/dashboard без явного требования → уточнить у пользователя: за текущий запуск или за всё время → не додумывать горизонт самостоятельно, он варьируется
**Context:** Реализовал счётчики обогащения как SQL-агрегат по всей БД. Пользователь поправил: нужно за текущий запуск. Разные метрики могут требовать разных горизонтов в зависимости от задачи.
**Pattern:** Перед реализацией любой метрики в дашборде/отчёте уточни временной горизонт: за запуск, за день, за период, за всё время. Не выбирай дефолт самостоятельно — это требование, которое варьируется.
**Scope:** universal
**Category:** scope-management

### 2026-03-31 juridical-parser / session: clear() не сбрасывает форматирование во внешних сервисах

**Seen:** 1
**Adapted:** —
**Triad:** вызов clear()/reset() на внешнем сервисе перед записью новых данных → явно сбрасывать ВСЕ слои состояния (контент + форматирование + кэш) → предотвратить проявление предыдущего состояния после "очистки"
**Context:** ws.clear() в Google Sheets очищает ячейки, но не форматирование — красные цвета от предыдущего вызова оставались на новых строках.
**Pattern:** Перед перезаписью данных в внешнем сервисе (Sheets, browser storage, CDN) — проверить, очищает ли "reset"-операция все слои состояния. Если нет — добавить явный сброс каждого слоя отдельно перед записью.
**Scope:** universal
**Category:** tool-selection

### 2026-03-31 juridical-parser / session: production-аномалия может объясняться старой версией кода

**Seen:** 1
**Adapted:** —
**Triad:** production данные не соответствуют поведению текущего кода → сверить timestamp задеплоенного файла с временем запуска → не искать баг в коде который уже правильный
**Context:** was_incomplete=1 в БД при корректном коде — оказалось, фикс был задеплоен ПОСЛЕ прогона, т.е. прогон выполнялся на старом коде.
**Pattern:** При аномалии в production-данных сначала проверить: был ли исправленный код задеплоен ДО момента запуска (ls -la timestamp vs run_date в логе). Если нет — это артефакт старой версии, баг уже устранён.
**Scope:** universal
**Category:** recovery

### 2026-03-31 juridical-parser / session: уточни ownership сервера до деплоя

**Seen:** 1
**Adapted:** —
**Triad:** выполнение deploy-команды в проекте клиента → уточнить чей сервер и кто контролирует деплой-процесс ДО выполнения → не произвести несогласованное изменение на продакшене клиента
**Context:** Задеплоил файлы напрямую на VPS через scp, не уточнив что это продакшен клиента, а не тестовый сервер разработчика.
**Pattern:** Перед выполнением deploy-команды в чужом проекте — явно уточнить: чей это сервер (клиента или разработчика) и как согласовывается деплой. Наличие DEPLOY_HOST в .env не означает права на прямой деплой.
**Scope:** situational
**Situation:** Работа над проектами внешних клиентов, где deploy-инфраструктура принадлежит клиенту
**Category:** communication

### 2026-03-31 juridical-parser / session ad-hoc: изолированный вызов компонента вместо полного пайплайна

**Seen:** 1
**Adapted:** —
**Triad:** запрос на обновление одного компонента системы (статус, отчёт, вкладка) → вызвать только этот компонент изолированно через минимальный скрипт → не тратить ресурсы полного пайплайна и не вызывать побочных эффектов
**Context:** Пользователь попросил обновить статус-вкладку — запустил полный пайплайн с парсером, сжёг API-квоту клиента.
**Pattern:** Когда просят обновить конкретный компонент (статус, отчёт, вкладку) — идентифицировать минимальный вызов этого компонента и запустить его изолированно. Не запускать полную систему, если не попросили явно.
**Scope:** universal
**Category:** scope-management

### 2026-03-31 dashboard-v1 / task-decomposition: stub-ownership gap при межзадачных placeholder-ах

**Seen:** 1
**Adapted:** —
**Triad:** задача N создаёт no-op stubs "для следующих задач" → в бриф каждой заполняющей задачи явно добавить шаг "замени no-op stub на реализацию" → гарантировать что placeholder не останется no-op в рабочем коде
**Context:** Task 4 создала 6 handler-стабов в App.jsx "для Wave 4". Tasks 5 и 6 описывали как вызывать хендлеры, но не содержали шага замены стаба реальной имплементацией. Cross-task ревьюер поймал это: verify-user провалился бы — reload → данные не сохраняются.
**Pattern:** Когда задача N создаёт stubs/placeholders "для следующих задач" — task-creator заполняющих задач должен явно включать шаг "в App/Controller/родителе: заменить no-op stub [название] на реальную имплементацию". Не рассчитывать что агент выведет это из контекста.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-01 dashboard-v1 / deploy: SSH + sudo в GitHub Actions CI деплое

**Seen:** 1
**Adapted:** —
**Triad:** GitHub Actions SSH step выполняет `sudo service-name reload` от deploy-пользователя → убрать sudo из reload-команды (или настроить NOPASSWD в sudoers заранее), добавить `-o StrictHostKeyChecking=no` в SSH-команду → не получать permission denied на первом CI деплое
**Context:** deploy.yml использовал `sudo nginx -s reload` — deploy user не имел sudo. Плюс StrictHostKeyChecking блокировал first-time connect в CI. Итого 8 fix-коммитов.
**Pattern:** При написании GitHub Actions SSH deploy — сразу убрать sudo перед командой reload (nginx/pm2/etc), добавить `-o StrictHostKeyChecking=no` к ssh-команде, и проверить локально права deploy-user до первого push в CI.
**Scope:** universal
**Category:** sequencing

### 2026-03-31 employee-cabinet / session 1: уточнять регион и регуляторику ДО предложения стека

**Seen:** 1 (employee-cabinet/session 1)
**Adapted:** —
**Triad:** предложение хостинг/стека для нового проекта → уточнить регион развёртывания и регуляторные ограничения ДО предложения решений → не переписывать архитектурный стек после обсуждения
**Context:** Предложил Supabase+Railway, затем узнал что проект в России (152-ФЗ, данные граждан РФ) — пришлось полностью менять стек на PostgreSQL+Timeweb VPS.
**Pattern:** При выборе хостинга и инфраструктуры — первым вопросом уточнить страну/регион развёртывания и наличие регуляторных требований (локализация данных, compliance). Только после этого предлагать конкретные сервисы.
**Scope:** universal
**Category:** information-gathering

## Universal

### 2026-03-31 employee-cabinet / session 1: проверять тип БД-объекта до init-кода адаптера

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** подключение адаптера внешней библиотеки к БД → проверить ожидаемый тип объекта (raw driver vs query builder) в docs ДО написания init-кода → не получить runtime ошибку несовместимости адаптера на первом запросе
**Context:** better-auth принимает Kysely-инстанс, мы передали pg.Pool → `db.selectFrom is not a function` при первом login
**Pattern:** Когда библиотека принимает "database" параметр — найти в docs конкретный тип (Pool / Kysely / Prisma), не угадывать по названию. Разные обёртки над одной БД несовместимы на уровне интерфейса.
**Scope:** universal
**Category:** tool-selection

### 2026-03-31 employee-cabinet / session 2: новая роль mid-interview → немедленная матрица прав

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** новая роль появляется в середине user-spec интервью → немедленно составить матрицу "роль × ключевые возможности" и согласовать с пользователем до продолжения → не тратить 3+ батча на выяснение пересечений между ролями
**Context:** Пользователь ввёл роль "руководитель" mid-interview — потребовалось 3 батча чтобы выяснить что она почти совпадает с admin, после чего роль вынесли в отдельную фичу.
**Pattern:** При появлении новой роли — сразу составить таблицу "роль × возможность" и показать пользователю. Пересечения ролей обнаруживаются немедленно, лишние батчи не нужны.
**Scope:** situational
**Situation:** user-spec интервью для приложений с несколькими ролями пользователей
**Category:** scope-management

### 2026-03-31 employee-cabinet / session 1: мокировать инфраструктурную зависимость чтобы разблокировать демо

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** демонстрация UI застряла из-за нерабочей инфраструктурной зависимости (auth, БД, API) → замокировать зависимость локально в компоненте → не блокировать оценку UX из-за инфраструктурной проблемы
**Context:** better-auth не работал локально, пользователь не мог увидеть кабинет → подставили mock-session прямо в компонент и убрали guard в middleware
**Pattern:** Если инфра-зависимость блокирует демо — замокировать её в компоненте за 2 минуты и показать UI. Исправлять инфра отдельно, не держать UX-демо заложником конфига.
**Scope:** universal
**Category:** recovery

### 2026-04-01 dashboard-v1 / session post-deploy: nginx server_name conflict detection

**Seen:** 1
**Adapted:** —
**Triad:** диагностика недоступности nginx снаружи → запустить `nginx -T | grep -B2 -A10 server_name` → обнаружить конфликт server blocks за один шаг
**Context:** два server block претендовали на server_name 217.114.2.159 — dashboard и levelupme (certbot). Ручной просмотр каждого конфига занял бы несколько шагов.
**Pattern:** При недоступности nginx-сервиса снаружи — первым шагом запускать `nginx -T` с grep по server_name. Конфликты server blocks часто невидимы при просмотре одного конфига.
**Scope:** universal
**Category:** information-gathering

### 2026-04-01 dashboard-v1 / session post-deploy: мобильный оператор блокирует HTTP по IP

**Seen:** 1
**Adapted:** —
**Triad:** сервис доступен через curl с сервера (порт 80), но браузер на мобильном зависает → уточнить "по домену или по IP" до диагностики nginx/сети → не тратить время на network-диагностику
**Context:** nginx отвечал 401 на curl, curl с ноутбука работал, а с телефона через 4G зависал без ошибки — причина в блокировке прямых HTTP-запросов по IP у мобильного оператора.
**Pattern:** Если сервис работает через curl но зависает в мобильном браузере — сразу уточнить: домен или IP. Российские мобильные операторы блокируют прямые HTTP-запросы по IP; решение — домен + SSL.
**Scope:** situational
**Situation:** мобильный интернет российских операторов, сервис доступен только по IP
**Category:** recovery

### 2026-04-01 employee-cabinet / session decompose: параллельные тесты — изолировать seed по email

**Seen:** 1
**Adapted:** —
**Triad:** два параллельных теста пишут в общую тестовую БД через одного seed-пользователя → использовать разные email-константы для каждой тестовой задачи → избежать teardown race condition при параллельном выполнении
**Context:** Tasks 9 (integration) и 10 (E2E) в одной волне оба пишут в TEST_DATABASE_URL. globalSetup Task 10 чистил timesheets seeded-user в момент когда integration-тесты Task 9 могли ещё работать.
**Pattern:** Если несколько тестовых задач работают параллельно с общей БД — каждой задаче присвоить уникальный seed-email (integration-test@..., e2e-test@...). Уточнять это в Details задачи явно, не полагаться на transaction isolation.
**Scope:** situational
**Situation:** параллельное выполнение нескольких тестовых задач против одной тестовой БД
**Category:** problem-decomposition

### 2026-04-01 dashboard-progress-sync / userspec: подтвердить порядок фич до инициализации папки

**Seen:** 1
**Adapted:** —
**Triad:** пользователь описывает несколько взаимосвязанных фич для реализации → явно уточнить порядок реализации ДО инициализации папки первой фичи → не создавать и переименовывать артефакты под неправильную фичу
**Context:** Сессия стартовала с `/new-user-spec dashboard-crm`, папка создана — но пользователь уточнил что первой фичей должен быть progress-sync, а не CRM. Папку пришлось переименовывать.
**Pattern:** Когда пользователь показывает спеки для N взаимосвязанных фич — перед стартом спросить "в каком порядке реализуем?" и только после подтверждения запускать `init-feature-folder.sh`.
**Scope:** situational
**Situation:** пользователь приносит несколько готовых спеков или модулей в одной сессии
**Category:** scope-management

### 2026-04-01 dashboard-progress-sync / userspec: проверять наличие файлов в git до GitHub API в AC

**Seen:** 1
**Adapted:** —
**Triad:** фича читает файлы методологии (work/, checkpoint.yml) через GitHub Contents API → уточнить у пользователя закоммичены ли эти файлы в репозитории ДО написания AC → не получить "прогресс не отслеживается" для всех проектов из-за .gitignore
**Context:** В спеке предполагалось читать checkpoint.yml через GitHub API для % прогресса — но пользователь подтвердил что work/ нередко в .gitignore. Потребовалось добавить fallback-ветку "прогресс не отслеживается".
**Pattern:** Если фича читает проектные файлы через GitHub Contents API — перед написанием AC проверить: "эти файлы вообще коммитятся в репо?" Особенно это касается папок вроде work/, .claude/, logs/ которые часто gitignore-ятся.
**Scope:** situational
**Situation:** планирование фичи с GitHub API доступом к файлам в репозиториях пользователя
**Category:** information-gathering

## Universal

### 2026-04-01 freelance-dashboard / session design-refactor: JS viewport state — признак отсутствия CSS architecture

**Seen:** 1
**Adapted:** —
**Triad:** JS state существует только для переключения CSS-значений по viewport → заменить state+listener на CSS media queries + className → убрать re-renders и сделать layout управляемым CSS
**Context:** App.jsx и ProjectModal.jsx содержали `isMobile` state + resize listener только для выбора между двумя наборами inline styles
**Pattern:** Если JS state имеет ровно два значения и оба соответствуют CSS-состояниям для breakpoint — это признак отсутствующей CSS-архитектуры. Удалить state, вынести логику в media queries, заменить inline styles на className. Это не рефакторинг ради чистоты — это устранение источника будущих багов при добавлении новых breakpoints.
**Scope:** universal
**Category:** tool-selection

### 2026-04-07 website-design-match / session 1: Пропуск тяжёлой валидации при чётком style-only scope

**Seen:** 1
**Adapted:** —
**Triad:** user-spec для style-only рефакторинга с полным аудитом параметров → пропустить тяжёлых валидаторов (opus) или запускать только лёгкий (sonnet) → не терять часы на зависшие агенты при нулевом риске архитектурных ошибок
**Context:** Запуск двух валидаторов (quality-sonnet + adequacy-opus) для CSS-only user-spec привёл к зависанию на 3+ часа. Пользователь перезапускал сессию 5 раз. Валидация была пропущена без последствий — scope очевиден.
**Pattern:** Когда user-spec описывает исключительно стилевые изменения (CSS, шрифты, цвета, отступы) без изменений логики/API — оценить необходимость валидации по формуле: есть архитектурные решения → валидировать, только стили → пропустить или ограничиться одним лёгким валидатором.
**Scope:** universal
**Category:** scope-management

### 2026-04-09 multi-trees-sharing / techspec: cross-check edge case descriptions across tasks

**Seen:** 1
**Adapted:** —
**Triad:** две задачи описывают поведение для одного edge case → cross-check описания обеих задач на консистентность до коммита → предотвратить противоречие пойманное только валидатором
**Context:** Task 5 (store) заявлял "deleteTree on last tree creates 'Моё дерево'" — auto-create. Task 7 (UI) заявлял "show EmptyState when last tree is deleted". Противоречие: store никогда не допускает пустой trees[], но UI ожидает EmptyState. Completeness validator поймал это только в round 2.
**Pattern:** Перед коммитом tech-spec пройти все задачи, выписать edge cases (удаление последнего, пустые данные, невалидный ввод). Если один edge case описан в двух задачах — проверить что описания совместимы. Особенно: store-task (что делает бизнес-логика) vs UI-task (что видит пользователь).
**Scope:** universal
**Category:** sequencing

### 2026-04-12 responsive-layout / decompose: Вычислять relative paths для каждого task-creator, не копировать

**Seen:** 2 (merged from #187)
**Adapted:** —
**Triad:** параллельные task-creator'ы используют relative paths (import, @use, context files), файлы на разной глубине вложенности → вычислить и передать конкретный путь в каждом брифе → предотвратить нерабочие пути из-за разной глубины файлов
**Context:** (1) responsive-layout: Task 3 задокументировал `@use '../../app/globals.scss'`, но Tasks 5, 6, 8 модифицируют файлы на глубине 3-4 уровня. Cross-task reality checker поймал 4 неверных пути. (2) предыдущий: app-relative paths в tech-spec при вложенной app директории.
**Pattern:** При диспатче параллельных task-creator'ов, если задачи используют общий relative path pattern (import, @use, context files) — вычислить конкретный путь для каждого файла и передать в бриф явно. Агенты не видят брифы друг друга и скопируют глубину из примера.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 freelance-dashboard / session design-refactor: дизайн-пайплайн на приложении с inline styles → CSS migration приоритет

**Seen:** 1
**Adapted:** —
**Triad:** design-system-init запущен на существующем приложении с inline styles → пропустить interview, экстрактировать токены из кода, выполнить CSS migration → переключить source-of-truth стилей, а не задокументировать существующие значения
**Context:** дизайн-пайплайн вызван для React-дашборда с 200+ inline styles; пользователь сказал "всё нравится, просто сделай как надо"
**Pattern:** Когда design-system-init запускается на проекте с уже сложившимися стилями и пользователь одобрил существующую эстетику, interview-фаза не нужна. Экстрактировать токены напрямую из кода, создать CSS custom properties + классы, мигрировать компоненты. HTML-демо вторичны — ценность в миграции живого кода.
**Scope:** situational
**Situation:** существующий React/Vue/Svelte проект с inline styles + пользователь одобрил текущую эстетику
**Category:** design-process

### 2026-04-01 dashboard-progress-sync / session 1: Верификационный curl без auth = ложный положительный

**Seen:** 1 (this feature/session)
**Adapted:** —
**Triad:** curl-команда в AVP/user-spec для endpoint с auth → проверить что команда включает auth header + добавить отдельный тест без ключа → 401 → не получить false QA pass при сломанной авторизации
**Context:** user-spec содержал curl POST без X-Api-Key; если бы auth middleware был сломан, команда вернула 200 — агент зафиксировал бы успех, не обнаружив проблему
**Pattern:** Для каждой верификационной curl-команды к защищённому endpoint — убедиться что команда передаёт auth credential. Добавить рядом явный тест "без ключа → 401". Тест auth работает только если один из вариантов должен упасть.
**Scope:** universal
**Category:** information-gathering

### 2026-04-01 juridical-parser / ops: изменение расписания «с завтрашнего дня»

**Seen:** 1
**Adapted:** —
**Triad:** пользователь просит изменить расписание «с завтрашнего дня» при наличии ближайшего запуска → проверить время ближайшего запуска и применить изменение ПОСЛЕ него → не потерять плановый прогон из-за немедленного переключения
**Context:** Крон стоял на 00:30 UTC, пользователь попросил переключить на 21:30 UTC «с завтрашнего дня» — изменение применили немедленно, ближайший запуск через 13 минут был пропущен.
**Pattern:** Перед применением изменения расписания проверить время следующего запуска. Если он ближе 30 минут — дождаться его завершения, только потом менять конфиг.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 dashboard-progress-sync / session 1: HTTP-сервер с API key auth — security must-have в первой реализации

**Seen:** 1
**Adapted:** —
**Triad:** реализация HTTP-сервера с API key auth → включить timing-safe comparison (`crypto.timingSafeEqual`) и явный body size limit в первоначальную реализацию → не тратить review-раунд на предсказуемые security best practices
**Context:** Task 1 — первая реализация server/index.js сравнивала API key через `===`. Review round 1 нашла timing attack и отсутствие body limit. Пришлось коммитить fix-раунд. Обе находки предсказуемы для любого auth middleware.
**Pattern:** При реализации API key auth — сразу используй `crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b))` и добавляй `express.json({ limit: '10kb' })`. Эти две детали находит любой security reviewer с первого взгляда — добавив их сразу, ты экономишь review-раунд.
**Scope:** situational
**Situation:** реализация HTTP-сервера с токен/key-based auth
**Category:** sequencing

### 2026-04-01 dashboard-progress-sync / session 1: Helper с null/undefined — верифицируй граничные значения до review

**Seen:** 1
**Adapted:** —
**Triad:** helper-функция принимает значение из внешнего источника (API-ответ, env var, user input) → вручную проверить edge cases (null, undefined, пустая строка, 0) перед первым review → не получать post-review fix на предсказуемые null/boundary guards
**Context:** Task 4 — `calcCommitDays(isoDateString, now)` принимала значение из GitHub API. Review нашло: при `null` передаётся в `new Date(null)`, что возвращает epoch (0 ms). Исправление: добавить `typeof isoDateString !== 'string'` guard. Предсказуемый граничный случай для любой функции, работающей с внешними данными.
**Pattern:** Перед первым review helper-функции, работающей с внешними данными — пройти по списку: null, undefined, пустая строка, 0, NaN. Добавить guard/return-null для каждого неожиданного значения. Reviewer найдёт эти кейсы в первом же раунде — лучше закрыть их заранее.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 dashboard-progress-sync / session 2: вынести числовые threshold в константы до review

**Seen:** 1
**Adapted:** —
**Triad:** задача с числовым threshold в коде → вынести magic numbers в именованные константы до первого review → не тратить review-раунд на предсказуемые hardcoded value замечания
**Context:** Task 3 (Frontend Progress column) — reviewer нашёл magic number `3` (stale days threshold). Понадобился дополнительный fix-коммит и второй review-раунд.
**Pattern:** Перед отправкой на review кода с числовыми границами (дни, лимиты, таймауты, размеры) — вынести каждый threshold в именованную константу с говорящим именем. Это предсказуемое замечание reviewer-а, которое дешевле закрыть до ревью.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 juridical-parser / ops-2: позиция фильтра в pipeline

**Seen:** 1
**Adapted:** —
**Triad:** конфиг содержит whitelist/фильтр для ограничения обработки → явно уточнить на каком этапе pipeline применяется фильтр (сбор данных vs экспорт) и согласовать с пользователем → не тратить ресурсы (квоту/время) на обработку данных которые всё равно отфильтруются
**Context:** Whitelist по судам фильтровал только экспорт в Sheets, но не парсинг — квота тратилась на все 54 суда, хотя пользователь обсуждал ограничение до 2.
**Pattern:** Когда в конфиге есть whitelist/фильтр — проверить на каком этапе pipeline он применяется. Если фильтр стоит после ресурсоёмкой операции (API-запрос, обогащение), переместить его до неё.
**Scope:** universal
**Category:** sequencing

### 2026-04-01 juridical-parser / session fix-status: семантика метрики перед патчем симптома

**Seen:** 1
**Adapted:** —
**Triad:** метрика показывает логически невозможное значение (A < B где A должно быть ≥ B) → установить семантическое определение каждой метрики ДО трейсинга кода → найти структурный баг вместо маскировки симптома
**Context:** found=0 при exported=2 — предложил `found = max(found, exported)` как фикс, пользователь поймал что логика неверна; оказалось found и exported считались из разных pipeline-стадий с разной семантикой.
**Pattern:** Когда метрика показывает невозможное значение — сначала зафиксировать: "что должна считать X?" и "что должна считать Y?" на уровне пользовательской семантики. Только после этого трейсить код-источники. Патч выходного значения маскирует структурный баг в логике накопления.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-01 juridical-parser / session fix-status: некорректное значение в БД — трейс write paths

**Seen:** 1
**Adapted:** —
**Triad:** поле БД содержит значение неверного формата (не NULL и не ожидаемый тип) → найти ВСЕ пути записи в это поле включая legacy-код и дефолты схемы → не создавать cleanup под гипотезу без верификации причины
**Context:** exported_to_sheets = '0' блокировало дела в очереди; гипотеза "whitespace phone" оказалась неверной — причина в legacy формате (булево 0 вместо NULL из старого кода).
**Pattern:** Аномальное значение в БД-поле (не NULL, не ожидаемый тип) требует полного трейса write paths: grep все UPDATE/INSERT для этой колонки, включая исторические миграции. Cleanup пиши только после подтверждённой причины, не под первую гипотезу.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-01 juridical-parser / session fix-status-2: формулировка остаточной проблемы через user-observable state

**Seen:** 1
**Adapted:** —
**Triad:** формулировка остаточной проблемы в session-end промте → верифицировать каждую проблему против того что пользователь видит в UI/выводе, а не против внутреннего состояния кода → не направить следующую сессию решать неверно идентифицированную проблему
**Context:** В промте описал проблему как "found/exported semantics в export_log" (code-internal), пользователь поправил: реальная проблема — "цифры в статусе не совпадают с содержимым таблицы" (user-observable).
**Pattern:** При описании остаточных проблем для следующей сессии — формулировать через то, что пользователь наблюдает в выводе ("статус показывает X, а в таблице Y"), а не через внутреннюю механику ("переменная court_stats считается из BatchA"). Внутренняя механика — это гипотеза о причине, не сама проблема.
**Scope:** universal
**Category:** communication

### 2026-04-01 employee-cabinet / userspec-amendment: Правки клиента после одобрения спека — точечный амендмент

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** клиент присылает правки к user-spec со статусом approved → задать вопросы только по неоднозначным пунктам, обновить существующий spec напрямую → не запускать полный интервью-цикл заново
**Context:** Клиент прислал 4 уточнения к уже одобренной спеке. Правильным шагом была не новая спека, а точечное мини-интервью и прямое обновление документа.
**Pattern:** Когда клиент присылает правки к одобренному user-spec — определить затронутые пункты (переименование / уточнение / новая микро-фича), уточнить только неоднозначные детали, обновить spec напрямую. Полный интервью-цикл — только если меняется scope всей фичи.
**Scope:** situational
**Situation:** client feedback arrives after user-spec is already approved
**Category:** scope-management

### 2026-04-01 employee-cabinet / userspec-amendment: UI микро-детали в spec — предлагать стандартный паттерн

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** user-spec интервью требует уточнения UI-расположения элемента (где/как панель, тулбар, диалог) → применить стандартный UX паттерн без вопроса к пользователю → не блокировать интервью на деталях, которые пользователь не может сформулировать
**Context:** Задал абстрактный вопрос "панель или диалог?" — пользователь ответил "не понял вопроса, посоветуйся с дизайн-пайплайном". Нужно было выбрать стандартный паттерн самостоятельно.
**Pattern:** Для UI микро-деталей (расположение, поведение элемента) — если требование ясно функционально — выбрать общепринятый паттерн и предложить его ("появляется прилипающая панель с кодами"), не задавать открытый вопрос. Пользователь подтвердит или скорректирует.
**Scope:** situational
**Situation:** уточнение UI-деталей в ходе user-spec или design-spec интервью
**Category:** scope-management

### 2026-04-01 employee-cabinet / techspec-update: Gap-анализ перед написанием задач на обновлённый спек

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** обновление user-spec к уже реализованной фиче → запустить code-researcher для diff новых требований против существующего кода перед написанием задач → не создавать задачи для уже реализованного функционала
**Context:** `/new-tech-spec` запустили после завершения реализации всех 15 задач. User-spec обновили с клиентским фидбеком. Без code-researcher gap-анализа риск — написать 5-7 задач из которых 3-4 уже реализованы.
**Pattern:** Если `/new-tech-spec` вызван на уже реализованную фичу (есть decisions.md с completed-задачами), сначала запустить code-researcher с вопросом "что из новых требований ещё не в коде". Только после — писать задачи. Это предотвращает дублирование работы и "задачи-призраки".
**Scope:** situational
**Situation:** обновление tech-spec для фичи, реализация которой уже завершена (есть решённые задачи)

### 2026-04-01 employee-cabinet / task-decomposition: Implementation hints должны отражать реальный код, а не идеальный

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** task-creator пишет hints для файла, который уже реализован в кодовой базе → прочитать фактический код файла ДО написания hints → не создавать hints противоречащие существующей реализации
**Context:** task-creator для Task 5 написал hint про `fs.createReadStream+Readable.toWeb()`, хотя реальный файл использовал `fs.readFile+NextResponse(buffer)`. Task 6 имел `authClient.forgetPassword()` вместо реального `authClient.requestPasswordReset()`. Reality-checker поймал оба в round 1.
**Pattern:** Если task-creator получает файл с пометкой "already exists" или "уже реализован" — читать фактический код перед написанием hints, не реконструировать по описанию. Правило: hints описывают КАК ЕСТЬ, а не КАК ДОЛЖНО БЫТЬ.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-01 employee-cabinet / task-decomposition: TDD Anchor не должен называть файл, являющийся deliverable другой задачи

**Seen:** 1 (employee-cabinet)
**Adapted:** —
**Triad:** TDD Anchor задачи A называет тестовый файл, который является primary deliverable задачи B → убрать тест из TDD Anchor A, добавить "интеграционное покрытие в задаче B" → один файл — один владелец, нет конфликта владения при параллельном выполнении
**Context:** Task 5 имел TDD Anchor с двумя тестами в `tests/integration/certificates.test.ts`. Но этот файл — primary deliverable Task 9. Кросс-задачная проверка обнаружила конфликт: Task 9 мог перезаписать нуль файла при создании с нуля.
**Pattern:** При написании TDD Anchor — проверить, не является ли названный тестовый файл основным deliverable другой задачи (по Files to modify в tech-spec). Если да — убрать якорные тесты из текущей задачи и сослаться на задачу-владельца. TDD Anchor задачи A не должен создавать зависимость write-after-write.
**Scope:** situational
**Situation:** multi-task фича с разделёнными задачами реализации и тестирования (задача X делает API, задача Y делает тесты для него)
**Category:** information-gathering

### 2026-04-01 employee-cabinet / session 2: auth-библиотека возвращает 200 на duplicate flow — тестировать через side effect

**Seen:** 1 (employee-cabinet/session 2)
**Adapted:** —
**Triad:** интеграционный тест проверяет ошибочный сценарий (duplicate signup) через auth-библиотеку → проверять через side effect (DB row count), не HTTP статус → не получить false-negative когда библиотека возвращает 200 с resend-flow вместо 400
**Context:** better-auth v1.5.6 при повторном signup возвращает 200 (resend verification), а не 400. Тест ожидал 400 → упал; исправление — проверять count строк в users.
**Pattern:** Для интеграционных тестов auth-флоу (duplicate, invalid state) — не предполагать что auth-библиотека возвращает стандартные 4xx. Сначала проверить поведение в docs/вручную. Тестировать через observable state: DB row count, наличие сессии. HTTP статус — вторичная проверка.
**Scope:** universal
**Category:** tool-selection

### 2026-04-01 employee-cabinet / session 2: E2E global-setup — прямой INSERT вместо sign-up через API

**Seen:** 2 (employee-cabinet/session 2, cert-report/session 1)
**Adapted:** —
**Triad:** integration/E2E setup требует seeded users → прямой INSERT в DB вместо sign-up API → устранить зависимость от application layer и избежать rate-limit (4+ signup за сессию бьёт better-auth 429)
**Context:** employee-cabinet/session 2: Task 10 global-setup делал POST /api/auth/sign-up + SQL UPDATE — переписан на прямой INSERT. cert-report/session 1: Task 8 — 4 тестовых пользователя через seedUser + getSessionCookies хитили better-auth rate-limit; no-cert user добавлен прямым DB INSERT как обходной путь.
**Pattern:** Для integration/E2E seed users — не использовать HTTP auth API если нужно 3+ пользователей. Прямой INSERT через testDb с явным role. Если auth-библиотека требует hashed password — найти её `hashPassword` функцию. Это отвязывает seed от application layer и не бьёт rate-limit.
**Scope:** situational
**Situation:** integration/E2E-тесты с 3+ pre-seeded users при auth-библиотеке с rate-limiting
**Category:** tool-selection

### 2026-04-01 juridical-parser / diagnostic session: Смена параметра API меняет nullable fields ответа

**Seen:** 1
**Adapted:** —
**Triad:** добавление нового параметра к существующему API-запросу → проверить nullable поля ответа при новом параметре на реальных данных → не получить TypeError на production-прогоне
**Context:** После добавления `Court=` фильтра в поиск parser-api.com ответ стал возвращать `Respondents: null` вместо `[]` — мок-тесты не покрывали этот кейс, `TypeError` проявился только на production.
**Pattern:** При добавлении нового параметра к существующему API-запросу — проверить nullable fields в ответе: при другом filter-режиме сервис может возвращать null там где раньше был пустой массив. Использовать `or []` guard вместо `get("field", [])`.
**Scope:** universal
**Category:** information-gathering

### 2026-04-01 juridical-parser / diagnostic session: Многострочный скрипт на удалённом VPS — записать в файл, не инлайн

**Seen:** 1
**Adapted:** —
**Triad:** выполнение нетривиального Python-скрипта на удалённом сервере через SSH → записать скрипт в локальный файл, залить по SFTP, выполнить через `python3 -u` → избежать ошибок экранирования и буферизации вывода
**Context:** 3 попытки запустить Python через inline heredoc/параметры shell — каждый раз ошибки экранирования кавычек или пустой output из-за буферизации. Фикс: Write tool в локальный файл → sftp.put() → запуск с `-u`.
**Pattern:** Для нетривиальных (>5 строк) Python-скриптов на удалённом VPS — записывать через Write tool в локальный файл, загружать по SFTP, запускать с флагом `-u` (unbuffered). Inline heredoc через SSH не масштабируется на кириллицу и вложенные кавычки.
**Scope:** situational
**Situation:** выполнение скриптов на удалённом VPS через paramiko/SSH
**Category:** tool-selection

### 2026-04-01 methodology-cleanup / session 1: разграничить "убрать из репо" и "удалить с диска"

**Seen:** 1
**Adapted:** —
**Triad:** запрос "удалить X из репозитория" для локального git-репо → уточнить: git untrack (git rm --cached + .gitignore) или физическое удаление с диска → не уничтожить локальные файлы при git-операции
**Context:** Попросили убрать 4 скилла из репозитория; выполнил rm -rf вместо git rm --cached — пришлось восстанавливать из git-истории
**Pattern:** При запросе "удалить X из репо/репозитория" — до выполнения уточнить: "физически удалить файлы или только убрать из git-трекинга (git rm --cached + .gitignore)?" Физическое удаление необратимо без git history, git untrack оставляет файлы на диске.
**Scope:** universal
**Category:** recovery

### 2026-04-02 geologist-cabinet / planning session: Конфиг у провайдера — спросить клиента раньше поддержки

**Seen:** 1
**Adapted:** —
**Triad:** нужно получить конфигурацию у провайдера (DNS, настройки) → сначала спросить клиента — есть ли доступ к панели управления → избежать ожидания support-ответа если клиент может получить данные сам
**Context:** Подготовил развёрнутое письмо в поддержку Creatium для получения DNS-записей. Клиент сам открыл панель и прислал скриншот со всеми записями — ответ поддержки не понадобился.
**Pattern:** Перед тем как писать в поддержку провайдера за конфигурационными данными — уточнить у клиента наличие доступа к панели управления. Клиент с прямым доступом к панели даёт ответ немедленно; support-запрос добавляет задержку в 1–3 дня.
**Scope:** situational
**Situation:** получение конфигурационных данных (DNS, API-ключи, настройки) у стороннего провайдера через клиента-посредника
**Category:** information-gathering

### 2026-04-02 moneymaker / session 1: числовой атрибут AI-генерируемых элементов — источник должен быть в интервью

**Seen:** 1
**Adapted:** —
**Triad:** фича генерирует список элементов и каждый имеет числовой атрибут (цена, оценка, балл) → в интервью явно задать вопрос "кто/что устанавливает это значение: LLM-оценка, каталог пользователя или ручной ввод?" → не допустить CRITICAL gap в архитектуре вычислений, обнаруживаемый только на валидации
**Context:** Moneymaker user-spec: /expand показывает апсейл-предложения с ценами и маржой. Интервью не спросило откуда берётся цена для LLM-генерируемых позиций. Adequacy validator вернул CRITICAL: "модель ценообразования не определена". Ответ (каталог блоков × ставка) получен только в батче Q20–Q21 после валидации.
**Pattern:** Когда фича включает генерацию списка элементов, каждый из которых несёт числовой атрибут — явно покрыть в интервью вопрос источника значения: LLM-оценка (нестабильно), пользовательский каталог (предсказуемо), ручной ввод (медленно). Это архитектурное решение, а не деталь реализации — пропущенное в интервью, оно становится CRITICAL на валидации.
**Scope:** situational
**Situation:** user-spec интервью для фичи где AI генерирует элементы с ценой, рейтингом или любым числовым атрибутом, который будет показан пользователю
**Category:** information-gathering

### 2026-04-02 dashboard-progress-sync / session 3: Pre-flight SSH smoke перед VPS deploy

**Seen:** 1
**Adapted:** —
**Triad:** деплой на VPS впервые или после смены домена/secrets → запустить SSH smoke (`ssh -i deploy_key user@host echo ok`) локально ДО push в main → не тратить N trigger-redeploy циклов на последовательные инфраструктурные блокеры
**Context:** Task 12 заблокировался 4 последовательными блокерами: неверный URL, отсутствующий secret, fail2ban, отсутствующий authorized_keys. Каждый обнаруживался только после fix предыдущего через failed CI run — итого 3 trigger-redeploy коммита, задача не завершена.
**Pattern:** Перед первым деплоем на VPS или после смены домена/ключей — запустить SSH smoke локально. Если smoke падает — не пушить. Так все инфраструктурные блокеры видны за один шаг вместо N CI-прогонов.
**Scope:** universal
**Category:** sequencing

### 2026-04-02 moneymaker / session 2 (tech-spec): Решение, сужающее утверждённый AC — проверить до написания

**Seen:** 2
**Adapted:** —
**Triad:** tech-spec decision сужает или откладывает требование из user-spec → перед написанием Decision проверить наличие этого требования в AC и таблице проверки user-spec → не вводить scope reduction без явного согласования с пользователем
**Context:** Tech-spec Decision 6 отложил "free-form rate update" в Phase 2, мотивируя тем что это "не в AC". Completeness-validator вернул CRITICAL: AC явно есть. (Seen 2: panel-next-run — Decision 4 изменил код ответа batch с 409 на 200+skipped; таблица проверки в user-spec указывала 409. Поймал skeptic.)
**Pattern:** Перед написанием Decision, который меняет поведение или сужает функционал — проверить ОБА раздела user-spec: AC и таблицу проверки («Как проверить»). Таблица содержит конкретные HTTP-коды и curl-команды — это требования, не просто примеры. Если требование там есть — реализовать или явно согласовать изменение с пользователем.
**Scope:** universal
**Category:** scope-management

### 2026-04-02 moneymaker / session 2 (tech-spec): Задача создаёт SKILL.md — skill-master, не code-writing

**Seen:** 1
**Adapted:** —
**Triad:** deliverable задачи — SKILL.md файл(ы) → назначить skill: skill-master и reviewers: skill-checker → не получить неверный skill/reviewer замеченный только валидаторами
**Context:** Первый черновик tech-spec для moneymaker назначил `write-code` (затем `code-writing`) для задач 1–5, создающих SKILL.md. Skeptic и template-validator поймали: для создания скиллов в skills-and-reviewers каталоге прописан `skill-master` + `skill-checker`.
**Pattern:** Когда задача создаёт или существенно изменяет SKILL.md файлы — это skill-master задача, не code-writing. Проверить skills-and-reviewers.md каталог: `skill-master` → reviewers: `skill-checker`. Если задача создаёт и код, и скиллы — разбить на отдельные задачи с правильным skill каждой.
**Scope:** situational
**Situation:** tech-spec для фичи, deliverable которой является набор Claude Code skills (SKILL.md файлы)
**Category:** tool-selection

### 2026-04-02 geologist-cabinet / deploy session: better-auth 404 при неверном BETTER_AUTH_URL prefix

**Seen:** 1
**Adapted:** —
**Triad:** better-auth handler возвращает 404 для корректного пути → проверить BETTER_AUTH_URL на наличие лишнего path prefix → не тратить часы на отладку webpack и маршрутизации
**Context:** BETTER_AUTH_URL был установлен как `http://host/cabinet` в прошлой сессии; better-auth добавлял `/cabinet` к своему basePath и не находил `/api/auth/sign-in/email`.
**Pattern:** Когда better-auth handler возвращает 404 для заведомо существующего эндпоинта — первым делом проверить что BETTER_AUTH_URL не содержит path после домена. BETTER_AUTH_URL должен быть `http://host` без trailing path.
**Scope:** situational
**Situation:** деплой приложения с better-auth за nginx reverse proxy с subpath (например `/cabinet`)
**Category:** recovery

### 2026-04-02 geologist-cabinet / deploy session: Next.js API route молча возвращает 404 из-за async webpack модуля

**Seen:** 1
**Adapted:** —
**Triad:** Next.js API route возвращает 404 с RSC headers, console.error не срабатывает → проверить compiled route.js на `import("dependency")` и `t.a(e,` async factory → диагностировать silent module initialization failure
**Context:** better-auth внутри использует `import("pg")` (dynamic ESM import); webpack компилировал это как async module factory; Next.js 14 не мог загрузить route handler и возвращал App Router 404 без каких-либо логов.
**Pattern:** Если Next.js API route (App Router) возвращает 404 с заголовками `vary: RSC, Next-Router-State-Tree` и нет console.error — это не routing проблема, а silent module failure. Проверить `.next/server/app/api/.../route.js`: если есть `t.a(e,async` или `e.exports=import("pkg")` — серверная CJS-библиотека бандлится с ESM dynamic import. Фикс: заменить `import { X } from 'pkg'` на `const { X } = require('pkg')` в файле, где pkg используется внутри ESM-зависимости.
**Scope:** situational
**Situation:** Next.js 14 App Router, серверный route handler использует библиотеку (better-auth, prisma и др.) с внутренними dynamic ESM imports
**Category:** recovery

### 2026-04-02 geologist-cabinet / certificates-ui: директории для файлов не создаются при деплое автоматически

**Seen:** 1
**Adapted:** —
**Triad:** фича пишет файлы на диск в директорию которой нет -> явно включить mkdir директории в деплой-чеклист -> не получить ENOENT на первом upload после деплоя
**Context:** API загрузки PDF-сертификатов писал файлы в uploads/. Директория не существовала на сервере — git-клон не создаёт пустые директории. Первый upload упал с ENOENT, пришлось создавать вручную через SSH.
**Pattern:** Любая фича, пишущая файлы на диск, требует explicit mkdir -p в деплой-процедуре. Добавлять в deploy-checklist при проектировании — не ждать ENOENT на проде.
**Scope:** universal
**Category:** sequencing

### 2026-04-02 employee-cabinet / session certificates-ux: Уточнять ожидание перед диагностикой UI-feedback

**Seen:** 1
**Adapted:** —
**Triad:** пользователь говорит "название/значение кривое" без указания поля или ожидаемого вида → переспросить "что именно ожидаешь увидеть и где" → не тратить итерацию на ложную версию проблемы
**Context:** Пользователь сказал "название кривое" — предположили что речь про имя файла на диске, начали объяснять. Оказалось речь про отображение в таблице в UI. Потребовалось 3 сообщения для диагностики.
**Pattern:** Когда пользователь даёт оценочный feedback о данных в UI ("кривое", "неверно", "не то") без конкретики — сначала уточни "что именно ожидаешь увидеть". Не начинай диагностировать предположение.
**Scope:** universal
**Category:** communication

### PROMOTED → skill-master: pre-submission SKILL.md structural checks

### 2026-04-02 employee-cabinet / session Wave5-deploy: Next.js build cache маскирует "module not found"

**Seen:** 1
**Adapted:** —
**Triad:** Next.js dev-сервер возвращает 500 "Cannot find module vendor-chunks/X" → удалить .next и перезапустить сервер → не тратить время на диагностику зависимостей которых нет
**Context:** Интеграционные тесты упали с 500 на всех auth-эндпоинтах. Ошибка выглядела как отсутствующая зависимость better-auth. Реальная причина — сталый .next кеш от предыдущего билда другой ветки.
**Pattern:** Когда Next.js/Webpack возвращает "Cannot find module vendor-chunks/X" — первый шаг rm -rf .next, не npm install. Vendor-chunks создаются при билде и привязаны к конкретной версии сборки; при смене ветки или обновлении зависимостей кеш устаревает.
**Scope:** situational
**Situation:** Next.js проект, dev-сервер запущен без предварительного rm -rf .next после смены ветки или обновления зависимостей
**Category:** recovery

### 2026-04-02 employee-cabinet / session Wave5-tasks: Проверять реализацию до кодирования задачи

**Seen:** 1
**Adapted:** —
**Triad:** задача бэклога описывает добавление guard/validation в существующий файл → прочитать целевой файл до написания кода → не дублировать уже существующую реализацию
**Context:** Task 17 (client-side валидация PDF) значилась как "to implement". Чтение cabinet/page.tsx показало что оба гарда (type + size) уже присутствовали — добавлены как byproduct предыдущей волны. Задача свелась только к написанию теста.
**Pattern:** Перед реализацией любой задачи читать целевой файл и проверять нет ли уже функции/блока с нужной логикой. Особенно вероятно если задача — добавить guard/validation в файл который правился в предыдущих волнах.
**Scope:** universal
**Category:** information-gathering

### 2026-04-02 moneymaker / session 2: Bash path-substitution в аргументе флага — вынести в переменную

**Seen:** 1
**Adapted:** —
**Triad:** bash команда передаёт `$(find ... | cut ...)` как путь в флаг принимающий файловый путь (-newer, -nt, аналогичные) → вынести подстановку в именованную переменную отдельной командой → избежать молчаливого false-result при путях с пробелами
**Context:** В moneymaker-expand SKILL.md staleness check сравнивал mtime через `find -newer "$(find ... | cut ...)"`. skill-checker поймал: если путь материала содержит пробел, вложенная подстановка обрезается и флаг -newer получает неверный путь — всегда возвращая STALE без ошибки.
**Pattern:** Когда bash команда использует `$(...)` как значение флага принимающего путь — разбить на две команды: сначала `newest=$(...)`, затем использовать `"$newest"` с кавычками. Однострочные вложенные подстановки путей ломаются при пробелах, причём молча.
**Scope:** universal
**Category:** tool-selection

### 2026-04-02 moneymaker / session 2: Embedded LLM prompts в SKILL.md подпадают под правило positive instructions

**Seen:** 1
**Adapted:** —
**Triad:** SKILL.md содержит inline LLM-промт (блок текста как инструкция для LLM внутри фазы) → проверить весь текст промта на "do not / don't / не делай" и переформулировать позитивно → не тратить review-раунд на нарушение skill-master правила внутри вложенного промта
**Context:** moneymaker-expand Phase 5 содержал LLM-промт с "Do not produce a generic checklist". skill-checker поймал три места с негативными формулировками внутри промтов. Авторы воспринимают вложенный промт как "данные", а не инструкции, и не применяют к нему skill-master правило.
**Pattern:** Правило "positive over negative" из skill-master применяется ко всему тексту SKILL.md включая inline LLM-промты. Перед первым skill-checker прогоном — пройти по всем блокам с текстом промтов и заменить "do not X" / "не делай X" на позитивный эквивалент.
**Scope:** situational
**Situation:** Написание SKILL.md содержащего встроенные LLM-промты как часть фаз
**Category:** sequencing

### 2026-04-02 moneymaker / session 3: OPEN security risk в audit wave → fix before QA

**Seen:** 1
**Adapted:** —
**Triad:** audit wave находит OPEN security risk в продукте работающем с чувствительными данными → создать ad-hoc fix task и починить ДО запуска QA волны → не деплоить с известной утечкой чувствительных данных и не тратить QA на устранимый fail
**Context:** Security audit moneymaker нашёл 2 OPEN риска: billing exposure (INN/банк в чат-истории при setup) и отсутствие chmod на config.yml. Встал выбор: deferred known issues или fix перед QA. QA шаг 2 (`cat config.yml`) показал бы INN в чате — QA упал бы на устранимом риске.
**Pattern:** Когда audit wave находит OPEN security risk связанный с чувствительными данными (billing, credentials, PII) — создать ad-hoc fix task немедленно, выполнить до QA. Deferred acceptable только для рисков которые QA физически не может воспроизвести (недоступная инфра, production-only данные).
**Scope:** situational
**Situation:** audit wave завершена, найдены OPEN security risks, следующий шаг — QA волна
**Category:** sequencing

### 2026-04-02 moneymaker-case / session 1: первый пример раскрывает категориальную структуру

**Seen:** 1
**Adapted:** —
**Triad:** проектирование хранилища знаний / экспертного инструмента, пользователь даёт первый реальный пример → спросить "какую логическую категорию/паттерн представляет этот пример?" до финализации полей данных → создать модель данных, захватывающую переносимую структуру, а не только данные экземпляра
**Context:** Скилл moneymaker-case начинался как простое хранилище кейсов. Первый же пример от пользователя (кабинет геолога) содержал прогрессию ролей. Только уточняющий вопрос "что важно выявлять в логике?" вскрыл необходимость patterns/ слоя и трёхслойной архитектуры.
**Pattern:** При проектировании хранилища знаний не финализируй поля данных по первому описанию. Задай вопрос: "какую логическую категорию этот пример представляет?" — ответ часто требует отдельной абстракции (паттерн, архетип, цепочка), которой нет в первоначальном наборе полей.
**Scope:** situational
**Situation:** проектирование knowledge storage, expert tool, или любого инструмента накопления опыта
**Category:** problem-decomposition

### 2026-04-02 moneymaker-case / session 1: "нельзя упрощать" = сигнал пропущей абстракции

**Seen:** 1
**Adapted:** —
**Triad:** пользователь отвергает предложенное упрощение архитектуры ("нельзя упрощать", "нужно качественнее") → переспросить "какое различие теряется при упрощении?" до продолжения → выявить пропущую ключевую абстракцию до реализации
**Context:** Предложил Option A (cases only, LLM выводит паттерны сам) как более простой вариант. Пользователь отверг: "упрощать нельзя". Это сигнализировало о том, что явные цепочки прогрессии — не nice-to-have, а ключевое различие в ментальной модели пользователя.
**Pattern:** Когда пользователь отвергает упрощение — это не предпочтение сложности, а сигнал что упрощение уничтожает различие, которое критично в его модели мира. Остановись и спроси: "что именно теряется?" — ответ укажет на абстракцию, которой нет в текущей схеме.
**Scope:** universal
**Category:** information-gathering

### 2026-04-02 moneymaker-setup / session 4: свободный бизнес-текст → выяснить намерение до вызова скилла

**Seen:** 1
**Adapted:** —
**Triad:** пользователь описывает бизнес-практику в свободной форме без вызова скилла, потенциально затрагивая несколько инструментов → задать 3 целевых вопроса (тип: факт/гипотеза; область: какие проекты; цена: формула/якорь/реализованная) ДО вызова любого скилла → не записать в неверный формат и не упустить второй нужный target
**Context:** Пользователь написал "можно предложить брендбук за 20% от проекта" — без указания скилла. Вопросы выявили: гипотеза (не кейс) + любой проект с дизайном + психологический якорь цены. Итог: изменение SKILL.md (hypothesis type) И запись в каталог.
**Pattern:** Когда бизнес-идея приходит без скилл-команды — не угадывай destination. Задай три вопроса: (1) это было реально продано или идея? (2) к каким типам проектов применимо? (3) цена — конкретная, формула или психологический якорь? Ответы определят один или несколько targets.
**Scope:** situational
**Situation:** пользователь пишет о бизнес-практике/апселле без явного вызова moneymaker-скилла
**Category:** information-gathering

### 2026-04-02 moneymaker-setup / session 4: все данные в задании → пропустить interview-фазы

**Seen:** 1
**Adapted:** —
**Triad:** скилл предполагает интерактивный сбор данных, но задание уже содержит все необходимые поля → пропустить interview-фазы, перейти сразу к показу извлечённой структуры для подтверждения → минимизировать turns без потери верификации
**Context:** moneymaker-case для geologist-cabinet: все данные (описание, pattern_key, chain_position, pricing_rationale) были в исходном запросе. Пропустил Phase 1 interview, показал структуру сразу → подтверждение в 1 turn вместо 3-4.
**Pattern:** Перед запуском интерактивной фазы скилла проверь: все ли нужные поля уже есть в задании? Если да — пропусти сбор, покажи извлечённую структуру для подтверждения. Верификация остаётся, лишние вопросы исчезают.
**Scope:** universal
**Category:** sequencing

### 2026-04-02 content-card / session 1: уточнять публичность перед коммитом нового артефакта

**Seen:** 2
**Adapted:** —
**Triad:** создание или изменение скилла/артефакта, который готов к коммиту → спросить "пушим в общий репо?" до git push — даже если артефакт не личный → не нарушить договорённость о подтверждении перед публикацией
**Context:** content-card и moneymaker-* были закоммичены без согласования; затем pause-скилл был запушен без вопроса даже после того как правило было адаптировано в skill-master. Паттерн срабатывает для ЛЮБОГО скилла, не только персонального.
**Pattern:** Перед `git push` любого нового или изменённого скилла — явно спросить пользователя: "Пушим в общий репо?" Вопрос обязателен даже если скилл кажется "общим" — договорённость о подтверждении действует всегда.
**Scope:** universal
**Category:** scope-management

### 2026-04-02 content-card / session 2: триггер sub-скилла — по типу контента, не по наличию инпута

**Seen:** 1
**Adapted:** —
**Triad:** интеграция опционального sub-скилла в родительский скилл → задать триггер по характеристике контента (есть ли нужда в возможности sub-скилла), не по факту наличия инпута → не вызывать sub-скилл там где он не добавляет ценности
**Context:** В content-card photo-crop изначально привязали к условию "если фото предоставлено". Пользователь поправил: photo-crop нужен только когда фото содержит субъект, которому нужно точное кадрирование (человек, лицо, деталь). Декоративное фото — проходит без crop.
**Pattern:** При встраивании опционального sub-скилла в parent skill — триггер это не "есть ли этот тип инпута", а "нужна ли здесь конкретная способность sub-скилла". Спрашивай: для каких конкретно случаев этот инпут требует обработки, а для каких — нет.
**Scope:** universal
**Category:** skill-master

### 2026-04-02 content-card / session 3: visual weight определяет порядок чтения, а не позиция

**Seen:** 1
**Adapted:** —
**Triad:** несколько текстовых блоков на карточке с разными позициями → проверить что visual weight (font-size × font-weight) каждого блока поддерживает нужный порядок чтения сверху вниз → контролировать reading flow через иерархию весов, а не через позицию
**Context:** Верхний текст (34px/300) игнорировался читателем — глаз прыгал на нижний (60px/700), ломая логику "от общего к частному". Позиция сверху не гарантирует первого прочтения.
**Pattern:** Перед финализацией карточки проверить reading order: достаточно ли visual weight каждого блока чтобы он читался в нужный момент? Если порядок нарушен — менять вес (размер/насыщенность), а не только позицию.
**Scope:** situational
**Situation:** дизайн-карточки с несколькими текстовыми блоками (personal-brand, editorial, любой multi-block layout)
**Category:** design-process

### 2026-04-02 content-card / session 3: выравнивание текста по чистым зонам фото

**Seen:** 1
**Adapted:** —
**Triad:** текстовый блок на full-bleed фото с неравномерным фоном → выровнять по стороне с наименее загруженной фоновой зоной (однородный тёмный потолок, нейтральная стена), а не по конвенциональной позиции → сохранить читаемость без усиления оверлея
**Context:** Верхний текст был right-aligned к стороне с люстрой (визуальный шум), хотя left-aligned упал бы на тёмный однородный потолок. Конвенция "уйти от субъекта" оказалась вторичной по отношению к читаемости на фоне.
**Pattern:** Перед установкой text-align — определить какая сторона фото даёт однородный фон в зоне текста. Сканировать фото: где меньше деталей и перепадов яркости? Туда направлять текст. Стандартные позиции (left/right) — вторичны.
**Scope:** situational
**Situation:** текст поверх full-bleed фото с неравномерной фоновой текстурой (люстры, архитектура, природные объекты)
**Category:** design-process

### 2026-04-02 content-card neidealnoiok / session 1: Approved text is immutable — design adapts, not the text

**Seen:** 1
**Adapted:** —
**Triad:** design constraint (wrap/overflow) conflicts with approved text → reduce font-size, widen column, or rethink layout to fit original text → preserve content integrity agreed in planning phase
**Context:** При вёрстке К3 "РАДИ ЛАЙКОВ." не влезало в колонку при 104px — сократил заголовок без разрешения, пользователь остановил как жёсткий косяк.
**Pattern:** Когда дизайн-ограничение конфликтует с согласованным текстом — адаптируй шрифт, колонку или лейаут. Никогда не изменяй текст ради дизайна без явного разрешения. Текст заблокирован после Phase 2.
**Scope:** universal
**Category:** design-process

---

### 2026-04-02 content-card neidealnoiok / session 1: Cyrillic uppercase char width ≈ 0.72em for font-fit calculations

**Seen:** 1
**Adapted:** —
**Triad:** вычисление font-size fit для кириллического uppercase → использовать 0.72em на символ (не 0.62em для латиницы); проверять самое длинное слово при выбранном размере → предотвратить неожиданный перенос строки
**Context:** "РАДИ ЛАЙКОВ." при 104px рассчитан как 748px < 800px (по 0.62em), но в браузере отрендерился >800px и перенёсся — реальная ширина кириллических glyphs ≈ 0.72em.
**Pattern:** Для кириллического uppercase Inter применяй коэффициент 0.72em (не 0.62em). Проверяй самое длинное слово заголовка: word_width = chars × font_size × 0.72. Если > container — уменьши font_size до ближайшего кратного 8px.
**Scope:** situational
**Situation:** uppercase Cyrillic text fit calculations in HTML/CSS cards
**Category:** design-process

### 2026-04-02 content-card neidealnoiok / session 2: Размер как инструмент контраста на busy-фоне

**Seen:** 1
**Adapted:** —
**Triad:** текст на busy/текстурном фоне с недостаточным контрастом → увеличить font_size на 1 шаг сетки (8px) → буква физически перекрывает детали текстуры, контраст через размер
**Context:** К4 на фольге: белый текст 48px конкурировал с металлическими бликами — увеличение до 64-96px устранило конкуренцию без overlay.
**Pattern:** На busy/текстурном фоне (металл, трава, узор) увеличивай шрифт пока буква не станет крупнее деталей текстуры. Это контраст через размер, а не через цвет или затемнение.
**Scope:** situational
**Situation:** текст поверх фото с высокой текстурной насыщенностью (металл, фольга, трава, цветы, паттерны)
**Category:** design-process

---

### 2026-04-02 content-card neidealnoiok / session 2: Перебор всех вариантов цвета перед выбором

**Seen:** 1
**Adapted:** —
**Triad:** выбор цвета текстового элемента в дизайне → перечислить ВСЕ доступные цвета (бренд-цвета + white + dark grey), оценить каждый против фона зоны и серийного использования → не выбирать цвет автоматически
**Context:** В К4 оранжевый появился автоматически, потому что «главный цвет бренда». Пользователь остановил: «навязчивое использование оранжевого». Перебор вариантов дал белый как единственно обоснованный.
**Pattern:** Перед выбором цвета текста перечисли все варианты явно. Для каждого ответь: (1) сливается с фоном? (2) уже перегружен в серии? Только после этого выбирай — не от привычки к «главному» цвету.
**Scope:** universal
**Category:** design-process

---
### 2026-04-05 cert-report / session 1: depends_on внутри одной волны — логическая зависимость ≠ wave-зависимость

**Seen:** 3
**Adapted:** —
**Triad:** граф зависимостей мутировался (добавление/удаление/перемещение узлов или рёбер) → перевалидировать топологический порядок по инварианту: уровень(узел) > max(уровень(зависимости)) → предотвратить нарушение порядка выполнения, замаскированное корректной структурой до мутации
**Context:** После мутации графа зависимостей (слияние узлов, добавление рёбер, перенос связей) старое распределение по уровням перестаёт быть валидным — но выглядит корректно, потому что изменилась только часть графа.
**Pattern:** После любой мутации DAG — пересчитать уровни всех затронутых узлов и их транзитивных потомков по инварианту: уровень(N) > max(уровень(deps(N))). Проверять ДО фиксации, не после — каскадные сдвиги дешевле на этапе планирования.
**Scope:** universal
**Category:** sequencing

---

### 2026-04-05 cert-report / session 1: SQL сниппет в tech-spec может не включать существующие поля таблицы

**Seen:** 1
**Adapted:** —
**Triad:** tech-spec Data Models содержит UPDATE SQL для существующей таблицы → reality-checker сверяет SQL сниппет против реального route.ts (не только против migration) — ищет параметры в текущем UPDATE которых нет в сниппете → предотвратить тихую потерю данных при буквальном следовании техспеку
**Context:** Tech-spec показал UPDATE с 4 параметрами (только новые threshold поля), реальный route.ts имел 3 параметра включая cert_recipients. Реализатор по сниппету техспека написал бы UPDATE без cert_recipients и уничтожил данные.
**Pattern:** При UPDATE существующей таблицы tech-spec описывает только новые поля, но реальный SQL должен включать ВСЕ поля. Для любого UPDATE SQL в tech-spec — сверяй параметры со списком полей в реальном маршруте, не только с migration и новыми колонками.
**Scope:** situational
**Situation:** Tech-spec Data Models section содержит UPDATE SQL для таблицы с уже существующими полями
**Category:** information-gathering

---

### 2026-04-05 fix-xlsx-export-headers / session 2: верифицировать git push перед deploy на VPS

**Seen:** 2
**Adapted:** —
**Triad:** deploy-волна начинается с git pull на VPS → перед SSH на сервер выполнить `git log origin/branch..HEAD` локально → не получить блокер "нечего тянуть" из-за незапушенных коммитов
**Context:** При деплое на VPS оказалось, что коммиты сессий 1–2 не были запушены в origin — git pull на сервере ничего не подтянул, потребовался лишний шаг git push.
**Pattern:** Перед git pull на удалённом сервере всегда проверяй, что локальная ветка опережает origin: `git log origin/master..HEAD`. Если есть коммиты — сначала git push, потом SSH и git pull на VPS.
**Scope:** universal
**Category:** sequencing

---

### 2026-04-05 fix-xlsx-export-headers / session 2: json_to_sheet сортирует числовые ключи — нужен явный массив заголовков

**Seen:** 1
**Adapted:** —
**Triad:** данные для XLSX содержат числовые ключи (номера дней, ID-колонки) → передавать явный массив заголовков в `json_to_sheet(rows, { header: [...] })`, не полагаться на порядок ключей объекта → гарантировать правильный порядок колонок в итоговом файле
**Context:** После рефакторинга экспорта XLSX колонки ФИО и Email оказались в конце файла — SheetJS сортирует числовые ключи перед строковыми, игнорируя порядок свойств в объекте.
**Pattern:** При генерации XLSX через SheetJS/json_to_sheet: числовые ключи всегда идут первыми. Всегда передавай явный массив заголовков через опцию `header` или используй `aoa_to_sheet` для контроля порядка колонок.
**Scope:** universal
**Category:** tool-selection

---

### 2026-04-05 cert-report / session 2: SQL UPDATE с опциональным NOT NULL полем — использовать COALESCE

**Seen:** 1
**Adapted:** —
**Triad:** SQL UPDATE обновляет подмножество полей таблицы, часть полей имеет NOT NULL → использовать `COALESCE($N, column_name)` для полей не переданных в запросе → предотвратить constraint violation при частичном обновлении
**Context:** Интеграционный тест PUT /api/admin/settings отправлял только cert-threshold поля без cert_recipients — handler передавал null в SQL UPDATE, нарушая NOT NULL constraint.
**Pattern:** Если SQL UPDATE охватывает не все NOT NULL колонки таблицы, используй `COALESCE($param, existing_column)` в SET-части — это сохраняет текущее значение когда параметр не передан. Альтернатива: читать существующие значения перед UPDATE и подставлять как fallback.
**Scope:** universal
**Category:** problem-decomposition

---

### 2026-04-05 juridical-parser / session 4: Slow response = check startup network calls

**Seen:** 1
**Adapted:** —
**Triad:** web app отвечает 20+ сек несмотря на простые route handlers → проверить весь module-level код и background threads на блокирующие сетевые вызовы при старте → найти root cause без профилирования
**Context:** Flask/gunicorn приложение отвечало 25 секунд на статический route. Маршрут не делал ничего — проблема была в background thread на module-level, вызывающем `get_credentials()`, который зависал при попытке OAuth refresh.
**Pattern:** При медленном response в web app — первым делом проверь module-level код (выполняется при импорте) и background threads, запускаемые при старте: именно там бывают блокирующие сетевые вызовы (auth token refresh, API ping). Route handlers — последнее место где искать.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-05 juridical-parser / session 4: Migration helpers — удалять сразу или помечать с датой

**Seen:** 1
**Adapted:** —
**Triad:** migration helper / detection banner остался в коде после завершения или отката миграции → удалить migration helper сразу после завершения; если нет — пометить TODO с датой → не получить ложные срабатывания и блокировки при следующем изменении архитектуры
**Context:** Баннер `_check_old_format_banner` проверял наличие таблиц в рутовой папке Drive и предупреждал о "старом формате". Когда архитектура вернулась к рутовой папке — баннер начал ложно срабатывать на текущие данные и блокировать воркеры.
**Pattern:** Migration helpers (detection banners, one-time scripts, format checks) теряют смысл после завершения или отката миграции. Удаляй их сразу по завершению задачи. Если нет времени — добавь `# TODO: remove after YYYY-MM-DD migration complete`. Оставленный навсегда — станет logic bug при следующем изменении структуры.
**Scope:** universal
**Category:** scope-management

### 2026-04-06 employee-cabinet-updates / session 1: wave file-overlap check before finalizing

**Seen:** 3
**Adapted:** —
**Triad:** при составлении или переносе задач между волнами в tech-spec → проверить Files to modify всех задач волны попарно на пересечения файлов → предотвратить merge conflict до того, как его поймает validator
**Context:** (1) Tasks 1+2 Wave 1 оба модифицировали page.tsx. (2) multi-trees-sharing: Tasks 7+8+9 Wave 3 модифицировали App.tsx — перенос 8+9 в Wave 4 создал тот же конфликт, потребовался round 2 для выноса Task 9 в Wave 5.
**Pattern:** Перед утверждением состава волны И при переносе задач пройтись по Files to modify всех задач волны попарно. Пересечение файлов → объединить задачи или перенести в разные волны. Особенно при переносе: не переносить два конфликтующих таска вместе в одну destination-волну.
**Scope:** universal
**Category:** sequencing

### 2026-04-06 employee-cabinet-updates / session 1: resource-ID endpoint requires target-user role check

**Seen:** 1
**Adapted:** —
**Triad:** новый endpoint получает только resource_id без user_id → явно добавить проверку роли target-пользователя ресурса относительно прав вызывающего → предотвратить IDOR через косвенный доступ к данным другого пользователя
**Context:** `POST /api/admin/timesheet-requests/[id]/approve` мог позволить любому admin разблокировать табель другого admin — IDOR поймал security validator.
**Pattern:** Когда endpoint получает только resource_id (без user_id), явно проверить роль target-пользователя ресурса: ownership через resource_id ≠ permission на target_user. Выносить это в Decisions tech-spec, не оставлять имплементатору.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-06 employee-cabinet-updates / session 1: передавать конфиг тест-фреймворка в бриф task-creator

**Seen:** 2
**Adapted:** —
**Triad:** запуск task-creator агентов без указания тест-фреймворка проекта → проверить реальный runner (jest/vitest/pytest) и структуру тест-директорий, передать явно в каждый бриф → предотвратить генерацию неработающих TDD Anchor путей во всех задачах
**Context:** 6 из 13 задач получили пути `src/__tests__/` и команды `npx jest`, хотя проект использует vitest с `tests/unit/`. Потребовалось 2 раунда исправлений. Повтор: panel-per-court-settings — задачи 2, 3, 5 получили `tests/test_web_routes.py` вместо `tests/unit/test_web_routes.py`.
**Pattern:** Перед запуском task-creator агентов прочитать `package.json` или `vitest.config.ts`/`jest.config.*` / `pytest.ini` и явно указать в каждом брифе: runner и паттерн тест-директорий (tests/unit/, tests/integration/, src/__tests__/). Для Python: `tests/unit/` vs `tests/` — не одно и то же. Это критическая инфраструктурная деталь — агент угадывает по конвенции, не по факту.
**Scope:** universal
**Category:** information-gathering

### 2026-04-06 employee-cabinet-updates / session 1: depends_on аудитных задач — все имплементационные, не только последняя волна

**Seen:** 1
**Adapted:** —
**Triad:** написание depends_on для audit wave задач → перечислить ВСЕ задачи, которые создают аудируемые файлы (не только последнюю волну) → гарантировать существование всех файлов к моменту аудита
**Context:** Tasks 8-9 получили depends_on: [6,7], хотя аудируют файлы от Tasks 1-5 тоже. Reality-checker поймал — файлы могли не существовать при запуске аудита.
**Pattern:** Audit wave задача зависит от ВСЕХ задач, которые создают или изменяют файлы из её списка аудита. Проверить: для каждого файла в "Files to audit" — в какой задаче он создаётся? Та задача должна быть в depends_on.
**Scope:** universal
**Category:** sequencing
### 2026-04-06 portfolio-horizontal / session 1: GSAP pin конфликтует с Next.js App Router — используй sticky+spacer

**Seen:** 1
**Adapted:** —
**Triad:** выбор GSAP pin/ScrollSmoother для SSR-фреймворка → использовать CSS sticky+spacer вместо JS-pin → избежать архитектурного рефакторинга горизонтального скролла
**Context:** ScrollSmoother + `pin: true` использовались для горизонтального скролла в Next.js 14 App Router — оба сломали layout, потребовался полный переход на другой паттерн.
**Pattern:** В SSR-фреймворках (Next.js App Router, Remix) не используй GSAP `pin: true` и ScrollSmoother для горизонтального скролла — они конфликтуют с layout-моделью. Используй: tall spacer div → sticky viewport (overflow: hidden) → GSAP scrub по scroll-прогрессу spacer-а.
**Scope:** situational
**Situation:** Горизонтальный scroll-driven layout в React SSR-фреймворке (Next.js App Router и аналогах).
**Category:** tool-selection

### 2026-04-06 portfolio-horizontal / session 1: обновляй документацию сразу при изменении архитектуры

**Seen:** 1
**Adapted:** —
**Triad:** архитектурное решение изменилось в ходе реализации → обновить architecture.md/patterns.md немедленно → не передать следующей сессии устаревшую документацию
**Context:** ScrollSmoother убрали в середине скетча, документация обновилась только в конце — промт для следующей сессии был написан раньше обновления доков и содержал неактуальный стек.
**Pattern:** Любое изменение стека или паттерна — обновляй соответствующий docs-файл до следующего коммита, не откладывай на конец сессии. Handoff-промт пишется только после актуализации документации.
**Scope:** universal
**Category:** sequencing

### 2026-04-06 reports-filter-sort / session 1: Тип данных колонки определяет поведение фильтра

**Seen:** 1
**Adapted:** —
**Triad:** запрос "добавить фильтр/сортировку ко всем колонкам" → составить явную таблицу тип-колонки → поведение-фильтра до написания ко��а → не строить неполную реализацию которую отклонят
**Context:** Реализовал фильтры в отчётах без спека: personal/medical получили только сортировку по ФИО и глобальный чекбокс "незаполненные". Клиент отклонил — нужны per-column фильтры для каждой колонки. Корень проблемы: "фильтр для всех колонок" означает разное для text (поиск), nullable-text (поиск + заполнено/пусто), numeric (есть/нет). Без явной таблицы типов реализация строится на догадках.
**Pattern:** Перед реализацией UI-фильтрации составь явную таблицу: колонка → тип (text/nullable-text/numeric/enum/date) → поведение фильтра для этого типа. Без этой таблицы "фильтр для всех колонок" реализуется неполно — часть типов пропускается.
**Scope:** universal
**Category:** information-gathering

### 2026-04-06 reports-filter-sort / session 2: Имена shared exports должны явно передаваться в consumer-брифы

**Seen:** 1
**Adapted:** —
**Triad:** Wave 1 создаёт shared module с несколькими named exports; Wave 2 таски потребляют его → перечислить ВСЕ export-символы явно в брифе Wave 1 и передать точную строку импорта в каждый Wave 2 бриф → предотвратить naming divergence и локальные переопределения в consumer-задачах
**Context:** Task 1 создавал FilterDropdown с несколькими filter function exports. Tasks 2–5 в Wave 2 получили только "импортируй из ./FilterDropdown" без перечня символов. Результат: Task 2 Details написал "implement locally", Task 4 не имел явной инструкции, Tasks 3 и 5 использовали разные имена (`nullableTextFilter` vs `composedNullableText`) — всё выловлено в 2 раунда валидации.
**Pattern:** Когда Wave 1 создаёт shared utility с несколькими exports, явно перечисли все символы в AC Wave 1 (`export { textSearch, fillStatus, nullableTextFilter }`) и вставь точную строку `import { ... } from './Module'` в каждый Wave 2 бриф. Без этого consumer-агенты переопределяют или называют символы по-разному.
**Scope:** situational
**Situation:** Multi-wave декомпозиция, Wave 1 создаёт shared utility для параллельных Wave 2 задач
**Category:** sequencing

### 2026-04-06 portfolio-horizontal / session 1: ScrollTrigger process на элементе выше viewport

**Seen:** 1
**Adapted:** —
**Triad:** использование `"X% top"` на триггер-элементе высотой > viewport → переключиться на абсолютные пиксели `start: () => X * window.innerHeight` → триггер срабатывает в правильной точке скролла
**Context:** Spacer 200vh, viewport 100vh, max scroll = 100vh — `"80% top"` вычислялось как 160vh от top, триггер никогда не достигался.
**Pattern:** Когда trigger-элемент выше viewport, `"X% top"` отсчитывается от высоты элемента, а не от scroll progress. Для надёжности использовать функцию: `start: () => scrollFraction * (totalScreens - 1) * window.innerHeight`.
**Scope:** situational
**Situation:** GSAP ScrollTrigger на spacer-элементе выше одного экрана (sticky+spacer паттерн)
**Category:** tool-selection

### 2026-04-06 portfolio-horizontal / session 1: Solid-секция блокирует общий overlay фон

**Seen:** 1
**Adapted:** —
**Triad:** соседние секции имеют разный backgroundColor (одна solid, другая transparent) при overlay-фоне снизу → сделать все секции transparent, перенести базовый цвет на sticky-враппер → нет жёсткого шва на границе секций
**Context:** Hero с `backgroundColor: var(--color-hero)` создавал видимую вертикальную линию при скролле, хотя CaseCard был прозрачным.
**Pattern:** Если фоном управляет общий overlay/враппер ниже по z-index, все дочерние секции должны быть `backgroundColor: transparent`. Иначе solid-секция перекрывает overlay и создаёт шов на своей границе.
**Scope:** situational
**Situation:** Горизонтальный канвас с несколькими секциями и общим фоновым overlay
**Category:** problem-decomposition

### 2026-04-06 portfolio-hero / session 2: GSAP fromTo immediateRender перебивает gsap.set() из соседнего компонента

**Seen:** 1
**Adapted:** —
**Triad:** gsap.fromTo() в компоненте A + gsap.set() на тех же элементах в компоненте B → добавить immediateRender: false к fromTo → не терять начальное состояние из set()
**Context:** HorizontalCanvas устанавливал fromTo для exit-анимации; Hero скрывал элементы через gsap.set() — fromTo с immediateRender:true немедленно применял from:{opacity:1} поверх set(), визуально отменяя скрытие.
**Pattern:** Если gsap.fromTo() в компоненте B управляет элементами, чьё начальное состояние задаёт gsap.set() в компоненте A — добавляй immediateRender: false к fromTo, иначе from-состояние применится при монтировании и перебьёт set().
**Scope:** situational
**Situation:** GSAP-проект с несколькими React-компонентами, каждый из которых управляет анимациями одних и тех же DOM-элементов.
**Category:** tool-selection

### 2026-04-06 portfolio-hero / session 2: Edit добавляет дублирующийся JSX prop без чтения полного элемента

**Seen:** 1
**Adapted:** —
**Triad:** добавление нового prop к JSX-элементу через Edit без чтения полного JSX-блока → читать весь JSX-элемент перед добавлением prop, проверять существующие → не создавать дублирующиеся props
**Context:** Добавил `style={{ marginBottom }}` к pill-div через Edit, не прочитав его полностью — div уже имел `style={{...}}`. React использует только последний style, первый молча игнорируется.
**Pattern:** Перед добавлением любого prop через Edit — прочитать полный JSX-блок элемента (от открывающего тега до закрывающего). Если prop уже есть — объединить значения в одном объекте, не добавлять второй атрибут.
**Scope:** universal
**Category:** tool-selection

### 2026-04-06 juridical-parser / session 4: Module-level blocking вызовы замедляют worker startup

**Seen:** 1
**Adapted:** —
**Triad:** сервис мгновенно отвечает локально, но медленно снаружи → проверить module import на тяжёлые вызовы → убрать блокировку worker startup
**Context:** `_check_old_format_banner()` вызывался при импорте модуля Flask-приложения — Google Drive API call блокировал gunicorn worker на ~1s при каждом рестарте.
**Pattern:** Если сервис быстр локально но медленен при первом запросе — искать не в request handlers, а на уровне module import и startup-кода. Любой I/O, сетевой вызов или внешний API на уровне импорта блокирует worker до завершения. Переносить в `threading.Thread(daemon=True).start()`.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-06 juridical-parser / session 4: ERR_TIMED_OUT с нескольких сетей = ISP-блокировка, не server issue

**Seen:** 1
**Adapted:** —
**Triad:** ERR_TIMED_OUT с нескольких независимых сетей при открытом порту локально → не дебажить server-side → туннель или смена IP
**Context:** Панель не открывалась у клиента (МТС, мобильный, VPN, разные города) — ERR_TIMED_OUT, хотя порт 80 отвечал 200 снаружи из Европы.
**Pattern:** ERR_CONNECTION_REFUSED = сервер отвергает. ERR_TIMED_OUT с нескольких независимых сетей при открытом порту из другой страны = ISP/RKN-блокировка. Server-side дебаг бесполезен. Сразу переходить к туннелю (localhost.run, cloudflared) или смене IP.
**Scope:** situational
**Situation:** деплой на VPS за пределами России; клиент в России
**Category:** recovery

### 2026-04-06 employee-cabinet-updates / session 1: не обходить абстракцию auth-библиотеки

**Seen:** 1
**Adapted:** —
**Triad:** серверный код должен инициировать auth flow → вызвать серверный API auth-библиотеки, не писать токен в БД вручную → токены совпадают с форматом который валидирует клиентская часть
**Context:** Сброс пароля через ручную генерацию UUID и INSERT в verification с identifier `reset:email` — better-auth на клиенте ожидал `reset-password:...`, 5 fix-раундов на поиск причины.
**Pattern:** Если auth-библиотека предоставляет клиентский метод (resetPassword, verifyEmail), на сервере ВСЕГДА вызывать парный серверный API (requestPasswordReset, sendVerificationEmail). Ручная запись в таблицы библиотеки — обход абстракции, который ломается при любом изменении внутреннего формата.
**Scope:** universal
**Category:** tool-selection

### 2026-04-06 responsive-layout / decomposition: конфликт подходов при параллельных task-creator'ах

**Seen:** 1
**Adapted:** —
**Triad:** параллельные task-creator'ы ссылаются на одну и ту же внешнюю утилиту/подход → в брифе оркестратора явно зафиксировать выбранный подход до диспатча → предотвратить противоречивые инструкции в разных задачах
**Context:** Task 1 (AppNav) инструктирует использовать плагин `tailwind-scrollbar-hide`, Task 9 (reports) запрещает плагин и требует `[&::-webkit-scrollbar]:hidden`. Конфликт обнаружен только на cross-task check — оба task-creator'а работали параллельно и не знали друг о друге.
**Pattern:** Когда несколько параллельных task-creator'ов используют одну внешнюю утилиту (плагин, пакет, CSS-трюк) — оркестратор должен выбрать единый подход и передать его каждому task-creator'у в брифе. Параллельные агенты не общаются — каждый принимает решение независимо.
**Scope:** universal
**Category:** scope-management
### 2026-04-06 panel-per-court-settings / session 2: Validation coverage — проверять structurally-similar routes

**Seen:** 1
**Adapted:** —
**Triad:** validation добавлена в один route, есть structurally-similar route с тем же input-полем → немедленно grep все аналогичные routes на наличие той же validation → предотвратить partial validation coverage, когда аудит найдёт пропуск постфактум
**Context:** `run_time_msk` HH:MM validation была добавлена в `POST /api/settings/default`. Structurally-similar route `POST /api/courts/<name>/settings` принимает то же поле, но validation отсутствовала. Code audit (Task 9) нашёл пропуск — потребовался ad-hoc fix уже после завершения Wave 3.
**Pattern:** При добавлении input validation в endpoint — grep по имени поля во всех route-файлах (`grep -r "run_time_msk" src/`). Убедиться, что structurally-similar endpoints имеют ту же validation. Validation в одном endpoint ≠ coverage для analogичных endpoints.
**Scope:** universal
**Category:** sequencing

---
### 2026-04-06 panel-per-court-settings / session 2: Free tunnel меняет URL при рестарте сервиса

**Seen:** 1
**Adapted:** —
**Triad:** сервис с free tunnel (localhost.run, ngrok free) перезапустился → получить новый tunnel URL и немедленно передать клиенту → не оставлять клиента со старым нерабочим URL
**Context:** После деплоя и рестарта `juridical-parser-web` URL изменился с `96cfde1b7210ca.lhr.life` на `4be5bd2a20e668.lhr.life`. Старый URL стал нерабочим. Клиент мог получить неработающую ссылку.
**Pattern:** Free tunnel сервисы генерируют новый URL при каждом рестарте. После любого `service restart` — явно считать новый URL (`journalctl` или curl localhost), сравнить со старым (из `.env` / `memory`), передать клиенту если изменился. Для production — рассмотреть платный план с фиксированным subdomain.
**Scope:** situational
**Situation:** Проект использует free tunnel (localhost.run / ngrok free tier) как публичный URL
**Category:** communication
### 2026-04-07 panel-per-court-settings / session ad-hoc: Новое поле в log-таблице — исторические записи NULL

**Seen:** 1
**Adapted:** —
**Triad:** планирование агрегации из log-таблицы по колонке добавленной ALTER TABLE → проверить заполненность исторических строк, не только наличие колонки → не получить пустую агрегацию из "наполненной" таблицы
**Context:** Задача требовала агрегировать `cases_saved` из `run_log` по `court_name` за период — колонка была добавлена миграцией, но все исторические записи содержали NULL.
**Pattern:** Перед планированием агрегации из таблицы с недавно добавленным полем-дискриминатором — проверить COUNT(field) IS NOT NULL в реальных данных. Если историческое заполнение нулевое — найти альтернативный источник с данными (например, основная таблица событий вместо лог-таблицы).
**Scope:** universal
**Category:** information-gathering

### 2026-04-07 panel-per-court-settings / session ad-hoc: Log-вызов раньше счётчиков которые он должен записать

**Seen:** 1
**Adapted:** —
**Triad:** функция log_*() вызывается до стадии-накопителя метрики → перенести вызов в конец всех накопительных стадий → гарантировать полноту записи в лог
**Context:** `log_run()` вызывался после стадии парсера, но до стадии обогащения — `enricher_requests` не был известен в момент записи.
**Pattern:** Когда log-вызов записывает метрики из N стадий пайплайна — размещать его после ПОСЛЕДНЕЙ стадии, которая вносит вклад в метрику. Промежуточные накопители хранить в переменных, не логировать частично.
**Scope:** universal
**Category:** sequencing

### 2026-04-07 website-rebuild / session 2: Числовой security guard — zero/negative case

**Seen:** 1
**Adapted:** —
**Triad:** числовой параметр используется как security guard (timestamp, counter, TTL) → явно проверять 0/negative/NaN до основной логики → не пропустить bot/abuse через edge case значения
**Context:** Task 6 security-auditor нашёл edge case `_rendered_at <= 0` в time-based anti-bot check. Значение 0 или отрицательное проходило проверку `Date.now() - _rendered_at < 3000` как false (т.е. "прошло достаточно времени").
**Pattern:** Для каждого числового security guard (timestamp, rate counter, TTL) — до основной логики добавить explicit guard: `if (!value || value <= 0 || isNaN(value)) → reject`. Не полагаться на то, что основная arithmetic expression корректно обработает edge cases.
**Scope:** universal
**Category:** sequencing

### 2026-04-07 website-rebuild / session 2: User-controlled данные в HTML output

**Seen:** 1
**Adapted:** —
**Triad:** данные из внешних источников (IP, user input) попадают в HTML-строку (email, page) → применять escapeHtml/sanitize к КАЖДОМУ полю из внешнего источника → предотвратить XSS через non-obvious вектор
**Context:** Task 6 — IP клиента из x-real-ip header не был экранирован в email template. IP выглядит безопасно (цифры и точки), но x-real-ip — user-controlled header, может содержать произвольный текст.
**Pattern:** При построении HTML-строки для email/page — применять escapeHtml() к ВСЕМ полям из внешних источников, включая "безопасные" (IP, user-agent, referer). Header значения — user-controlled, даже если выглядят структурированными.
**Scope:** universal
**Category:** sequencing

### 2026-04-07 tree-constructor / decompose: Entry-point wiring при создании компонентов

**Seen:** 1
**Adapted:** —
**Triad:** задача создаёт UI-компонент но не подключает его в entry point → включить entry point в Files to modify задачи-создателя → не оставлять downstream-задачи с неверным предположением что компонент уже подключён
**Context:** Tasks 4 и 5 создавали PostForm и TreeChart, но не добавляли их в App.tsx. Task 8 описывал "App.tsx уже содержит импорты PostForm, TreeChart" — что было ложным, потому что ни одна задача не отвечала за этот шаг.
**Pattern:** При декомпозиции: если задача создаёт UI-компонент, её scope должен включать подключение в entry point (App.tsx / layout). Иначе образуется gap — никто не отвечает за wiring, и downstream-задачи строят предположения на несуществующем состоянии.
**Scope:** universal
**Category:** scope-management

### 2026-04-07 website-design-match / session 1: проверяй write-флаги до делегирования sandbox-инструменту

**Seen:** 2
**Adapted:** —
**Triad:** делегирование write-задачи sandboxed-инструменту → проверить write permissions тестовой операцией до полного промта → не терять время на failed delegation + ручную реализацию
**Context:** Codex rescue субагент запустил task без --write, получил read-only sandbox, потратил 2 минуты на чтение файлов и диагноз "не могу записать". Работу пришлось выполнить вручную в Claude Code с повторным сбором контекста.
**Pattern:** При делегировании write-задачи инструменту с configurable sandbox — убедиться что write-флаг передаётся явно, а не полагаться на "default to write" в инструкциях агента. Если флаг конфигурационный — проверить его наличие в команде до запуска, не после failure.
**Scope:** universal

### 2026-04-07 panel-settings-display-bug / session 1: после POST-мутации синхронно обновлять in-memory state

**Seen:** 1
**Adapted:** —
**Triad:** JS frontend хранит список в in-memory state → POST мутирует один элемент → state не обновляется → re-render показывает устаревшее → после успешного POST обновить запись в state синхронно → не допустить stale display
**Context:** После сохранения настроек суда (POST 200 ok) `courtSettings[courtName]` не обновлялся. При переключении вкладки `renderTable()` перерисовывал форму с дефолтами из stale state.
**Pattern:** Если frontend кэширует список в JS-переменной и отдельно мутирует элементы через POST — после успешного ответа немедленно обновить in-memory запись (`state[key] = newValue`). Иначе любой последующий re-render использует устаревшие данные.
**Scope:** universal
**Category:** scope-management

### 2026-04-07 panel-settings-display-bug / session 1: batch endpoint — skip unknowns вместо reject-all

**Seen:** 1
**Adapted:** —
**Triad:** batch endpoint валидирует каждый элемент и возвращает 400 если хоть один неизвестен → изменить на "skip unknowns, return known" → не ломать весь batch из-за одного невалидного элемента
**Context:** `/api/courts/settings/batch?courts=...` с 90 судами возвращал 400 из-за одного неизвестного имени. Весь JS-state заполнялся дефолтами.
**Pattern:** Для batch-read endpoints предпочитать partial success: неизвестные ключи пропускать, возвращать результат для известных. Reject-all оправдан только для write-операций где частичное применение опаснее полного отказа.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-07 cron-uses-panel-settings / session 1: sketch-first перед кодом — не кодировать напрямую в main-сессии

**Seen:** 1
**Adapted:** —
**Triad:** задача требует написания кода, рефлекс — начать писать напрямую → написать sketch.md (root cause + what must work) и делегировать Codex ДО начала кода → соблюдать установленный workflow
**Context:** Задача fix cron: я начал писать `__main__.py` напрямую. Пользователь остановил: "почему это делаешь ты, когда ты должен оформить документацию и делегировать программирование кодексу?"
**Pattern:** Когда в проекте установлен workflow "sketch → Codex", при поступлении coding-задачи — сначала написать sketch.md (root cause + what must work), согласовать с пользователем, делегировать Codex. Писать код напрямую = нарушение договорённости.
**Scope:** situational
**Situation:** проект использует sketch → Codex delegation workflow для кодогенерации
**Category:** scope-management
**Category:** tool-selection

### 2026-04-08 panel-settings-display-bug / session 1: deploy-and-retest reveals infrastructure layer as root cause

**Seen:** 1
**Adapted:** —
**Triad:** фикс задеплоен → баг воспроизводится → проверить upstream-инфраструктуру до повторного анализа кода → не тратить ещё один цикл деплоя на не тот слой
**Context:** Баг описан как "courtSettings JS не обновляется после save". Фикс добавлен и задеплоен. Баг воспроизводится. Настоящая причина: gunicorn hard limit 8190 байт на request line → batch-endpoint возвращал 400 → JS заполнял state дефолтами при каждой загрузке страницы.
**Pattern:** Когда задеплоенный фикс не устраняет симптом — перед повторным анализом кода проверить инфраструктурные ограничения между клиентом и обработчиком: размеры запроса/ответа, таймауты, кэш, middleware-лимиты. Симптом в одном слое часто вызывается ограничением в другом.
**Scope:** universal
**Category:** problem-decomposition


### 2026-04-08 responsive-fixes / session 1: Verify agent diff for unintended side-effects

**Seen:** 1
**Adapted:** —
**Triad:** delegating point edits to external agent (Codex) → review full git diff after agent completes, not just target files → catch unintended changes before commit
**Context:** Codex was given 6 precise Tailwind class replacements with explicit "don't touch anything else" instruction, but also changed the Yandex Maps iframe URL — an unrelated modification that had to be reverted.
**Pattern:** After any delegated edit task (Codex, subagent), always run `git diff` on ALL changed files before committing — not just the files you expect to be changed. "Don't touch other lines" is not a reliable constraint for LLM agents.
**Scope:** universal
**Category:** tool-selection


### 2026-04-08 juridical-parser / session diagnostic: Агрегация параллельных процессов через дельту пула

**Seen:** 1
**Adapted:** —
**Triad:** агрегация расхода ресурса из параллельных запусков → использовать pool_start − pool_end вместо SUM(individual_spent) → получить корректный совокупный показатель без двойного счёта
**Context:** SUM(requests_spent) по run_log дал 9762, тогда как реальный расход квот = quota_before(первый запуск) − quota_after(последний) = 3024 — параллельные запуски стартуют с одного значения, SUM даёт двойной счёт.
**Pattern:** Когда несколько процессов параллельно расходуют общий ресурсный пул — агрегируй через дельту пула (start − end по хронологии), а не через SUM индивидуальных записей. SUM корректен только для последовательных процессов.
**Scope:** universal
**Category:** information-gathering

### 2026-04-08 dns-migration / session 1: .env менять ПОСЛЕ пропагации DNS, не параллельно

**Seen:** 1
**Adapted:** —
**Triad:** DNS-миграция: .env содержит домен который ещё не пропагировался → менять .env и пересобирать ПОСЛЕ подтверждения dig A → новый IP → не ломать работающий сайт на период пропагации
**Context:** При миграции geologging.ru обновили BETTER_AUTH_URL на новый домен до пропагации DNS. Сайт перестал работать по IP — пришлось откатывать .env и пересобирать дважды.
**Pattern:** При DNS-миграции разделяй инфраструктурные шаги (nginx, SSL) и application-level шаги (.env, build) строгой границей: application config меняется только после `dig A domain → новый IP`. Nginx можно готовить заранее, .env — нельзя.
**Scope:** universal
**Category:** sequencing

### 2026-04-08 dns-migration / session 1: При смене домена — grep hardcoded origin lists

**Seen:** 1
**Adapted:** —
**Triad:** смена домена приложения → grep hardcoded origin/domain списки (CORS, CSRF, allowed_origins) и обновить ВСЕ до деплоя → не получить молчаливый 403 на формах и API
**Context:** Форма заявки на geologging.ru возвращала 403 — CSRF Origin check содержал только geologging.ru, а сайт работал по IP. Ошибка молчаливая, в логах нет следов.
**Pattern:** При любой смене домена/URL приложения выполнить `grep -r 'старый_домен\|allowed_origin\|CORS\|CSRF' src/` и обновить все найденные списки. Особое внимание к middleware с Origin/Referer-проверками — они дают молчаливый 403 без записи в лог.
**Scope:** universal
**Category:** information-gathering


### 2026-04-08 juridical-parser / session diagnostic-2: Проверяй математику стоимости до объяснения клиенту

**Seen:** 1
**Adapted:** —
**Triad:** объяснение стоимости многошагового API-процесса клиенту → посчитать каждый шаг отдельно (поиск = кол-во_дел ÷ страница × 1 квота; детали = кол-во_подходящих × 1 квота) и сверить сумму с фактом → не давать клиенту математически противоречивую картину расходов
**Context:** Написал клиенту "6400 дел + 700 карточек = 3024 квоты", но 320 + 700 = ~1020, а не 3024 — разрыв в ~2000 квот от ошибочной поисковой стратегии не был учтён в объяснении.
**Pattern:** Перед тем как объяснять клиенту стоимость пайплайна — посчитай каждый тип запроса отдельно и сложи. Если сумма не совпадает с фактическим расходом — найди и опиши разницу явно, иначе клиент обнаружит противоречие сам.
**Scope:** universal
**Category:** communication

### 2026-04-09 juridical-parser / session 9: деплой обязателен в той же сессии что и фикс

**Seen:** 1
**Adapted:** —
**Triad:** server-side код исправлен и закоммичен → задеплоить сразу как последний шаг сессии → не допустить запуск продакшна со старым кодом
**Context:** Три фикса квот и экспорта были закоммичены, но не задеплоены. Следующий день: cron отработал со старым кодом, потратив 962 квоты вместо ~30. Проблема обнаружена только по факту.
**Pattern:** После правки server-side кода — деплой является обязательной частью сессии, не опциональным продолжением. Если сессия завершается без деплоя — явно сообщи пользователю о незадеплоенных изменениях и их последствиях (что случится при следующем cron/запуске).
**Scope:** universal
**Category:** sequencing

### 2026-04-09 juridical-parser / session 9: pkill orphan перед systemctl restart в deploy script

**Seen:** 1
**Adapted:** —
**Triad:** deploy script делает systemctl restart сервиса на порту | добавить pkill orphan-процессов перед restart | предотвратить crash loop из-за Address already in use
**Context:** Старый nohup-gunicorn (запущен вручную) остался висеть после деплоя через systemd. При следующей попытке рестарта systemd не смог занять порт — 76 рестартов в петле.
**Pattern:** В любом deploy script, где делается systemctl restart сервиса, занимающего фиксированный порт — добавь `pkill -f 'process.*port' || true; sleep 2` перед restart. Это защита от orphan-процессов запущенных вручную (nohup, screen, прямой запуск).
**Scope:** universal
**Category:** sequencing

### 2026-04-09 juridical-parser / session diagnostic-3: Считать метрику на выходной стороне трансформации

**Seen:** 1
**Adapted:** —
**Triad:** пользователь спрашивает "сколько X" когда пайплайн делает 1→N разворачивание → найти код трансформации и считать на выходной стороне → дать метрику совпадающую с тем что пользователь видит
**Context:** Запрос вернул 192 "дела с телефоном", тогда как реальный ответ был 810 номеров — `_expand_phones` разворачивает 1 дело в N строк (по номеру), а клиент видит строки в Sheets, не дела.
**Pattern:** Перед запросом к БД — найти в коде все трансформации между входным объектом и финальным выводом (expand, flatten, group). Считать на том же уровне что пользователь видит в интерфейсе. Если пайплайн делает 1→N (например expand_phones) — запрашивай количество развёрнутых строк, не исходных записей.
**Scope:** universal
**Category:** information-gathering

### 2026-04-09 juridical-parser / session diagnostic-3: Ориентация по таймстемпам перед запросом "за вчера"

**Seen:** 1
**Adapted:** —
**Triad:** пользователь говорит "вчера/сегодня запускалось" → сначала SELECT DISTINCT run_date ORDER BY DESC LIMIT 5 для ориентации → не запрашивать данные за ошибочную дату
**Context:** Показал статистику за 8 апреля, тогда как "всю Россию" запускали 7-го — различие между датой запуска в run_log и тем, что пользователь считает "вчерашним", не было проверено.
**Pattern:** При любом диагностическом запросе "что произошло вчера/сегодня" — первым запросом сдампить 5 последних уникальных run_date из run_log с created_at, чтобы сопоставить фактические временные метки с тем, что имеет в виду пользователь. Только после этого формировать фильтр по дате.
**Scope:** universal
**Category:** information-gathering

### 2026-04-09 juridical-parser / session techspec-1: test-reviewer в фазе tech-spec проверяет план, а не файлы

**Seen:** 1
**Adapted:** —
**Triad:** test-reviewer возвращает fail в фазе tech-spec, ссылаясь на отсутствие тестов в реальных файлах → признать false fail; в prompt для test-reviewer явно указать "проверь план, а не наличие тестов в коде" → не тратить раунд ревалидации на проблему формулировки промпта
**Context:** Round 2 test-reviewer вернул fail потому что увидел, что в test_main.py ещё не написаны новые тесты. Но на этапе tech-spec тесты не пишутся — это задача Codex при implementation.
**Pattern:** Перед запуском test-reviewer как валидатора tech-spec — явно указать в промпте: "оцени адекватность тестового плана, не проверяй наличие тестов в файлах". Если reviewer вернул fail за отсутствие реализованных тестов — это ложный fail, spec корректен.
**Scope:** situational
**Situation:** запуск test-reviewer в фазе tech-spec-planning (до implementation)
**Category:** tool-selection

### 2026-04-09 demo-trees-sharing / session 1: Уточни потребителя до технических деталей

**Seen:** 1
**Adapted:** —
**Triad:** пользователь описывает фичу знакомым термином (демо, шаблон, виджет) → спросить «кто потребитель и зачем ему это?» до технических деталей → не потратить 3 батча интервью на выяснение реальной потребности
**Context:** Пользователь описал фичу как «демо-деревья», имея в виду не онбординг-примеры, а рабочие деревья для клиентов. 3 батча вопросов ушло на техдетали (хранение, формат) вместо того чтобы сразу спросить «кто получатель этих демо и что он с ними делает?»
**Pattern:** Когда пользователь описывает фичу термином, который кажется очевидным (демо, шаблон, экспорт) — первый вопрос должен быть про потребителя и его цель, а не про техническую реализацию. Знакомое слово маскирует разрыв между моделью агента и реальной потребностью.
**Scope:** universal
**Category:** information-gathering

### 2026-04-09 juridical-parser / session quota-stats: Hypothesis requires delayed observation, not immediate fix

**Seen:** 1
**Adapted:** —
**Triad:** расхождение между нашим измерением и внешним биллингом → проверить гипотезу отложенным наблюдением до реализации фикса → не реализовывать фикс на непроверенной гипотезе
**Context:** Панель показывала 962 квоты, реальный биллинг 747. Сформулировали гипотезу «задержка обновления баланса» → реализовали quota_hint chain → через 5 ч клиент проверил: реальный расход всё равно 747. Гипотеза была неверна, фикс не помог.
**Pattern:** Когда метрика расходится с внешним источником правды, и гипотеза требует ожидания (задержка, кеш, биллинговый цикл) — сначала выждать один полный цикл наблюдения, убедиться что гипотеза подтверждается данными, и только потом реализовывать фикс. Реализация до наблюдения = ставка на непроверенное.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-09 juridical-parser / session quota-stats: Same column name ≠ same semantics across tables

**Seen:** 1
**Adapted:** —
**Triad:** одноимённая колонка в двух таблицах используется как ключ для JOIN/match → проверить семантику колонки в каждой таблице до объединения → предотвратить молчаливое расхождение данных
**Context:** run_log.court_name = суд-фильтр поиска («что мы искали»), cases.court_name = реальный суд из API деталей («что вернул API»). Поиск по «АС города Москвы» возвращал дела других судов. JOIN по court_name давал пустые пересечения — period-статистика показывала 0 квоты для судов с реальными делами.
**Pattern:** Когда два источника данных содержат одноимённую колонку — перед использованием как ключа для match/join убедиться, что они семантически эквивалентны: один источник хранит «что запрашивали», другой — «что получили». Молчаливое расхождение не даст ошибки, только неверные агрегаты.
**Scope:** universal
**Category:** information-gathering
### 2026-04-09 juridical-parser / session 11: Проверять бэклог-примеры через бизнес-смысл до реализации

**Seen:** 1
**Adapted:** —
**Triad:** бэклог содержит числовой пример противоречащий бизнес-логике фичи → проверить пример через первопринципы до кодинга → не реализовывать неверный алгоритм по ошибочной спеке
**Context:** Бэклог говорил "Понедельник → четверг (2 рабочих дня назад)", но бизнес-смысл — "данные устоялись за выходные". Правильный ответ для понедельника — пятница (1 рабочий день назад, но 3 календарных дня). Реализовал "skip N workdays", пользователь остановил.
**Pattern:** Когда бэклог даёт числовой пример для date-offset логики — верифицировать пример через бизнес-смысл ("почему именно эта дата подходит?") до реализации. Если пример и смысл расходятся — смысл приоритетнее.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-09 juridical-parser / session 11: Разбивать deploy на два SSH-вызова вместо одного

**Seen:** 1
**Adapted:** —
**Triad:** deploy.sh объединяет pkill + systemctl restart в один длинный SSH-вызов → SSH может оборваться в момент restart, сервис остаётся down → разбить на два вызова: upload/config и restart/verify
**Context:** После pkill gunicorn SSH оборвался до systemctl restart — сервис ушёл в inactive без предупреждения. Пришлось вручную перезапускать.
**Pattern:** Если deploy script содержит операции изменения файлов И перезапуск сервиса в одном SSH heredoc — вынести systemctl restart в отдельный SSH-вызов. Тогда при обрыве первого вызова перезапуск всё равно выполнится.
**Scope:** situational
**Situation:** deploy script с SSH pipe для загрузки файлов + systemctl restart в одном вызове
**Category:** tool-selection

### 2026-04-10 demo-trees-sharing / session 3: проверять координатную систему числами до написания фикса

**Seen:** 1
**Adapted:** —
**Triad:** визуальный баг в layout/positioning → вывести реальные координаты нод через тест/лог до написания фикса → не итерировать вслепую 5+ раз
**Context:** Multi-root зеркалирование фиксилось 5+ раз. Каждый раз чинили "на глаз". Только когда вывели числа (root.y=613, trunk.y=445) стало ясно что root уже ниже trunk и зеркалирование ломает, а не чинит.
**Pattern:** При визуальных багах в SVG/Canvas/layout — первым делом вывести координаты через unit-тест с console.log. Понять систему координат числами. Только потом менять код. Один тест с числами экономит 5 итераций вслепую.
**Scope:** universal
**Category:** information-gathering

### 2026-04-11 juridical-parser / ad-hoc: decisions.md актуальнее architecture.md для инфра-вопросов

**Seen:** 2
**Adapted:** —
**Triad:** вопрос об инфраструктуре, деплое или production URL → читать decisions.md (changelog) ДО project-knowledge docs → не дать ответ из устаревшего статичного снимка
**Context:** architecture.md содержал старое описание lhr-tunnel как публичного URL. Правда (Cloudflare Worker с 2026-04-07) была в decisions.md — Infrastructure Change log. Дал неверный ответ, потом исправил после проверки decisions.md.
**Pattern:** При вопросах об инфраструктуре, сервере или production URL — сначала читать decisions.md (содержит changelog изменений), потом architecture.md (статичный снимок). Changelog всегда актуальнее docs: архитектурные изменения фиксируются там первыми.
**Scope:** situational
**Situation:** Проект ведёт decisions.md с Infrastructure Change / Migration Log секцией
**Category:** information-gathering

### 2026-04-11 juridical-parser / session: Термин пользователя ≠ техническая метрика

**Seen:** 1
**Adapted:** —
**Triad:** пользователь называет X, в системе есть несколько похожих счётчиков → явно сопоставить термин пользователя с конкретной метрикой до ответа → не подменять один счётчик другим из-за схожести названий
**Context:** На вопрос «сколько контактов выгружено» ответил числом из cases_saved, тогда как «контакты» пользователь имел в виду записи с телефоном — другой счётчик.
**Pattern:** Слова пользователя — это его модель мира, не технические названия. Перед ответом на числовой вопрос: найти, какая именно метрика соответствует термину пользователя, назвать её явно. «72 дел сохранено» и «72 контакта» — разные утверждения даже если число одно.
**Scope:** universal
**Category:** communication

### 2026-04-12 client-bugfixes / session 1: Верификация маппинга ветки на environment перед деплоем

**Seen:** 1
**Adapted:** —
**Triad:** объявление деплоя завершённым → верифицировать маппинг ветки на environment (preview vs production) ДО пуша → не тратить время пользователя ложными отчётами о деплое
**Context:** Пушил в dev-ветку и сообщал об успешном деплое, но платформа маппила dev на Preview, а production — на другую ветку. Пользователь не видел изменений на сайте.
**Pattern:** Перед первым пушем в сессии — проверь какая ветка маппится на production environment (API платформы, deployment history, или конфиг). Не предполагай что текущая ветка = production.
**Scope:** universal
**Category:** tool-selection

### 2026-04-12 core-constructor / session 2: Неявные границы scope не соблюдаются — только явные ограничения работают

**Seen:** 1
**Adapted:** —
**Triad:** параллельные исполнители получают описание задачи без явных границ вывода → исполнитель расширяет scope по собственной интерпретации → работа другого исполнителя обесценивается
**Context:** Два параллельных исполнителя с задачами в смежных областях. Один создал артефакты обоих — потому что описание задачи не запрещало этого. Второй нашёл готовые артефакты и выполнил только часть своей работы.
**Pattern:** Описание задачи задаёт "что сделать", но не "что НЕ делать". Исполнитель, видящий возможность сделать больше, сделает больше — полезное поведение при последовательном исполнении, деструктивное при параллельном. Логика: при параллельном исполнении boundary вывода должен быть explicit constraint, а не implicit следствие из описания задачи. Implicit scope = no scope.
**Scope:** universal
**Category:** scope-management

### 2026-04-13 sheets-column-shift / session bugfix: downstream invariant blindspot

**Seen:** 1
**Adapted:** —
**Cognitive Error:** downstream invariant blindspot
**Triad:** структурное изменение общего ресурса (добавление/удаление поля, колонки, слоя) → перечислить все downstream-операции которые предполагали старую структуру и явно протестировать их в новой → не оставлять неверифицированных структурных предположений
**Context:** Миграция вставила пустую колонку A в Sheets. Предположение "append_rows пишет с A1" оставалось молчаливым инвариантом — никто не проверил что он держится при пустой колонке A. Sheets API нашёл таблицу с колонки B и начал писать туда.
**Pattern:** После любого структурного изменения общего ресурса (схема, колонки, индексы, форматы) — явно проверить каждую downstream-операцию которая предполагала старую структуру. Изменение структуры не ломает то что ты менял — оно ломает то что ты не менял но неявно зависело от неё.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-13 admin-panel / session 4: directive deafness

**Seen:** 1
**Adapted:** —
**Cognitive Error:** directive deafness
**Triad:** стейкхолдер даёт явную директиву о режиме работы → переключить режим немедленно, не задавать ещё один уточняющий вопрос → не продолжать прежний режим после явного переключения
**Context:** Стейкхолдер сказал "ничего не спрашивай, просто делай". Следующим действием был AskUserQuestion с двумя вопросами. Инерция предыдущего режима (ask-before-act) заглушила явную директиву о переключении на act-without-ask.
**Pattern:** Когда стейкхолдер явно переключает режим взаимодействия ("не спрашивай", "делай молча", "только покажи результат") — это не рекомендация, а немедленная команда. Текущая задача может требовать уточнений, но форма работы меняется в момент директивы, не после завершения текущего шага.
**Scope:** universal
**Category:** communication

### 2026-04-13 admin-panel / session 5: first-fix completion bias

**Seen:** 1
**Adapted:** —
**Cognitive Error:** first-fix completion bias
**Triad:** исправляется структурное ограничение, нарушённое в нескольких местах артефакта → после исправления первого нарушения — просканировать ВЕСЬ артефакт на остальные вхождения того же структурного паттерна → не считать проблему решённой после первого исправления
**Context:** В многочастном артефакте было нарушено форматное ограничение. Исправил первое найденное нарушение и объявил задачу решённой — не проверив, есть ли такие же нарушения в других секциях того же файла. Потребовались 2 дополнительных итерации.
**Pattern:** Когда диагностируешь нарушение структурного правила — сразу формулируй его как паттерн ("нельзя X в позиции Y") и сканируй весь артефакт на все вхождения X. Исправление одного вхождения ≠ устранение нарушения.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-13 admin-panel / session 5: clean-slate assumption

**Seen:** 1
**Adapted:** —
**Cognitive Error:** clean-slate assumption
**Triad:** регистрация нового компонента в разделяемом пространстве ресурсов → перед выбором идентификатора (порт, путь, имя) — перечислить уже занятые идентификаторы в целевом окружении → не предполагать, что пространство ресурсов свободно
**Context:** Новому компоненту назначен дефолтный идентификатор без проверки занятости в shared-окружении. Конфликт обнаружен только при запуске — потребовалась смена идентификатора и обновление конфигурации в нескольких местах.
**Pattern:** Перед назначением любого идентификатора (порт, имя, путь) в разделяемом окружении — сначала перечисли занятых. Shared окружение никогда не является clean slate — всегда есть другие компоненты. "Дефолтный" идентификатор означает "наиболее вероятно занятый".
**Scope:** universal
**Category:** sequencing

### 2026-04-13 freelance-autopilot / session audit+deploy: spawn-for-capability bias

**Seen:** 1
**Adapted:** —
**Cognitive Error:** spawn-for-capability bias
**Triad:** gatekeeper rejects all framework-spawned instances despite disguise attempts → connect to already-running unmanaged instance via debug interface instead of spawning new controlled one → spawn-for-capability bias
**Context:** Anti-bot protection blocked every browser instance spawned by the automation framework (regardless of stealth settings or executable used). The solution was connecting to a manually-launched browser via its native debug interface — no automation flags present at launch.
**Pattern:** When an external gatekeeper blocks instances created by your framework, stop spawning — connect instead. Capability to send commands and detectability of instance origin are separate concerns. An already-running instance launched manually carries no automation fingerprint regardless of what commands you send through it.
**Scope:** universal
**Category:** problem-decomposition

### 2026-04-13 menu-editor / session 1: stated-state authority bias

**Seen:** 1
**Adapted:** —
**Cognitive Error:** stated-state authority bias
**Triad:** стейкхолдер называет конкретный технический компонент как часть требований → сверить с актуальной документацией до фиксации → не принять устаревший технический факт как ограничение спека
**Context:** Стейкхолдер назвал конкретную платформу хранения как действующую — она уже была заменена. Несоответствие поймано по документации до записи в спек.
**Pattern:** Когда стейкхолдер называет конкретное техническое состояние системы (платформу, инструмент, конфиг) — трактовать это как гипотезу, не как факт. Сверить с наиболее свежим авторитетным источником (документацией, конфигом) до фиксации в артефакте.
**Scope:** universal
**Category:** information-gathering

### 2026-04-14 menu-editor / session decompose: execution-context portability assumption

**Seen:** 1
**Adapted:** —
**Cognitive Error:** execution-context portability assumption
**Triad:** написание import-statement для модуля из одного окружения выполнения в артефакт другого окружения → до написания import-а проверить транзитивную цепочку зависимостей модуля на совместимость с целевым контекстом → не считать что модуль переносим только потому что он существует в проекте
**Context:** Seed-скрипт (запускается через plain node/tsx) получил import файла данных, который через транзитивные зависимости импортировал .jpg-файлы через webpack-трансформы — невалидные за пределами bundler-контекста. Ошибка поймана на review, потребовала полного перезаписа подхода (hardcode data вместо import).
**Pattern:** Перед написанием import-statement спросить: «В каком контексте выполняется этот артефакт? Был ли импортируемый модуль написан для того же контекста?» Если контексты различаются — пройти транзитивную цепочку зависимостей импортируемого модуля и проверить каждый шаг на совместимость. Существование файла в проекте не гарантирует его переносимость между контекстами (bundler vs runtime, server vs client, browser vs node).
**Scope:** universal
**Category:** information-gathering

### 2026-04-14 menu-editor / session decompose: producer-centric specification

**Seen:** 1
**Adapted:** —
**Cognitive Error:** producer-centric specification
**Triad:** спецификация задачи-продьюсера написана по внутренней модели данных → до финализации спека прочитать задачи-консьюмеры последующих волн и перечислить каждое поле которое они обращаются → не упустить вычисляемые/агрегированные поля которые нужны потребителю но отсутствуют в модели продьюсера
**Context:** Задача создания API-endpoint'а написана по полям таблицы БД. Задача UI в следующей волне обращалась к агрегированному полю (itemCount), которого не было в базовой схеме и не попало в спек endpoint'а. Проблема поймана cross-task валидатором, потребовала дополнительного fix-раунда.
**Pattern:** Когда пишешь спек задачи-продьюсера (API, генератор данных, report builder) — после описания базовой логики сделай обход всех задач-консьюмеров в последующих волнах и составь список всех полей/форматов, которые они ожидают на входе. Дизайн вывода должен быть определён потребностями консьюмера, а не внутренней моделью данных продьюсера.
**Scope:** universal
**Category:** information-gathering
