# Learned Patterns — Design Generate

> Loaded at Phase 2 start. Meta-rules from design sessions.

**1. Типографика — проверяй ДО генерации CSS:**
Верифицируй шрифты по референсу до написания стилей. When вычисление font-size для текста с фиксированной шириной контейнера → проверить коэффициент ширины символа для используемого шрифта и скрипта; ориентироваться на самое длинное слово, to предотвратить неожиданный перенос строки в рендере. When текст на busy/текстурном фоне с недостаточным контрастом → увеличить font-size на один шаг дизайн-сетки пока буква визуально перекрывает детали текстуры, to добиться контраста через размер без overlay. Layout constraint vs согласованный текст → адаптируй layout, не текст.

**2. Фото и позиционирование — анализируй субъект ДО размещения:**
Текст поверх фото → найди зону субъекта, размести текст на наименее загруженной стороне. Full-bleed фото → проверь ориентацию и crop feasibility против формы контейнера. Элемент на границе тёмного/светлого фона → solid opaque bg, не rgba.

**3. Цвет и визуальный вес — перебирай все варианты:**
При выборе цвета текста → перечисли ВСЕ опции (brand + white + dark grey), оцени каждую против фона. Несколько текстовых блоков → проверь visual weight (size × weight) на соответствие reading order.

**4. Структура — от данных к UI, не наоборот:**
Structured data → каждое поле = UI-элемент, не изобретать структуру. Alternative design → выбирай layout независимо от существующей разметки. Сложный UI (N×M) → один блок полностью → одобрение → масштабирование. Нет референсов → спроси 1-2 сайта + "что раздражает" ДО старта.

**5. Единый структурный контейнер при разнородных секциях:**
When deliverable has sections carrying different content types (quote, data grid, narrative, list) within one frame → pick ONE structural treatment for all sections; let content differences live as minimal inline variations (italic span, bold label), not as separate visual containers, to avoid variety-by-content-type bias that produces visual cacophony the user reads as "unbalanced".

**6. Типографика коммерческих форматов в редакторском контексте:**
When implementing a conventional format for a commercial category (pricing list, product spec, comparison) inside an editorial/personal-voice context → before reaching for the category's typography kit (strikethrough, discount arrows, % badges, SKU tables), check whether the voice actually wants those conventions; substitute neutral typographic variants when not, to avoid category-typography reflex that produces a commercially-toned artifact in an editorial context.
