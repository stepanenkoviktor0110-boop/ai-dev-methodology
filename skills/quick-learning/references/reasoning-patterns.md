# Reasoning Patterns

Accumulated insights about decision-making logic across projects.
Single transit buffer for ALL methodology knowledge — both reasoning patterns and operational lessons.

**This is a transit buffer.** Patterns that reach `Seen: 3` get promoted into skill SKILL.md files and removed from here. Stale entries (Seen: 1, older than 30 days) get pruned.

---

## Universal

Patterns that apply to any project, any stack, any domain.

<!-- Append universal patterns below -->

### 2026-03-29 stylist-website / client-edits: Верифицируй результат, а не только изменение

**Seen:** 2
**Triad:** создание/изменение артефакта → верифицировать результат в реальной среде перед объявлением "готово" → не объявлять "готово" пока результат не подтверждён
**Context:** (1) Скилл создан в репо, но не попал в runtime. (2) CSS flex-выравнивание добавлено, но цена была вложена слишком глубоко в HTML — flex не мог до неё достать. Дважды сказал "готово", пользователь дважды увидел что ничего не изменилось.
**Pattern:** После любого изменения — проверь что результат действительно работает в целевой среде. Для layout-изменений: убедись что целевой элемент структурно доступен механизму (прямой потомок flex-контейнера и т.д.). Изменить код ≠ получить результат.
**Scope:** universal
**Category:** sequencing

### 2026-03-28 employee-dashboard / session 3: Build-before-commit при server/client boundary

**Seen:** 3 → PROMOTED to feature-execution
**Triad:** изменение server/client boundary или сигнатуры → запустить build между волнами → поймать type/import violations до QA
**Context:** Tasks 8-9 импортировали getSession() (server-only, uses next/headers) в "use client" pages. Unit-тесты прошли, build сломался. Обнаружено только на QA wave. Ранее: callback type mismatch тоже поймал только build.
**Pattern:** Запускай полный build после каждой волны (не только на QA). Unit-тесты не ловят: server/client boundary violations, callback type mismatches, import ошибки runtime-only модулей.
**Scope:** universal
**Category:** sequencing

### 2026-03-26 mvp-parser / session 1: Retry-декоратор должен знать, что НЕ ретраить

**Seen:** 1
**Triad:** generic retry decorator оборачивает API-вызов → явно исключить non-retryable exceptions → не ретраить ошибки, которые повторятся всегда
**Context:** `retry_with_backoff` ловил все Exception, включая HTTP 429 (quota exceeded). Ревьюер поймал: quota не восстановится через 30 секунд, retry бессмыслен и тратит время. Пришлось менять архитектуру: _request возвращает Response без raise, caller проверяет status code.
**Pattern:** При проектировании retry-обёртки сразу определи список non-retryable исключений. Если декоратор generic (ловит Exception) — добавь параметр `exclude` или проверяй тип перед retry. Retryable = транспортные ошибки + 5xx. Non-retryable = 4xx (quota, auth, not found).
**Scope:** universal
**Category:** tool-selection

### 2026-03-26 tech-spec / meta: Верифицируй API response shapes из code-research

**Seen:** 2
**Triad:** code-research описывает внешний API (методы или response shape) → сделать live call и проверить реальную документацию до включения в спек и написания тестов → предотвратить propagation миражей code-research → tech-spec → implementation → тесты
**Context:** (1) Code-research может содержать неточные описания API — если tech-spec копирует их без проверки, мираж распространяется до реализации. (2) mvp-parser: code-research задокументировал `/stat/` как `{"remaining": N}`. Реальный ответ — `[{"service":"arbitr","month_request_count":2,"month_limit":200,...}]`. Тесты написаны под неверную форму, прошли 100%. Audit-агенты нашли код консистентным. Баг обнаружен только при live testing.
**Pattern:** Перед включением API response shapes из code-research в tech-spec — сделай реальный API call и сверь с документацией. Один live call стоит дёшево, а propagation миража через весь pipeline (spec → code → tests → audit) стоит дорого.
**Scope:** universal
**Category:** information-gathering

### 2026-03-29 tech-spec / meta: Error state machine для внешних API

**Seen:** 3 → PROMOTED to tech-spec-planning
**Triad:** спек для интеграции с внешним API → перенести ВСЕ коды ответа И формат данных из документации/code-research в спек → предотвратить пропуск нестандартных ответов API при реализации
**Context:** (1) user-spec court-workdays пропустил isDayOff код 2 и ошибки 100/101/199. (2) tech-spec указал xmlcalendar как JSON, реально — XML. Название "xmlcalendar" буквально содержит "xml", но спек копировал предположение. (3) Ранее: без error state machine исполнители реализуют handling по-своему.
**Pattern:** PROMOTED: При написании спека для внешнего API — перенести ВСЕ коды ответа, формат данных, и edge cases. Сделать live call для проверки формата до включения в спек.
**Scope:** universal
**Category:** information-gathering

### 2026-03-24 payroll-full-calc: Post-deploy UX-правки — это норма

**Seen:** 1
**Triad:** post-deploy verification с пользователем → планировать 2-4 итерации UX-правок как норму → не считать UX-корректировки проблемой процесса
**Context:** 6 post-deploy коммитов с UX-правками (скрыть штрафы, показать обе ставки, авто-перезагрузка, выравнивание, добавить роль ADMIN). Все обнаружены только при live-верификации — user-spec не покрывал UI-детали.
**Pattern:** При post-deploy verification — планировать 2-4 итерации UX-правок. Пользователь видит реальный UI впервые и уточняет требования. Коммитить каждый фикс отдельно для чистой истории.
**Scope:** universal
**Category:** scope-management

### 2026-03-29 design-pipeline-v2: Проверяй все cross-references в сгенерированных задачах

**Seen:** 2
**Triad:** генерация задач из tech-spec → проверять все cross-references (пути файлов через test -e, номера решений, depends_on) → предотвратить битые ссылки в задачах
**Context:** (1) 2026-03-25: task-creator сгенерировал несуществующие пути к файлам и неверные depends_on ссылки в 12 задачах. (2) 2026-03-29: task-creator создал ссылку "Decision 12" в tech-spec с только 10 решениями — номер взят по предположению.
**Pattern:** После генерации задач проверяй все cross-references по source: пути через `test -e`, номера решений — пересчётом по tech-spec, depends_on — что зависимость реально создаёт нужный артефакт. Агент генерирует ссылки по аналогии/предположению, не по факту.
**Scope:** universal
**Category:** problem-decomposition

### 2026-03-29 design-pipeline-v2 / session 6: awk не фейлит pipe — используй [ ... ] для size guard

**Seen:** 1
**Triad:** smoke-команды с проверкой размера файла → использовать `[ $(wc -l < FILE) -lt N ]` вместо awk-условия → предотвратить ложно-проходящий size guard
**Context:** Smoke-команды из tech-spec содержали `wc -l | awk '{if ($1 < 500) print "OK"; else print "OVER LIMIT"}'` — повторились в 4 задачах и Task 8 QA. awk всегда exit 0 (даже когда печатает OVER LIMIT), поэтому smoke всегда проходит.
**Pattern:** Для проверки размера через CLI используй `[ $(wc -l < FILE) -lt N ]` — это bash test, exit 1 при провале. Awk в конце pipe не фейлит pipeline независимо от вывода. Проверяй exit-логику в smoke-командах перед тем как копировать из tech-spec в задачи.
**Scope:** universal
**Category:** sequencing

### 2026-03-26 design-pipeline-v1: AC через артефакты, не через поведение

