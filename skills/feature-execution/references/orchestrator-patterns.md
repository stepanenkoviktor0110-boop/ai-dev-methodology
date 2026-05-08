# Orchestrator Learned Patterns

> Loaded by feature-execution lead at Phase 2 start. Meta-rules generalized from experience.
> Details in quick-learning triad-index.

**1. Серверные операции — проверяй preconditions:**
Перед deploy/restart/подключением verify: порт, push state (`git log origin..HEAD`), ручная проверка подключения, количество процессов на порту. Серверные проблемы имеют физические причины (порт занят, ISP-блок, hung process) — проверяй до дебага логики. Сервис недоступен с нескольких сетей при открытом порте = проблема провайдера → туннель/смена IP. В deploy script явно завершать зависшие процессы перед restart. Auth по ключу падает при корректных ключах — проверить права на home-dir.

**2. Пользовательские инструкции — уточняй scope:**
"Не нужен" → уточни: UI или вся функциональность (API, DB)? "X здесь, а не там" → добавь в новое место, убери только из названного. Неоднозначное название → покажи варианты, спроси. При нескольких похожих метриках/счётчиках — явно сопоставить термин пользователя с конкретной метрикой до ответа, не подменять один другим по схожести. Диагностический вопрос ≠ запрос на действие. Task file > prompt для значений.

**3. Любое изменение — проверяй радиус поражения:**
Изменён элемент из группы → примени к каждому sibling. Синхронизация файлов → проверь index-файлы. Hotfix вне плана → добавь в audit wave. Новый marker в промте → опиши во всех секциях. DRY-нарушение в N задачах → extraction-задача в audit. Validation добавлена в route → немедленно grep по имени поля во всех route-файлах, убедиться что structurally-similar endpoints имеют ту же validation. Смена домена → grep hardcoded CORS/CSRF/allowed_origins в кодовой базе и обновить ВСЕ до деплоя, иначе молчаливый 403 после переключения. Частный случай: пользователь изменил ранее принятое решение, зафиксированное в нескольких артефактах (spec, decisions, task) → сначала перечислить ВСЕ места захвата, затем синхронизировать одним заходом, чтобы reviewer не флажил phantom-противоречия из устаревших sibling-документов.

**4. Не подтверждай без проверки реальности:**
"Это работает?" → grep до ответа. Pipeline ok но экспорт упал → алерт на N consecutive 0. Тесты зелёные но покрытие иллюзорно → ad-hoc fix. Pre-existing failures → проверь working tree (git stash). Done только после проверки реального эффекта (файл создан ≠ фича работает; graceful fallback с success ≠ полнота — count/sample ключевых полей).

**5. Планирование задач — валидируй зависимости:**
depends_on=[N] в той же wave → проверить wave(dep) < wave(task). Фильтр ко всем колонкам → таблица тип→поведение до кода. Endpoint с resource_id без user_id → проверка роли target-user. Off-by-one в индексах → подставить числа вручную. State-файл → путь от якоря (db_path.parent), не от CWD.

**6. Порядок вызовов — лог после накопления:**
When функция log_*() вызывается до стадии-накопителя метрики → перенести вызов в конец всех накопительных стадий, to гарантировать полноту записи в лог.

**7. Non-ASCII в HTTP-ответах:**
When файл с non-ASCII именем отдаётся через HTTP Content-Disposition → использовать RFC 5987 encoding (filename*=UTF-8''...) + ASCII fallback, to предотвратить ByteString crash и некорректное имя при скачивании.

**8. Shared state для UI табов:**
When общий state объект для нескольких UI табов с разными типами данных → защищать доступ к type-specific полям optional chaining или разделять state по табам, to предотвратить runtime crash при переключении табов из-за stale данных чужого типа.

**9. Tunnel URL после перезапуска:**
When сервис с free tunnel перезапустился → считать новый tunnel URL и немедленно передать клиенту, to не оставлять клиента со старым нерабочим URL.

**10. Проверка запретов из спека перед коммитом:**
When task-файл содержит явный запрет ("NEVER X"), реализация нарушает запрет → grep по запрещённому паттерну в изменённых файлах ДО коммита, to не тратить review round на нарушение явного спрета из спека.

