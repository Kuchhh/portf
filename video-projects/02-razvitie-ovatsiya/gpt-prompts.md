# «Овация»: промпты для ChatGPT (листы персонажей, предметов, локаций и раскадровка)

Ролик застройщика «Развитие» для **арт-квартала «Зарядье»**. YouTube, 16:9, 20 секунд, финальная фраза **«Лучший застройщик года»**. Файл подготовлен 03.10.2026 в облачной сессии Claude Code. Это **набор инструкций для Claude в десктоп-приложении**: он генерирует картинки в ChatGPT через браузер дизайнера.

Сценарий и подробная раскадровка лежат в [`storyboard.md`](storyboard.md) рядом, но всё нужное для генераций есть и здесь.

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
6. Прошлые генерации из папок «Рендеры» в рефы не идут. Исключение — лист козы из «Новосёла» (N-K01): это наш персонаж кампании, он нужен только для пасхалки 9б.
7. Чужие референсы — только образец приёма. Образцы сеток, которые прислал дизайнер (мокрая девушка, фиолетовая папка, робот Яндекса), **в ChatGPT не прикладывать**: раскладка описана в промптах словами.
8. **Лайм — единственный яркий цвет**, и только на бабочке дедушки (и на шарфе козы в пасхалке). Люди одеты в спокойные синие, графитовые, серые, белые и бежевые тона. На предметах нет логотипов и надписей.
9. Лица освещены спереди, без контрового света. Эмоции сдержанные и разные.
10. Двор без машин. Спортплощадка под ровным снегом, катка нет.

### Порядок работы

