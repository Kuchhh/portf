# «Новосёл»: промпты для ChatGPT (листы персонажей, предметов, локаций и раскадровка)

Ролик застройщика «Развитие» для ЖК **Суворов-Сити 2**. YouTube, 16:9, 20 секунд. Файл подготовлен 03.10.2026 в облачной сессии Claude Code. Это **набор инструкций для Claude в десктоп-приложении**: он генерирует картинки в ChatGPT через браузер дизайнера.

---

## 0. Для Claude: что делать с этим файлом

Ты работаешь ассистентом дизайнера. Задача — сгенерировать в ChatGPT (генерация картинок):
1. листы персонажей;
2. листы предметов;
3. фоны локаций;
4. раскадровку.

Всё это потом станет референсами для видео в Seedance 2.0 (сервис «Виви»). Работай в браузере дизайнера через расширение Claude in Chrome.

### Правила дизайнера (обязательные)

1. **Одна генерация — один новый чат.** Исправления тоже делаются новой генерацией с нуля в новом чате. Никаких «исправь на картинке», edit-промптов и дорисовок, если дизайнер сам не попросил.
2. **Промпт вставляй дословно**: весь текст внутри блока ```` ```text ````. Меняй только то, что попросил дизайнер.
3. Папку `Новогодние баннеры 2027\Отобранные\` ведёт сам дизайнер. **Туда ничего не сохранять.**
4. Субагентов не запускать, пока дизайнер не попросит.
5. **Детей и подростков генерируем только по словам.** Фото реальных детей не прикладывать. Листы детей, которые мы сами сгенерируем, в раскадровку тоже не прикладываем: дети в раскадровке описаны словами.
6. Прошлые генерации из папок «Рендеры» в рефы не идут. **Исключение — баннер с козой** (см. раздел 1): дизайнер сам назвал его отправной точкой.
7. Чужие референсы — только образец приёма. Образцы сеток, которые прислал дизайнер (мокрая девушка, фиолетовая папка, робот Яндекса), **в ChatGPT не прикладывать**: раскладка описана в промптах словами.
8. **Лайм — единственный яркий цвет**, и только на шарфе козы, её пряже и стрелках кнопки лифта. Люди одеты в спокойные синие, серые, белые и бежевые тона. На предметах нет логотипов и надписей.
9. Лица освещены спереди, без контрового света. Эмоции сдержанные и разные.
10. Без катка. Ёлка во дворе есть.

### Порядок работы

**Шаг 0. Один раз перед стартом:**
- найди на компьютере файлы из раздела 1 и выпиши соответствие «код → путь»;
- покажи это дизайнеру одним сообщением и спроси, куда сохранять результаты (предложи `Ролики 2027\01 Новосёл\Листы\`);
- если какой-то файл не нашёлся, спроси о нём в этом же сообщении. Другой файл вместо него не подставляй.

**Шаг 1. Коза.**
- Сделай **N-K01 три раза в трёх новых чатах**: два раза с баннером-рефом, один раз без рефов.
- Покажи дизайнеру и дождись выбора.
- Дальше везде, где в рефах стоит «лист козы», прикладывай выбранный вариант.

**Шаг 2. Основа ролика (приоритет А).**
- Сделай всё с пометкой **А**: N-K01B, люди, предметы, локации. Каждый промпт по одному разу.
- Покажи все листы одной сводкой и дождись утверждения.

**Шаг 3. Запасные реакции (приоритет Б).**
- Сделай всё с пометкой **Б**.
- Если ChatGPT упёрся в лимит генераций, остановись и сообщи, что готово, а что нет.

**Шаг 4. Раскадровка.**
- Делай её только из **утверждённых** листов: сначала N-SB1…SB4, потом N-SB5…SB6.

### Как делать одну генерацию

1. ChatGPT → **новый чат**.
2. Приложи файлы из строки «Рефы» **строго в указанном порядке**: в промпте они названы *image 1, image 2…*. Если написано «без рефов», ничего не прикладывай.
3. Вставь текст промпта целиком и отправь.
4. Если ChatGPT задаёт уточняющий вопрос, ответь: `Generate it exactly as described, no questions.`
5. Если ChatGPT не умеет 16:9, соглашайся на самый широкий горизонтальный формат.
6. Скачай картинку в полном размере и сохрани под именем из строки «Файл». Если делаешь повтор, увеличь номер: `_v2`, `_v3`.
7. Проверь по чек-листу ниже.
   - Если провален пункт с ❗, сделай **одну** повторную генерацию в новом чате.
   - Если снова не вышло, отметь это в отчёте и больше не повторяй.

### Чек-лист листа

- раскладка как в промпте: у персонажа портрет слева + анфас + спина; у предмета 4 ячейки;
- фон ровный серый;
- ❗ нет текста, подписей, логотипов и водяных знаков;
- ❗ лайм только там, где он указан;
- одежда, причёска, пропорции и детали совпадают во всех ракурсах;
- лицо освещено спереди.

### Отчёт дизайнеру после каждого шага

Таблица: код — файл — что получилось — что не так. Без оценок «отлично», только факты.

---

## 1. Референсы (файлы на компьютере дизайнера)

| Код | Что это | Как узнать файл |
|---|---|---|
| **REF-GOAT** | Баннер с козой (отправная точка образа) | Баннер «Авиапарк в Шилово»: белая коза в золотых очках и лаймовом вязаном шарфе, во рту веточка ели, слева «КВАРТИРЫ от 2.6 млн». **Берём только козу:** без текста, без домов и без веточки |
| **REF-SS2-A** | Суворов-Сити 2, вечер | Вид с луга на закате: светло-серый кирпич, графитовые верхние этажи, терракотовые корпуса, тёплые окна, фонари |
| **REF-SS2-B** | Суворов-Сити 2, день | Вид с дороги: высокая башня из светлого кирпича с графитовым верхом, терракотовые корпуса, машины, деревья |
| **REF-SS2-C** | Суворов-Сити 2, двор | Двор сверху: оранжевое покрытие площадки, деревянные башни-цилиндры из реек, металлическая горка, плитка, парковка |
| **REF-SS2-D** | Суворов-Сити 2, квартал | Вид с высоты на весь квартал среди деревьев |

---

## 2. О ролике (контекст для генераций)

- **Герой** — прямоходящая белая коза, символ 2027 года, в золотых очках-авиаторах и лаймовом вязаном шарфе. Она несёт коробку с вещами и переезжает в ЖК.
- Зритель видит только её глаза, хвост, копыта, коробку и спину, а реакции соседей — сдержанные и разные. **Целиком козу видно только в финале, в лифте.**
- **Картинка:**
  - солнечный морозный день, низкое тёплое солнце, синие тени на снегу;
  - глубокие чёрные тени, лёгкое плёночное зерно;
  - спокойная палитра, лайм — только на козе и на кнопке лифта.
- **Пэкшот:** коза и парень в открытом лифте в **правой половине** кадра. Левая половина пустая, под титры.

---

## 3. Персонажи

Формат персонажа (как в присланной сетке): слева большой портрет по плечи, справа два роста — анфас и со спины. Фон ровный серый.

### N-K01 · Коза — главный герой · А · 3 генерации

- **Рефы:** генерации 1 и 2 — `REF-GOAT`; генерация 3 — без рефов (удали первую строку промпта).
- **Файл:** `N-K01_koza_v1.png`, `_v2`, `_v3`

```text
Image 1 is a reference only for the goat's face, fur, horns, sunglasses and scarf; ignore the text, the buildings and the spruce twig in her mouth.