**11. Async агент — старт и мониторинг:**
When запуск async инструмента/агента с неизвестным временем выполнения → сообщить пользователю ожидаемое время ДО запуска + мониторить прогресс + при молчании >5 мин алертить; при отсутствии новых записей в лог — убить и перезапустить, to не допустить, что пользователь ждёт в неведении и не тратить 15+ мин на зависшую задачу.

**12. Визуальная фича — по одному экрану:**
When визуальная фича с несколькими экранами/блоками → показать один экран/блок полностью → дождаться одобрения → следующий, to получить ранний фидбэк на каждый экран до следующего.

**13. Баг после деплоя — upstream сначала:**
When фикс задеплоен и баг воспроизводится, или билд/деплой ОК но 4xx → проверить upstream-инфраструктуру (настройки платформы, framework detection, access policies, маппинг веток) до повторного анализа кода/DNS, to не тратить цикл деплоя на не тот слой.

**14. Внешний агент (Codex) — полный diff:**
When делегирование точечных правок внешнему агенту (Codex) → проверить полный git diff после завершения, не только целевые файлы, to поймать непрошеные изменения до коммита.

**15. DNS-миграция — .env после propagation:**
When DNS-миграция: .env содержит домен который ещё не пропагировался → менять .env и пересобирать ПОСЛЕ подтверждения dig A → новый IP, не параллельно с nginx, to не ломать работающий сайт на период пропагации DNS.

**16. Агрегация ресурса из параллельных прогонов:**
When агрегация расхода ресурса из параллельных запусков → использовать pool_start − pool_end вместо SUM(individual_spent), to получить корректный совокупный показатель без двойного счёта.

**17. Стоимость многошагового API — верифицируй математику:**
When объяснение стоимости многошагового API-процесса клиенту → посчитать каждый шаг отдельно и сверить сумму с фактом до отправки, to не давать клиенту математически противоречивую картину расходов.

**18. «Сколько X» при 1→N разворачивании:**
When пользователь спрашивает «сколько X» когда пайплайн делает 1→N разворачивание → найти код трансформации и считать на выходной стороне, to дать метрику совпадающую с тем что пользователь видит.

**19. «Вчера/сегодня запускалось» — ориентируйся по датам:**
When пользователь говорит «вчера/сегодня запускалось» в контексте диагностики → сначала SELECT DISTINCT run_date ORDER BY DESC LIMIT 5 для ориентации, to не запрашивать данные за ошибочную дату.

**20. Код закоммичен — деплой сразу:**
When server-side код исправлен и закоммичен → задеплоить сразу как последний шаг сессии, to не допустить запуск продакшна со старым кодом.

**21. Расхождение с внешним биллингом — отложенное наблюдение:**
When расхождение между нашим измерением и внешним биллингом → проверить гипотезу отложенным наблюдением до реализации фикса, to не реализовывать фикс на непроверенной гипотезе.

**22. Бэклог с числовым примером — проверь через первопринципы:**
When бэклог содержит числовой пример противоречащий бизнес-логике фичи → проверить пример через первопринципы до кодинга, to не реализовывать неверный алгоритм по ошибочной спеке.

**23. Deploy script — два SSH-вызова вместо одного:**
When deploy.sh объединяет pkill + systemctl restart в один длинный SSH-вызов → разбить на два вызова: upload/config и restart/verify, to убедиться что сервис перезапущен даже если SSH рвётся.

**24. Параллельные исполнители — явные границы:**
When параллельные исполнители получают описание без явных границ вывода → добавить explicit boundary: что НЕ делать, to не обесценить работу другого исполнителя scope drift'ом.

**25. Audit/review задача — Claude напрямую:**
When задача типа audit/review (read-only, без кодогенерации) → выполнять Claude напрямую, не делегировать Codex, to избежать повторных крашей сессии из-за mismatch executor/task-type.

**26. Ownership verification — не перезапрашивать:**
When верификация ownership через одноразовый токен, система не подтверждает → после отправки proof не перезапрашивать проверку через UI — ждать автопроверки системы, to не инвалидировать свой proof повторным запросом, который генерирует новый challenge.

**27. Сборка падает с сетевой ошибкой — подтверди код:**
When сборка падает с сетевой/инфраструктурной ошибкой (timeout, ECONNRESET, DNS) → подтвердить корректность кода через tsc + тесты, пометить как заблокировано окружением, to не тратить время на debug кода при инфраструктурном сбое.