**Seen:** 1
**Triad:** AC для markdown-only фич → формулировать через наличие конкретных артефактов → сделать AC автоматически проверяемыми
**Context:** User-spec прошёл 2 раунда валидации — AC описывались на уровне поведения агента ("агент предлагает"), а не верифицируемых артефактов. Переписаны в формат "файл X содержит Y".
**Pattern:** При написании AC для markdown-only фич (скиллы, reference-файлы) формулировать критерии через наличие конкретных артефактов: "файл X содержит Y", "SKILL.md содержит шаг Z в Phase N".
**Scope:** universal
**Category:** scope-management

### 2026-03-26 mvp-parser / session 2: HTTP timeout — обязательный параметр

**Seen:** 1
**Triad:** реализация вызовов к внешним сервисам → устанавливать явный timeout на каждый вызов → предотвратить бесконечное зависание pipeline при stale соединении
**Context:** Вызов к внешнему API без timeout привёл к бесконечному зависанию pipeline — сервер начал отдавать ответ, но не завершил передачу.
**Pattern:** При любом вызове к внешнему сервису — устанавливай явный timeout. Отсутствие timeout превращает stale соединение в бесконечное зависание всего pipeline. Это касается HTTP, gRPC, WebSocket, DB-соединений.
**Scope:** universal
**Category:** tool-selection

### 2026-03-26 mvp-parser / session 2: Эскалирующая диагностика перед гипотезой "сервис сломан"

**Seen:** 1
**Triad:** внешний сервис возвращает неожиданный результат → провести эскалирующую диагностику (менять параметры запроса, сравнить с curl, перечитать документацию) → найти рабочий обходной путь через существующие API-параметры, не ждать исправления сервиса
**Context:** parser-api.com обрывал ответ на ~23KB. Агент сначала предположил "API сломан" — пользователь возразил. Последовательная диагностика: разные даты → curl-тест → streaming → повторное чтение docs с нуля → обнаружено, что `Inn` принимает строку, не только ИНН → `Inn=ИП` дало малый ответ → решение: разбить запросы по типу ответчика.
**Pattern:** Когда внешний сервис ведёт себя неожиданно — не объявляй "сервис сломан" без исчерпывающей диагностики: (1) измени параметры запроса, (2) протестируй curl (изолируй Python), (3) перечитай документацию целиком с нуля. Часто fix — это нестандартное использование уже существующего параметра.
**Scope:** universal
**Category:** recovery

### 2026-03-28 bp-pipeline / skeleton-pipe Phase 4: проверять enum-значения при генерации конфигов

**Seen:** 1
**Triad:** генерация конфигурационного файла с enum-полями (frontmatter, YAML, JSON schema) → проверить допустимые значения enum перед записью → избежать невалидных значений, которые выглядят правдоподобно но отклоняются средой
**Context:** В agent-файле записал `model: claude-sonnet-4-6` — выглядит логично (полный model ID), но Claude Code принимает только `sonnet|opus|haiku|inherit`. IDE диагностика поймала, без неё ошибка проявилась бы только в runtime.
**Pattern:** При генерации конфигурационных файлов с enum-полями — не подставляй "логичный" вариант, а проверь список допустимых значений из документации или схемы. "Правдоподобно" ≠ "валидно".
**Scope:** universal
**Category:** tool-selection

### 2026-03-28 mvp-parser / session 4: Кэш обработанных записей при работе с платным API

**Seen:** 1 (this feature/session)
**Triad:** платный API с лимитом + данные пересекаются между запусками → кэшировать обработанные записи в БД, пропускать известные → не тратить квоту на уже обработанные данные
**Context:** parser-api.com, 200 квот/месяц, 231 дело/день — без кэша квота сгорает за 1 день полностью. С кэшем (пропуск уже известных case_number) расход падает в 5-7 раз со второго дня.
**Pattern:** При интеграции с любым платным API с лимитом запросов — сразу закладывай кэш обработанных записей в БД. Перед запросом details/enrichment проверяй, есть ли запись в базе. Это не оптимизация, а обязательный паттерн — без него лимит может сгореть за один запуск.
**Scope:** universal
**Category:** information-gathering

### 2026-03-28 mvp-parser / session 5: Фильтр по модели знаний читателя при написании документации

**Seen:** 1
**Triad:** написание клиентской документации от имени пользователя → пройти каждый абзац через фильтр «что читатель уже знает / что не может увидеть сам / почему это работает так» → избежать итеративных коррекций от пользователя
**Context:** 5 раундов коррекций на документе для заказчика: (1) забыл упомянуть ООО/АО как запланированные, (2) не объяснил ПОЧЕМУ парсер сам фильтрует по сумме, (3) объяснил размер пакета, который заказчик и так знает, (4) не назвал второй сервис по имени. Все ошибки одной природы — документ описывал систему с точки зрения разработчика, а не с точки зрения читателя.
**Pattern:** При написании клиентской документации делать «reader filter» проход по каждому абзацу: (1) читатель уже это знает? → убрать, (2) видит ли читатель откуда берутся данные? → назвать каждый источник, (3) понимает ли читатель ПОЧЕМУ ограничение существует? → объяснить причину. Режим по умолчанию «описать систему» пропускает все три.
**Scope:** universal
**Category:** communication

### 2026-03-28 ai-dev-methodology / ad-hoc: "Пусто" ≠ "данных нет" — проверь все каналы

**Seen:** 1
**Triad:** запрос данных из внешней системы вернул "пусто" → перечислить и проверить все каналы/endpoints где данные могут храниться → не пропустить данные в альтернативном канале
**Context:** `gh pr list --json comments` вернул 0 комментариев для обоих PR. На самом деле Codex-бот оставил 5 review comments (inline на строках кода). GitHub хранит комментарии в 3 местах: issue comments, PR conversation, PR review comments — каждый со своим API-эндпоинтом. Первый запрос проверил только один.
**Pattern:** Когда запрос к внешней системе вернул пустой результат, но есть основания полагать что данные существуют — не заключай "ничего нет". Перечисли все каналы/endpoints где данные могут храниться (GitHub: issues/comments + pulls/comments + pulls/reviews; Slack: channel + threads; Jira: comments + linked issues) и проверь каждый.
**Scope:** universal
**Category:** information-gathering

### 2026-03-28 employee-dashboard / session 3: Auth credentials для импортированных данных

**Seen:** 1
**Triad:** добавление auth flow к данным, импортированным вне seed → проверить что все записи имеют auth credentials → не обнаруживать missing auth на user verification
**Context:** Сотрудники были импортированы на прод вручную (вне seed.ts). При деплое employee-dashboard — credential для Горбунова существовала, но isActive=false. Обнаружено только при user verification ("Доступ заблокирован"). Потребовался debug-скрипт и ручной UPDATE.
**Pattern:** При добавлении auth flow — проверять не только наличие credential records, но и их isActive status. Для данных, импортированных вне стандартного seed — написать миграционный скрипт, который создаёт/активирует credentials.
**Scope:** universal
**Category:** sequencing

### 2026-03-28 performance-review / session 2: Маскируй секреты ДО выполнения команды

**Seen:** 2 → PROMOTED to code-writing
**Triad:** чтение конфигов удалённой системы для диагностики → маскировать секретные поля в самой команде (sed/pipe), не полагаться на пост-обработку → не допустить утечку секретов в персистентные логи сессии
**Context:** (1) При диагностике скорости VPS: `cat .env | grep DATABASE` — пароль PostgreSQL в логах. (2) 2026-03-29: повторно `grep DATABASE_URL .env` на сервере — пароль снова в логах. Два сайта недоступны несколько часов.
**Pattern:** При любом чтении конфигов с удалённой машины — встраивать маскировку прямо в команду (`sed 's/:[^@]*@/:***@/'`). Лучше: проверять наличие переменной без вывода значения (`grep -c`). Никогда не выводить .env, credentials, secrets целиком — даже если кажется что "это только в контексте".
**Scope:** universal
**Category:** tool-selection