Character: a photorealistic anthropomorphic white she-goat who walks upright on her hind legs like a person, about 160 cm tall to the top of her head. Long, silky, slightly wavy pure-white fur, longest on the shoulders, chest and legs, creamy at the tips; a long white goatee; long drooping ears with pink insides; large ridged horns, warm tan-beige with darker ridges, sweeping up and back from the forehead and curling outward at the tips; amber eyes with horizontal goat pupils; a soft pinkish-grey nose. Her front legs work like arms and end in glossy dark-grey cloven hooves; her hind legs end in dark cloven hooves; a short white tail. She wears gold thin-wire aviator sunglasses with dark smoky-green lenses, perched low on her muzzle so her amber eyes look over the top of the lenses, and a chunky hand-knitted scarf in vivid lime green, thick garter stitch, wrapped twice around her neck: one end hangs down her chest, the other is thrown over her left shoulder and hangs down her back; both ends have a short fringe. Nothing else on her. Expression: calm, content, self-assured, a touch of mischief, mouth closed.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same goat stands upright full length twice at the same scale, with a little space above the horns and below the hooves — front view on the left, back view on the right, front legs relaxed at her sides. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the hooves. Photorealistic fur and materials, natural colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

**Проверить:**
- рога, шерсть и уши похожи на баннер;
- ❗ очки сидят низко, глаза видны поверх;
- ❗ шарф лаймовый: один конец спереди, второй за спиной;
- ❗ во рту ничего нет;
- ❗ на спине виден конец шарфа и хвост.

### N-K01B · Коза с коробкой · А

- **Рефы:** 1 — выбранный лист козы N-K01; 2 — лист коробки N-P01. Значит, делается после N-P01.
- **Файл:** `N-K01B_koza_s_korobkoy_v1.png`

```text
Image 1 is the character sheet of the goat — keep her look exactly. Image 2 is the moving box — keep it exactly.

The same upright white goat carries the packed cardboard moving box from image 2 in front of her chest, holding it from below with both front hooves; the top of the potted spruce and the framed photo stick out above the box, below her chin.

Character pose sheet for a TV commercial, 16:9 landscape: three full-length views of the goat holding the box, side by side at the same scale, separated by thin black vertical lines — front view on the left, right-side profile view in the middle, back view on the right (from behind we see the edges of the box on both sides of her body, the fringed end of the lime scarf down her back and her short tail). Seamless neutral mid-grey studio backdrop, soft even frontal light, soft contact shadows. Photorealistic. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

**Проверить:** ❗ коза и коробка совпадают с листами; со спины видны края коробки.

### N-K02 · Мужчина со щёткой (кадр 4) · А

- **Рефы:** без рефов.
- **Файл:** `N-K02_muzhchina_shchetka_v1.png`

```text
Character: a Russian man of about 35, average build, a short neat dark-brown beard, grey-blue eyes, an ordinary calm face. A dark-navy winter parka with the hood down and a dark faux-fur trim on the hood, a grey knitted beanie, dark jeans, black lace-up winter boots, black gloves. In his right hand a car snow brush with a black handle and dark-grey bristles. Expression: calm, a little sleepy, an ordinary weekend morning.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same man stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing straight, arms relaxed. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### N-K03 · Мальчик ~6 лет (кадр 6) · А

- **Рефы:** без рефов (ребёнок — только по словам).
- **Файл:** `N-K03_malchik_v1.png`

```text
Character: a boy of about six with round rosy cheeks, a wide gap-toothed grin and a light-brown fringe peeking out from under a dark-blue knitted hat with a pompom. An off-white one-piece winter snowsuit, dark-blue mittens on a string, light-grey snow boots. Expression: delighted, bursting to tell something.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same boy stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing straight, arms relaxed. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### N-K04 · Мама ~30 (кадр 6) · А

- **Рефы:** без рефов.
- **Файл:** `N-K04_mama_v1.png`

```text
Character: a Russian woman of about 30 with a soft, friendly face and straight light-brown shoulder-length hair under a white knitted hat. A long light-blue down coat, a light-grey knitted scarf, dark-grey jeans, white winter boots, light-grey knitted gloves. Expression: calm, a hint of a smile.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same woman stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing straight, arms relaxed. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### N-K05 · Дворник (кадр 8) · А