**Шаг 0. Один раз перед стартом:**
- найди на компьютере файлы из раздела 1 и выпиши соответствие «код → путь»;
- покажи это дизайнеру одним сообщением и спроси, куда сохранять результаты (предложи `Ролики 2027\02 Овация\Листы\`);
- если какой-то файл не нашёлся, спроси о нём в этом же сообщении. Другой файл вместо него не подставляй.

**Шаг 1. Дедушка.**
- Сделай **O-K01 три раза в трёх новых чатах**.
- Покажи дизайнеру и дождись выбора.
- Дальше везде, где в рефах стоит «лист дедушки», прикладывай выбранный вариант.

**Шаг 2. Основа ролика (приоритет А).**
- Сделай всё с пометкой **А**, каждый промпт по одному разу.
- Покажи все листы одной сводкой и дождись утверждения.

**Шаг 3. Запасные варианты (приоритет Б).**
- Сделай всё с пометкой **Б**.
- Если ChatGPT упёрся в лимит генераций, остановись и сообщи, что готово, а что нет.

**Шаг 4. Раскадровка.**
- Делай её только из **утверждённых** листов: сначала O-SB1…SB4, потом O-SB5.

### Как делать одну генерацию

1. ChatGPT → **новый чат**.
2. Приложи файлы из строки «Рефы» **строго в указанном порядке**: в промпте они названы *image 1, image 2…*. Если написано «без рефов», ничего не прикладывай.
3. Вставь текст промпта целиком и отправь.
4. Если ChatGPT задаёт уточняющий вопрос, ответь: `Generate it exactly as described, no questions.`
5. Если ChatGPT не умеет нужный формат, соглашайся на ближайший: самый широкий горизонтальный или самый высокий вертикальный.
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
| **REF-ZR-A** | «Зарядье», деревянный мост | Деревянный пешеходный мост с высокими вертикальными рейками разной высоты, на мосту пара делает селфи. Сзади башни: бежево-песочный кирпич с чёрными решётчатыми коробами и белый кирпич с графитовыми вставками. Слева детская площадка с лаймовыми тентами |
| **REF-ZR-B** | «Зарядье», вход и башни | Башня из коричнево-красного кирпича с белым обрамлением окон, слева светлая бежево-серая башня, справа белая башня. Чёрная стальная пергола со стеклянной крышей, мокрый асфальт, машины |
| **REF-ZR-C** | «Зарядье», вид с высоты | Квартал сверху: башни из терракотового, красного, бежевого и белого кирпича, во дворе синяя баскетбольная площадка и жёлто-оранжевые детские зоны |
| **N-K01** | Лист козы из «Новосёла» | Утверждённый лист козы из папки листов первого ролика. Нужен только для пасхалки 9б |

---

## 2. О ролике (контекст для генераций)

- **Сюжет.** По телевизору объявляют, что «Развитие» — лучший застройщик года, и новость проходит по дому **овацией**.
  - Первым начинает торжественно хлопать дедушка на последнем этаже.
  - Камера идёт сквозь стены и перекрытия, как в кукольном домике в разрезе. Каждый сосед подхватывает по-своему, тем, что у него в руках: мама с младенцем беззвучно, подросток не отрываясь от экрана, хозяйка прихватками, консьерж звонком.
  - Во дворе подхватывают остальные: ковёр на снегу, варежки детей, хвост пса, пакеты на мосту.
  - Окна башни загораются в ритм. Дедушка встаёт: стоячая овация.
- **Пэкшот:** квартал вечером в **правой половине** кадра, левая половина — небо под титры.
- **Картинка:**
  - зимний **синий час** сразу после заката: глубокое синее небо, тёплые окна и фонари, лёгкий снег;
  - глубокие чёрные тени, плёночное зерно;
  - спокойная палитра, лайм — **только на бабочке дедушки**.

---

## 3. Персонажи

Формат персонажа (как в присланной сетке): слева большой портрет по плечи, справа два роста — анфас и со спины. Фон ровный серый.

### O-K01 · Дедушка — главный герой (кадры 1, 11) · А · 3 генерации

- **Рефы:** без рефов. **Файл:** `O-K01_dedushka_v1.png`, `_v2`, `_v3`

```text
Character: a slim, upright Russian man of about 75 with a kind, dignified face: neatly combed white hair with a side parting, a trimmed white moustache, deep laugh lines, bright attentive grey eyes. He has dressed up at home for a solemn occasion: a crisp white shirt, a vivid lime-green satin bow tie — the only bright colour on him — a charcoal-grey wool cardigan, buttoned, dark-grey trousers with sharp creases, and worn brown leather house slippers. Expression: solemn and quietly proud, the hint of a smile under the moustache.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same man stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing straight, arms relaxed. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

**Проверить:**
- ❗ бабочка ярко-лаймовая, остальная одежда спокойная;
- тапочки, а не туфли: в этом шутка.

### O-K02 · Молодая мама с младенцем (кадр 2) · А

- **Рефы:** без рефов. **Файл:** `O-K02_mama_v1.png`

```text
Character: a Russian woman of about 30 with a gentle, tired-but-happy face, dark hair in a loose low ponytail, no make-up, in a soft light-grey knitted lounge set and thick cream socks. She carries a sleeping baby in a beige fabric sling on her chest: the baby's face is turned into her chest, so only a small cream knitted hat and one round cheek are visible. Expression: calm and tender. From behind, the sling straps cross on her back.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same woman stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K03 · Подросток (кадр 3) · А

- **Рефы:** без рефов (подросток — только по словам). **Файл:** `O-K03_podrostok_v1.png`

```text
Character: a lanky boy of about fifteen with messy dark-blond hair and a bored, deadpan look. A navy hoodie, grey sweatpants, white socks; large matte-black over-ear headphones without any logos hang around his neck.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same boy stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, hands in the hoodie pocket. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K04 · Хозяйка с пирожками (кадр 4) · А

- **Рефы:** без рефов. **Файл:** `O-K04_khozyayka_v1.png`

```text
Character: a full-figured Russian woman of about 55 with a warm rosy face, chestnut hair in a short neat cut and small gold earrings. A cream blouse with rolled-up sleeves under a navy-and-white striped apron, dark trousers, soft house shoes; grey linen oven mitts on both hands. Expression: restrained pride, a small satisfied smile.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same woman stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, the apron ties visible from behind. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K05 · Консьерж (кадр 5) · А

- **Рефы:** без рефов. **Файл:** `O-K05_konserzh_v1.png`

```text
Character: a neat Russian woman of about 60 with a short silver bob and thin-rimmed glasses. A grey cardigan over a white blouse with a small round brooch, a dark-navy knee-length skirt, low comfortable black shoes. Expression: strict but kind, a barely visible smile.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same woman stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing straight, arms relaxed. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K06 · Мужчина с выбивалкой (кадр 6) · А

- **Рефы:** без рефов. **Файл:** `O-K06_muzhchina_kover_v1.png`

```text
Character: a broad-shouldered Russian man of about 40 who has run outside for a minute: ruddy cheeks, a short dark beard, a dark-grey knitted hat pushed back on his head, an open graphite puffer jacket over a thick oatmeal knitted sweater, dark track trousers tucked into grey felt boots (valenki) with black rubber galoshes. In his right hand a twisted rattan carpet beater. Expression: focused, in rhythm, a satisfied half-smile.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same man stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K07 · Девочка ~7 лет (кадр 7) · А

- **Рефы:** без рефов (ребёнок — только по словам). **Файл:** `O-K07_devochka_v1.png`

```text
Character: a girl of about seven with rosy cheeks, freckles and a wide grin with one missing front tooth. A navy one-piece winter snowsuit, a white knitted hat with a big pompom, white knitted mittens with a navy pattern on a string, navy snow boots. Expression: pure delight.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same girl stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, arms relaxed. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K08 · Мальчик ~7 лет (кадр 7) · А

- **Рефы:** без рефов (ребёнок — только по словам). **Файл:** `O-K08_malchik_v1.png`

```text
Character: a boy of about seven with a round face, rosy cheeks and a light-brown fringe peeking out from under a light-blue knitted hat. A grey one-piece winter snowsuit with light-blue cuffs, grey knitted mittens on a string, black snow boots. Expression: a happy, slightly shy grin.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same boy stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, arms relaxed. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K09 · Пёс (кадр 8) · А

- **Рефы:** без рефов. **Файл:** `O-K09_pyos_v1.png`

```text
Character: a medium-sized fluffy mixed-breed dog with a fox-like face: a ginger-and-white coat with a white chest, muzzle and paws, pointed ears, warm brown eyes, a big plumed tail curling over its back, a plain dark-navy collar without tags. Happy and alert.

Animal reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head portrait facing the camera; a thin black vertical line separates it from the right part, where the same dog is shown full body twice at the same scale — sitting, front view on the left; standing, left side profile with the tail clearly visible on the right. Seamless neutral mid-grey studio backdrop, soft even frontal light, soft contact shadows. Photorealistic fur, natural colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K10 · Молодой мужчина с пакетами (кадр 9) · А

- **Рефы:** без рефов. **Файл:** `O-K10_paren_pakety_v1.png`

```text
Character: a tall Russian man of about 28 with a short dark beard and a friendly, amused face. A black knitted beanie, a long graphite parka, dark jeans, brown leather winter boots. In each hand a full natural-canvas grocery tote bag with no prints — a baguette and leeks stick out of one, apples show in the other.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same man stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, a bag in each hand. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K11 · Молодая женщина (кадр 9) · А

- **Рефы:** без рефов. **Файл:** `O-K11_devushka_v1.png`

```text
Character: a Russian woman of about 27 with laughing eyes, a warm open face and light-brown hair falling from under a cream knitted hat. A long cream puffer coat, a huge chunky light-grey knitted scarf, dark-grey knitted mittens, black winter boots. Expression: about to laugh.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same woman stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing straight, arms relaxed. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### Запасные варианты (приоритет Б)

#### O-K12 · Бабушка со спицами (A1) · Б

- **Рефы:** без рефов. **Файл:** `O-K12_babushka_spitsy_v1.png`

```text
Character: a plump Russian woman of about 72 with silver hair in a bun and round glasses on a thin chain. A dusty-blue knitted cardigan over a dark-grey dress with a small muted floral print, thick grey woollen socks, felt house slippers. In her hands two wooden knitting needles with a piece of grey knitting. Expression: peering over her glasses, a faint mischievous smile.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same woman stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

#### O-K13 · Лыжник (A2) · Б

- **Рефы:** без рефов. **Файл:** `O-K13_lyzhnik_v1.png`

```text
Character: a lean, fit Russian man of about 60 with grey stubble and a weathered, cheerful face. A dark-blue retro knitted ski hat, a fitted navy-and-grey cross-country ski jacket and trousers, black ski boots, thin black gloves; a pair of black ski poles in his hands. Expression: energetic, a broad satisfied grin.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same man stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, holding the poles. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, like a high-end casting photo: real skin texture, true-to-life fabrics, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

#### O-K14 · Девочка со скрипкой (A3) · Б

- **Рефы:** без рефов (ребёнок — только по словам). **Файл:** `O-K14_devochka_skripka_v1.png`

```text
Character: a girl of about nine with two neat braids and a serious, concentrated face. A dark-blue dress over a white turtleneck, white tights, dark-blue shoes. She holds a warm-brown violin under her chin and a bow in her right hand.

Character reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same girl stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right. Seamless neutral mid-grey studio backdrop, soft even frontal light, a soft contact shadow under the feet. Photorealistic, natural muted colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

#### O-K15 · Кот (A4) · Б

- **Рефы:** без рефов. **Файл:** `O-K15_kot_v1.png`

```text
Character: a well-fed grey tabby cat with a white chest and white paws, green-gold eyes, a long striped tail, an expression of calm superiority.

Animal reference sheet for a TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head portrait facing the camera, eyes half closed; a thin black vertical line separates it from the right part, where the same cat is shown full body twice at the same scale — sitting, front view on the left; lying stretched out, left side profile with the tail clearly visible on the right. Seamless neutral mid-grey studio backdrop, soft even frontal light, soft contact shadows. Photorealistic fur, natural colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

---

## 4. Предметы

Формат предмета (как в присланной сетке): 4 ячейки 2×2 на сером фоне — спереди, сзади, сбоку, три четверти. Там, где ракурсы другие, это сказано в промпте.

### O-P01 · Лаймовая бабочка дедушки (кадры 1, 11) · А

- **Рефы:** без рефов. **Файл:** `O-P01_babochka_v1.png`

```text
Object: a classic pre-tied bow tie in vivid lime-green satin with a soft sheen, a neat butterfly shape, on a thin black adjustable neck band with a small metal clasp.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same bow tie on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view; top-right — back view with the band and clasp; bottom-left — side view; bottom-right — three-quarter view. True-to-life satin. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-P02 · Стакан в подстаканнике (кадр 1) · А

- **Рефы:** без рефов. **Файл:** `O-P02_podstakannik_v1.png`

```text
Object: a faceted clear tea glass in an ornate nickel-silver tea-glass holder (podstakannik) with a curved handle and a simple geometric relief pattern, no emblems; the glass is two-thirds full of amber tea with a teaspoon in it.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same glass in its holder on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view, handle on the right; top-right — back view, handle on the left; bottom-left — side view with the handle facing the camera; bottom-right — three-quarter view from slightly above. True-to-life metal and glass. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-P03 · Противень с пирожками и прихватки (кадр 4) · А

- **Рефы:** без рефов. **Файл:** `O-P03_pirozhki_v1.png`

```text
Object: a dark metal baking tray with twelve golden, glossy, freshly baked Russian pirozhki in neat rows, a light dusting of flour on the tray rim, and a pair of grey linen oven mitts.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same set on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred at the same scale: top-left — the tray seen from directly above with the mitts beside it; top-right — the tray from the front at eye level; bottom-left — the tray from the side; bottom-right — the tray held in both oven mitts, three-quarter view. True-to-life food and materials. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-P04 · Наушники подростка (кадр 3) · А

- **Рефы:** без рефов. **Файл:** `O-P04_naushniki_v1.png`

```text
Object: large matte-black over-ear headphones with soft cushions and a plain padded headband, no logos anywhere.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same headphones on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view; top-right — back view; bottom-left — side view; bottom-right — three-quarter view. True-to-life materials. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-P05 · Настольный звонок консьержа (кадр 5) · А

- **Рефы:** без рефов. **Файл:** `O-P05_zvonok_v1.png`

```text
Object: a classic chrome desk call bell with a polished dome and a small plunger on top, on a round black base.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same bell on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view; top-right — back view; bottom-left — side view; bottom-right — three-quarter view from slightly above. True-to-life chrome. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-P06 · Ковёр (кадр 6) · А

- **Рефы:** без рефов. **Файл:** `O-P06_kovyor_v1.png`

```text
Object: a wool carpet about 2 × 3 m with a traditional ornamental pattern in muted burgundy, beige and dark blue, fringed short ends, a little worn.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid), every cell on a seamless neutral mid-grey studio backdrop with soft even studio light: top-left — the carpet laid flat, seen from directly above; top-right — the carpet rolled up; bottom-left — the carpet folded in half; bottom-right — the carpet lying flat, three-quarter view at eye level. True-to-life wool. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-P07 · Выбивалка для ковра (кадр 6) · А

