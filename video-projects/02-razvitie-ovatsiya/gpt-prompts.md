# «Овация»: промпты для ChatGPT, v4

Ролик застройщика «Развитие» для **арт-квартала «Зарядье»**. YouTube, 16:9, 20 секунд, финальная фраза **«Лучший застройщик года»**. Версия v4 от 04.10.2026: игра актёров по разбору эмоций (v3), цвет и фотостиль по пяти стилевым референсам дизайнера (v4).

Это **набор инструкций для Claude в десктоп-приложении**: он генерирует картинки в ChatGPT через браузер дизайнера. Сценарий и раскадровка — [`storyboard.md`](storyboard.md).

## Что изменилось в v4

- **Цвет и фотостиль** теперь опираются на пять стилевых референсов дизайнера, REF-STYLE-A…E (раздел «Стилевые референсы»).
  - Стиль описан словами в общем блоке каждого кадра.
  - В фонах и раскадровке нужный кадр прикладывается последней картинкой, только как образец цвета и света.
- Листы персонажей и предметов не менялись.

## Что изменилось в v3

Изменилась только **раскадровка** (O-SB1…SB5).
- Каждая реакция записана движениями лица, а не словами-эмоциями: что делают брови, глаза, губы. Правила — в `video-research/06-emotions.md`.
- **Дедушка торжественный:** подбородок чуть вверх, губы в прямую линию, без улыбки. В финале он кивает в объектив, тепло только в глазах.
- **Остальные соседи сдержанные:** у мамы уголки рта приподняты при сомкнутых губах, хозяйка сдерживает гордую улыбку, подросток с каменным лицом.
- **Большая эмоция в ролике одна** — смех детей во дворе.
- **Соседи хлопают вразнобой:** каждый вступает в свою долю.

## Что изменилось в v2

Этот ролик ещё не генерировали. Его поправили по тем же замечаниям, что и раскадровку «Новосёла»:
- **Фотостиль как у Яндекса:**
  - тёплый контровой свет ламп и окон рисует силуэт, лицо читается мягкой подсветкой спереди;
  - живая фактура кожи;
  - эмоции без позирования.
- **Палитра бренда в одежде и интерьерах.**
  - У каждой квартиры свой цвет из палитры.
  - Люди в синих тонах палитры, без чёрного и тёмно-синего.
  - Лайм — самый яркий акцент на бабочке дедушки.
- **Пасхалка 9б** — с новой, изящной козой из «Новосёла» v2.

## Стилевые референсы: основа цвета и фотостиля

Дизайнер выбрал пять кадров как эталон цвета и фотостиля (04.10.2026). Найди их у дизайнера на компьютере по описанию.

| Код | Кадр |
|---|---|
| **REF-STYLE-A** | Квартира: мужчина в клетчатой рубашке танцует в прихожей, утреннее солнце из окна слева, светлая кухня с голубыми фасадами, красные ковры |
| **REF-STYLE-B** | Летний двор: женщина в розовой футболке на качелях с телефоном, кружевные тени листвы на лице, светлый дом, девочка на качелях |
| **REF-STYLE-C** | Крупно парень в чёрных очках и красной худи: мокрое лицо, контровой свет, зелёный размытый фон |
| **REF-STYLE-D** | Батарея с белым терморегулятором «22°» у окна: солнечные полосы, глиняные горшки, льняная штора |
| **REF-STYLE-E** | Девушка в зелёной майке медитирует у больших окон, жёлтые кубики и мяч, свет сзади |

**Что в них общего** (замеры по пяти кадрам):
- **Свет:** тёплый натуральный, с чёткими пятнами и тенями от реального источника — окна, листвы.
- **Яркость:** медиана 78–121 из 255. Пересвета нет совсем, светлые места не выше 206–233.
- **Тени:** глубокие (1-й перцентиль 5–45), но мягкие.
- **Цвет:** насыщенность умеренная (0,25–0,37), тёплый баланс (R − B от +18 до +52). Кремово-бежевая основа и 1–2 сочных акцента: голубые фасады и красный ковёр, розовая футболка, красная худи, зелёная майка и жёлтый мяч.
- **Пространство:** живая обжитая фактура, малая глубина резкости, плёночное зерно.

**Как используем:**
- в промптах раскадровки и фонов этот стиль описан словами в общем блоке;
- там, где в рефах стоит `REF-STYLE-…`, кадр прикладывается **последней картинкой**, только как образец цвета и света;
- листы персонажей и предметов остаются на сером фоне, без стилевых референсов;
- наша палитра бренда при этом остаётся в одежде и предметах: стилевой кадр задаёт свет и тон, а не цвета вещей.

## Фотостиль v2: как у Яндекса, а не «нейросеть»

Раскадровка v1 вышла постной и нейросетевой. Мы сравнили её с кадрами Яндекса, которые прислал дизайнер: 5 кадров Яндекса против 21 кадра нашей v1. Цифры показывают, в чём ошибка:

| | Яндекс | Наша v1 |
|---|---|---|
| Средняя яркость (медиана, из 255) | 41–112 | на улице 124–172 |
| Пересвет, доля пикселей ≥ 250 | 0–0,4% | на улице 0,4–4,2%: снег выбит в белое |
| Цветовых семейств в кадре | 2–3 | чаще 1 |
| Теплота интерьеров (R − B) | от +4 до +25 | от +45 до +70: «оранжевый суп» |
| Насыщенных пикселей в интерьере | до 44% | 65–90% |

Ещё три причины, которые не меряются цифрами:
- одинаковое «золотое сияние» в каждом кадре;
- позирующие улыбки;
- коза — лохматый костюм вместо изящного персонажа.

**Что делаем в v2** (всё уже вписано в промпты):
1. **Свет как в кино.** Солнце или лампа сбоку-сзади даёт контур на волосах, шерсти, паре и кромке снега. Лицо читается за счёт мягкой подсветки спереди: от снега, от лампы. Сияния на весь кадр нет.
2. **Экспозиция по лицу.** Снег сохраняет фактуру, в тени он голубой. Блики мягко сворачиваются, чёрное глубокое, но не провальное.
3. **Цвет.** В кадре 2–3 цветовые семьи: белый снег, голубое небо, тёплое солнце и палитра бренда на одежде и предметах. Интерьеры светлые и сбалансированные.
4. **Объектив.** ~35–40 мм на общих, 50–85 мм на лицах. Малая глубина резкости, передний план.
5. **Люди.** Настоящие лица с фактурой кожи, без глянца. Микроэмоции в середине действия. Улыбка только там, где она написана, и маленькая.

## Палитра бренда

| Цвет (как в палитре) | HEX | В промптах |
|---|---|---|
| Зелёно-жёлтый (лайм) | `#ADFC30` | lime |
| Васильковый | `#0F7DF5` | cornflower blue |
| Лазурный | `#1A45D5` | azure |
| Небесный | `#66A3FF` | sky blue |
| «Синий» (на палитре — самый светлый голубой) | `#DAEEFC` | pale ice blue |
| Светлый (без подписи) | `#F4F8FC` | near-white |

- HEX сняты с картинки палитры на глаз. Лайм и васильковый сверены с баннером «Авиапарк».
- Если в брендбуке есть точные значения, их надо подставить в промпты.
- **На палитре подпись «Синий» стоит на самом светлом голубом.** Цвет беру по образцу, а не по подписи. Если имелся в виду другой — скажите.

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
6. Прошлые генерации из папок «Рендеры» в рефы не идут.
7. **Чужие референсы — только образец приёма.**
   - Образцы сеток (мокрая девушка, фиолетовая папка, робот Яндекса) в ChatGPT не прикладываем.
   - Пять **стилевых референсов REF-STYLE-A…E** дизайнер выбрал основой цвета и фотостиля. Их прикладываем **только там, где они стоят в рефах, и всегда последней картинкой**. Из них берём только цвет и свет; людей, предметы, место, сезон и композицию не берём.
8. **Палитра бренда — в одежде и предметах** (таблица ниже). Лайм — самый яркий акцент. Чёрной и тёмно-синей одежды нет. На предметах нет логотипов и надписей.
9. **Свет как в кино.** Источник сбоку-сзади рисует контур волос, шерсти и пара изо рта. Лицо при этом читается мягкой подсветкой спереди. Эмоции сдержанные, у всех разные, никто не позирует.
10. Двор без машин. Спортплощадка под ровным снегом, катка нет.
11. Лист козы для пасхалки 9б берём из «Новосёла» (N-K01 v2, утверждённый).