### 2026-03-28 performance-review / deploy-fix: Чисти ресурс по identity, не по management context

**Seen:** 1
**Triad:** deploy script с именованным ресурсом (container_name, named volume, PID-файл) → чистить по identity (имя/ID), а не через management tool (compose down) → предотвратить сбой от orphaned ресурса, созданного другим инструментом или прерванным запуском
**Context:** `docker compose -f docker-compose.prod.yml down` не удалял контейнер `analiticxxs-app`, созданный ранее через другой compose-файл или ручной запуск. Deploy падал с "container already exists". Фикс: `docker rm -f analiticxxs-app` перед `compose down`.
**Pattern:** Если deploy/teardown скрипт управляет именованным ресурсом — чисти его напрямую по имени (`docker rm -f`, `rm -f pidfile`, `kill $(cat pidfile)`), а не только через management tool (`compose down`, `systemctl stop`). Management tool знает только о "своих" ресурсах, но ресурс с тем же именем мог быть создан другим способом.
**Scope:** universal
**Category:** sequencing

### 2026-03-28 performance-review / analiticxxs: Timing с первого дня в комплексных проектах

**Seen:** 1
**Triad:** старт комплексного проекта по методологии → включить server action timing (withTiming-обёртка + таблица + UI) в scope MVP → иметь baseline метрик до оптимизаций, видеть деградацию на проде
**Context:** В AnaliticXXS timing добавлен постфактум — после 4 блоков оптимизаций. Baseline "до" потерян, сравнить before/after невозможно. Если бы timing был с MVP — каждая оптимизация имела бы измеримый эффект.
**Pattern:** В комплексных проектах включать server action timing в MVP scope наравне с audit log. Стоимость минимальна (модель + обёртка + 1 страница), а ценность растёт с каждой итерацией: baseline → оптимизации → мониторинг деградации.
**Scope:** universal
**Category:** sequencing

### 2026-03-30 design-pipeline-v2 / session 2: Off-by-one в bounded loops — тестировать граничное значение

**Seen:** 1
**Triad:** AC содержит числовую границу (max N iterations/attempts/rounds) → включить граничное значение N в smoke или AC как executable check → поймать off-by-one до code audit
**Context:** design-session-execution Phase 3 Step 4 написан как `< 3` вместо `<= 3`, что даёт только 2 re-spawn вместо заявленных 3. Дефект обнаружен только на wave 3 code audit (Task 5), хотя фича была почти готова.
**Pattern:** Если AC описывает "max N iterations/retries/rounds" — добавь в smoke-команду или в отдельный AC check условие с граничным значением N. Компилятор и unit-тесты не ловят off-by-one в условиях цикла агента; только явный тест на граничное значение даёт гарантию.
**Scope:** universal
**Category:** sequencing

### 2026-03-30 design-pipeline-v2 / session 2: TRIZ-идеальность при выборе между эквивалентными фиксами

**Seen:** 1
**Triad:** два варианта фикса корректны, но один требует ручного обновления при эволюции артефакта → применить TRIZ-принцип идеальности — выбрать вариант с нулевой стоимостью обслуживания → не создавать технический долг при исправлении
**Context:** design-done Step 6: зафиксировать ретроспективные артефакты через `git add <specific files>` (точность) vs `git add -A` (идеальность). При росте design-system выходные файлы ретроспективы меняются — `git add <files>` требовало бы ручного обновления скилла при каждом расширении.
**Pattern:** При выборе между двумя корректными исправлениями — оцени стоимость обслуживания каждого через TRIZ-принцип идеальности: выбирай вариант, который не требует изменений при эволюции системы. "Идеальная" система делает своё дело сама, без вмешательства.
**Scope:** universal
**Category:** problem-decomposition

<!-- PROMOTED → feature-execution (Seen: 2, 2026-03-30) -->

### 2026-03-30 methodology-sync-sketch / session 1: агент-файл для multi-context — нейтральные сигналы завершения

**Seen:** 1 (methodology-sync-sketch / session 1)
**Triad:** написание агент-файла, который используется и inline, и через spawn_agent → не использовать ссылки на родительский контекст ("return to Phase N"), давать нейтральный сигнал завершения ("task complete. [result]") → артефакт работает корректно в обоих execution environments
**Context:** sketch-interviewer.md написан с `"return to SKILL.md Phase 5"` — это работает в Claude Code (inline load), но ломается в Codex spawn_agent где агент не знает про родителя.
**Pattern:** Когда файл агента предназначен для нескольких execution environments (inline + spawned) — описывать завершение нейтрально: "task complete. [result description]". Вызывающая сторона сама решает что делать дальше. Back-reference на parent step — это coupling на конкретную среду.
**Scope:** universal
**Category:** sequencing

## Situational

Patterns that apply only in specific contexts. Each has a `Situation` field describing when it's relevant.

<!-- Append situational patterns below -->

<!-- PROMOTED → feature-execution (Seen: 2, 2026-03-30) -->

### 2026-03-26 shift-confirmation: Ошибки повторяются между волнами

**Seen:** 1
**Triad:** ревью нашло паттерн ошибки (не разовый баг) → добавить предупреждение в промт следующего teammate → предотвратить повторение ошибки в следующих задачах
**Context:** В Task 1 ревьюер нашёл `confirmationStatus: string` вместо enum. Исправили. В Task 4 — ровно та же ошибка. Агент Task 4 не знал о находке Task 1, т.к. каждый teammate с чистым контекстом.
**Pattern:** Когда ревью находит паттерн ошибки (не разовый баг), lead добавляет предупреждение в промт следующего teammate: "В предыдущих задачах ревьюеры находили [X] — убедись, что новый код не повторяет эту ошибку."
**Scope:** situational
**Situation:** multi-agent feature execution с несколькими волнами
**Category:** communication

<!-- PROMOTED → code-writing (Seen: 2, 2026-03-30) -->

### 2026-03-26 shift-confirmation: Known-issues реестр для аудитов

**Seen:** 1
**Triad:** security/code audit в multi-task feature → вести known-issues.md, аудитор читает перед ревью → не тратить время на повторный репорт известных проблем
**Context:** Security auditor нашёл IDOR в `markEvent()` при ревью Task 2. Та же находка повторилась в audit wave. Нет реестра известных проблем — тратит время на уже известное.
**Pattern:** Завести `known-issues.md` на уровне проекта. Перед ревью агент читает его и пропускает задокументированные проблемы.
**Scope:** situational
**Situation:** multi-task features с security/code audit
**Category:** information-gathering

### 2026-03-28 mvp-pipeline-core + mvp-parser: Тесты на моках скрывают расхождение с реальным внешним процессом

**Seen:** 2
**Triad:** unit-тесты с моками для внешнего процесса/API → провести минимум 1 live smoke-прогон перед объявлением QA passed → предотвратить ложное "all tests pass" при расхождении мока и реальности
**Context:** (1) mvp-parser: 75 тестов pass, но реальный API возвращал другую структуру. (2) mvp-pipeline-core: 77 тестов pass, QA passed — но реальный `claude -p` вернул JSON в envelope + markdown fences + свой формат полей. 7 fix-коммитов после "успешного" QA.
**Pattern:** Перед объявлением QA passed — сделать минимум 1 live прогон с реальным внешним процессом (API/CLI). Не доверять мокнутым тестам для валидации интеграции. Сохранить реальный ответ как golden fixture.
**Scope:** universal
**Category:** information-gathering