- **Рефы:** без рефов. **Файл:** `O-P07_vybivalka_v1.png`

```text
Object: a traditional carpet beater about 70 cm long, made of twisted rattan, with a looped pretzel-shaped head and a handle wrapped in rattan strips.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same carpet beater on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view; top-right — back view; bottom-left — side view; bottom-right — three-quarter view. True-to-life rattan. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-P08 · Варежки на резинке (кадр 7) · А

- **Рефы:** без рефов. **Файл:** `O-P08_varezhki_v1.png`

```text
Object: two pairs of children's knitted mittens, each pair joined by a long knitted string: one pair white with a navy snowflake pattern, the other plain grey; a few snowflakes stuck to the wool.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid), every cell on a seamless neutral mid-grey studio backdrop with soft even studio light and a soft contact shadow: top-left — both pairs laid flat, palms down; top-right — both pairs laid flat, palms up; bottom-left — one mitten from the side; bottom-right — both pairs hanging by their strings, three-quarter view. True-to-life wool. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-P09 · Пакеты с продуктами (кадр 9) · А

- **Рефы:** без рефов. **Файл:** `O-P09_pakety_v1.png`

```text
Object: two full natural-canvas tote bags with no prints: one with a long baguette and green leeks sticking out, the other with red apples and a glass bottle of milk on top.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same two bags side by side on a seamless neutral mid-grey studio floor, soft even studio light, a soft contact shadow, centred at the same scale: top-left — front view; top-right — back view; bottom-left — side view; bottom-right — three-quarter view from slightly above. True-to-life canvas and food. Clean image: no text, no letters, no labels, no prints, no logos, no watermarks.
```