- **Рефы:** без рефов.
- **Файл:** `N-K05_dvornik_v1.png`

```text
Character: a stocky Russian yard keeper of about 55 with a weathered face and a grey moustache. A black knitted hat, a dark-navy insulated work jacket and matching work trousers with silver-grey reflective stripes on the chest, sleeves and legs, black work gloves, heavy black boots. Expression: a stone face — unflappable, nothing in the world surprises him.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same man stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing straight, arms relaxed. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

**Проверить:** ❗ светоотражающие полосы серебристые, не лаймовые и не жёлтые.

### N-K06 · Мужчина ~50 из пары у подъезда (кадр 9) · А

- **Рефы:** без рефов.
- **Файл:** `N-K06_para_muzhchina_v1.png`

```text
Character: a Russian man of about 52 with a short salt-and-pepper beard and rimless glasses. A charcoal wool overcoat, a navy knitted scarf, a dark-grey flat cap, dark trousers, brown leather winter boots, dark leather gloves. Expression: polite, composed, a gentleman.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same man stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing straight, arms relaxed. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### N-K07 · Женщина ~50 из пары у подъезда (кадр 9) · А

- **Рефы:** без рефов.
- **Файл:** `N-K07_para_zhenshchina_v1.png`

```text
Character: a Russian woman of about 50 with short ash-blonde hair and small pearl earrings. A long camel wool coat, a cream knitted beret, a soft taupe scarf, black leather gloves, dark heeled winter boots. Expression: composed, quietly curious.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same woman stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing straight, arms relaxed. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### N-K08 · Парень ~25 с мандаринами (кадры 12–13) · А

- **Рефы:** без рефов.
- **Файл:** `N-K08_paren_mandariny_v1.png`

```text
Character: a slim Russian man of about 25 with short dark hair, light stubble and a slightly nervous, friendly face. A medium-blue puffer jacket, a grey hoodie underneath with the hood out over the collar, black joggers, grey winter sneakers. In his left hand a white cotton string shopping bag full of tangerines. Expression: awkward politeness, a careful half-smile.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same man stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing straight, arms relaxed. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### Запасные реакции (приоритет Б)

#### N-K09 · Мужчина с ёлкой на плече (реакция 1) · Б

- **Рефы:** без рефов. **Файл:** `N-K09_muzhchina_yolka_v1.png`

```text
Character: a Russian man of about 45 with ruddy cheeks and a short greying beard. A dark-brown jacket with a shearling collar, a grey knitted hat, dark jeans, brown winter boots. A freshly cut spruce about 180 cm tall, wrapped in white netting, rests on his right shoulder. Expression: kind, a slow one-sided smile.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same man stands full length twice at the same scale, with a little space above the head and the top of the tree and below the feet — front view on the left, back view on the right. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

#### N-K10 · Бабушка с термосом (реакция 2) · Б

- **Рефы:** без рефов. **Файл:** `N-K10_babushka_termos_v1.png`

```text
Character: a small Russian woman of about 75 with a kind round face, deep wrinkles and glasses. A light-grey knitted shawl tied over a dark fur hat, a long dark-grey down coat, grey felt boots. With both hands she holds the steaming steel cup-lid of a thermos. Expression: warm, unhurried, a soft smile.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same woman stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

#### N-K11 · Хозяйка собаки (реакция 3) · Б

- **Рефы:** без рефов. **Файл:** `N-K11_khozyayka_sobaki_v1.png`

```text
Character: a Russian woman of about 40 with a dark bob haircut. A long graphite wool coat, a light-grey knitted snood, black gloves, dark jeans, black winter boots; in her right hand a dark-navy dog leash. Expression: one eyebrow slightly raised — sceptical amusement.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same woman stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing straight. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

#### N-K12 · Бигль (реакция 3) · Б

- **Рефы:** без рефов. **Файл:** `N-K12_bigl_v1.png`

```text
Character: a young beagle with a classic tricolour coat — white legs, chest and muzzle, tan head and ears, a black saddle on the back — long soft ears, warm brown eyes, wearing a dark-navy harness.

Animal reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head portrait facing the camera, the head tilted to one side in curiosity; a thin black vertical line separates it from the right part, where the same dog is shown full body twice at the same scale — sitting, front view on the left; standing, left side profile on the right. Seamless neutral mid-grey studio backdrop, soft even frontal light, soft contact shadows. Photorealistic fur, natural colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

#### N-K13 · Подросток на качелях (реакция 4) · Б

- **Рефы:** без рефов (подросток — только по словам). **Файл:** `N-K13_podrostok_v1.png`

```text
Character: a lanky boy of about fifteen with a deadpan expression and messy dark hair under a black beanie. A graphite puffer jacket, black joggers, grey winter sneakers, white wireless earbuds in both ears.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same boy stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, hands in pockets. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

#### N-K14 · Женщина на балконе с гирляндой (реакция 5) · Б

- **Рефы:** без рефов. **Файл:** `N-K14_zhenshchina_balkon_v1.png`

```text
Character: a Russian woman of about 35 with hair in a messy bun and a few loose strands. A chunky cream knitted sweater, grey lounge trousers, grey felt house boots. In her hands a string of old-fashioned round warm-white bulbs on a dark cable. Expression: caught mid-task, attentive.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same woman stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

#### N-K15 · Девочка у снеговика (реакция 6) · Б

- **Рефы:** без рефов (ребёнок — только по словам). **Файл:** `N-K15_devochka_snegovik_v1.png`