### 2026-03-28 mvp-parser / live-test: Программное создание документа — зачищай дефолтные артефакты

**Seen:** 1
**Triad:** программное создание документа через API → после создания кастомного контента удалить дефолтные артефакты → не оставлять мусор в финальном документе
**Context:** При создании spreadsheet через API дефолтный лист остался пустым рядом с кастомными вкладками. Проверка пустоты по техническому свойству (row_count) не сработала — свойство имеет ненулевой default. Фикс: идентифицировать дефолтные артефакты по имени.
**Pattern:** При программном создании документа через API — проверить какие дефолтные элементы создаются автоматически и зачистить их после наполнения кастомным контентом. Идентифицировать дефолтные элементы по имени/типу, не по содержимому (пустота может не определяться из-за default-значений).
**Scope:** universal
**Category:** tool-selection


<!-- PROMOTED → feature-execution SKILL.md (2026-03-30, Seen: 2) -->

### 2026-03-28 bp-pipeline / skeleton-pipe: Язык пользователя, не профессиональный жаргон

**Seen:** 1
**Triad:** обсуждение решений с пользователем → использовать язык и терминологию пользователя, расшифровывать каждый термин → ускорить принятие решений, не тратить время на "а что это значит?"
**Context:** Спорные пункты pipeline.md были описаны с аббревиатурами (T1/T2/T3, ICE, severity levels). Пользователь сказал: "я не знаю что такое Т1, ты знаешь, не сокращай ничего". После переформулирования простым языком — все 6 решений приняты за один раунд.
**Pattern:** При обсуждении решений с пользователем — каждый термин расшифровывать при первом упоминании, объяснять последствия на примерах из его домена. Если пользователь хоть раз спросил "что это?" — это сигнал переключиться на простой язык для ВСЕХ последующих обсуждений.
**Scope:** universal
**Category:** communication

### 2026-03-27 mvp-parser / live-test: Проверить стоимость retry до включения

**Seen:** 1
**Triad:** API с лимитом запросов + retry decorator → проверить считаются ли неудачные запросы в лимит ДО включения retry → не сжечь квоту на бессмысленные повторы
**Context:** retry_with_backoff на parser-api.com сжёг 51 запрос из 200/месяц за одну сессию. Каждый обрыв соединения (ConnectionError, ReadTimeout) = запрос списан. Документация не указывает, считаются ли failed requests. Предположение "считаются только успешные" оказалось ложным.
**Pattern:** Перед добавлением retry на API с жёстким лимитом, сделать 2-3 тестовых запроса и сверить счётчик через /stat/ (или аналог). Если failed считаются — retry убрать или ограничить 1 попыткой.
**Scope:** universal
**Category:** tool-selection

### 2026-03-28 mvp-parser / session 3: Согласуй структуру выходного артефакта до реализации

**Seen:** 1
**Triad:** требования к формату выходных данных поступают итеративно → согласовать полную структуру на макете до написания кода → не переписывать реализацию на каждое уточнение
**Context:** Структура экспорта менялась 4 раза за сессию. Каждое изменение = переписывание export + query + тесты.
**Pattern:** Когда фича генерирует выходной артефакт для заказчика — показать пример на 2-3 строках и получить подтверждение структуры ДО реализации. Цена согласования минимальна, цена переделки кратна количеству итераций.
**Scope:** universal
**Category:** scope-management

### 2026-03-28 design-pipeline-v2 / techspec: Verify-smoke для markdown — проверяй структуру, не ключевые слова

**Seen:** 1
**Triad:** verify-smoke для markdown-артефакта (SKILL.md, шаблон) → проверять структурные элементы (фазы, ссылки на файлы, guard-ы), не просто ключевые слова → убедиться что артефакт полноценный, а не stub с нужными словами
**Context:** Изначально verify-smoke для ~180-строчного deep skill содержал 2 grep-проверки (имя скилла + слово "Phase"). Test reviewer справедливо указал: SKILL.md из одной строки с этими словами пройдёт проверку. После фикса — 6-8 проверок: Phase 0, Phase 2, ссылки на input-файлы, corruption guard.
**Pattern:** Для markdown-only артефактов verify-smoke должен проверять не наличие слов, а структурные элементы: (1) множественные фазы по номерам, (2) ссылки на input/output файлы, (3) guard-ы для edge cases, (4) resolution ссылок на reference-файлы. Количество проверок пропорционально размеру артефакта.
**Scope:** universal
**Category:** tool-selection

### 2026-03-28 design-pipeline-v2 / userspec: Генерируй все шаги deliverable целиком, не только ближайший

**Seen:** 2
**Triad:** создание multi-step deliverable (план, roadmap, серия промптов) → сгенерировать все шаги целиком, не только ближайший → не заставлять пользователя ловить недостающие части
**Context:** Создал промпт только для Session 1 из 6. Пользователь сразу заметил что промпт для Session 2 будет некорректным. Пришлось создавать session-roadmap.md со всеми промптами — то, что нужно было сделать сразу.
**Pattern:** Когда deliverable состоит из нескольких шагов (серия промптов, roadmap, план сессий) — генерировать ВСЕ шаги сразу, даже если пользователь явно просил только следующий. Предвидеть проблему устаревания, а не ждать пока пользователь её поймает.
**Scope:** universal
**Category:** scope-management

### 2026-03-28 analiticxxs / perf-fix: Проверяй дефолты библиотек до оптимизации кода

**Seen:** 1
**Triad:** performance problem на сервере с низким трафиком → проверить дефолтные таймауты/лимиты connection pool и кэшей → найти root cause в конфигурации до оптимизации кода
**Context:** TTFB 7-23 секунд на Next.js SSR. Инстинкт — искать тяжёлые запросы, N+1, SSR complexity. Реальная причина: pg Pool `idleTimeoutMillis: 10000` (дефолт) — на low-traffic сервере ВСЕ соединения закрывались каждые 10 секунд, каждый запрос = DNS + TCP + PG handshake. Фикс: одно число `10000 → 60000` = TTFB с 7-23 сек до 196 мс.
**Pattern:** При performance-проблемах на low-traffic серверах — первым делом проверять дефолтные таймауты и лимиты библиотек (connection pool idle timeout, cache TTL, keepalive). Одно число в конфиге часто даёт больше, чем рефакторинг запросов.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 methodology-sync-sketch / techspec: Файловые пути — верифицировать, не угадывать (PROMOTED)

**Seen:** 2 → PROMOTED → tech-spec-planning
**Triad:** написание файловых путей в tech-spec или skill из памяти/docs → верифицировать через ls/glob или прочитать source-файл → не допустить неверных путей в artifacts
**Context:** (1) design-task-decompose: путь к session-plan.md указан по аналогии, реальный путь отличался. (2) methodology-sync-sketch: tech-spec написал `~/.claude/skills/shared/work-templates/`, реальный — `~/.claude/shared/work-templates/`. Оба поймал mirage detector в validation round 1.
**Pattern:** Перед написанием любого файлового пути в tech-spec — верифицировать ls/glob. Architecture docs описывают намерение, а не факт filesystem.
**Scope:** universal
**Category:** information-gathering

### 2026-03-29 fix-knowledge-pipeline / decompose: Заменяй межзадачную зависимость на общий source of truth