### Предметы запасных вариантов (приоритет Б)

#### O-P10 · Спицы с вязанием (A1) · Б

- **Рефы:** без рефов. **Файл:** `O-P10_spitsy_v1.png`

```text
Object: two long wooden knitting needles holding a half-finished piece of grey wool knitting, with a ball of the same grey yarn attached.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same knitting on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view; top-right — back view; bottom-left — side view; bottom-right — three-quarter view. True-to-life wood and wool. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

#### O-P11 · Лыжи и палки (A2) · Б

- **Рефы:** без рефов. **Файл:** `O-P11_lyzhi_v1.png`

```text
Object: a pair of classic cross-country skis in a natural varnished wood finish with black bindings, and a pair of black ski poles with leather wrist straps and small round baskets; no logos or graphics.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same skis and poles on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred at the same scale: top-left — skis and poles lying flat, seen from above; top-right — the underside of the skis; bottom-left — side view, skis standing upright with the poles beside them; bottom-right — three-quarter view, skis and poles leaning crossed. True-to-life materials. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

#### O-P12 · Скрипка и пюпитр (A3) · Б

- **Рефы:** без рефов. **Файл:** `O-P12_skripka_v1.png`

```text
Object: a warm-brown student violin with its bow, and a black folding music stand holding a closed dark-blue music folder.

Product reference sheet for a TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred: top-left — the violin front view with the bow beside it; top-right — the violin back view; bottom-left — the violin side view; bottom-right — the music stand with the folder, three-quarter view. True-to-life wood and metal. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

---

## 5. Локации (пустые фоны, без людей)

Эти фоны станут референсом окружения для раскадровки и Seedance. **Дома точно как на рендерах «Зарядья», только зимой и вечером.**

### O-L01 · Дом в разрезе — «кукольный домик» (кадры 1–5) · А

Главный фон ролика: он фиксирует, где чья квартира и куда едет камера.
- **Рефы:** 1 — `REF-ZR-A`.
- **Файл:** `O-L01_razrez_doma_v1.png`

```text
Image 1 shows the residential quarter; use only the facade of the white-brick tower with graphite vertical bands for the outer edges of the building.