**28. Деплой — верифицируй маппинг ветки:**
When объявление деплоя завершённым на целевой платформе → верифицировать маппинг ветки на environment (preview vs production) ДО пуша, to не тратить время пользователя ложными отчётами о деплое.

**29. Мерж в production — полный diff:**
When мерж ветки разработки с накопленными коммитами в production-ветку → проверить полный diff против HEAD production, не только свои коммиты, to не задеплоить непроверенные изменения из предыдущих сессий.

**30. Symlink-deploy с процесс-менеджером — пересоздать процесс:**
When деплой через symlink-releases с процесс-менеджером, кэширующим cwd → удалять и пересоздавать процесс при каждом деплое вместо reload, to не запускать процесс из директории старого релиза после смены symlink.

**31. Release-артефакт — копируй конфиги явно:**
When подготовка release-артефакта из framework-сборки (standalone, Docker build) → явно копировать конфиги процесс-менеджера/рантайма в release, не полагаться на трейсинг фреймворка, to не получить crash при деплое из-за отсутствия конфигов вне dependency tree.

**32. Очевидность из категории — перепроверь данные:**
When решение кажется очевидным из категории/типа объекта → проверить имеющиеся данные о конкретном случае ДО действия — очевидность = сигнал перепроверить, to не подменить факт конкретного случая свойством по умолчанию его категории (category default bias).

**33. Структурное изменение — проверь downstream:**
When структурное изменение общего ресурса (миграция, переименование) завершено → перечислить все downstream-операции и протестировать в новой структуре, to не оставить downstream invariant blindspot.

**34. Несколько гипотез — evidence first:**
When симптом имеет несколько правдоподобных объяснений → прочитать observable evidence ДО объявления диагноза, to не попасть в hypothesis anchoring bias.

**35. Стейкхолдер просит результат — интерпретируй буквально:**
When стейкхолдер просит увидеть результат при наличии плана с ≥2 оставшимися шагами → интерпретировать запрос буквально, не через призму следующего шага плана, to избежать pipeline momentum bias.

**36. Явная директива о режиме — переключай немедленно:**
When стейкхолдер даёт явную директиву о режиме работы ("не спрашивай", "делай молча") → переключить режим немедленно, не задавать ещё один уточняющий вопрос, to избежать directive deafness: продолжения прежнего режима после явного переключения.

**37. Регистрация нового компонента в разделяемом пространстве — перечисли занятые:**
When регистрация нового компонента в разделяемом пространстве ресурсов → перед выбором идентификатора перечислить уже занятые в целевом окружении, to избежать clean-slate assumption и конфликта имён.

**39. Расхождение документация/состояние — фиксируй сразу:**
When обнаружено расхождение между документацией и наблюдаемым состоянием → добавить disambiguation note в deliverable в момент обнаружения, до передачи ревьюерам, to не тратить validation round на факт уже известный автору.

**40. Batch артефакты/операции — верифицируй каждый до коммита:**
When multiple artifacts generated in batch (под давлением или массовой операцией над файлами) → run mental execution of each artifact, или verify через tool's check/dry-run mode, до declaring done/коммита, to избежать compound error debt от batch без верификации.

**41. Большой deliverable после многошаговой работы — предложи следующий шаг:**
When large deliverable produced after extended multi-step work → proactively offer the natural completion action without waiting for request, to избежать completion assumption bias: producing output feels like finishing, but delivery is a separate step.

**42. Расследование production во времени — durable источники первыми:**
When расследование «что произошло во время T» на production/long-running системе → сначала опросить durable audit источники (file mtime, append-only audit-таблицы, system event logs с retention-политикой) — потом уже grep по текстовым логам, to избежать log-first forensics bias: текстовые логи могут быть ротированы или усечены.

**43. Читай конфиг прежде чем спрашивать пользователя:**
When system investigation with a dedicated settings/control layer present → read authoritative config first, then interpret data through that lens, to avoid misidentifying configured state as a bug. Обобщение: when вот-вот спросить пользователя про дефолт/настройку инструмента который он использует локально → сначала проверить home-dir dotfiles, registry, env для этого инструмента; спрашивать только если конфиг не найден.

**44. Ранее «решённая» проблема снова в продакшне — проверь деплой:**
When previously "resolved" issue recurs in production → verify fix was actually persisted in deployment artifacts (env, config files, infra state), to избежать fix documentation conflated with fix deployment.