**Seen:** 1
**Triad:** задача в одной волне ссылается на результат другой задачи той же волны → заменить зависимость на чтение общего source of truth (decisions.md, tech-spec.md) → сохранить параллельность волны без рисков read-after-write
**Context:** Task 2 (align retrospective) ссылалась на quick-learning/SKILL.md "after Task 1 modifies it", но обе задачи в Wave 1 (параллельно). depends_on: [1] + wave: 1 — противоречие. Решение: Task 2 читает decisions.md напрямую (те же решения, но source of truth, а не output другой задачи). Зависимость убрана, параллельность сохранена.
**Pattern:** При декомпозиции на параллельные задачи — если задача "читает результат другой" в той же волне, заменить зависимость на чтение общего документа (decisions.md, tech-spec.md). Если это невозможно — перенести задачу в следующую волну. Третьего не дано: depends_on + same wave = гонка данных.
**Scope:** universal
**Category:** problem-decomposition

### 2026-03-29 missing-ui-details / wave-2: Сверяй типографику с референсом ДО реализации

**Seen:** 1
**Triad:** визуальная задача с референс-скриншотами → сверить типографику (шрифт, вес, размер, padding) с референсом ДО написания CSS → избежать серии итеративных fix-коммитов по визуальному несоответствию
**Context:** Task 2 (visual polish) выполнен по спеку, но спек не описывал конкретный шрифт и пропорции. Пользователь увидел несоответствие — 9 fix-коммитов подряд: condensed шрифт, +20% размер, padding, кнопки, единообразие строк. Каждый fix был очевиден при сравнении с референсом.
**Pattern:** Перед реализацией визуальной задачи с референсами — открыть скриншот и составить чеклист: шрифт (семейство, condensed/normal), размеры относительно строки, вес, межстрочные отступы, цвет акцентов. Реализовывать по чеклисту, не по абстрактному описанию в спеке.
**Scope:** universal
**Category:** information-gathering

### 2026-03-29 pipeline-stabilization / session 1: Перед ревью — проверить артефакты удаления

**Seen:** 1
**Triad:** задача на удаление фичи/константы/поля → перед отправкой на ревью проверить dead variables, stale comments, duplicate tests от удалённого кода → не тратить review-раунд на предсказуемые артефакты удаления
**Context:** Task 1 удалил MAX_OUTPUT_CHARS и два поля из REQUIRED_FIELDS. Task 2 удалил extended mode и wave-поля. Все 6 ревьюеров нашли только minor-находки: мёртвая переменная `missing` (ссылалась на удалённый check), stale-комментарии с "extended", дублирующийся тест (старый обновлён до пустого набора — совпал с новым TDD-тестом). Все предсказуемы.
**Pattern:** После задачи на удаление — перед отправкой на ревью пройти чеклист: (1) dead variables/imports, ссылающиеся на удалённый код, (2) комментарии/docstrings, упоминающие удалённую функциональность, (3) тесты, ставшие дублями или тестирующие удалённое поведение. Три минуты проверки экономят review-раунд.
**Scope:** universal
**Category:** sequencing

### 2026-03-29 pipeline-stabilization / session 2: При редактировании AI-промтов — явно проверять emphasis-framing

**Seen:** 1
**Triad:** редактирование/компрессия AI-промта → явно проверить все prohibition/caps формулировки ("НЕЛЬЗЯ", "ЖЁСТКИЕ ОГРАНИЧЕНИЯ", "ГЛАВНОЕ ПРАВИЛО") и заменить на motivation-framing → не тратить review-раунды на предсказуемую emphasis-ошибку
**Context:** Tasks 4, 5, 6 (компрессия agent-04..10) — три задачи подряд получили major-находку от prompt-reviewer: prohibition lists и капслок ("СТРОГО СОБЛЮДАЙ", "ЖЁСТКИЕ ОГРАНИЧЕНИЯ", "ГЛАВНОЕ ПРАВИЛО"). Паттерн повторился во всех трёх задачах. Все найдены в одном review-раунде и исправлены в одном коммите.
**Pattern:** При редактировании или компрессии AI-промтов — добавить финальный чеклист перед ревью: (1) найти все КАПСЛОК-заголовки, (2) найти все формулировки "нельзя/запрещено/жёсткие/строгие", (3) заменить на мотивационное обоснование ("чтобы X, делай Y" вместо "ЗАПРЕЩЕНО делать Y"). Prohibition-framing — предсказуемая находка в любом AI-промте.
**Scope:** universal
**Category:** sequencing

### 2026-03-29 fix-knowledge-pipeline: Overflow-политика при распределении в capped buckets

**Seen:** 1
**Triad:** алгоритм распределяет записи по bucket-ам с max-cap → определить overflow-политику (куда идут записи сверх лимита) до реализации → не терять записи при заполнении bucket-а
**Context:** Task 5 генерировал per-skill quick-ref файлы с лимитом 10 записей. quick-ref-feature-execution.md заполнился (10 записей из sequencing/recovery/communication), запись #32 была молча отброшена. Reviewer обнаружил: #32 должна попасть в do-task (overflow bucket). Задача не описывала overflow-поведение.
**Pattern:** При реализации алгоритма "распределить N элементов по M buckets с max-cap" — явно определить политику overflow до написания кода: (1) куда попадают элементы сверх cap (следующий bucket, default bucket, ошибка), (2) как проверить что ни один элемент не потерян. Без явной политики реализатор молча выбросит overflow.
**Scope:** universal
**Category:** tool-selection

### 2026-03-29 design-pipeline-v2 v2.3 / session 1: При cross-domain адаптации шаблона — проверять совместимость каждого поля

**Seen:** 1
**Triad:** адаптация шаблона задачи из одного домена в другой → проверить каждое поле frontmatter на применимость к целевому домену → не исправлять domain-несовместимые defaults отдельной задачей после деплоя
**Context:** design-task.md.template был создан в v2.2 по образцу task.md.template. Поле `reviewers: [skill-checker]` скопировано из code-domain шаблона — там оно осмысленно. В design-domain quality gate — user visual review, не skill-checker. Несовместимость обнаружена при написании tech-spec v2.3 и потребовала отдельной Task 2 в следующей версии.
**Pattern:** При адаптации шаблона из одного домена в другой — пройти каждое поле frontmatter через вопрос "это поле имеет смысл в целевом домене?". Если нет — изменить default прямо при адаптации, не копировать как есть. Несовместимые defaults, скопированные "на потом", становятся отдельными задачами в следующей итерации.
**Scope:** universal
**Category:** sequencing

### 2026-03-29 design-pipeline-v2 v2.3 / task-decomposition: Пилотная задача перед массовой генерацией по новому шаблону

**Seen:** 1
**Triad:** массовая генерация задач по шаблону, применяемому к новому домену впервые → сначала 1 пилотная задача → проверить и валидировать → масштабировать на все задачи → не накапливать 30+ правок при первом прогоне
**Context:** task-creator сгенерировал 8 задач по design-task.md.template за один прогон. Validation round 1 дал 30+ находок (несовместимые поля, неверные пути, domain-mismatch в reviewers). Если бы задача 1 была проверена первой — паттерн ошибок был бы найден до масштабирования на 7 оставшихся.
**Pattern:** При первом применении шаблона к новому домену — сгенерировать 1 пилотную задачу, прогнать через валидатор, зафиксировать все несоответствия. Только после успешной пилотной — генерировать остальные. Стоимость пилота минимальна; стоимость 30+ правок в 8 задачах — в 8 раз выше.
**Scope:** universal
**Category:** problem-decomposition

### 2026-03-29 pipeline-stabilization / session-3: Security severity привязывается к модели развёртывания