Photorealistic architectural cut-away of a modern residential tower at winter blue hour, like a dollhouse with the whole front wall removed, portrait orientation 2:3, viewed perfectly straight on with a long lens, no perspective distortion, an empty scene with no people. Thick, deep-black section cuts of walls and floor slabs divide the building into rooms of equal height. Top floor, left: a cosy living room — a caramel-brown leather armchair, a warm floor lamp, bookshelves, framed family photos, a small spruce with warm lights and old glass ornaments, oak parquet. Top floor, right: a softly lit nursery with a white crib and a warm night lamp. One floor down, right: a teenager's room with dark-blue walls, a desk with a monitor glowing and a gaming chair. Below that, right: a warm kitchen with white cabinets, an oak worktop and a pendant lamp. Ground floor: a warm lobby with a warm-grey stone floor, an oak concierge desk, graphite mailboxes and glass entrance doors on the right. The remaining rooms on the left are lived-in flats with warm light. Every room has one normal-size window in its back wall — black frame, white sill — with a snowy deep-blue evening outside. Warm interior light, deep true blacks, fine film grain. Clean image: no text, no letters, no numbers, no logos.
```

**Проверить:**
- ❗ срезы стен и перекрытий густо-чёрные и толстые: это наши швы;
- ❗ людей нет;
- окна обычного размера, не панорамные.

### O-L02 · Гостиная дедушки (кадры 1, 11) · А

- **Рефы:** 1 — `O-L01` (утверждённый разрез). **Файл:** `O-L02_gostinaya_v1.png`

```text
Image 1 is the cut-away of the building; this is its top-floor living room on the left — keep the furniture and the colours exactly.