```text
Character: a girl of about six with rosy cheeks and wide curious eyes. A dark-blue one-piece snowsuit, a white knitted hat with ear flaps tied under the chin, white mittens, dark-blue snow boots. Expression: open-mouthed wonder.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same girl stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, arms relaxed. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

#### N-K16 · Мальчик у снеговика (реакция 6) · Б

- **Рефы:** без рефов (ребёнок — только по словам). **Файл:** `N-K16_malchik_snegovik_v1.png`

```text
Character: a boy of about seven with a freckled nose and a serious, absorbed face. A grey one-piece snowsuit, a light-blue knitted hat, grey mittens, black snow boots; in his right mitten a carrot.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same boy stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

#### N-K17 · Мальчик с санками (реакция 7) · Б

- **Рефы:** без рефов (ребёнок — только по словам). **Файл:** `N-K17_malchik_sanki_v1.png`

```text
Character: a boy of about seven with big round eyes and pink cheeks. A navy one-piece snowsuit with light-grey knee patches, a grey knitted hat with a pompom, a light-blue knitted scarf, navy mittens, black snow boots; in his right mitten the end of a sled rope. Expression: frozen in mid-step, staring.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same boy stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

---

## 4. Предметы

Формат предмета (как в присланной сетке): 4 ячейки 2×2 на сером фоне — спереди, сзади, сбоку, три четверти. Там, где ракурсы другие, это сказано в промпте.

### N-P01 · Коробка с вещами (кадры 7, 9, 12, 13) · А

- **Рефы:** без рефов. Делай после N-P02…P05, если хочешь сверить вещи; прикладывать их не нужно.
- **Файл:** `N-P01_korobka_v1.png`

```text
Object: a medium corrugated cardboard moving box, kraft brown, about 50 × 35 × 35 cm, open top with the four flaps folded outward, a strip of plain beige packing tape along the bottom seam, slightly dented corners, a cut-out hand hole on each side. Packed inside and sticking out of the top: at the back, an upright framed photo in a light-oak frame, the picture side facing forward; a small live spruce about 35 cm tall in an unglazed terracotta pot; a white enamel mug with a dark-blue rim; at the front, a big ball of chunky lime-green wool yarn with two long wooden knitting needles stuck through it.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same packed box on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view; top-right — back view; bottom-left — side view; bottom-right — three-quarter view from above, showing the contents. True-to-life materials and colours. Clean image: no text, no letters, no labels, no logos, no markings on the cardboard, no watermarks.
```

**Проверить:** ❗ на картоне нет надписей и значков; лайм только на пряже.

### N-P02 · Фото семьи коз в рамке (кадр 7) · А

- **Рефы:** 1 — выбранный лист козы N-K01.
- **Файл:** `N-P02_foto_semi_koz_v1.png`

```text
Image 1 shows our goat character — the young goat in the photo is her as a child.

Object: an old-fashioned colour family photo print, slightly faded, in a simple light-oak frame with glass, about 20 × 25 cm, with a cardboard back and a fold-out stand. The photo shows a family of white goats standing upright like people at the edge of a snowy spruce forest, posing solemnly for a family portrait: a bearded grandfather goat with big curled horns, a grandmother goat with a grey knitted shawl over her shoulders, and between them a young white goat with small horns wearing a lime-green knitted scarf. Warm, nostalgic colours, a slight vignette.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same framed photo on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view, standing on its stand; top-right — back view with the cardboard back and the stand; bottom-left — side view; bottom-right — three-quarter view. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### N-P03 · Ёлочка в горшке (кадр 7) · А

- **Рефы:** без рефов. **Файл:** `N-P03_yolochka_v1.png`

```text
Object: a small live spruce about 35 cm tall with dense dark-green needles, in a simple unglazed terracotta pot with a matching saucer, a little dark soil visible.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same potted spruce on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view; top-right — back view; bottom-left — side view; bottom-right — three-quarter view from slightly above. True-to-life materials and colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### N-P04 · Эмалированная кружка (кадр 7) · А

- **Рефы:** без рефов. **Файл:** `N-P04_kruzhka_v1.png`

```text
Object: a classic white enamel mug, about 9 cm tall, with a dark-blue rim and a dark-blue edge on the handle; a small chip on the rim shows black metal; lightly worn, clearly loved.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same mug on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view, handle on the right; top-right — back view, handle on the left; bottom-left — side view with the handle facing the camera; bottom-right — three-quarter view from slightly above, showing the inside. True-to-life materials and colours. Clean image: no text, no letters, no labels, no logos, no pictures on the mug, no watermarks.
```

### N-P05 · Клубок лаймовой пряжи со спицами (кадр 7) · А

- **Рефы:** без рефов. **Файл:** `N-P05_klubok_v1.png`

```text
Object: a big ball of chunky wool yarn in vivid lime green, about 15 cm across, with two long wooden knitting needles stuck through it crosswise; from one needle hangs a short knitted strip of a few rows in the same lime yarn, in thick garter stitch.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same yarn ball on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view; top-right — back view; bottom-left — side view; bottom-right — three-quarter view from slightly above. True-to-life wool texture and colour. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### N-P06 · Очки-авиаторы козы · А

- **Рефы:** `REF-GOAT` (только очки). **Файл:** `N-P06_ochki_v1.png`

```text
Image 1 is a reference only for the sunglasses the goat wears; ignore everything else.

Object: gold thin-wire aviator sunglasses with dark smoky-green teardrop lenses, a double bridge, slim temples with dark tips, slightly oversized.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same sunglasses on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view, temples open; top-right — back view, temples open; bottom-left — side view; bottom-right — three-quarter view, temples folded. True-to-life metal and lenses. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### N-P07 · Лаймовый шарф козы · А

- **Рефы:** `REF-GOAT` (только шарф). **Файл:** `N-P07_sharf_v1.png`

```text
Image 1 is a reference only for the knitted scarf the goat wears; ignore everything else.