**Seen:** 3 → PROMOTED to security-auditor
**Triad:** security audit находит medium-уязвимости в локальном CLI-инструменте → классифицировать как non-blocking с явным условием "до перехода на service/multi-user деплой" → не блокировать релиз по находкам нерелевантным текущей модели развёртывания
**Context:** Task 9 нашла 3 medium-находки (отсутствие hard-limit на --text, произвольный --data-dir, отсутствие size limits на validator fields). Все три реальны и требуют fix — но только перед service deployment. Для single-user CLI они не создают угрозы.
**Pattern:** При аудите безопасности явно привязывать severity к модели развёртывания. Medium-находка в single-user CLI и medium-находка в multi-user service — разные приоритеты. Записывать условие перехода ("before service deployment") прямо в статус задачи, не только в comments.
**Scope:** situational
**Situation:** инструмент развёртывается как локальный CLI для одного пользователя; есть планы перейти на service-модель
**Category:** scope-management

<!-- PROMOTED → task-decomposition (Seen: 2, 2026-03-30) -->

### 2026-03-29 pipeline-stabilization / session-3: QA разделяет failed и deferred

**Seen:** 1
**Triad:** QA-критерий требует live-вызова внешнего сервиса (LLM, API, DB) недоступного в test-среде → отметить как deferred с явным условием, не как failed → получить чистый QA pass на автоматизируемых критериях без блокировки
**Context:** Task 11 (pre-deploy QA) прошла 20 из 22 критериев. 2 оставшихся требуют live Claude CLI вызова с активной подпиской. Вместо fail или skip — deferred с записью в deferredToPostDeploy, что даёт чёткий план для post-deploy verification.
**Pattern:** В QA-отчёте явно разделять три статуса: passed, failed, deferred. Deferred — критерий, истинность которого не может быть проверена автоматически (требует live-среды, подписки, внешнего пользователя). Deferred не блокирует релиз, но создаёт обязательный чеклист для post-deploy. Не смешивать с "не успели проверить".
**Scope:** universal
**Category:** sequencing

### 2026-03-29 analiticxxs / recovery: Давай команды по одной нетехническому пользователю

**Seen:** 1
**Triad:** нетехнический пользователь выполняет команды на сервере по инструкции → давать по одной команде с явным "запусти, скажи результат" между шагами → предотвратить вставку блока в неправильный контекст
**Context:** Пользователь вставил весь блок команд (read + ALTER USER + python3 + pm2) прямо в psql вместо bash. В результате пароль postgres установлен буквально как "$NEWPASS" вместо реального значения.
**Pattern:** Когда пользователь выполняет команды на сервере вручную — никогда не давать блоки. Давать ровно одну команду, ждать вывода, убедиться что контекст правильный, только потом следующую.
**Scope:** situational
**Situation:** нетехнический пользователь выполняет команды на сервере (psql, bash, python repl)
**Category:** communication

### 2026-03-30 design-pipeline-v2 v2.3: Граничное условие счётчика — верифицируй против спецификации

**Seen:** 1
**Triad:** написание числовой логики с граничным условием (max N повторений, retry limit, iteration cap) → сразу подставить граничное значение и убедиться что условие выполняется ровно N раз → не пропустить off-by-one через code review
**Context:** Wave-итерации в design-session-execution: counter=1, условие `< 3` — вместо 3 re-spawn получилось 2. Decision 9 требовал max 3 итерации. Code audit (HIGH finding) поймал; обычный review не заметил бы. Fix: `< 3` → `<= 3`.
**Pattern:** При написании логики "повторять максимум N раз" — сразу подставить граничное значение и посчитать итерации вручную: если counter=1, то `<= N` даёт N итераций, `< N` даёт N-1. Off-by-one визуально неотличим от правильного кода — review ловит редко.
**Scope:** universal
**Category:** sequencing

### 2026-03-30 design-pipeline-v2 v2.3: git add scope должен покрывать все write locations скилла

**Seen:** 1
**Triad:** скилл или агент делает commit и пишет файлы в несколько директорий → перечислить все write locations из тела скилла перед написанием git add → не потерять файлы вне основного дерева при коммите
**Context:** design-done: `git add work/completed/{feature}/` не захватывал `.design-system/` файлы, которые design-retrospective пишет в корне проекта. Архивный коммит был неполным. HIGH finding на code audit; fix: `git add -A`.
**Pattern:** При написании шага commit в скилле — просмотреть все фазы, которые пишут файлы, и составить список write locations. Если хотя бы одна запись происходит вне основной директории — использовать `git add -A`. Path-specific `git add` скрыто ломается при добавлении новых write locations в будущем.
**Scope:** universal
**Category:** sequencing

### 2026-03-30 design-pipeline-v2 v2.3: TRIZ для выбора между равнозначными вариантами фикса

**Seen:** 1
**Triad:** два варианта фикса дают одинаковый результат но отличаются по устойчивости к будущим изменениям → применить tradeoff-анализ (minimal diff vs systemic robustness) → выбрать вариант с меньшим coupling к текущим деталям реализации
**Context:** HIGH #1: `< 3` vs `counter=0` — оба дают 3 итерации, но `<= 3` семантически точнее и ближе к спецификации. HIGH #2: `git add work/completed/` vs `git add -A` — оба фиксируют текущие файлы, но `-A` устойчив к добавлению новых write locations. Оба выбора сделаны за один раунд без обсуждения.
**Pattern:** Когда два варианта фикса технически корректны — проверить: (1) какой вариант продолжает работать при изменении смежного требования, (2) какой вариант создаёт меньше implicit coupling с деталями реализации. Выбрать более устойчивый даже если diff чуть больше.
**Scope:** universal
**Category:** tool-selection

### 2026-03-30 agent-research-prompt-fix userspec: поведение агента после пропуска — логика, не маркер

**Seen:** 1
**Triad:** описание skip-поведения агента при пустом user input → явно описать что агент ДЕЛАЕТ после пропуска (продолжает анализ), не только какой маркер ставит в поле → не допустить реализации label-swap без изменения логики
**Context:** Спек описывал [ПРОПУЩЕНО ПОЛЬЗОВАТЕЛЕМ] как замену [НЕТ ДАННЫХ]. Пользователь уточнил: агент должен реально завершить анализ с имеющимися данными, а не просто переименовать заглушку. Разница критическая для реализации.
**Pattern:** Когда описываешь поведение агента при пустом/пропущенном вводе — формулируй не только output marker, но и processing logic: "агент продолжает анализ с тем, что есть, и помечает только вычислительно недостижимые поля". Без явной processing logic разработчик реализует label-swap.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 agent-research-prompt-fix userspec: active + planned stubs для многочастного скопа

**Seen:** 1
**Triad:** user spec вырастает до 3+ последовательно зависимых deliverable разного размера → оставить первый deliverable active draft, остальные создать как planned stubs → пользователь видит прогресс на каждой части и контекст постфич сохранён
**Context:** Спек начался как 3 пункта, вырос до 4, потом пользователь попросил разбить "чтобы видеть прогресс". Создали 3 отдельных файла: part1 (active/approved), part2+3 (planned). Части 2 и 3 полностью проработаны для контекста, но не запускаются сразу.
**Pattern:** Если feature вырастает до 3+ частей с чёткими зависимостями — не пытайся уместить всё в один спек. Создай первую часть как active draft, остальные как planned stubs с полным описанием. Это даёт видимость прогресса без потери плана. Planned stubs не требуют повторного интервью при запуске.
**Scope:** universal
**Category:** scope-management

### 2026-03-30 design-v2 / session 1: Зона субъекта фото — до расстановки UI overlay

**Seen:** 1
**Triad:** размещение текста/UI поверх full-bleed фото → определить зону субъекта в кропированном вьюпорте ДО расстановки элементов → не перекрыть лицо/объект текстом
**Context:** Hero с portrait фото в landscape viewport — текст был поставлен по центру экрана и накрыл лицо стилиста. Потребовался полный редизайн grid-структуры.
**Pattern:** Перед расстановкой UI-элементов поверх фото — вычислить где окажется субъект после object-fit cover кропа. Portrait в landscape → субъект всегда около горизонтального центра. Текст ставить только в негативное пространство: низ (bottom gradient zone), крайний угол или зону без субъекта.
**Scope:** situational
**Situation:** Hero или full-bleed секция с фото, поверх которой размещаются текст или UI-блоки
**Category:** design-process