Photorealistic location plate for a TV commercial, 16:9 landscape, an empty scene with no people. The cosy top-floor living room seen strictly frontally and planimetrically through the removed front wall, at the eye height of a seated person: in the centre the caramel-brown leather armchair facing the camera, a small side table with a lace doily, a warm floor lamp at the front left, bookshelves and a wall of framed family photos, a small spruce with warm lights and old glass ornaments in the corner, oak parquet, light warm-grey walls; in the back wall a normal-size window with a black frame and a white sill, a snowy deep-blue evening outside. The thick black cut of the wall frames the right edge of the shot. Warm lamp light, deep true blacks in the corners, fine film grain, normal lens about 47° horizontal field of view, level horizon. Clean image: no text, no letters, no logos.
```

### O-L03 · Двор зимним вечером (кадры 6–8) · А

- **Рефы:** 1 — `REF-ZR-B`; 2 — `REF-ZR-C`. **Файл:** `O-L03_dvor_v1.png`

```text
Image 1 shows the buildings at ground level and image 2 the whole quarter from above; keep the architecture exactly, but turn it into a winter evening.

Photorealistic location plate for a TV commercial, 16:9 landscape, an empty scene with no people. An eye-level view across the car-free inner courtyard at winter blue hour: the sports court lies under smooth untouched snow; the playground with curved wooden structures under snow caps, its shade sails taken down for winter; cleared paving paths lined with neat snowbanks; warm street lamps; behind, the towers from the references — brown-red brick with white window surrounds, beige-sand brick with black slatted boxes, white brick with graphite vertical bands — their normal-size windows glowing warm, and the black steel pergola with a glass roof by one of the entrances. Deep-blue sky, gentle snowfall, warm 3000 K lamp light on the snow, deep true blacks, fine film grain, normal lens about 47° horizontal field of view, level horizon. Clean image: no text, no letters, no logos, no signs, no cars.
```

**Проверить:** ❗ ни машин, ни людей, ни льда для катания.

### O-L04 · Деревянный мост вечером (кадры 9, 12) · А

- **Рефы:** 1 — `REF-ZR-A`. **Файл:** `O-L04_most_v1.png`

```text
Image 1 shows the wooden pedestrian bridge and the towers behind it; keep the architecture exactly, but turn it into a winter evening.

Photorealistic location plate for a TV commercial, 16:9 landscape, an empty scene with no people. The wooden pedestrian bridge with tall vertical timber slats of different heights on both sides and a plank deck with a thin layer of fresh snow, small warm lamps set low along the railing, looking along the bridge towards the towers — beige-sand brick with black slatted boxes and white brick with graphite vertical bands — their normal-size windows glowing warm. Winter blue hour, deep-blue sky, gentle snowfall, warm lamp light on the timber, deep true blacks, fine film grain, normal lens about 47° horizontal field of view, level horizon. Clean image: no text, no letters, no logos, no signs.
```

### O-L05 · Белая башня снизу (кадр 10) · А

- **Рефы:** 1 — `REF-ZR-A`; 2 — `REF-ZR-B`. **Файл:** `O-L05_bashnya_snizu_v1.png`

```text
Images 1 and 2 show the quarter; this is the white-brick tower with graphite vertical bands — keep its facade exactly, in winter at blue hour.

Photorealistic location plate for a TV commercial, 16:9 landscape, an empty scene with no people. A worm's-eye view from the snowy ground at the very foot of the white-brick tower, an ultra-wide lens about 84° horizontal field of view, looking straight up the facade, which converges dramatically towards the deep-blue sky; the windows of the lower half glow warm, the upper floors are still dark; snowflakes fly towards the lens. Deep true blacks, fine film grain. Clean image: no text, no letters, no logos, no signs.
```

---

## 6. Раскадровка

Только из утверждённых листов. Каждый лист раскадровки — 4 кадра 2×2. Пэкшот (O-SB4) — один большой кадр.

Общее для всех кадров:
- камера едет **вправо и вниз** по дому, во дворе вправо;
- лица освещены спереди;
- лайм только на бабочке.

### O-SB1 · Кадры 1–4 · А

- **Рефы:**
  1. лист дедушки O-K01;
  2. O-L02 гостиная;
  3. O-K02 мама;
  4. O-K04 хозяйка;
  5. O-P03 пирожки;
  6. O-L01 разрез.
- Подросток описан словами.
- **Файл:** `O-SB1_kadry_01-04_v1.png`

```text
References: image 1 — the grandfather (keep him exactly, with his lime bow tie); image 2 — his living room; image 3 — the young mother with the baby; image 4 — the woman in the apron; image 5 — her tray of pirozhki and oven mitts; image 6 — the cut-away of the whole building, showing where each room is.