### Порядок работы

**Шаг 0. Один раз перед стартом:**
- найди на компьютере файлы из раздела «Референсы» и выпиши соответствие «код → путь»;
- покажи это дизайнеру одним сообщением и спроси, куда сохранять результаты (предложи `Ролики 2027\02 Овация\Листы\`);
- если какой-то файл не нашёлся, спроси о нём в этом же сообщении. Другой файл вместо него не подставляй.

**Шаг 1. Дедушка.**
- Сделай **O-K01 три раза в трёх новых чатах**.
- Покажи дизайнеру и дождись выбора.
- Дальше везде, где в рефах стоит этот лист, прикладывай выбранный вариант.

**Шаг 2. Основа ролика (приоритет А).**
1. Люди O-K02…K11.
2. Предметы O-P01…P09.
3. Локации: сначала O-L01 (разрез), потом O-L02 с ним в рефах, потом O-L03…L05.

Покажи все листы одной сводкой и дождись утверждения.

**Шаг 3. Запасные варианты (приоритет Б).**
- Сделай всё с пометкой **Б**.
- Если ChatGPT упёрся в лимит генераций, остановись и сообщи, что готово, а что нет.

**Шаг 4. Раскадровка.** Только из утверждённых листов: сначала O-SB1…SB4, потом O-SB5.

### Как делать одну генерацию

1. ChatGPT → **новый чат**.
2. Приложи файлы из строки «Рефы» **строго в указанном порядке**: в промпте они названы *image 1, image 2…*. Если написано «без рефов», ничего не прикладывай.
3. Вставь текст промпта целиком и отправь.
4. Если ChatGPT задаёт уточняющий вопрос, ответь: `Generate it exactly as described, no questions.`
5. Если ChatGPT не умеет нужный формат, соглашайся на ближайший: самый широкий горизонтальный или самый высокий вертикальный.
6. Скачай картинку в полном размере и сохрани под именем из строки «Файл». Повтор того же промпта — следующий номер: `_2`, `_3`.
7. Проверь по чек-листу ниже.
   - Если провален пункт с ❗, сделай **одну** повторную генерацию в новом чате.
   - Если снова не вышло, отметь это в отчёте и больше не повторяй.

### Чек-лист

- раскладка как в промпте: у персонажа портрет слева + анфас + спина; у предмета 4 ячейки;
- ❗ нет текста, подписей, логотипов и водяных знаков;
- ❗ цвета одежды и предметов как в промпте: палитра бренда, **никакой чёрной и тёмно-синей одежды**, если её нет в промпте;
- ❗ кадр выглядит как фото с настоящей камеры: живая кожа, снег с фактурой, а не белое пятно, нет «золотого сияния» на весь кадр;
- ❗ эмоция как в промпте: никто не позирует и не улыбается, если улыбки нет в промпте;
- детали совпадают во всех ракурсах и с листами персонажей.

### Отчёт дизайнеру после каждого шага

Таблица: код — файл — что получилось — что не так. Без оценок «отлично», только факты.

## 1. Референсы (файлы на компьютере дизайнера)

| Код | Что это | Как узнать файл |
|---|---|---|
| **REF-ZR-A** | «Зарядье», деревянный мост | Деревянный пешеходный мост с высокими вертикальными рейками разной высоты, на мосту пара делает селфи. Сзади башни: бежево-песочный кирпич с чёрными решётчатыми коробами и белый кирпич с графитовыми вставками. Слева детская площадка с лаймовыми тентами |
| **REF-ZR-B** | «Зарядье», вход и башни | Башня из коричнево-красного кирпича с белым обрамлением окон, слева светлая бежево-серая башня, справа белая башня. Чёрная стальная пергола со стеклянной крышей, мокрый асфальт, машины |
| **REF-ZR-C** | «Зарядье», вид с высоты | Квартал сверху: башни из терракотового, красного, бежевого и белого кирпича, во дворе синяя баскетбольная площадка и жёлто-оранжевые детские зоны |
| **N-K01** | Лист козы из «Новосёла» v2 | Утверждённый лист новой козы из папки листов первого ролика. Нужен только для пасхалки 9б |

## 2. О ролике (контекст для генераций)

- **Сюжет.** По телевизору объявляют, что «Развитие» — лучший застройщик года, и новость проходит по дому **овацией**.
  - Первым начинает торжественно хлопать дедушка на последнем этаже: лаймовая бабочка, лазурный кардиган, тапочки.
  - Камера идёт сквозь стены и перекрытия, как в кукольном домике в разрезе. Каждый сосед подхватывает по-своему, тем, что у него в руках.
  - Во дворе подхватывают остальные: ковёр на снегу, варежки детей, хвост пса, пакеты на мосту.
  - Окна башни загораются в ритм. Дедушка встаёт: стоячая овация.
- **Пэкшот:** квартал вечером в **правой половине** кадра, левая половина — небо под титры.
- **Картинка:**
  - зимний **синий час**: глубокое синее небо, тёплые окна и фонари, лёгкий снег;
  - контровой тёплый свет и читаемые лица;
  - синие тона палитры в одежде и комнатах, лайм — акцентами.

## 3. Персонажи

Формат персонажа (как в присланной сетке): слева большой портрет по плечи, справа два роста — анфас и со спины. Фон ровный серый.

### O-K01 · Дедушка — главный герой (кадры 1, 11) · А · 3 генерации

- **Рефы:** без рефов.
- **Файл:** `O-K01_dedushka_1.png`
- **Что изменилось с v1:** лазурный кардиган вместо графитового, светло-серые брюки.

```text
Character: a slim, upright Russian man of about 75 with a kind, dignified face: neatly combed white hair with a side parting, a trimmed white moustache, deep laugh lines, real age spots and wrinkles, bright attentive grey eyes. He has dressed up at home for a solemn occasion: a crisp white shirt, a vivid lime-green satin bow tie (#ADFC30), an azure wool cardigan (#1A45D5), buttoned, light-grey trousers with sharp creases, and worn brown leather house slippers. Expression: solemn and quietly proud; no smile, only a hint of warmth under the moustache.

Character reference sheet for a live-action TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same man stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing naturally, arms relaxed. Seamless neutral mid-grey studio backdrop, soft light from a large softbox, a soft contact shadow under the feet. Photographed like a real casting photo of a real man: natural skin texture with pores, fine lines and small imperfections, flyaway hairs, true-to-life fabrics with real creases, accurate garment colours, no retouching gloss. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

**Проверить:**
- ❗ бабочка ярко-лаймовая, кардиган лазурный
- тапочки, а не туфли: в этом шутка
- не улыбается, торжественный

### O-K02 · Молодая мама с младенцем (кадр 2) · А

- **Рефы:** без рефов.
- **Файл:** `O-K02_mama_1.png`
- **Что изменилось с v1:** бледно-голубой домашний костюм, небесная шапочка младенца.

```text
Character: a Russian woman of about 30 with a gentle, tired-but-happy face, dark hair in a loose low ponytail, no make-up, in a soft pale ice-blue knitted lounge set (#DAEEFC) and thick cream socks. She carries a sleeping baby in a beige fabric sling on her chest: the baby's face is turned into her chest, so only a small sky-blue knitted hat (#66A3FF) and one round cheek are visible. Expression: calm and tender. From behind, the sling straps cross on her back.

Character reference sheet for a live-action TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same woman stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing naturally, arms relaxed. Seamless neutral mid-grey studio backdrop, soft light from a large softbox, a soft contact shadow under the feet. Photographed like a real casting photo of a real woman: natural skin texture with pores, fine lines and small imperfections, flyaway hairs, true-to-life fabrics with real creases, accurate garment colours, no retouching gloss. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K03 · Подросток (кадр 3) · А

- **Рефы:** без рефов.
- **Файл:** `O-K03_podrostok_1.png`
- **Что изменилось с v1:** васильковое худи, белые наушники.
- Подросток — только по словам.

```text
Character: a lanky boy of about fifteen with messy dark-blond hair and a bored, deadpan look. A cornflower-blue hoodie (#0F7DF5), light-grey sweatpants, white socks; large matte-white over-ear headphones without any logos hang around his neck.

Character reference sheet for a live-action TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same boy stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing, hands in the hoodie pocket. Seamless neutral mid-grey studio backdrop, soft light from a large softbox, a soft contact shadow under the feet. Photographed like a real casting photo of a real boy: natural skin texture, real child proportions, flyaway hairs, true-to-life fabrics with real creases, accurate garment colours, no retouching gloss. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K04 · Хозяйка с пирожками (кадр 4) · А

- **Рефы:** без рефов.
- **Файл:** `O-K04_khozyayka_1.png`
- **Что изменилось с v1:** фартук в васильковую полоску, небесные прихватки.

```text
Character: a full-figured Russian woman of about 55 with a warm rosy face, chestnut hair in a short neat cut and small gold earrings. A cream blouse with rolled-up sleeves under an apron with cornflower-blue and white stripes (#0F7DF5), light-grey trousers, soft house shoes; sky-blue quilted oven mitts (#66A3FF) on both hands. Expression: restrained pride, lips pressed together in a small satisfied way.

Character reference sheet for a live-action TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same woman stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing naturally, arms relaxed, the apron ties visible from behind. Seamless neutral mid-grey studio backdrop, soft light from a large softbox, a soft contact shadow under the feet. Photographed like a real casting photo of a real woman: natural skin texture with pores, fine lines and small imperfections, flyaway hairs, true-to-life fabrics with real creases, accurate garment colours, no retouching gloss. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K05 · Консьерж (кадр 5) · А

- **Рефы:** без рефов.
- **Файл:** `O-K05_konserzh_1.png`
- **Что изменилось с v1:** лазурный кардиган, светло-серая юбка.

```text
Character: a neat Russian woman of about 60 with a short silver bob and thin-rimmed glasses. An azure cardigan (#1A45D5) over a white blouse with a small round brooch, a light-grey knee-length skirt, low comfortable shoes. Expression: strict but kind, a barely visible smile in the eyes.

Character reference sheet for a live-action TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same woman stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing naturally, arms relaxed. Seamless neutral mid-grey studio backdrop, soft light from a large softbox, a soft contact shadow under the feet. Photographed like a real casting photo of a real woman: natural skin texture with pores, fine lines and small imperfections, flyaway hairs, true-to-life fabrics with real creases, accurate garment colours, no retouching gloss. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K06 · Мужчина с выбивалкой (кадр 6) · А

- **Рефы:** без рефов.
- **Файл:** `O-K06_muzhchina_kover_1.png`
- **Что изменилось с v1:** васильковый пуховик, светло-серая шапка.

```text
Character: a broad-shouldered Russian man of about 40 who has run outside for a minute: ruddy cheeks, a short dark beard, a light-grey knitted hat pushed back on his head, an open cornflower-blue puffer jacket (#0F7DF5) over a thick oatmeal knitted sweater, grey track trousers tucked into grey felt boots (valenki) with black rubber galoshes. In his right hand a twisted rattan carpet beater. Expression: focused, in rhythm.

Character reference sheet for a live-action TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same man stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing naturally, arms relaxed. Seamless neutral mid-grey studio backdrop, soft light from a large softbox, a soft contact shadow under the feet. Photographed like a real casting photo of a real man: natural skin texture with pores, fine lines and small imperfections, flyaway hairs, true-to-life fabrics with real creases, accurate garment colours, no retouching gloss. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K07 · Девочка ~7 лет (кадр 7) · А

- **Рефы:** без рефов.
- **Файл:** `O-K07_devochka_1.png`
- **Что изменилось с v1:** небесный комбинезон, лаймовый помпон.
- Ребёнок — только по словам.

```text
Character: a girl of about seven with rosy cheeks, freckles and a wide grin with one missing front tooth. A sky-blue one-piece winter snowsuit (#66A3FF), a white knitted hat with a big lime pompom (#ADFC30), white knitted mittens with a cornflower-blue pattern on a string, white snow boots. Expression: pure delight.

Character reference sheet for a live-action TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same girl stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing naturally, arms relaxed. Seamless neutral mid-grey studio backdrop, soft light from a large softbox, a soft contact shadow under the feet. Photographed like a real casting photo of a real girl: natural skin texture, real child proportions, flyaway hairs, true-to-life fabrics with real creases, accurate garment colours, no retouching gloss. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K08 · Мальчик ~7 лет (кадр 7) · А

- **Рефы:** без рефов.
- **Файл:** `O-K08_malchik_1.png`
- **Что изменилось с v1:** васильковый комбинезон, лаймовые варежки.
- Ребёнок — только по словам.

```text
Character: a boy of about seven with a round face, rosy cheeks and a light-brown fringe peeking out from under a pale ice-blue knitted hat (#DAEEFC). A cornflower-blue one-piece winter snowsuit (#0F7DF5) with pale ice-blue cuffs, lime knitted mittens on a string (#ADFC30), grey snow boots. Expression: a happy, slightly shy grin.

Character reference sheet for a live-action TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same boy stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing naturally, arms relaxed. Seamless neutral mid-grey studio backdrop, soft light from a large softbox, a soft contact shadow under the feet. Photographed like a real casting photo of a real boy: natural skin texture, real child proportions, flyaway hairs, true-to-life fabrics with real creases, accurate garment colours, no retouching gloss. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K09 · Пёс (кадр 8) · А

- **Рефы:** без рефов.
- **Файл:** `O-K09_pyos_1.png`
- **Что изменилось с v1:** лаймовый ошейник.

```text
Character: a medium-sized fluffy mixed-breed dog with a fox-like face: a ginger-and-white coat with a white chest, muzzle and paws, pointed ears, warm brown eyes, a big plumed tail curling over its back, a plain lime collar (#ADFC30) without tags. Happy and alert.

Animal reference sheet for a live-action TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head portrait facing the camera, alert and happy; a thin black vertical line separates it from the right part, where the same dog is shown full body twice at the same scale — sitting, front view on the left; standing, left side profile with the tail clearly visible on the right. Seamless neutral mid-grey studio backdrop, soft light from a large softbox, soft contact shadows. Photographed like a real animal portrait: a real dog, true-to-life fur and natural colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K10 · Молодой мужчина с пакетами (кадр 9) · А

- **Рефы:** без рефов.
- **Файл:** `O-K10_paren_pakety_1.png`
- **Что изменилось с v1:** лазурная парка, небесная шапка, один пакет васильковый.

```text
Character: a tall Russian man of about 28 with a short dark beard and a friendly, amused face. A sky-blue knitted beanie (#66A3FF), a long azure parka (#1A45D5), light-wash jeans, tan leather winter boots. In each hand a full canvas grocery tote bag with no prints — a natural one with a baguette and leeks sticking out, a cornflower-blue one with apples showing.

Character reference sheet for a live-action TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same man stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing naturally, a bag in each hand. Seamless neutral mid-grey studio backdrop, soft light from a large softbox, a soft contact shadow under the feet. Photographed like a real casting photo of a real man: natural skin texture with pores, fine lines and small imperfections, flyaway hairs, true-to-life fabrics with real creases, accurate garment colours, no retouching gloss. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K11 · Молодая женщина (кадр 9) · А

- **Рефы:** без рефов.
- **Файл:** `O-K11_devushka_1.png`
- **Что изменилось с v1:** бледно-голубой пуховик, васильковый шарф.

```text
Character: a Russian woman of about 27 with laughing eyes, a warm open face and light-brown hair falling from under a white knitted hat. A long pale ice-blue puffer coat (#DAEEFC), a huge chunky cornflower-blue knitted scarf (#0F7DF5), light-grey mittens, white winter boots. Expression: about to laugh.

Character reference sheet for a live-action TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same woman stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing naturally, arms relaxed. Seamless neutral mid-grey studio backdrop, soft light from a large softbox, a soft contact shadow under the feet. Photographed like a real casting photo of a real woman: natural skin texture with pores, fine lines and small imperfections, flyaway hairs, true-to-life fabrics with real creases, accurate garment colours, no retouching gloss. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K12 · Бабушка со спицами (A1) · Б

- **Рефы:** без рефов.
- **Файл:** `O-K12_babushka_spitsy_1.png`
- **Что изменилось с v1:** небесный кардиган, бледно-голубое вязание.

```text
Character: a plump Russian woman of about 72 with silver hair in a bun and round glasses on a thin chain. A sky-blue knitted cardigan (#66A3FF) over a light-grey dress with a small muted floral print, thick grey woollen socks, felt house slippers. In her hands two wooden knitting needles with a piece of pale ice-blue knitting. Expression: peering over her glasses, a faint mischievous look.

Character reference sheet for a live-action TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same woman stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing naturally, arms relaxed. Seamless neutral mid-grey studio backdrop, soft light from a large softbox, a soft contact shadow under the feet. Photographed like a real casting photo of a real woman: natural skin texture with pores, fine lines and small imperfections, flyaway hairs, true-to-life fabrics with real creases, accurate garment colours, no retouching gloss. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K13 · Лыжник (A2) · Б

- **Рефы:** без рефов.
- **Файл:** `O-K13_lyzhnik_1.png`
- **Что изменилось с v1:** васильково-белый лыжный костюм с лаймовой полоской.

```text
Character: a lean, fit Russian man of about 60 with grey stubble and a weathered, cheerful face. A retro cross-country ski suit in cornflower blue and white (#0F7DF5) with a thin lime stripe on the sleeves (#ADFC30), a white knitted ski hat, black ski boots, thin light-grey gloves; a pair of light-grey ski poles in his hands. Expression: energetic, a broad satisfied grin.

Character reference sheet for a live-action TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same man stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing, holding the poles. Seamless neutral mid-grey studio backdrop, soft light from a large softbox, a soft contact shadow under the feet. Photographed like a real casting photo of a real man: natural skin texture with pores, fine lines and small imperfections, flyaway hairs, true-to-life fabrics with real creases, accurate garment colours, no retouching gloss. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K14 · Девочка со скрипкой (A3) · Б

- **Рефы:** без рефов.
- **Файл:** `O-K14_devochka_skripka_1.png`
- **Что изменилось с v1:** лазурное платье.
- Ребёнок — только по словам.

```text
Character: a girl of about nine with two neat braids and a serious, concentrated face. An azure dress (#1A45D5) over a white turtleneck, white tights, light-grey shoes. She holds a warm-brown violin under her chin and a bow in her right hand.

Character reference sheet for a live-action TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line separates it from the right part, where the same girl stands full length twice at the same scale, with a little space above the head and below the feet — front view on the left, back view on the right, standing, playing the violin. Seamless neutral mid-grey studio backdrop, soft light from a large softbox, a soft contact shadow under the feet. Photographed like a real casting photo of a real girl: natural skin texture, real child proportions, flyaway hairs, true-to-life fabrics with real creases, accurate garment colours, no retouching gloss. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-K15 · Кот (A4) · Б

- **Рефы:** без рефов.
- **Файл:** `O-K15_kot_1.png`

```text
Character: a well-fed grey tabby cat with a white chest and white paws, green-gold eyes, a long striped tail, an expression of calm superiority.

Animal reference sheet for a live-action TV commercial, 16:9 landscape. Layout: the left 45% of the sheet is a large head portrait facing the camera, eyes half closed; a thin black vertical line separates it from the right part, where the same cat is shown full body twice at the same scale — sitting, front view on the left; lying stretched out, left side profile with the tail clearly visible on the right. Seamless neutral mid-grey studio backdrop, soft light from a large softbox, soft contact shadows. Photographed like a real animal portrait: a real cat, true-to-life fur and natural colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

---

## 4. Предметы

Формат предмета (как в присланной сетке): 4 ячейки 2×2 на сером фоне — спереди, сзади, сбоку, три четверти. Там, где ракурсы другие, это сказано в промпте.

### O-P01 · Лаймовая бабочка дедушки (кадры 1, 11) · А

- **Рефы:** без рефов.
- **Файл:** `O-P01_babochka_1.png`

```text
Object: a classic pre-tied bow tie in vivid lime-green satin (#ADFC30) with a soft sheen, a neat butterfly shape, on a thin black adjustable neck band with a small metal clasp.

Product reference sheet for a live-action TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same bow tie on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view; top-right — back view with the band and clasp; bottom-left — side view; bottom-right — three-quarter view. Photographed like a real product shot: true-to-life materials with real wear, accurate colours. Clean image: no text, no letters, no labels, no logos, no brand marks, no watermarks.
```

### O-P02 · Стакан в подстаканнике (кадр 1) · А

- **Рефы:** без рефов.
- **Файл:** `O-P02_podstakannik_1.png`

```text
Object: a faceted clear tea glass in an ornate nickel-silver tea-glass holder (podstakannik) with a curved handle and a simple geometric relief pattern, no emblems; the glass is two-thirds full of amber tea with a teaspoon in it.

Product reference sheet for a live-action TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same glass in its holder on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view, handle on the right; top-right — back view, handle on the left; bottom-left — side view with the handle facing the camera; bottom-right — three-quarter view from slightly above. Photographed like a real product shot: true-to-life materials with real wear, accurate colours. Clean image: no text, no letters, no labels, no logos, no brand marks, no watermarks.
```

### O-P03 · Противень с пирожками и прихватки (кадр 4) · А

- **Рефы:** без рефов.
- **Файл:** `O-P03_pirozhki_1.png`
- **Что изменилось с v1:** небесные прихватки.

```text
Object: a dark metal baking tray with twelve golden, glossy, freshly baked Russian pirozhki in neat rows, a light dusting of flour on the tray rim, and a pair of sky-blue quilted oven mitts (#66A3FF).

Product reference sheet for a live-action TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same set on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — the tray seen from directly above with the mitts beside it; top-right — the tray from the front at eye level; bottom-left — the tray from the side; bottom-right — the tray held in both oven mitts, three-quarter view. Photographed like a real product shot: true-to-life materials with real wear, accurate colours. Clean image: no text, no letters, no labels, no logos, no brand marks, no watermarks.
```

### O-P04 · Наушники подростка (кадр 3) · А

- **Рефы:** без рефов.
- **Файл:** `O-P04_naushniki_1.png`
- **Что изменилось с v1:** белые вместо чёрных.

```text
Object: large matte-white over-ear headphones with soft light-grey cushions and a plain padded headband, no logos anywhere.

Product reference sheet for a live-action TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same headphones on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view; top-right — back view; bottom-left — side view; bottom-right — three-quarter view from slightly above. Photographed like a real product shot: true-to-life materials with real wear, accurate colours. Clean image: no text, no letters, no labels, no logos, no brand marks, no watermarks.
```

### O-P05 · Настольный звонок консьержа (кадр 5) · А

- **Рефы:** без рефов.
- **Файл:** `O-P05_zvonok_1.png`

```text
Object: a classic chrome desk call bell with a polished dome and a small plunger on top, on a round black base.

Product reference sheet for a live-action TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same bell on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view; top-right — back view; bottom-left — side view; bottom-right — three-quarter view from slightly above. Photographed like a real product shot: true-to-life materials with real wear, accurate colours. Clean image: no text, no letters, no labels, no logos, no brand marks, no watermarks.
```

### O-P06 · Ковёр (кадр 6) · А

- **Рефы:** без рефов.
- **Файл:** `O-P06_kovyor_1.png`
- **Что изменилось с v1:** орнамент в синих тонах палитры вместо бордового.

```text
Object: a wool carpet about 2 × 3 m with a traditional ornamental pattern in cornflower blue, azure, pale ice blue and cream, fringed short ends, a little worn.

Product reference sheet for a live-action TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid), every cell on a seamless neutral mid-grey studio backdrop with soft even studio light and a soft contact shadow: top-left — the carpet laid flat, seen from directly above; top-right — the carpet rolled up; bottom-left — the carpet folded in half; bottom-right — the carpet lying flat, three-quarter view at eye level. Photographed like a real product shot: true-to-life materials, accurate colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-P07 · Выбивалка для ковра (кадр 6) · А

- **Рефы:** без рефов.
- **Файл:** `O-P07_vybivalka_1.png`

```text
Object: a traditional carpet beater about 70 cm long, made of twisted rattan, with a looped pretzel-shaped head and a handle wrapped in rattan strips.

Product reference sheet for a live-action TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same carpet beater on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view; top-right — back view; bottom-left — side view; bottom-right — three-quarter view from slightly above. Photographed like a real product shot: true-to-life materials with real wear, accurate colours. Clean image: no text, no letters, no labels, no logos, no brand marks, no watermarks.
```

### O-P08 · Варежки на резинке (кадр 7) · А

- **Рефы:** без рефов.
- **Файл:** `O-P08_varezhki_1.png`
- **Что изменилось с v1:** белые с васильковым узором и лаймовые.

```text
Object: two pairs of children's knitted mittens, each pair joined by a long knitted string: one pair white with a cornflower-blue snowflake pattern (#0F7DF5), the other plain lime (#ADFC30); a few snowflakes stuck to the wool.

Product reference sheet for a live-action TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid), every cell on a seamless neutral mid-grey studio backdrop with soft even studio light and a soft contact shadow: top-left — both pairs laid flat, palms down; top-right — both pairs laid flat, palms up; bottom-left — one mitten from the side; bottom-right — both pairs hanging by their strings, three-quarter view. Photographed like a real product shot: true-to-life materials, accurate colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

### O-P09 · Пакеты с продуктами (кадр 9) · А

- **Рефы:** без рефов.
- **Файл:** `O-P09_pakety_1.png`
- **Что изменилось с v1:** одна сумка васильковая.

```text
Object: two full canvas tote bags with no prints: a natural one with a long baguette and green leeks sticking out, and a cornflower-blue one (#0F7DF5) with red apples and a glass bottle of milk on top.

Product reference sheet for a live-action TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same two bags side by side on a studio floor on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view; top-right — back view; bottom-left — side view; bottom-right — three-quarter view from slightly above. Photographed like a real product shot: true-to-life materials with real wear, accurate colours. Clean image: no text, no letters, no labels, no logos, no brand marks, no watermarks.
```

### O-P10 · Спицы с вязанием (A1) · Б

- **Рефы:** без рефов.
- **Файл:** `O-P10_spitsy_1.png`
- **Что изменилось с v1:** бледно-голубая пряжа.

```text
Object: two long wooden knitting needles holding a half-finished piece of pale ice-blue wool knitting (#DAEEFC), with a ball of the same yarn attached.

Product reference sheet for a live-action TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same knitting on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — front view; top-right — back view; bottom-left — side view; bottom-right — three-quarter view from slightly above. Photographed like a real product shot: true-to-life materials with real wear, accurate colours. Clean image: no text, no letters, no labels, no logos, no brand marks, no watermarks.
```

### O-P11 · Лыжи и палки (A2) · Б

- **Рефы:** без рефов.
- **Файл:** `O-P11_lyzhi_1.png`
- **Что изменилось с v1:** васильковые крепления.

```text
Object: a pair of classic cross-country skis in a natural varnished wood finish with cornflower-blue bindings (#0F7DF5), and a pair of light-grey ski poles with leather wrist straps and small round baskets; no logos or graphics.

Product reference sheet for a live-action TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid). In every cell the same skis and poles on a seamless neutral mid-grey studio backdrop, soft even studio light, a soft contact shadow, centred and fully visible at the same scale: top-left — skis and poles lying flat, seen from above; top-right — the underside of the skis; bottom-left — side view, skis standing upright with the poles beside them; bottom-right — three-quarter view, skis and poles leaning crossed. Photographed like a real product shot: true-to-life materials with real wear, accurate colours. Clean image: no text, no letters, no labels, no logos, no brand marks, no watermarks.
```

### O-P12 · Скрипка и пюпитр (A3) · Б

- **Рефы:** без рефов.
- **Файл:** `O-P12_skripka_1.png`
- **Что изменилось с v1:** светло-серый пюпитр, лазурная папка.

```text
Object: a warm-brown student violin with its bow, and a light-grey folding music stand holding a closed azure music folder (#1A45D5).

Product reference sheet for a live-action TV commercial, 16:9 landscape, split into four equal cells by thin white lines (a 2×2 grid), every cell on a seamless neutral mid-grey studio backdrop with soft even studio light and a soft contact shadow: top-left — the violin, front view, with the bow beside it; top-right — the violin, back view; bottom-left — the violin, side view; bottom-right — the music stand with the folder, three-quarter view. Photographed like a real product shot: true-to-life materials, accurate colours. Clean image: no text, no letters, no labels, no logos, no watermarks.
```

---

## 5. Локации (пустые фоны, без людей)

Эти фоны станут референсом окружения для раскадровки и Seedance. **Дома точно как на рендерах «Зарядья», только зимой и вечером.** Порядок: сначала O-L01 (разрез), потом O-L02 с ним в рефах.

### O-L01 · Дом в разрезе — «кукольный домик» (кадры 1–5) · А

- **Рефы** (строго в этом порядке):
  1. REF-ZR-A
  2. REF-STYLE-A — стилевой референс, только цвет и свет
- **Файл:** `O-L01_razrez_doma_1.png`
- **Что изменилось с v1:** у каждой комнаты свой цвет из палитры вместо «тёплого» однотона.

```text
Image 2 is a colour-and-light reference only: match its colour grade, warmth, contrast, light quality and film texture; take nothing else from it — no people, objects, rooms, season, weather or composition; everything in the frame comes from the text and the other references.

Image 1 shows the residential quarter; use only the facade of the white-brick tower with graphite vertical bands for the outer edges of the building.

Photorealistic architectural cut-away of a modern residential tower at winter blue hour, like a dollhouse with the whole front wall removed, portrait orientation 2:3, viewed perfectly straight on with a long lens, no perspective distortion, an empty scene with no people. Thick, deep-black section cuts of walls and floor slabs divide the building into rooms of equal height. Top floor, left: a cosy living room with pale ice-blue walls (#DAEEFC) — a caramel-brown leather armchair, a warm floor lamp, bookshelves, framed family photos, a small spruce with warm lights and baubles in blue and lime, oak parquet. Top floor, right: a nursery with sky-blue walls (#66A3FF), a white crib and a warm night lamp. One floor down, right: a teenager's room with azure walls (#1A45D5), a desk with a glowing monitor and a lime desk lamp (#ADFC30). Below that, right: a kitchen with white cabinets, an oak worktop, a cornflower-blue tiled backsplash (#0F7DF5) and a warm pendant lamp. Ground floor: a lobby with a pale stone floor, an oak concierge desk, a pale ice-blue wall and glass entrance doors on the right. The remaining rooms on the left are lived-in flats with warm light and walls in light, calm colours. Every room has one normal-size window in its back wall — black frame, white sill — with the snowy deep-blue evening outside. Warm interior light, deep true blacks in the cuts, gentle highlight roll-off, fine film grain. Clean image: no text, no letters, no numbers, no logos.
```

**Проверить:**
- ❗ срезы стен и перекрытий густо-чёрные и толстые: это наши швы
- ❗ людей нет
- окна обычного размера, не панорамные
- комнаты разного цвета из палитры, без оранжевого «супа»

### O-L02 · Гостиная дедушки (кадры 1, 11) · А

- **Рефы** (строго в этом порядке):
  1. O-L01 (утверждённый разрез)
  2. REF-STYLE-E — стилевой референс, только цвет и свет
- **Файл:** `O-L02_gostinaya_1.png`
- **Что изменилось с v1:** бледно-голубые стены.

```text
Image 2 is a colour-and-light reference only: match its colour grade, warmth, contrast, light quality and film texture; take nothing else from it — no people, objects, rooms, season, weather or composition; everything in the frame comes from the text and the other references.

Image 1 is the cut-away of the building; this is its top-floor living room on the left — keep the furniture and the colours exactly.

Photorealistic location plate for a live-action TV commercial, 16:9 landscape, an empty scene with no people.

The cosy top-floor living room seen strictly frontally and planimetrically through the removed front wall, at the eye height of a seated person: in the centre the caramel-brown leather armchair facing the camera, a small side table with a lace doily, a warm floor lamp just behind the armchair on the left, bookshelves and a wall of framed family photos, a small spruce with warm lights and blue and lime baubles in the corner, oak parquet, pale ice-blue walls (#DAEEFC); in the back wall a normal-size window with a black frame and a white sill, the snowy deep-blue evening outside. The thick black cut of the wall frames the right edge of the shot.

It is a real film frame, shot on an ARRI Alexa 35 with Cooke prime lenses and graded like a modern premium Russian TV commercial: photographic and alive, natural exposure, gentle highlight roll-off, deep but not crushed blacks, fine film grain, shallow depth of field with a soft but recognisable background, foreground layers where natural. Colour grade: warm, natural and gently contrasted — a creamy off-white and beige base with one or two saturated accents, crisp light-and-shadow shapes from the real light source falling on walls and faces, soft highlights with nothing clipped, deep shadows, real lived-in detail. Warm lamps inside, the deep-blue snowy evening in the window; balanced colour, never orange-brown; 40 mm lens look, level horizon. Clean image: no text, no letters, no numbers, no logos, no signs.
```

### O-L03 · Двор зимним вечером (кадры 6–8) · А

- **Рефы** (строго в этом порядке):
  1. REF-ZR-B
  2. REF-ZR-C
- **Файл:** `O-L03_dvor_1.png`
- **Что изменилось с v1:** ёлка с синими и лаймовыми шарами, небесные санки.

```text
Image 1 shows the buildings at ground level and image 2 the whole quarter from above; keep the architecture exactly, but turn it into a winter evening.

Photorealistic location plate for a live-action TV commercial, 16:9 landscape, an empty scene with no people.

An eye-level view across the car-free inner courtyard: the sports court lies under smooth untouched snow; the playground with curved wooden structures under snow caps, its shade sails taken down for winter; cleared paving paths lined with neat snowbanks; a spruce in the yard with warm lights and blue and lime baubles; a sky-blue sled by a bench; warm street lamps; behind, the towers from the references — brown-red brick with white window surrounds, beige-sand brick with black slatted boxes, white brick with graphite vertical bands — their normal-size windows glowing warm, and the black steel pergola with a glass roof by one of the entrances. No cars in the yard.

It is a real film frame, shot on an ARRI Alexa 35 with Cooke prime lenses and graded like a modern premium Russian TV commercial: photographic and alive, natural exposure, gentle highlight roll-off, deep but not crushed blacks, fine film grain, shallow depth of field with a soft but recognisable background, foreground layers where natural. Colour grade: warm, natural and gently contrasted — a creamy off-white and beige base with one or two saturated accents, crisp light-and-shadow shapes from the real light source falling on walls and faces, soft highlights with nothing clipped, deep shadows, real lived-in detail. Winter blue hour just after sunset: a deep-blue sky, blue snow, warm 3000 K windows and lamps, gentle snowfall; 35 mm lens look, about 47° horizontal field of view, level horizon. Clean image: no text, no letters, no numbers, no logos, no signs.
```

**Проверить:**
- ❗ ни машин, ни людей, ни льда для катания

### O-L04 · Деревянный мост вечером (кадры 9, 12) · А

- **Рефы** (строго в этом порядке):
  1. REF-ZR-A
- **Файл:** `O-L04_most_1.png`

```text
Image 1 shows the wooden pedestrian bridge and the towers behind it; keep the architecture exactly, but turn it into a winter evening.

Photorealistic location plate for a live-action TV commercial, 16:9 landscape, an empty scene with no people.

The wooden pedestrian bridge with tall vertical timber slats of different heights on both sides and a plank deck with a thin layer of fresh snow, small warm lamps set low along the railing, looking along the bridge towards the towers — beige-sand brick with black slatted boxes and white brick with graphite vertical bands — their normal-size windows glowing warm.

It is a real film frame, shot on an ARRI Alexa 35 with Cooke prime lenses and graded like a modern premium Russian TV commercial: photographic and alive, natural exposure, gentle highlight roll-off, deep but not crushed blacks, fine film grain, shallow depth of field with a soft but recognisable background, foreground layers where natural. Colour grade: warm, natural and gently contrasted — a creamy off-white and beige base with one or two saturated accents, crisp light-and-shadow shapes from the real light source falling on walls and faces, soft highlights with nothing clipped, deep shadows, real lived-in detail. Winter blue hour just after sunset: a deep-blue sky, blue snow, warm 3000 K windows and lamps, gentle snowfall; 35 mm lens look, about 47° horizontal field of view, level horizon. Clean image: no text, no letters, no numbers, no logos, no signs.
```

### O-L05 · Белая башня снизу (кадр 10) · А

- **Рефы** (строго в этом порядке):
  1. REF-ZR-A
  2. REF-ZR-B
- **Файл:** `O-L05_bashnya_snizu_1.png`

```text
Images 1 and 2 show the quarter; this is the white-brick tower with graphite vertical bands — keep its facade exactly, in winter at blue hour.

Photorealistic location plate for a live-action TV commercial, 16:9 landscape, an empty scene with no people.

A worm's-eye view from the snowy ground at the very foot of the white-brick tower, an ultra-wide lens about 84° horizontal field of view, looking straight up the facade, which converges dramatically towards the deep-blue sky; the windows of the lower half glow warm, the upper floors are still dark; snowflakes fly towards the lens.

It is a real film frame, shot on an ARRI Alexa 35 with Cooke prime lenses and graded like a modern premium Russian TV commercial: photographic and alive, natural exposure, gentle highlight roll-off, deep but not crushed blacks, fine film grain, shallow depth of field with a soft but recognisable background, foreground layers where natural. Colour grade: warm, natural and gently contrasted — a creamy off-white and beige base with one or two saturated accents, crisp light-and-shadow shapes from the real light source falling on walls and faces, soft highlights with nothing clipped, deep shadows, real lived-in detail. Winter blue hour, deep-blue sky, warm windows. Clean image: no text, no letters, no numbers, no logos, no signs.
```

---

## 6. Раскадровка

Только из утверждённых листов. Каждый лист раскадровки — 4 кадра 2×2. Пэкшот (O-SB4) — один большой кадр.

Общее для всех кадров:
- камера едет **вправо и вниз** по дому, во дворе вправо;
- лица читаются, контровой свет рисует силуэт;
- лайм — самый яркий акцент на бабочке дедушки.

### O-SB1 · Кадры 1–4 · А

- **Рефы** (строго в этом порядке):
  1. лист дедушки O-K01
  2. O-L02 гостиная
  3. O-K02 мама
  4. O-K04 хозяйка
  5. O-P03 пирожки
  6. O-L01 разрез
  7. REF-STYLE-A — стилевой референс, только цвет и свет
- **Файл:** `O-SB1_kadry_01-04_1.png`
- Подросток описан словами.

```text
Image 7 is a colour-and-light reference only: match its colour grade, warmth, contrast, light quality and film texture; take nothing else from it — no people, objects, rooms, season, weather or composition; everything in the frame comes from the text and the other references.

References: image 1 — the grandfather (keep him exactly, with his lime bow tie and azure cardigan); image 2 — his living room; image 3 — the young mother with the baby; image 4 — the woman in the striped apron; image 5 — her tray of pirozhki and oven mitts; image 6 — the cut-away of the whole building, showing where each room is.

Storyboard sheet: four film stills from the same live-action TV commercial in a 2×2 grid, each still 16:9, separated by thin white gutters, with a small white label in the top-left corner of each still (1, 2, 3, 4) and no other text.

Each still is a real film frame, shot on an ARRI Alexa 35 with Cooke prime lenses and graded like a modern premium Russian TV commercial: photographic and alive, natural exposure, gentle highlight roll-off, deep but not crushed blacks, fine film grain, shallow depth of field with a soft but recognisable background, foreground layers where natural. Colour grade: warm, natural and gently contrasted — a creamy off-white and beige base with one or two saturated accents, crisp light-and-shadow shapes from the real light source falling on walls and faces, soft highlights with nothing clipped, deep shadows, real lived-in detail. Interiors: lived-in flats seen straight on like a dollhouse with the front wall removed; warm lamps in the room and the deep-blue evening in the window behind; a warm practical light behind or beside each person draws a rim on the hair, soft light from the front keeps the face readable; the cut walls and floor slabs are thick and deep black. Colour: the evening blue and the brand blues in clothes and interiors — cornflower #0F7DF5, azure #1A45D5, sky blue #66A3FF, pale ice blue #DAEEFC — against warm lamplight, with lime #ADFC30 only as small bright accents, the brightest being the grandfather's bow tie; nobody wears black.

People are real, characterful and unglamorous, with natural skin texture; each face is caught in the middle of one small reaction, described below by what the brows, eyes and mouth do — never a posed expression; the eyes react first, the mouth follows; smiles are closed-lip and small unless stated; nobody looks into the lens unless stated; people around react out of sync, not together.

1 — The living room from image 2, strictly frontal like a dollhouse, a medium shot, 40 mm lens look, his face about a third of the frame height: the grandfather from image 1 sits upright in the caramel leather armchair, a glass of tea in a metal holder on the side table; chin slightly lifted, a steady solemn gaze just below the camera as if at a TV; his lips press into a straight line under the moustache; he claps slowly and evenly; no smile. The floor lamp behind his shoulder draws a warm rim on his white hair; soft light from the TV in front keeps his face readable.

2 — Same floor, the next flat to the right: the left edge of the frame is a thick black band — the cut of the wall between the flats. The sky-blue nursery: the young mother from image 3 rocks the sleeping baby in the sling; hearing the clapping through the wall, she glances at the wall — a beat later the corners of her mouth lift a little, lips closed — and taps two fingers into her palm without a sound; the baby sleeps on. The night lamp beside her warms her hair; her face is softly lit.

3 — One floor down: the top edge of the frame is a thick black band — the cut of the floor slab. The azure teenager's room with a lime desk lamp: a lanky boy of about fifteen with messy dark-blond hair, in a cornflower-blue hoodie and big white over-ear headphones with one ear cup slid off, sits at his desk; eyes still on the monitor, he gives two dry claps; a perfectly flat face, nothing moves but his hands. The monitor lights his face from the front, the lime lamp rims his hair.

4 — Another floor down, a black slab band at the top: the white kitchen with the cornflower-blue tiles; the woman from image 4 holds the tray from image 5 in her sky-blue oven mitts, sets it down and claps the mitts together; a small puff of flour glitters in the light of the pendant lamp; she presses her lips together to hold back a proud smile, and the corners lift anyway.
```

**Проверить:**
- ❗ дедушка не улыбается, торжественный
- ❗ комнаты разных цветов палитры, не оранжевые

### O-SB2 · Кадры 5–8 · А

- **Рефы** (строго в этом порядке):
  1. O-K05 консьерж
  2. O-L01 разрез
  3. O-K06 мужчина с выбивалкой
  4. O-P06 ковёр
  5. O-L03 двор
  6. O-K09 пёс
  7. REF-STYLE-A — стилевой референс, только цвет и свет
- **Файл:** `O-SB2_kadry_05-08_1.png`
- Дети описаны словами.

```text
Image 7 is a colour-and-light reference only: match its colour grade, warmth, contrast, light quality and film texture; take nothing else from it — no people, objects, rooms, season, weather or composition; everything in the frame comes from the text and the other references.

References: image 1 — the concierge; image 2 — the cut-away of the building (its ground-floor lobby); image 3 — the man with the carpet beater; image 4 — the carpet; image 5 — the courtyard; image 6 — the dog.

Storyboard sheet: four film stills from the same live-action TV commercial in a 2×2 grid, each still 16:9, separated by thin white gutters, with a small white label in the top-left corner of each still (5, 6, 7, 8) and no other text.

Each still is a real film frame, shot on an ARRI Alexa 35 with Cooke prime lenses and graded like a modern premium Russian TV commercial: photographic and alive, natural exposure, gentle highlight roll-off, deep but not crushed blacks, fine film grain, shallow depth of field with a soft but recognisable background, foreground layers where natural. Colour grade: warm, natural and gently contrasted — a creamy off-white and beige base with one or two saturated accents, crisp light-and-shadow shapes from the real light source falling on walls and faces, soft highlights with nothing clipped, deep shadows, real lived-in detail. Interiors: lived-in flats seen straight on like a dollhouse with the front wall removed; warm lamps in the room and the deep-blue evening in the window behind; a warm practical light behind or beside each person draws a rim on the hair, soft light from the front keeps the face readable; the cut walls and floor slabs are thick and deep black. Exteriors: winter blue hour just after sunset — a deep-blue sky and blue snow, warm 3000 K windows, lamps and street lights, gentle snowfall; warm lights behind and beside people draw a rim on hair and shoulders, while soft light from the front keeps every face readable. Colour: the evening blue and the brand blues in clothes and interiors — cornflower #0F7DF5, azure #1A45D5, sky blue #66A3FF, pale ice blue #DAEEFC — against warm lamplight, with lime #ADFC30 only as small bright accents, the brightest being the grandfather's bow tie; nobody wears black.

People are real, characterful and unglamorous, with natural skin texture; each face is caught in the middle of one small reaction, described below by what the brows, eyes and mouth do — never a posed expression; the eyes react first, the mouth follows; smiles are closed-lip and small unless stated; nobody looks into the lens unless stated; people around react out of sync, not together.

5 — The ground-floor lobby from image 2 seen frontally, 40 mm lens look: the concierge from image 1 in her azure cardigan, behind the oak desk, taps a chrome desk bell twice and gives one short approving nod, lips pressed, eyes warm; through the glass entrance doors behind her, the blue winter courtyard. The right edge of the frame is a dark blurred band — the cut of the facade wall right at the lens.

6 — The car-free courtyard from image 5 at blue hour, 35 mm lens look: the man from image 3 — open cornflower-blue puffer, oatmeal sweater, grey felt boots — beats the blue-patterned carpet from image 4, laid flat on the snow, with his rattan carpet beater; snow dust rises and glitters in the warm lamp light behind him; behind, the snowy playground and towers with warm windows. A lamp in front keeps his face readable: focused, eyes on the carpet, a satisfied half-smile just appearing at one corner of his mouth.

7 — At a child's eye height in the same courtyard, 50 mm lens look: two children of about seven face the camera and clap their mittens — a girl in a sky-blue snowsuit and a white hat with a lime pompom, with freckles and a missing front tooth, laughing for real, eyes crinkled almost shut; a boy in a cornflower-blue snowsuit, a pale ice-blue hat and lime mittens, a beat behind her, grinning shyly — the biggest emotion of the film; snow bursts off the mittens like confetti in the lamp light.

8 — A ground-level insert, 85 mm lens look: the dog from image 6 in its lime collar sits on the snow, its plumed tail sweeping the snow from side to side like a wiper; snow sparkles in the lamplight behind it.
```

### O-SB3 · Кадры 9, 9б, 10, 11 · А

- **Рефы** (строго в этом порядке):
  1. O-L04 мост
  2. O-K10 молодой мужчина
  3. O-K11 молодая женщина
  4. лист козы N-K01 v2 из «Новосёла»
  5. O-L05 башня снизу
  6. лист дедушки O-K01
  7. REF-STYLE-C — стилевой референс, только цвет и свет
- **Файл:** `O-SB3_kadry_09-11_1.png`
- Если лист козы v2 из «Новосёла» ещё не утверждён, сделай этот лист позже.

```text
Image 7 is a colour-and-light reference only: match its colour grade, warmth, contrast, light quality and film texture; take nothing else from it — no people, objects, rooms, season, weather or composition; everything in the frame comes from the text and the other references.

References: image 1 — the wooden bridge; image 2 — the young man with grocery bags; image 3 — the young woman; image 4 — the white goat character from our previous film (keep her exactly: tall and slender, blue aviator sunglasses, lime scarf); image 5 — the white-brick tower from below; image 6 — the grandfather (keep him exactly, with his lime bow tie and azure cardigan).

Storyboard sheet: four film stills from the same live-action TV commercial in a 2×2 grid, each still 16:9, separated by thin white gutters, with a small white label in the top-left corner of each still (9, 9b, 10, 11) and no other text.

Each still is a real film frame, shot on an ARRI Alexa 35 with Cooke prime lenses and graded like a modern premium Russian TV commercial: photographic and alive, natural exposure, gentle highlight roll-off, deep but not crushed blacks, fine film grain, shallow depth of field with a soft but recognisable background, foreground layers where natural. Colour grade: warm, natural and gently contrasted — a creamy off-white and beige base with one or two saturated accents, crisp light-and-shadow shapes from the real light source falling on walls and faces, soft highlights with nothing clipped, deep shadows, real lived-in detail. Interiors: lived-in flats seen straight on like a dollhouse with the front wall removed; warm lamps in the room and the deep-blue evening in the window behind; a warm practical light behind or beside each person draws a rim on the hair, soft light from the front keeps the face readable; the cut walls and floor slabs are thick and deep black. Exteriors: winter blue hour just after sunset — a deep-blue sky and blue snow, warm 3000 K windows, lamps and street lights, gentle snowfall; warm lights behind and beside people draw a rim on hair and shoulders, while soft light from the front keeps every face readable. Colour: the evening blue and the brand blues in clothes and interiors — cornflower #0F7DF5, azure #1A45D5, sky blue #66A3FF, pale ice blue #DAEEFC — against warm lamplight, with lime #ADFC30 only as small bright accents, the brightest being the grandfather's bow tie; nobody wears black.

People are real, characterful and unglamorous, with natural skin texture; each face is caught in the middle of one small reaction, described below by what the brows, eyes and mouth do — never a posed expression; the eyes react first, the mouth follows; smiles are closed-lip and small unless stated; nobody looks into the lens unless stated; people around react out of sync, not together.

9 — The wooden bridge from image 1, tall timber slats blurred in the foreground, 50 mm lens look: the young couple from images 2 and 3 have stopped; she — pale ice-blue coat, cornflower-blue scarf — claps in her mittens and laughs into her scarf, eyes crinkling; he — azure parka, sky-blue beanie — hands full with two grocery bags, taps the bags together, one eyebrow up, amused. Small warm lamps low along the railing light their faces softly from the front; the windows behind glow warm.

9b — The same shot, and at the far end of the bridge the tall, slender white goat from image 4 — blue aviator sunglasses, lime knitted scarf — claps her front hooves.

10 — A worm's-eye view from the snowy ground at the foot of the tower from image 5, ultra-wide lens: its windows are lighting up one by one, floor after floor upward, the wave of warm light nearly at the top; snowflakes fly towards the lens; deep-blue sky.

11 — The grandfather's living room again, strictly frontal: the grandfather from image 6 now stands, straightening his lime bow tie in the middle of a final clap, chin lifting a little, with one small dignified nod straight into the lens; warmth in the eyes, the mouth stays still, no smile. The floor lamp rims his hair, soft light keeps his face readable, the snowy blue window behind him.
```

**Проверить:**
- ❗ кадр 11: дедушка стоит, кивает в объектив, без улыбки

### O-SB4 · Кадр 12, пэкшот · А

- **Рефы** (строго в этом порядке):
  1. O-L04 мост
  2. REF-ZR-A
  3. REF-ZR-C
- **Файл:** `O-SB4_kadr_12_pekshot_1.png`

```text
References: image 1 — the wooden bridge at winter blue hour; image 2 — the bridge and the towers in the original render; image 3 — the whole quarter from above. Keep the architecture exactly.

A single film still — the final shot of a live-action TV commercial, 16:9 landscape.

It is a real film frame, shot on an ARRI Alexa 35 with Cooke prime lenses and graded like a modern premium Russian TV commercial: photographic and alive, natural exposure, gentle highlight roll-off, deep but not crushed blacks, fine film grain, shallow depth of field with a soft but recognisable background, foreground layers where natural. Colour grade: warm, natural and gently contrasted — a creamy off-white and beige base with one or two saturated accents, crisp light-and-shadow shapes from the real light source falling on walls and faces, soft highlights with nothing clipped, deep shadows, real lived-in detail. Exteriors: winter blue hour just after sunset — a deep-blue sky and blue snow, warm 3000 K windows, lamps and street lights, gentle snowfall; warm lights behind and beside people draw a rim on hair and shoulders, while soft light from the front keeps every face readable. Colour: the evening blue and the brand blues in clothes and interiors — cornflower #0F7DF5, azure #1A45D5, sky blue #66A3FF, pale ice blue #DAEEFC — against warm lamplight, with lime #ADFC30 only as small bright accents, the brightest being the grandfather's bow tie; nobody wears black.

People are real, characterful and unglamorous, with natural skin texture; each face is caught in the middle of one small reaction, described below by what the brows, eyes and mouth do — never a posed expression; the eyes react first, the mouth follows; smiles are closed-lip and small unless stated; nobody looks into the lens unless stated; people around react out of sync, not together.

A wide view from the wooden bridge at winter blue hour, 40 mm lens look: the tall timber slats lead the eye to the right, where the towers of the quarter — the white-brick tower with graphite vertical bands and its beige-sand brick neighbour — stand in the right half of the frame with warm glowing windows; far below, tiny figures of residents in bright blue snowsuits and coats in the snowy courtyard; gentle snowfall. The left half of the frame is a calm, empty deep-blue evening sky above dark snow-covered park trees, with nothing in it. Clean image: no text, no letters, no logos.
```

**Проверить:**
- ❗ дома в правой половине; левая половина — пустое небо под титры

### O-SB5 · Запасные варианты A1–A4 · Б

- **Рефы** (строго в этом порядке):
  1. O-K12 бабушка
  2. O-P10 спицы
  3. O-K13 лыжник
  4. O-P11 лыжи
  5. O-K15 кот
  6. O-L01 разрез
  7. REF-STYLE-A — стилевой референс, только цвет и свет
- **Файл:** `O-SB5_varianty_A1-A4_1.png`
- Девочка описана словами.

```text
Image 7 is a colour-and-light reference only: match its colour grade, warmth, contrast, light quality and film texture; take nothing else from it — no people, objects, rooms, season, weather or composition; everything in the frame comes from the text and the other references.

References: image 1 — the grandmother; image 2 — her knitting; image 3 — the skier; image 4 — his skis and poles; image 5 — the cat; image 6 — the cut-away of the building, for the look of the rooms.

Storyboard sheet: four film stills from the same live-action TV commercial in a 2×2 grid, each still 16:9, separated by thin white gutters, with a small white label in the top-left corner of each still (A1, A2, A3, A4) and no other text.

Each still is a real film frame, shot on an ARRI Alexa 35 with Cooke prime lenses and graded like a modern premium Russian TV commercial: photographic and alive, natural exposure, gentle highlight roll-off, deep but not crushed blacks, fine film grain, shallow depth of field with a soft but recognisable background, foreground layers where natural. Colour grade: warm, natural and gently contrasted — a creamy off-white and beige base with one or two saturated accents, crisp light-and-shadow shapes from the real light source falling on walls and faces, soft highlights with nothing clipped, deep shadows, real lived-in detail. Interiors: lived-in flats seen straight on like a dollhouse with the front wall removed; warm lamps in the room and the deep-blue evening in the window behind; a warm practical light behind or beside each person draws a rim on the hair, soft light from the front keeps the face readable; the cut walls and floor slabs are thick and deep black. Exteriors: winter blue hour just after sunset — a deep-blue sky and blue snow, warm 3000 K windows, lamps and street lights, gentle snowfall; warm lights behind and beside people draw a rim on hair and shoulders, while soft light from the front keeps every face readable. Colour: the evening blue and the brand blues in clothes and interiors — cornflower #0F7DF5, azure #1A45D5, sky blue #66A3FF, pale ice blue #DAEEFC — against warm lamplight, with lime #ADFC30 only as small bright accents, the brightest being the grandfather's bow tie; nobody wears black.

People are real, characterful and unglamorous, with natural skin texture; each face is caught in the middle of one small reaction, described below by what the brows, eyes and mouth do — never a posed expression; the eyes react first, the mouth follows; smiles are closed-lip and small unless stated; nobody looks into the lens unless stated; people around react out of sync, not together.

A1 — A cosy room of the building from image 6 seen frontally like a dollhouse, a thick black slab band along the top edge, 40 mm lens look: the grandmother from image 1 in an armchair taps her knitting needles from image 2 together like applause, peering over her glasses with a faint mischievous look. A lamp beside her rims her silver hair.

A2 — The snowy park of the quarter, a ski track between birches, warm park lamps, 50 mm lens look: the skier from image 3 has stopped on his skis from image 4 and taps his ski poles together above his head, grinning. A lamp lights his face softly from the front.

A3 — A small room of the same building, seen frontally, 50 mm lens look: a girl of about nine with two neat braids, in an azure dress over a white turtleneck, stands at a light-grey music stand and plays a short solemn fanfare on a violin, eyes shut with concentration. A warm desk lamp lights her face from the front.

A4 — A windowsill with the snowy blue evening outside, 85 mm lens look: the cat from image 5 lies on the sill with half-closed eyes, its tail thumping the sill in rhythm. Warm room light on its face from the front.
```

---

## 7. После раскадровки

Следующий этап — ключевые кадры (по одному на план) и промпты Seedance 2.0 для «Виви». Это делаем отдельно, после того как дизайнер утвердит раскадровку и выберет варианты.