### 2026-03-30 design-v2 / session 1: Редизайн = независимый выбор layout, не наследование структуры

**Seen:** 1
**Triad:** задача "альтернативный дизайн" или "редизайн существующей страницы" → выбирать layout pattern независимо от существующей верстки → получить реальную альтернативу, а не ресайн с другими цветами
**Context:** Первый preview был отклонён ("всё ещё сильно основан на прошлой версии") — структура 50/50 split была перенесена из v1, изменены только шрифты и цвета.
**Pattern:** При задаче редизайна — не смотреть в существующий CSS/HTML при выборе layout. Начинать с вопроса: "как принципиально иначе можно показать этот контент?" Только после независимого решения сверяться с существующим кодом для понимания контента (тексты, фото), но не структуры.
**Scope:** situational
**Situation:** Задача создать v2, альтернативный вариант или редизайн существующей страницы
**Category:** design-iteration

### 2026-03-30 methodology-sync-sketch / session 1: Классификация глубины diff до написания sync scope

**Seen:** 1
**Triad:** планирование синка файлов между двумя версиями одного репо → запустить code-research для классификации глубины различий до написания scope → не описывать в AC механический синк который требует ручного ревью каждого файла
**Context:** Планировали синк 26 скиллов в Codex через замену путей (.claude/→.agents/). Code-research показал что 24 из 26 имеют реальные content-различия (feature-execution переписан под spawn_agent API) — scope пришлось полностью переписать.
**Pattern:** Перед тем как включить cross-repo sync в scope спека — запустить code-research с вопросом "path-only diff или content diff?". Если content diff > 50% файлов — это не механическая задача, это ручной ревью. Отдельная фича.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 methodology-sync-sketch / session 1: Итеративная классификация доменов в mono-repo

**Seen:** 1
**Triad:** репо содержит скиллы из нескольких доменов → явно перечислить каждый домен и получить is_in_scope per domain до написания спека → не переписывать scope в 3 итерации из-за постепенного уточнения границ
**Context:** Один репо содержит методологию, дизайн-пайплайн, promoter, skeleton-pipe, sketch. Уточнения "это отдельный пайплайн" происходили трижды (design → promoter/skeleton → уточнение что sketch ВХОДИТ). Каждый раз — реакция на вопрос.
**Pattern:** При старте user-spec для проекта с несколькими доменами — сразу предъявить полный список всего что есть в репо и попросить пометить каждый домен: in/out/separate. Одним вопросом, а не серией уточнений.
**Scope:** universal
**Category:** scope-management

### 2026-03-30 agent-research-prompt-fix / session 2: верифицировать содержимое каждого целевого файла перед описанием операции

**Seen:** 2 (agent-research-prompt-fix × 2)
**Triad:** spec (user, tech, task) называет набор файлов и описывает трансформацию → верифицировать каждый файл на наличие изменяемого элемента → не допустить ошибочный тип операции (replace вместо add)
**Context:** (1) User-spec назвал "runner.py" и "счётчик уже есть" — неточные утверждения, пойманы code-research. (2) Tech-spec описал "убрать [НЕТ ДАННЫХ] из всех 9 промптов" — agent-03 этой строки не содержит, нужна другая операция (add instruction). Поймано reality-checker при декомпозиции.
**Pattern:** Любой spec-артефакт (user-spec/tech-spec/task) доверяет, что файлы содержат описываемый элемент. Перед тем как зафиксировать "удалить X" или "заменить X" — grep по каждому целевому файлу. Файлы без X требуют операции add, не replace. Ошибка типа операции обнаруживается только при выполнении.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 agent-research-prompt-fix / session 2: тест с точной строкой-маркером создаёт неявный depends_on

**Seen:** 1 (agent-research-prompt-fix)
**Triad:** задача содержит тест с точной строкой-маркером определённой в другой задаче → объявить depends_on на задачу-источник даже если строка — литерал → не пропустить неявную зависимость через разделённый дизайн-маркер
**Context:** Task 4 содержала `test_propushcheno_not_pipeline_defect` ассертящий на `"[ПРОПУЩЕНО ПОЛЬЗОВАТЕЛЕМ]"`. Строка определяется в Task 2 (pipeline.py). Task 4 объявила only `depends_on: [1]`. Индивидуальные валидаторы пропустили — cross-task валидатор поймал.
**Pattern:** Если задача содержит тест ассертящий на конкретную строку/константу/маркер — проверить: кто принял дизайн-решение об этой строке? Задача-источник должна быть в depends_on даже если строка используется как литерал а не импортируется.
**Scope:** situational
**Situation:** multi-task декомпозиция с sentinel strings / protocol markers общими между задачами
**Category:** problem-decomposition

### 2026-03-30 methodology-sync-sketch / techspec: Каталог скиллов — читай ДО написания задач

**Seen:** 1
**Triad:** написание секции Implementation Tasks в tech-spec → прочитать skills-and-reviewers.md перед заполнением Skill и Reviewers → не использовать несуществующие или неверные skill-имена
**Context:** Tasks 1-5 использовали `write-code` (wrapper) вместо `skill-master`, `documentation-writing`. Template-validator поймал в validation round 1 — потребовал полный перезаголовок задач.
**Pattern:** Перед написанием Implementation Tasks — открыть `tech-spec-planning/references/skills-and-reviewers.md`. Wrapper-skills (`write-code`, `new-tech-spec`) не являются execution skills. Всегда проверять: skill в tasks = строка из каталога, не интуитивный псевдоним.
**Scope:** universal
**Category:** information-gathering

### 2026-03-30 pipeline-report / decompose: TDD Anchor для private метода — вызов через инстанс

**Seen:** 1
**Triad:** TDD Anchor описывает тест для private метода класса → указывать вызов через инстанс объекта, не через прямой импорт → тесты не падают с ImportError до запуска реальной логики
**Context:** task-creator написал TDD Anchor с инструкцией `import _generate_report from bp_pipeline.pipeline`. Private метод нельзя импортировать напрямую — reality-checker поймал как critical. Правка: `pipeline_instance._generate_report(session, session_dir)`.
**Pattern:** В TDD Anchor для private/protected метода — явно указывать паттерн доступа: создать инстанс класса, вызвать `instance._method()`. Не писать `from module import _method` — это ImportError. Актуально для любого языка с private convention (Python `_`, JS `#`).
**Scope:** situational
**Situation:** task-creator генерирует TDD Anchor для private метода класса
**Category:** problem-decomposition

### 2026-03-30 design-v2-stylist / session 2: Совместимость фото с контейнером — проверять до CSS

**Seen:** 1
**Triad:** выбор лейаута с full-bleed фото → проверить ориентацию фото и кадрирование субъекта против формы контейнера ДО написания CSS → не тратить итерации на геометрически невозможный кроп
**Context:** Портретное фото стилиста (субъект стоит в полный рост на фоне яркого окна) поставили в 50vh landscape-баннер. Ни один Y не мог показать субъекта — это геометрический факт определяемый до верстки. Понадобилось 3 итерации и полная переделка лейаута.
**Pattern:** Перед вёрсткой секции с фото: (1) посмотреть фото через Read, (2) проверить ориентацию (portrait/landscape), (3) оценить где субъект в кадре (верх/центр/низ, % от края), (4) сопоставить с контейнером. Если субъект занимает <30% ширины landscape-контейнера или фото portrait при контейнере landscape — сменить лейаут на тот, который сохраняет пропорцию.
**Scope:** situational
**Situation:** верстка секций с фотографиями в фиксированных контейнерах (hero, banner, split)
**Category:** design-process