Storyboard sheet for a 20-second TV commercial: four photorealistic film stills in a 2×2 grid, each still 16:9, separated by thin white gutters, with a small white panel number in the top-left corner of each still (1, 2, 3, 4) and no other text. Every still: a room of the building from image 6 seen strictly frontally through the removed front wall, like a dollhouse, normal lens, level horizon; winter blue hour outside the window, warm interior light, deep true blacks, fine film grain, calm natural colours; the only vivid colour is the lime-green bow tie.

1 — The living room from image 2: the grandfather from image 1 sits in the caramel leather armchair, a glass of tea in a metal holder on the side table beside him; he looks just below the camera as if at a TV and claps slowly and solemnly. Warm floor-lamp light and a faint bluish TV glow on his face from the front.

2 — Same floor, the next flat to the right: the left edge of the frame is a thick black band — the cut of the wall between the flats. A softly lit nursery: the young mother from image 3 rocks the sleeping baby in the sling, smiles to herself and taps two fingers into her palm — a silent applause. Warm night-lamp light on her face from the front.

3 — One floor down: the top edge of the frame is a thick black band — the cut of the floor slab. A teenager's room with dark-blue walls: a lanky boy of about fifteen with messy dark-blond hair, in a navy hoodie and big black over-ear headphones with one ear cup slid off, sits at his desk; eyes still on the monitor, he gives two flat, deadpan claps. The monitor lights his face from the front.

4 — Another floor down, a black slab band at the top: a warm kitchen; the woman from image 4 holds the tray from image 5 in her oven mitts, sets it down and claps the mitts together; a small puff of flour glitters in the light; a restrained, proud smile. A warm pendant lamp lights her face from the front.
```

### O-SB2 · Кадры 5–8 · А

- **Рефы:**
  1. O-K05 консьерж;
  2. O-L01 разрез;
  3. O-K06 мужчина с выбивалкой;
  4. O-P06 ковёр;
  5. O-L03 двор;
  6. O-K09 пёс.
- Дети описаны словами.
- **Файл:** `O-SB2_kadry_05-08_v1.png`

```text
References: image 1 — the concierge; image 2 — the cut-away of the building (its ground-floor lobby); image 3 — the man with the carpet beater; image 4 — the carpet; image 5 — the courtyard; image 6 — the dog.

Storyboard sheet for a 20-second TV commercial: four photorealistic film stills in a 2×2 grid, each still 16:9, separated by thin white gutters, with a small white panel number in the top-left corner of each still (5, 6, 7, 8) and no other text. Every still: winter blue hour, warm lamps, gentle snowfall, deep true blacks, fine film grain, calm natural colours, faces lit from the front.

5 — The ground-floor lobby from image 2 seen frontally: the concierge from image 1 behind the oak desk taps a chrome desk bell twice and gives a small approving nod; through the glass entrance doors behind her, the blue winter courtyard. The right edge of the frame is a dark blurred band — the cut of the facade wall right at the lens.

6 — The courtyard from image 5: the man from image 3 beats the carpet from image 4, laid flat on the snow, with his rattan carpet beater; snow dust rises and glitters in the warm lamp light; behind him the snowy playground and towers with warm windows. A warm lamp lights his face from the front.

7 — At a child's eye height in the same courtyard: two children of about seven face the camera and clap their mittens — a girl in a navy snowsuit and a white knitted hat with a pompom, with freckles and a missing front tooth; a boy in a grey snowsuit and a light-blue knitted hat — snow bursts off the mittens like confetti in the lamp light; wide grins.

8 — A ground-level insert with a long lens: the dog from image 6 sits on the snow, its plumed tail sweeping the snow from side to side like a wiper; snow sparkles in the lamp light.
```

### O-SB3 · Кадры 9, 9б, 10, 11 · А

- **Рефы:**
  1. O-L04 мост;
  2. O-K10 молодой мужчина;
  3. O-K11 молодая женщина;
  4. лист козы N-K01 из «Новосёла»;
  5. O-L05 башня снизу;
  6. лист дедушки O-K01.
- **Файл:** `O-SB3_kadry_09-11_v1.png`

```text
References: image 1 — the wooden bridge; image 2 — the young man with grocery bags; image 3 — the young woman; image 4 — the white goat character (keep her exactly); image 5 — the white-brick tower from below; image 6 — the grandfather (keep him exactly, with his lime bow tie).