Object: a chunky hand-knitted scarf in vivid lime green, thick garter stitch, about 200 × 25 cm, with a short fringe on both ends.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid), every cell on a seamless neutral mid-grey studio backdrop with soft even studio light: top-left — the whole scarf laid flat at full length, seen from above; top-right — close-up of the knit texture and the fringe; bottom-left — the scarf neatly folded; bottom-right — the scarf on a plain grey display neck form, wrapped twice around the neck, one end hanging down the front, the other thrown over the left shoulder. True-to-life wool texture and colour. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### N-P08 · Щётка для снега (кадр 4) · А

- **Рефы:** без рефов. **Файл:** `N-P08_shchetka_v1.png`

```text
Object: a car snow brush with an ice scraper, about 60 cm long: a black plastic handle with a dark-grey foam grip, dense dark-grey bristles at one end, a black scraper blade at the other, a few flakes of snow caught in the bristles.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same brush on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view; top-right — back view; bottom-left — side view; bottom-right — three-quarter view. True-to-life materials. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### N-P09 · Машина мужчины (кадр 4) · А

- **Рефы:** без рефов. **Файл:** `N-P09_mashina_v1.png`

```text
Object: a compact crossover SUV in dark graphite-blue metallic, a generic modern design with no badges or emblems anywhere, black wheels, plain licence plates without any characters. A layer of fresh snow lies on the roof and bonnet, half brushed off on the driver's side.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same car on a seamless neutral mid-grey studio floor, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view; top-right — rear view; bottom-left — left side view; bottom-right — three-quarter front view. True-to-life materials. Clean image: no text, no letters, no numbers, no labels, no logos, no watermarks.
```

**Проверить:** ❗ ни эмблем, ни букв на номерах.

### N-P10 · Лопата-движок дворника (кадр 8) · А

- **Рефы:** без рефов. **Файл:** `N-P10_lopata_v1.png`

```text
Object: a wide snow pusher shovel of the kind Russian yard keepers use: a dark-grey plastic blade about 75 cm wide with a galvanised metal strip along the bottom edge, a long wooden handle ending in a U-shaped metal crossbar grip with a black rubber cover; worn and scratched from use.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same shovel on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view of the blade; top-right — back view; bottom-left — side view; bottom-right — three-quarter view. True-to-life materials. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### N-P11 · Панель вызова лифта со стрелками (кадр 11) · А

- **Рефы:** без рефов. **Файл:** `N-P11_panel_lifta_v1.png`

```text
Object: a slim vertical elevator call panel in brushed graphite metal, about 12 × 30 cm, set into a wall of warm light-grey stone. One round brushed-steel push button in the lower half; above it a small square indicator window with two stacked up-pointing chevrons.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same panel in the same piece of stone wall, soft even light: top-left — front view, indicator off, the chevrons dark; top-right — front view, indicator on: the two chevrons glow vivid lime green and a thin lime ring glows around the button; bottom-left — side view showing the slim panel profile; bottom-right — three-quarter view, indicator on. True-to-life metal and stone. Clean image: no text, no letters, no numbers, no labels, no logos, no watermarks.
```

**Проверить:** ❗ стрелки именно двойные шевроны вверх; лайм только в подсветке.

### N-P12 · Авоська с мандаринами (кадры 12–13) · А

- **Рефы:** без рефов. **Файл:** `N-P12_avoska_v1.png`

```text
Object: a classic Russian string shopping bag (avoska) knitted from off-white cotton cord, with two long handles, filled with about fifteen bright tangerines, a few still with green leaves.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same bag on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view, hanging by its handles; top-right — back view, hanging; bottom-left — side view, hanging; bottom-right — three-quarter view, standing on the floor. True-to-life materials. Clean image: no text, no letters, no labels, no stickers, no logos, no watermarks.
```

### Предметы запасных реакций (приоритет Б)

#### N-P13 · Ёлка в сетке (реакция 1) · Б

- **Рефы:** без рефов. **Файл:** `N-P13_yolka_v_setke_v1.png`

```text
Object: a freshly cut spruce about 180 cm tall, tightly wrapped in white plastic netting, the cut trunk end sticking out at the bottom, a few branches poking through the net.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same wrapped tree on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — standing upright, front view; top-right — standing upright, back view; bottom-left — lying on its side; bottom-right — three-quarter view, leaning. True-to-life materials. Clean image: no text, no letters, no labels, no tags, no logos, no watermarks.
```

#### N-P14 · Термос (реакция 2) · Б

- **Рефы:** без рефов. **Файл:** `N-P14_termos_v1.png`

```text
Object: a 1-litre stainless-steel thermos with a matte dark-blue body, a brushed-steel cup-lid and a stopper.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same thermos on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred at the same scale: top-left — front view, closed; top-right — back view, closed; bottom-left — side view, closed; bottom-right — three-quarter view with the cup-lid off, standing beside the thermos, filled with steaming tea. True-to-life materials. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

#### N-P15 · Деревянные санки (реакция 7) · Б

- **Рефы:** без рефов. **Файл:** `N-P15_sanki_v1.png`

```text
Object: a classic Russian children's sled: a seat of light varnished wooden slats on bent steel runners painted dark blue, a folding push handle at the back, a thick natural rope tied to the front.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same sled on a seamless neutral mid-grey studio floor, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view; top-right — back view; bottom-left — side view; bottom-right — three-quarter view from above. True-to-life materials. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

#### N-P16 · Гирлянда (реакция 5) · Б

- **Рефы:** без рефов. **Файл:** `N-P16_girlyanda_v1.png`