### 2026-03-30 design-v2-stylist / session 2: Структурированные данные → UI напрямую

**Seen:** 1
**Triad:** верстка контентной секции из структурированных данных пользователя → маппировать каждое поле данных в UI-элемент напрямую → не изобретать структуру отображения которая расходится с источником
**Context:** Пользователь прислал услуги в формате: название → суть → цена → буллеты. Вместо прямого маппинга была создана отдельная таблица-индекс + аккордеон с другими именами. Потребовались 2 раунда переделки пока структура не совпала с источником.
**Pattern:** Получив от пользователя структурированные данные с явными полями — написать маппинг полей в HTML-элементы ДО верстки (поле_1 → тег_1, поле_2 → тег_2). Дополнительные UI-слои (таблица-индекс, фильтры) добавлять только если пользователь явно запросил.
**Scope:** universal
**Category:** design-process

### 2026-03-30 methodology-sync-sketch / code-audit: Граница ответственности SKILL.md vs. agent-file

**Seen:** 1
**Triad:** создание скилла с companion agent-file (SKILL.md + agents/{name}.md) → явно разграничить что делает SKILL.md (оркестрация фаз) и что делает agent-file (протокол одного шага) → избежать дублирования одного действия в обоих файлах
**Context:** sketch/SKILL.md Phase 3 и sketch-interviewer.md оба описывали сохранение sketch.md. Code audit поймал дублирование как minor finding — execution model оказалась неоднозначной: кто реально выполняет save?
**Pattern:** При написании скилла с companion agent-file: SKILL.md описывает ЧТО происходит на каждой фазе (вход, выход, переход), agent-file описывает КАК выполняется конкретный шаг внутри одной фазы. Каждое конкретное действие (save, send, transform) должно быть явно описано ровно в одном месте.
**Scope:** situational
**Situation:** Новый скилл делегирует часть логики в отдельный agents/{name}.md файл
**Category:** problem-decomposition

### 2026-03-30 pipeline-report / techspec: AC — единственная верификационная рамка при противоречии с описательным блоком

**Seen:** 1
**Triad:** user-spec содержит описательный блок с требованием не отражённым в AC → следовать только AC как источнику истины; противоречие зафиксировать decision-записью и обновить user-spec → не тащить неопределённость из описательного блока в реализацию
**Context:** pipeline-report: описательный блок говорил "стандартный запрос по шаблону поля" — AC этого не содержал. tech-spec принял AC за истину, оформил разрыв решением, обновил user-spec. Без этого разрыв дошёл бы до реализации как неоднозначность.
**Pattern:** Если user-spec содержит описательный блок с требованием не отражённым в AC — AC является источником истины. Зафиксировать разрыв в tech-spec decisions и обновить user-spec, иначе следующий агент снова наткнётся на то же противоречие и будет вынужден решать его самостоятельно.
**Scope:** universal
**Category:** scope-management

### 2026-03-30 pipeline-report / techspec: Файловые пути из десериализованных данных — валидировать против allowlist

**Seen:** 1
**Triad:** конструирование файловых путей из значений, десериализованных с диска → валидировать каждое значение против известного allowlist перед включением в path → предотвратить path traversal из данных, кажущихся доверенными
**Context:** pipeline-report: agent_id из stages_completed использовался в f"{agent_id}-output.json" без проверки. Скептик поймал CRITICAL — stages_completed читается с диска и может быть изменён между записью и чтением.
**Pattern:** Данные, прочитанные с диска, не являются доверенными, даже если записаны самим приложением. Перед построением файлового пути из таких значений — проверить каждое значение против allowlist (список допустимых идентификаторов). Исправление — одна строка; цена игнорирования — path traversal.
**Scope:** universal
**Category:** tool-selection

### 2026-03-30 methodology-sync-sketch / test-audit: grep в AVP чувствителен к регистру

**Seen:** 1
**Triad:** написание grep-based smoke check для markdown-контента → проверить фактический регистр строки в целевом файле перед финализацией команды → предотвратить ложно-отрицательный AVP check при несовпадении регистра
**Context:** AVP step 2 искал `'decision gate'` (lowercase), SKILL.md содержал `## Phase 6: Decision Gate` (Title Case). grep -c вернул бы 0 вместо ожидаемого ≥ 2. Поймано в test audit, не в момент написания AVP.
**Pattern:** При написании grep-смоков для markdown: открыть целевой файл и убедиться что искомая строка написана именно так. Если регистр не предсказуем (фаза, секция, метка) — добавить флаг -i. Правило: "сначала прочитай, потом grep".
**Scope:** universal
**Category:** tool-selection

### 2026-03-30 methodology-sync-sketch / done: Атомарная запись в shared-файл при конкурентных сессиях

**Seen:** 1
**Triad:** Edit tool возвращает "File has been unexpectedly modified" на shared файле методологии → переключиться на атомарный read-modify-write через скрипт, не повторять Edit → избежать накопления partial writes и дублирующихся записей
**Context:** При исправлении дублирующихся номеров в triad-index.md Edit tool 3 раза падал с "unexpectedly modified" — файл одновременно изменялся другими сессиями. Python-скрипт с прямой записью решил за 1 попытку.
**Pattern:** Первое "File has been unexpectedly modified" — сигнал конкурентной записи, не случайная ошибка. Не повторяй Edit — переключайся сразу на atomic read-modify-write: прочитать файл целиком, преобразовать в памяти, записать атомарно через скрипт.
**Scope:** situational
**Situation:** Shared файлы методологии (triad-index.md, reasoning-patterns.md), редактируемые из нескольких сессий одновременно
**Category:** recovery

### 2026-03-30 pipeline-report / session 1: параллельный запуск ломает смысловой порядок

**Seen:** 1
**Triad:** два шага процесса связаны по смыслу (A должен завершиться до показа B) → запускать A синхронно, ждать завершения, только потом выполнять B → гарантировать смысловой порядок — фоновый запуск A не означает A < B
**Context:** quick-learning запущен в фоне одновременно с генерацией next-session prompt — уведомление пришло после, нарушив ожидаемый порядок "сначала анализ, потом промт".
**Pattern:** Если два шага имеют смысловую зависимость для пользователя (B опирается на результат A или должен следовать после него), не оптимизируй под параллелизм — запускай A синхронно. Фоновый запуск сохраняет время, но ломает порядок и доверие.
**Scope:** universal
**Category:** sequencing

### 2026-03-30 photo-crop / session 1: структурные gate-вопросы при конвертации алгоритма в процедурный скилл

**Seen:** 1
**Triad:** конвертация пользовательского алгоритма (список шагов) в процедурный SKILL.md → добавить gate-вопрос («перечисли что определил на этом шаге») в конце каждой фазы, даже если его нет в оригинале → удовлетворить структурные требования процедурного скилла без повторного прогона валидатора
**Context:** пользователь передал 4-шаговый алгоритм для расчёта object-position; первый черновик точно воспроизвёл шаги, но пропустил межфазовые чекпоинты — skill-checker потребовал второй прогон.
**Pattern:** Пользовательский алгоритм — это контент, не формат. При конвертации в процедурный скилл добавляй checkpoint-gates независимо от исходника: в конце каждой фазы явно требуй от агента зафиксировать промежуточный результат перед переходом к следующему шагу.
**Scope:** situational
**Situation:** создание нового процедурного SKILL.md на основе алгоритма, предоставленного пользователем или взятого из документации
**Category:** sequencing