Storyboard sheet for a 20-second TV commercial: four photorealistic film stills in a 2×2 grid, each still 16:9, separated by thin white gutters, with a small white label in the top-left corner of each still (9, 9b, 10, 11) and no other text. Every still: winter blue hour, warm lamps, gentle snowfall, deep true blacks, fine film grain, calm natural colours, faces lit from the front; the only vivid colour is lime green — on the bow tie, and on the goat's scarf in 9b.

9 — The wooden bridge from image 1, tall vertical timber slats blurred in the foreground: the young couple from images 2 and 3 have stopped; she claps in her mittens and laughs into her scarf; he, hands full with two grocery bags, taps the bags together. Small warm lamps low along the railing light their faces from the front.

9b — The same shot, and at the far end of the bridge the white goat from image 4 — upright, gold aviator sunglasses, lime knitted scarf — claps her front hooves.

10 — A worm's-eye view from the snowy ground at the foot of the tower from image 5, ultra-wide lens: its windows are lighting up one by one, floor after floor upward, the wave of warm light nearly at the top; snowflakes fly towards the lens; deep-blue sky.

11 — The grandfather's living room again, seen strictly frontally: the grandfather from image 6 now stands, straightening his lime bow tie in the middle of a final clap, with a small dignified nod straight into the lens. Warm lamp light on his face from the front, the snowy blue window behind him.
```

### O-SB4 · Кадр 12, пэкшот · А

- **Рефы:**
  1. O-L04 мост;
  2. `REF-ZR-A`;
  3. `REF-ZR-C`.
- **Файл:** `O-SB4_kadr_12_pekshot_v1.png`

```text
References: image 1 — the wooden bridge at winter blue hour; image 2 — the bridge and the towers in the original render; image 3 — the whole quarter from above. Keep the architecture exactly.

A single photorealistic film still for the final shot of a TV commercial, 16:9 landscape. A wide view from the wooden bridge at winter blue hour: the tall timber slats lead the eye to the right, where the towers of the quarter — the white-brick tower with graphite vertical bands and its beige-sand brick neighbour — stand in the right half of the frame with warm glowing windows; far below, tiny figures of residents in the snowy courtyard; gentle snowfall. The left half of the frame is a calm, empty deep-blue evening sky above dark snow-covered park trees, with nothing in it. Deep true blacks, warm windows, fine film grain, normal lens about 47° horizontal field of view, level horizon. Clean image: no text, no letters, no logos, no signs.
```

**Проверить:** ❗ дома в правой половине; левая половина — пустое небо под титры.

### O-SB5 · Запасные варианты A1–A4 · Б

- **Рефы:**
  1. O-K12 бабушка;
  2. O-P10 спицы;
  3. O-K13 лыжник;
  4. O-P11 лыжи;
  5. O-K15 кот;
  6. O-L01 разрез.
- Девочка описана словами.
- **Файл:** `O-SB5_varianty_A1-A4_v1.png`

```text
References: image 1 — the grandmother; image 2 — her knitting; image 3 — the skier; image 4 — his skis and poles; image 5 — the cat; image 6 — the cut-away of the building, for the look of the rooms.

Storyboard sheet for a TV commercial: four photorealistic film stills in a 2×2 grid, each still 16:9, separated by thin white gutters, with a small white label in the top-left corner of each still (A1, A2, A3, A4) and no other text. Every still: winter blue hour, warm light, deep true blacks, fine film grain, calm natural colours, faces lit from the front.

A1 — A cosy room of the building from image 6 seen frontally like a dollhouse, a thick black slab band along the top edge: the grandmother from image 1 in an armchair taps her knitting needles from image 2 together like applause, peering over her glasses with a faint smile. A warm lamp in front of her.

A2 — The snowy park of the quarter, a ski track between birches, warm park lamps: the skier from image 3 has stopped on his skis from image 4 and taps his ski poles together above his head, grinning. A lamp lights his face from the front.

A3 — A small room of the same building, seen frontally: a girl of about nine with two neat braids, in a dark-blue dress over a white turtleneck, stands at a music stand and plays a short solemn fanfare on a violin, eyes shut with concentration. A warm desk lamp lights her face from the front.

A4 — A windowsill with a snowy blue evening outside the window: the cat from image 5 lies on the sill with half-closed eyes, its tail thumping the sill in rhythm. Warm room light on its face from the front.
```

---

## 7. После раскадровки

Следующий этап — ключевые кадры (по одному на план) и промпты Seedance 2.0 для «Виви». Это делаем отдельно, после того как дизайнер утвердит раскадровку и выберет варианты.