```text
Object: a string of old-fashioned round warm-white light bulbs, about 5 m long, on a dark cable, the bulbs glowing softly.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid), every cell on a seamless neutral mid-grey studio backdrop with soft even light: top-left — the garland loosely coiled; top-right — the garland hanging in two soft swags; bottom-left — close-up of three bulbs on the cable; bottom-right — the garland held up in a loose loop, three-quarter view. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

#### N-P17 · Снеговик (реакция 6) · Б

- **Рефы:** без рефов. **Файл:** `N-P17_snegovik_v1.png`

```text
Object: a hand-made three-ball snowman about 120 cm tall, slightly lumpy snow, twig arms, coal eyes and a coal smile, a carrot nose stuck in crookedly at an angle.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same snowman on a seamless neutral mid-grey studio floor with a little snow around its base, soft even studio light, centred and fully visible at the same scale: top-left — front view; top-right — back view; bottom-left — side view showing the crooked nose; bottom-right — three-quarter view. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

---

## 5. Локации (пустые фоны, без людей)

Эти фоны станут референсом окружения для раскадровки и Seedance. **Дома точно как на рендерах, только зимой.**

### N-L01 · Опушка, вид на ЖК (кадр 1) · А

- **Рефы:** 1 — `REF-SS2-A`; 2 — `REF-SS2-B`. **Файл:** `N-L01_opushka_v1.png`

```text
Images 1 and 2 show the residential complex; keep its architecture exactly — light-grey brick, graphite top floors, terracotta-red blocks, black window frames — but turn the season to deep winter.

Photorealistic location plate for a TV commercial, 16:9 landscape, an empty scene. Point of view from inside the edge of a snowy spruce forest at a height of 1.5 m: heavy snow-laden spruce branches frame the shot on the left, the right and the top; through the opening, a wide sunlit snowy field, and on its far side the residential complex from images 1 and 2, roofs white with snow. Clear deep-blue sky, a low sun from behind on the left, long blue shadows, sparkling snow crystals, frosty air. Normal lens, about 47° horizontal field of view, level horizon. Deep true blacks in the shadows of the branches, warm sunlight, fine film grain. Clean image: no text, no letters, no logos, no people.
```

### N-L02 · Двор зимой (кадры 4–8, запасные реакции) · А

- **Рефы:** 1 — `REF-SS2-C`; 2 — `REF-SS2-A`. **Файл:** `N-L02_dvor_v1.png`

```text
Image 1 shows the courtyard and image 2 the facades of the residential complex; keep the architecture and the playground exactly, but turn the season to winter.

Photorealistic location plate for a TV commercial, 16:9 landscape, an empty scene with no people. Eye-level view across the courtyard on a sunny frosty day: the playground with its orange rubber surface showing in patches through thin snow, the cylindrical wooden-slat towers and the stainless steel slide with snow caps, a tall spruce in the yard decorated with warm-white lights, cleared paving paths with neat snowbanks, a few snow-covered parked cars along the edge, the facades behind — light-grey brick with the two lower floors in graphite, black window frames, normal-size windows. Low warm sun, blue shadows on the snow, deep true blacks, fine film grain, normal lens about 47° horizontal field of view, level horizon. Clean image: no text, no letters, no logos, no signs.
```

**Проверить:** ❗ ни катка, ни людей; окна обычные, не панорамные.

### N-L03 · Подъезд (кадр 9) · А

- **Рефы:** 1 — `REF-SS2-C`. **Файл:** `N-L03_podezd_v1.png`

```text
Image 1 shows the residential complex; keep its architecture — light-grey brick, graphite ground floors, black window frames — but in winter.

Photorealistic location plate for a TV commercial, 16:9 landscape, an empty scene with no people. A building entrance on the graphite ground floor, seen straight on from the path at shoulder height: a dark metal-framed glass door under a slim dark canopy, three wide grey stone steps brushed clean of snow, neat snowbanks on both sides, warm lobby light glowing through the glass; above, light-grey brick with black window frames. Sunny frosty day, sunlight from the side, blue shadows, deep true blacks, fine film grain, normal lens about 47° horizontal field of view. Clean image: no text, no letters, no numbers, no logos, no signs.
```

### N-L04 · Холл с лифтом (кадры 10–13, пэкшот) · А

- **Рефы:** без рефов. **Файл:** `N-L04_holl_v1.png`

```text
Photorealistic location plate for a TV commercial, 16:9 landscape, an empty scene with no people. A warm modern residential lobby seen strictly frontally and symmetrically at chest height: polished warm-grey stone floor; in the right half of the frame the elevator — brushed-steel doors set in a wall clad with warm oak panels, a slim brushed graphite call panel to the right of the doors; the left half of the frame is a calm, empty wall of warm light-grey stone, softly washed with light from above, with nothing on it. Warm recessed downlights, deep true blacks in the corners, fine film grain, normal lens about 47° horizontal field of view, level horizon. Clean image: no text, no letters, no numbers, no logos, no signs.
```

**Проверить:** ❗ левая половина кадра пустая и спокойная: это место под титры пэкшота.

### N-L05 · Кабина лифта (кадры 12–13) · А

- **Рефы:** без рефов. **Файл:** `N-L05_kabina_v1.png`

```text
Photorealistic location plate for a TV commercial, 16:9 landscape, an empty scene with no people. Strictly frontal, symmetric view at chest height into an open elevator cabin, the brushed-steel doors fully open: warm oak-veneer walls on three sides, a brushed-steel handrail at hip height along the back and side walls, a warm light panel in the ceiling, a dark polished stone floor. Warm light, deep true blacks at the edges, fine film grain, normal lens about 47° horizontal field of view. Clean image: no text, no letters, no numbers, no logos, no mirror.
```

---

## 6. Раскадровка

Только из утверждённых листов. Каждый лист раскадровки — 4 кадра 2×2. Пэкшот (N-SB4) — один большой кадр.