**45. Редактирование документа с возможными копиями — найди канонический:**
When editing a document that may have multiple copies across repo locations (root + nested, overlays, forks) → enumerate all copies via file-name survey, compare mtime/content to identify the canonical one, edit only canonical, to avoid first-found copy bias: treating the first opened copy as source-of-truth without verifying.

**46. Тяжёлый процесс на лёгкий артефакт — проверь соответствие:**
When a heavyweight multi-phase process is invoked on a lightweight deliverable (content-first, small glue code, one-shot) → inspect target artefact first, check whether process's core units (tasks/waves/reviewers) fit the work's shape, propose lightweight mode before Phase 0 output, to avoid blindly following process pipeline because it was invoked, without checking that its abstractions are meaningful for this work.

**47. Преамбула обещает ресурсы — верифицируй демонстрацию:**
When the preface of a multi-section deliverable declares a resource/convention as part of the approach → before declaring done, walk every preface declaration and verify at least one concrete later section actually exercises it, to avoid declaration-demonstration gap: shipping a deliverable that promises resources/conventions it never demonstrates.

**48. Делегирование падает с permission error — пробей все слои:**
When delegation fails with a permission/access error → enumerate ALL permission layers (config trust, OS ACL, sandbox identity) and probe adjacent paths in the same hierarchy to identify the actual failing layer, to avoid single-layer trust assumption: fixing the first found layer and hitting the same failure from a second.

**49. Неожиданное изменение состояния — сначала спроси человека:**
When state in a shared system turns out to be unexpectedly changed (flag reset, config zeroed, data gone) → first ask the operator directly "did you touch this manually?" — before investigating automated mutation paths, to avoid human-as-last-resort bias: hunting a phantom code-mutator while ignoring out-of-band human intervention.

**50. Глобальное правило маршрутизации в середине пайплайна — классифицируй по слою:**
When a user announces a global routing rule ("всё X → Y") mid-pipeline whose current phase produces methodology artifacts and later phases produce domain code → classify each upcoming output by layer (planning artifact vs execution output) and apply rule only to matching layer, to avoid artifact-as-code conflation: treating user's "всё/every" as workflow-spanning when it actually scopes to the next phase boundary.

**51. Запуск >3 параллельных субагентов — оцени стоимость:**
When about to spawn >3 parallel subagents for any purpose (research, validation, fix, review, generation) → before spawn estimate fanout cost (agents × expected context each) vs remaining session budget; if wave would consume a large share or a prior wave already did, halt and surface options (one sequential agent / smaller batch / narrower scope / stop), to avoid silent-scaling bias: treating "parallelism available" as permission to use maximum fanout without checking session budget.

**52. Задача зависит от компонента из предыдущей волны — читай живой код:**
When implementing a task that depends on a component written in a prior wave → read actual source code interface before using the spec description, to avoid spec-text as ground truth: trusting task document over live implementation.

**53. Планирование межагентного взаимодействия — верифицируй инструменты заранее:**
When designing a session workflow that plans multi-agent review rounds using inter-agent tooling → verify tooling availability (e.g. SendMessage between subagents) at session start before committing the review plan, to avoid environment availability assumed: planning as if listed tools will be usable at runtime.

**54. Автономный исполнитель без явного окончания — добавь терминатор:**
When an autonomous worker receives a step-by-step completion protocol without explicit scope termination → close the protocol with explicit termination: "only these N steps, no additional actions", to avoid permissive gap assumption: executor treats gap between not-listed and not-prohibited as permission.

**56. Применение фикса к «известному сломанному» состоянию — перечитай текущее состояние:**
When about to apply a repair targeting a known broken pattern → read actual current state and confirm it still matches the expected broken pattern before mutating, to avoid double-damage when state has already partially recovered or been changed out-of-band since the diagnosis.

**57. Источник синхронизации vs downstream — мутируй только источник:**
When two stores hold the same value and one syncs into the other (deploy script, replication, build pipeline) → mutate only the source-of-sync; direct edits to the downstream are silently overwritten on the next sync, to avoid resync-trap: change appears to take effect, then disappears on next sync cycle.

**58. Верификационный цикл по случаям через долгоживущий рантайм — свежий инстанс на случай:**
When a verification loop iterates multiple cases through a long-lived runtime instance whose state the act-under-test mutates → default to one fresh runtime instance per case; reuse only when each case is purely additive read-only, to avoid cross-case state leakage: earlier case's mutations contaminate later case's observed result.