Общее для всех кадров:
- люди смотрят **левее камеры**: коза за кадром рядом с объективом;
- коза идёт **слева направо**;
- до кадра 12 козу целиком не показываем.

### N-SB1 · Кадры 1–4 · А

- **Рефы:**
  1. лист козы N-K01;
  2. N-L01 опушка;
  3. N-L02 двор;
  4. N-K02 мужчина;
  5. N-P09 машина.
- **Файл:** `N-SB1_kadry_01-04_v1.png`

```text
References: image 1 — the goat character (keep her fur, hooves and lime scarf exactly); image 2 — the forest edge with the view of the residential complex; image 3 — the courtyard; image 4 — the man; image 5 — his car.

Storyboard sheet for a 20-second TV commercial: four photorealistic film stills in a 2×2 grid, each still 16:9, separated by thin white gutters, with a small white panel number in the top-left corner of each still (1, 2, 3, 4) and no other text. Every still: cinematic, as if shot on a cinema camera with a normal lens, sunny frosty winter day, low warm sun, blue shadows on the snow, deep true blacks, fine film grain, calm natural colours; the only vivid colour is the lime green of the goat's scarf.

1 — Point of view of someone 1.5 m tall standing inside the forest edge from image 2: a goat's front leg with long white fur and a glossy dark cloven hoof reaches in from the lower right and pushes heavy snow-laden spruce branches apart; snow tumbles and sparkles in the sun; through the gap, the snowy field and the residential towers far away.

2 — A low shot from behind at knee height, framing only from the hooves to the waist of the upright white goat standing in deep forest snow: long white fur, a short white tail flicking snow off in a sparkling puff, the fringed lime end of her scarf hanging down her back. Sunlight from the side.

3 — Side view at hoof height, only the goat's legs from the knees down: two dark cloven hooves step out of deep forest snow onto the cleared grey paving of the courtyard path, walking from left to right past a low snowbank.

4 — The courtyard from image 3 at eye level. In the right foreground the man from image 4 brushes snow off the roof of the car from image 5; behind him the playground with the orange surface and wooden towers under snow, the decorated spruce and the light-grey brick facades. He glances to the left of the camera, the brush slowing in mid-stroke, eyebrows slightly raised — restrained puzzlement. Sunlight on his face from the front.
```

### N-SB2 · Кадры 5–8 · А

- **Рефы:**
  1. лист козы N-K01;
  2. N-P01 коробка;
  3. N-L02 двор;
  4. N-K04 мама;
  5. N-K05 дворник;
  6. N-P10 лопата.
- Мальчик описан словами, его лист не прикладываем.
- **Файл:** `N-SB2_kadry_05-08_v1.png`

```text
References: image 1 — the goat character; image 2 — her packed moving box; image 3 — the courtyard; image 4 — the mother; image 5 — the yard keeper; image 6 — his snow shovel.

Storyboard sheet for a 20-second TV commercial: four photorealistic film stills in a 2×2 grid, each still 16:9, separated by thin white gutters, with a small white panel number in the top-left corner of each still (5, 6, 7, 8) and no other text. Every still: cinematic, sunny frosty winter day, low warm sun, blue shadows on the snow, deep true blacks, fine film grain, calm natural colours; the only vivid colour is lime green, only on the goat's yarn.

5 — A ground-level insert with a long lens and shallow depth of field: the goat's dark cloven hooves with long white fur walk across the grey paving straight towards the camera; the nearest hoof is about to cover the lens; snow dust glows in the sun behind.

6 — At a child's eye height in the courtyard from image 3: a boy of about six — round rosy cheeks, a wide gap-toothed grin, an off-white snowsuit, a dark-blue knitted hat with a pompom, mittens on a string — tugs the sleeve of the mother from image 4 and points just to the left of the camera; the mother turns her head that way, eyebrows slightly raised, a half-smile, her hands still straightening his hat. Sunlight on their faces from the front.

7 — A close side view at box height: the edge of the moving box from image 2 is carried past from left to right; inside, the framed family photo, the small potted spruce, the white enamel mug and the ball of lime yarn with wooden needles sway with the step. Soft sunlight.

8 — Medium-wide, static: the yard keeper from image 5 keeps pushing the wide shovel from image 6 while looking to the left of the camera with a stone face; a heap of snow grows in front of the blade. Sunlight on his face from the front.
```

### N-SB3 · Кадры 9–12 · А

- **Рефы:**
  1. N-K01B коза с коробкой;
  2. N-L03 подъезд;
  3. N-K06 мужчина ~50;
  4. N-K07 женщина ~50;
  5. N-L04 холл;
  6. N-K08 парень.
- **Файл:** `N-SB3_kadry_09-12_v1.png`

```text
References: image 1 — the goat carrying her box (keep her look and the box exactly); image 2 — the building entrance; image 3 and image 4 — the couple; image 5 — the lobby with the elevator; image 6 — the young man.

Storyboard sheet for a 20-second TV commercial: four photorealistic film stills in a 2×2 grid, each still 16:9, separated by thin white gutters, with a small white panel number in the top-left corner of each still (9, 10, 11, 12) and no other text. Every still: cinematic, normal lens, deep true blacks, warm light, fine film grain, calm natural colours; the only vivid colour is lime green, only on the goat's scarf and on the elevator chevrons.

9 — From behind at shoulder height, about 1.2 m behind the upright goat from image 1, centred in frame: the back of her head with the tips of her horns, long white fur, the lime scarf end down her back, the top of the box she carries. Ahead, the entrance from image 2: the couple from images 3 and 4 have just come out, mid-conversation; they pause and glance at each other, and the man holds the door open with a small polite gesture. Warm light inside the doorway, sunlight from the side.

10 — A low side view from the knees down as the camera passes through the facade: the left third of the frame is a dark blurred band — the cut edge of the wall right at the lens; beyond it the warm lobby from image 5 with a polished stone floor, the goat's hooves clicking from left to right towards the elevator. Warm downlights, deep shadows.

11 — Macro: the slim graphite call panel in the warm stone wall; a glossy dark cloven hoof presses the round steel button; above it two stacked up-chevrons glow vivid lime green. Shallow depth of field.

12 — Strictly frontal and symmetric at chest height: the elevator doors have slid open; inside the warm oak-panelled cabin, on the right, stands the young man from image 6 holding a string bag of tangerines; the goat has stepped in and turned to face us — seen whole for the first time: gold aviator sunglasses low on her muzzle, the lime scarf, the box in her hooves, a content, self-assured look. The young man glances at her sideways with an awkward smile and a small nod. Warm cabin light on both faces from the front.
```

### N-SB4 · Кадр 13, пэкшот · А

- **Рефы:**
  1. N-K01B коза с коробкой;
  2. N-K08 парень;
  3. N-L04 холл;
  4. N-L05 кабина.
- **Файл:** `N-SB4_kadr_13_pekshot_v1.png`

```text
References: image 1 — the goat carrying her box; image 2 — the young man; image 3 — the lobby; image 4 — the elevator cabin. Keep all of them exactly.

A single photorealistic film still for the final shot of a TV commercial, 16:9 landscape. A wide, strictly frontal and symmetric view of the warm lobby from image 3 at chest height: the open elevator stands in the right half of the frame; inside it, full length and side by side, the white goat from image 1 — gold aviator sunglasses, lime knitted scarf, holding her moving box — and the young man from image 2 with his string bag of tangerines; both face the camera; the goat looks content and nudges her sunglasses up with one hoof, the young man shifts his weight with an awkward smile. The left half of the frame is a calm, empty, softly lit wall of warm light-grey stone with nothing on it. Warm even light, deep true blacks, fine film grain, normal lens about 47° horizontal field of view, level horizon; the only vivid colour is the lime of the scarf. Clean image: no text, no letters, no logos.
```

**Проверить:** ❗ лифт и герои в правой половине, левая половина пустая.

### N-SB5 · Запасные реакции 1–4 · Б

- **Рефы:**
  1. N-L02 двор;
  2. N-K09 мужчина с ёлкой;
  3. N-P13 ёлка в сетке;
  4. N-K10 бабушка;
  5. N-K11 хозяйка собаки;
  6. N-K12 бигль.
- Подросток описан словами.
- **Файл:** `N-SB5_reaktsii_1-4_v1.png`

```text
References: image 1 — the courtyard; image 2 — the man; image 3 — the net-wrapped spruce; image 4 — the grandmother; image 5 — the dog owner; image 6 — the beagle.

Storyboard sheet for a TV commercial: four photorealistic film stills in a 2×2 grid, each still 16:9, separated by thin white gutters, with a small white label in the top-left corner of each still (R1, R2, R3, R4) and no other text. Every still takes place in the courtyard from image 1 on a sunny frosty day: low warm sun, blue shadows on the snow, deep true blacks, fine film grain, calm natural colours, faces lit from the front. In every still the person looks at something just to the left of the camera that we never see.

R1 — By a parked car, the man from image 2 with the net-wrapped spruce from image 3 on his shoulder has stopped; the top of the tree still sways; he follows something with his eyes and slowly smiles with one corner of his mouth.

R2 — On a bench, the grandmother from image 4 holds the steaming cup-lid of a thermos; she stopped it halfway to her mouth and now slowly lowers it, smiling warmly.

R3 — At low height on a snowy path: the beagle from image 6 on its leash sits down and tilts its head to one side; the leash goes slack; above it, the owner from image 5 raises one eyebrow.

R4 — On the playground swing, a lanky boy of about fifteen with a deadpan face — graphite puffer jacket, black beanie, white wireless earbuds — keeps swinging, turns his head to follow something and pulls out one earbud.
```

### N-SB6 · Запасные реакции 5–7 · Б

- **Рефы:**
  1. N-L02 двор;
  2. N-K14 женщина на балконе;
  3. N-P16 гирлянда;
  4. N-P17 снеговик;
  5. N-P15 санки.
- Дети описаны словами.
- **Файл:** `N-SB6_reaktsii_5-7_v1.png`

```text
References: image 1 — the courtyard and its buildings; image 2 — the woman; image 3 — her garland; image 4 — the snowman; image 5 — the sled.

Storyboard sheet for a TV commercial, portrait orientation: three photorealistic film stills stacked vertically, each still 16:9, separated by thin white gutters, with a small white label in the top-left corner of each still (R5, R6, R7) and no other text. Every still: the residential complex from image 1 on a sunny frosty day, low warm sun, blue shadows on the snow, deep true blacks, fine film grain, calm natural colours, faces lit from the front. In every still the people look at something just to the left of the camera that we never see.

R5 — On a balcony of the light-grey brick building, seen at her eye level from the next balcony: the woman from image 2 froze in the middle of hanging the garland from image 3 along the railing; she looks down to the left of the camera; the bulbs keep glowing.

R6 — In the courtyard by the snowman from image 4: a girl of about six (dark-blue snowsuit, white knitted hat with ear flaps, rosy cheeks) and a boy of about seven (grey snowsuit, light-blue knitted hat) both stare to the left of the camera; without looking, the boy sticks the carrot nose into the snowman crooked.

R7 — On a courtyard path: a boy of about seven (navy snowsuit with light-grey knee patches, grey knitted hat with a pompom, light-blue scarf) pulling the sled from image 5 by its rope has stopped dead, staring; the sled rolls on and bumps into the back of his legs.
```

---

## 7. После раскадровки

Следующий этап — ключевые кадры (по одному на план) и промпты Seedance 2.0 для «Виви». Это делаем отдельно, после того как дизайнер утвердит раскадровку и выберет реакции.
