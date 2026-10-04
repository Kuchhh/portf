"""«Новосёл» (коза, Суворов-Сити 2): спецификация промптов для ChatGPT, v2 (04.10.2026).

Сборка: python3 video-projects/_kit/build_prompts.py
"""
from build_prompts import (FILM_SINGLE, animal_layout, board_text, person_layout, plate_text, prop_layout,
                           prop_layout_free, single_text)
from common_md import instructions, palette_section, photostyle

EXPORT = {"prompts": "Промпты_Развитие_Коза_v3.md", "storyboard": "Сториборд_Развитие_Коза_v3.md"}

# ── Свет и цвет ролика ──
LIGHT_EXT = (
    "Exteriors: a clear frosty winter day; the sun sits to the side and slightly behind the subjects, outlining "
    "hair, fur, breath and the edges of the snow with warm rim light, while faces get soft fill bounced off the "
    "snow and stay fully readable; the snow keeps its texture in the highlights and turns cool blue in the shade."
)
LIGHT_INT = (
    "Interiors: a bright modern lobby and elevator — soft daylight from the glass entrance mixed with "
    "warm-neutral downlights; pale stone, light oak, brushed steel and pale ice-blue plaster; balanced colour, "
    "never orange-brown."
)
PALETTE_EN = (
    "cornflower blue #0F7DF5, azure #1A45D5, sky blue #66A3FF, pale ice blue #DAEEFC and lime #ADFC30; the goat's "
    "lime scarf is the strongest accent; nobody wears black."
)
COLOUR = (
    "Colour: lively and fresh — white snow, blue sky and warm sunlight, with the brand palette carried by clothes "
    "and everyday objects: " + PALETTE_EN
)
COLOUR_INT = (
    "Colour: lively and fresh — pale stone, light oak and pale ice-blue plaster, with the brand palette carried by "
    "clothes and objects: " + PALETTE_EN
)
LOOK_EXT = f"{LIGHT_EXT} {COLOUR}"
LOOK_ALL = f"{LIGHT_EXT} {LIGHT_INT} {COLOUR}"
LOOK_INT = f"{LIGHT_INT} {COLOUR_INT}"
PLATE_EXT = (
    f"{FILM_SINGLE} The sun sits to the side and slightly behind, giving warm rim light to the snow edges and "
    "branches; the snow keeps its texture in the highlights and turns cool blue in the shade; 35 mm lens look, "
    "about 47° horizontal field of view, level horizon."
)
PLATE_INT = (
    f"{FILM_SINGLE} Soft daylight from the glass entrance mixed with warm-neutral downlights; balanced colour, "
    "never orange-brown; 40 mm lens look, about 47° horizontal field of view, level horizon."
)

GOAT = (
    "Character: a photoreal anthropomorphic white she-goat — tall, slender and graceful — who walks upright on "
    "her hind legs with the poise of a fashion model, about 175 cm tall to the top of her head. Long slim legs, "
    "a narrow waist, a long elegant neck, a light, upright posture. A sleek, short, silky pure-white coat that lies "
    "smooth and glossy on her body, only slightly longer and softly feathered on the chest and on the backs of her "
    "legs. A refined, narrow, pretty goat face: long white eyelashes, gentle amber eyes with horizontal pupils, a "
    "soft pinkish-grey nose, a small neat tuft of a beard, slender ears; slim smooth horns, warm ivory with fine "
    "rings, sweeping back from the forehead in one graceful curve. Her front legs work like slender arms and end in "
    "small polished dark-grey cloven hooves; small neat dark hooves on her hind legs; a short white tail. She wears "
    "aviator sunglasses with thin glossy azure-blue metal frames (#1A45D5) and gradient sky-blue lenses (#66A3FF "
    "fading to clear at the bottom), sitting slightly low on her muzzle, and a chunky hand-knitted scarf in vivid "
    "lime green (#ADFC30), thick garter stitch, wrapped twice around her neck — one end hangs down her chest, the "
    "other is thrown over her left shoulder and hangs down her back; both ends have a short fringe. Nothing else on "
    "her. Expression: calm, self-assured, a touch of amusement in the eyes, mouth closed."
)
GOAT_LAYOUT = (
    "Character reference sheet for a live-action TV commercial with a photoreal VFX character, 16:9 landscape. "
    "Layout: the left 45% of the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical "
    "line separates it from the right part, where the same goat stands upright full length twice at the same scale, "
    "with a little space above the horns and below the hooves — front view on the left, back view on the right, "
    "poised like a model, front legs relaxed at her sides. Seamless neutral mid-grey studio backdrop, soft light "
    "from a large softbox, a soft contact shadow under the hooves. Real goat anatomy and real fur detail, as if "
    "photographed — a living animal, not a costume and not a cartoon. Clean image: no text, no letters, no labels, "
    "no logos, no watermarks."
)


def P(id, title, prio, prompt, file, refs=None, checks=None, changed=None, reuse=None, note=None, runs=1):
    return dict(id=id, title=title, prio=prio, prompt=prompt, file=file, refs=refs, checks=checks,
                changed=changed, reuse=reuse, note=note, runs=runs)


def person(desc, who, pose="standing naturally, arms relaxed"):
    return f"{desc}\n\n{person_layout(who, pose)}"


# ── 3. Персонажи ──
CHARACTERS = [
    P("N-K01", "Коза — главный герой", "А", f"{GOAT}\n\n{GOAT_LAYOUT}", "N-K01_koza_1.png", runs=3,
      changed="высокая, стройная, изящная; гладкая короткая шерсть вместо лохматой; очки-авиаторы с лазурной "
              "оправой и голубыми стёклами. Баннер с козой больше не прикладываем: он тянет лохматую козу в "
              "золотых очках.",
      checks=["❗ высокая и стройная, гладкая короткая шерсть — не «йети» и не костюм",
              "❗ очки: тонкая лазурная оправа, голубые стёкла",
              "❗ шарф лаймовый, один конец на груди, второй за спиной",
              "❗ во рту ничего нет",
              "морда изящная и приятная, как у живого животного"]),
    P("N-K01B", "Коза с коробкой", "А",
      "Image 1 is the character sheet of the goat — keep her look exactly. Image 2 is the packed moving box — keep "
      "it exactly.\n\nThe same tall, slender goat carries the packed box from image 2 in front of her chest, holding "
      "it from below with both slender front legs; the potted spruce and the framed photo stick out above the box, "
      "below her chin; her posture stays light and upright, like a model carrying a parcel.\n\n"
      "Character pose sheet for a live-action TV commercial with a photoreal VFX character, 16:9 landscape: three "
      "full-length views of the goat holding the box, side by side at the same scale, separated by thin black "
      "vertical lines — front view on the left, right-side profile in the middle, back view on the right (from "
      "behind we see the edges of the box on both sides of her body, the fringed lime end of her scarf down her back "
      "and her short tail). Seamless neutral mid-grey studio backdrop, soft light from a large softbox, soft contact "
      "shadows. Real goat anatomy and fur, as if photographed. Clean image: no text, no letters, no labels, no logos, "
      "no watermarks.",
      "N-K01B_koza_s_korobkoy_1.png",
      refs=["выбранный лист козы N-K01 (v2)", "лист коробки N-P01 (v2)"],
      note="Делается после N-P01.",
      checks=["❗ коза и коробка совпадают с листами", "со спины видны края коробки и конец шарфа"]),
    P("N-K02", "Мужчина со щёткой (кадр 4)", "А", person(
        "Character: a Russian man of about 35, average build, a short neat dark-brown beard, grey-blue eyes, an "
        "ordinary likeable face with a little winter redness on the cheeks. A sky-blue down parka (#66A3FF) with the "
        "hood down and a light-grey faux-fur trim on the hood, a light-grey knitted beanie, light-wash jeans, tan "
        "suede winter boots, light-grey knitted gloves; in his right hand a car snow brush with a cornflower-blue "
        "handle (#0F7DF5). Expression: calm, a little sleepy — an ordinary weekend morning.", "man"),
      "N-K02_muzhchina_shchetka_1.png", changed="небесная парка вместо тёмно-синей; щётка с васильковой ручкой."),
    P("N-K03", "Мальчик ~6 лет (кадр 6)", "А", person(
        "Character: a boy of about six with round rosy cheeks, a gap-toothed grin and a light-brown fringe peeking "
        "out from under a white knitted hat with a lime pompom (#ADFC30). A cornflower-blue one-piece winter "
        "snowsuit (#0F7DF5), lime knitted mittens on a string, light-grey snow boots. Expression: bursting with "
        "excitement.", "boy"),
      "N-K03_malchik_1.png", note="Ребёнок — только по словам.",
      changed="васильковый комбинезон, лаймовые помпон и варежки."),
    P("N-K04", "Мама ~30 (кадр 6)", "А", person(
        "Character: a Russian woman of about 30 with a soft, friendly face, a few freckles and straight light-brown "
        "shoulder-length hair under a cream knitted hat. A long pale ice-blue down coat (#DAEEFC), a chunky "
        "cornflower-blue knitted scarf (#0F7DF5), light-wash jeans, white winter boots, light-grey knitted gloves. "
        "Expression: calm and attentive.", "woman"),
      "N-K04_mama_1.png", changed="бледно-голубой пуховик, васильковый шарф."),
    P("N-K05", "Дворник (кадр 8)", "А", person(
        "Character: a stocky Russian yard keeper of about 55 with a weathered, wind-reddened face and a grey "
        "moustache. An azure insulated work jacket and matching work trousers (#1A45D5) with fluorescent lime "
        "reflective stripes (#ADFC30) across the chest, sleeves and legs, a grey knitted hat, light-grey work gloves, "
        "sturdy brown work boots. Expression: a stone face — nothing in the world surprises him.", "man"),
      "N-K05_dvornik_1.png", changed="лазурная спецовка с лаймовыми светоотражающими полосами.",
      checks=["❗ спецовка лазурная, полосы лаймовые флуоресцентные"]),
    P("N-K06", "Мужчина ~50 из пары у подъезда (кадр 9)", "А", person(
        "Character: a Russian man of about 52 with a short salt-and-pepper beard and rimless glasses. A light-grey "
        "herringbone wool overcoat, an azure knitted scarf (#1A45D5), a grey tweed flat cap, mid-grey trousers, "
        "brown leather winter boots, tan leather gloves. Expression: polite and composed — a gentleman.", "man"),
      "N-K06_para_muzhchina_1.png", changed="светло-серое пальто в ёлочку, лазурный шарф."),
    P("N-K07", "Женщина ~50 из пары у подъезда (кадр 9)", "А", person(
        "Character: a Russian woman of about 50 with short ash-blonde hair and small pearl earrings. A long camel "
        "wool coat, a sky-blue knitted beret (#66A3FF), a cream cashmere scarf, sky-blue leather gloves, tan heeled "
        "winter boots. Expression: composed, quietly curious.", "woman"),
      "N-K07_para_zhenshchina_1.png", changed="небесные берет и перчатки."),
    P("N-K08", "Парень ~25 с мандаринами (кадры 12–13)", "А", person(
        "Character: a slim Russian man of about 25 with short dark tousled hair, light stubble and an intelligent, "
        "slightly anxious face. A cornflower-blue puffer jacket (#0F7DF5), a light-grey hoodie underneath with the "
        "hood out over the collar, light-wash jeans, white winter sneakers; in his left hand a white cotton string "
        "bag full of tangerines. Expression: slight bewilderment — brows a little raised and drawn together, lips "
        "slightly parted, no smile.", "man"),
      "N-K08_paren_mandariny_1.png",
      changed="васильковый пуховик; эмоция — лёгкое недоумение без улыбки (как у парня в очках на кадре-образце).",
      checks=["❗ не улыбается: брови чуть приподняты и сведены, губы приоткрыты"]),
    P("N-K09", "Мужчина с ёлкой на плече (реакция 1)", "Б", person(
        "Character: a Russian man of about 45 with ruddy cheeks and a short greying beard. An azure padded jacket "
        "(#1A45D5) with a cream shearling collar, an oatmeal knitted hat, light-wash jeans, brown winter boots. A "
        "freshly cut spruce about 180 cm tall, wrapped in white netting, rests on his right shoulder. Expression: "
        "kind, unhurried.", "man", "standing naturally, the tree on his shoulder, a little space above its top"),
      "N-K09_muzhchina_yolka_1.png", changed="лазурная куртка с кремовым воротником."),
    P("N-K10", "Бабушка с термосом (реакция 2)", "Б", person(
        "Character: a small Russian woman of about 75 with a kind round face, deep wrinkles and glasses. A cream "
        "knitted shawl tied over her head, a long sky-blue down coat (#66A3FF), light-grey felt boots; with both "
        "hands she holds the steaming cup-lid of a cornflower-blue thermos (#0F7DF5). Expression: warm and "
        "unhurried.", "woman"),
      "N-K10_babushka_termos_1.png", changed="небесный пуховик, кремовая шаль, васильковый термос."),
    P("N-K11", "Хозяйка собаки (реакция 3)", "Б", person(
        "Character: a Russian woman of about 40 with a dark bob haircut. A long off-white wool coat, a "
        "cornflower-blue knitted snood (#0F7DF5), light-grey gloves, light-wash jeans, white winter boots; in her "
        "right hand a lime dog leash (#ADFC30). Expression: one eyebrow slightly raised — sceptical amusement.",
        "woman"),
      "N-K11_khozyayka_sobaki_1.png", changed="светлое пальто, васильковый снуд, лаймовый поводок."),
    P("N-K12", "Бигль (реакция 3)", "Б",
      "Character: a young beagle with a classic tricolour coat — white legs, chest and muzzle, tan head and ears, a "
      "black saddle on the back — long soft ears, warm brown eyes, wearing a lime harness (#ADFC30).\n\n"
      + animal_layout("beagle", "the head tilted to one side in curiosity",
                      "sitting, front view on the left; standing, left side profile on the right"),
      "N-K12_bigl_1.png", changed="лаймовая шлейка."),
    P("N-K13", "Подросток на качелях (реакция 4)", "Б", person(
        "Character: a lanky boy of about fifteen with a deadpan expression and messy dark hair under a light-grey "
        "beanie. An azure puffer jacket (#1A45D5), light-grey joggers, white winter sneakers, white wireless "
        "earbuds in both ears.", "boy", "standing, hands in pockets"),
      "N-K13_podrostok_1.png", note="Подросток — только по словам.", changed="лазурный пуховик."),
    P("N-K14", "Женщина на балконе с гирляндой (реакция 5)", "Б", person(
        "Character: a Russian woman of about 35 with hair in a messy bun and a few loose strands. A chunky sky-blue "
        "knitted sweater (#66A3FF), cream lounge trousers, grey felt house boots; in her hands a string of "
        "old-fashioned round warm-white bulbs on a cable. Expression: caught mid-task, attentive.", "woman"),
      "N-K14_zhenshchina_balkon_1.png", changed="небесный свитер."),
    P("N-K15", "Девочка у снеговика (реакция 6)", "Б", person(
        "Character: a girl of about six with rosy cheeks and wide curious eyes. A sky-blue one-piece snowsuit "
        "(#66A3FF), a white knitted hat with ear flaps tied under the chin, lime mittens (#ADFC30), white snow "
        "boots. Expression: open-mouthed wonder.", "girl"),
      "N-K15_devochka_snegovik_1.png", note="Ребёнок — только по словам.", changed="небесный комбинезон, лаймовые варежки."),
    P("N-K16", "Мальчик у снеговика (реакция 6)", "Б", person(
        "Character: a boy of about seven with a freckled nose and a serious, absorbed face. A pale ice-blue "
        "snowsuit (#DAEEFC) with cornflower-blue trim (#0F7DF5), a light-grey knitted hat, light-grey mittens, grey "
        "snow boots; in his right mitten a carrot.", "boy"),
      "N-K16_malchik_snegovik_1.png", note="Ребёнок — только по словам.", changed="бледно-голубой комбинезон с васильковой отделкой."),
    P("N-K17", "Мальчик с санками (реакция 7)", "Б", person(
        "Character: a boy of about seven with big round eyes and pink cheeks. An azure one-piece snowsuit (#1A45D5) "
        "with light-grey knee patches, a white knitted hat with a sky-blue stripe and a pompom, a cream knitted "
        "scarf, light-grey mittens, grey snow boots; in his right mitten the end of a sled rope. Expression: frozen "
        "mid-step, staring.", "boy"),
      "N-K17_malchik_sanki_1.png", note="Ребёнок — только по словам.", changed="лазурный комбинезон, белая шапка с небесной полосой."),
]

# ── 4. Предметы ──
PROPS = [
    P("N-P02", "Фото семьи коз в рамке (кадр 7)", "А",
      "Image 1 shows our goat character — the young goat in the photo is her as a child.\n\n"
      "Object: an old-fashioned colour family photo print, slightly faded, in a simple light-oak frame with glass, "
      "about 20 × 25 cm, with a cardboard back and a fold-out stand. The photo shows a family of white goats with "
      "sleek coats standing upright like people at the edge of a snowy spruce forest, posing solemnly for a family "
      "portrait: a tall bearded grandfather goat with long curved horns, an elegant grandmother goat with a sky-blue "
      "knitted shawl, and between them a slender young goat with small horns in a lime knitted scarf. The picture "
      "inside the frame clearly shows these three goats. Warm, nostalgic colours, a slight vignette.\n\n"
      + prop_layout("top-left — front view, standing on its stand; top-right — back view with the cardboard back "
                    "and the stand; bottom-left — side view; bottom-right — three-quarter view", "the same framed photo"),
      "N-P02_foto_semi_koz_1.png", refs=["выбранный лист козы N-K01 (v2)"],
      changed="коза новая; в v1 на фото в коробке вышел пейзаж.",
      checks=["❗ на фото именно семья из трёх коз, а не пейзаж"]),
    P("N-P03", "Ёлочка в горшке (кадр 7)", "А",
      "Object: a small live spruce about 35 cm tall with dense dark-green needles, in a matte sky-blue ceramic pot "
      "(#66A3FF) with a matching saucer, a little dark soil visible.\n\n" + prop_layout(same="the same potted spruce"),
      "N-P03_yolochka_1.png", changed="небесный керамический горшок вместо терракотового."),
    P("N-P04", "Эмалированная кружка (кадр 7)", "А",
      "Object: a classic white enamel mug, about 9 cm tall, with a cornflower-blue rim and a cornflower-blue edge on "
      "the handle (#0F7DF5); a small chip on the rim shows dark metal; lightly worn, clearly loved.\n\n"
      + prop_layout("top-left — front view, handle on the right; top-right — back view, handle on the left; "
                    "bottom-left — side view with the handle facing the camera; bottom-right — three-quarter view "
                    "from slightly above, showing the inside", "the same mug"),
      "N-P04_kruzhka_1.png", changed="васильковый кант."),
    P("N-P05", "Клубок лаймовой пряжи со спицами (кадр 7)", "А",
      "Object: a big ball of chunky wool yarn in vivid lime green (#ADFC30), about 15 cm across, with two long "
      "wooden knitting needles stuck through it crosswise; from one needle hangs a short knitted strip of a few rows "
      "in the same lime yarn, in thick garter stitch.\n\n" + prop_layout(same="the same yarn ball"),
      "N-P05_klubok_1.png", reuse="N-P05_klubok_v1.png"),
    P("N-P01", "Коробка с вещами (кадры 7, 9, 12, 13)", "А",
      "Images 1–4 are the items packed in the box — keep them exactly: image 1 the framed goat-family photo, image 2 "
      "the potted spruce, image 3 the enamel mug, image 4 the lime yarn ball with knitting needles.\n\n"
      "Object: a medium corrugated cardboard moving box, kraft brown, about 50 × 35 × 35 cm, open top with the four "
      "flaps folded outward, a strip of lime packing tape (#ADFC30) along the bottom seam, slightly dented corners, a "
      "cut-out hand hole on each side. Packed inside and sticking out of the top: at the back, the framed photo from "
      "image 1, standing upright with the picture of the goat family facing forward; the potted spruce from image 2; "
      "the enamel mug from image 3; at the front, the yarn ball from image 4.\n\n"
      + prop_layout("top-left — front view; top-right — back view; bottom-left — side view; bottom-right — "
                    "three-quarter view from above, showing the contents", "the same packed box"),
      "N-P01_korobka_1.png",
      refs=["N-P02 фото семьи коз", "N-P03 ёлочка", "N-P04 кружка", "N-P05 клубок"],
      changed="вещи из коробки теперь прикладываются рефами, чтобы фото было тем самым; лаймовый скотч.",
      note="Делается после N-P02…P05.",
      checks=["❗ в коробке фото семьи коз", "❗ на картоне нет надписей и значков"]),
    P("N-P06", "Очки козы", "А",
      "Object: aviator sunglasses with thin glossy azure-blue metal frames (#1A45D5), a double bridge, slim temples "
      "with sky-blue tips, and gradient sky-blue lenses (#66A3FF fading to clear at the bottom), slightly oversized.\n\n"
      + prop_layout("top-left — front view, temples open; top-right — back view, temples open; bottom-left — side "
                    "view; bottom-right — three-quarter view, temples folded", "the same sunglasses"),
      "N-P06_ochki_1.png", changed="лазурная оправа и голубые стёкла вместо золотых очков.",
      checks=["❗ оправа лазурная, стёкла голубые с градиентом"]),
    P("N-P07", "Лаймовый шарф козы", "А",
      "Object: a chunky hand-knitted scarf in vivid lime green (#ADFC30), thick garter stitch, about 200 × 25 cm, "
      "with a short fringe on both ends.\n\n"
      + prop_layout_free("top-left — the whole scarf laid flat at full length, seen from above; top-right — "
                         "close-up of the knit texture and the fringe; bottom-left — the scarf neatly folded; "
                         "bottom-right — the scarf on a plain grey display neck form, wrapped twice around the neck, "
                         "one end hanging down the front, the other thrown over the left shoulder"),
      "N-P07_sharf_1.png", reuse="N-P07_sharf_v1.png"),
    P("N-P08", "Щётка для снега (кадр 4)", "А",
      "Object: a car snow brush with an ice scraper, about 60 cm long: a cornflower-blue plastic handle (#0F7DF5) "
      "with a light-grey foam grip, dense grey bristles at one end, a translucent scraper blade at the other, a few "
      "flakes of snow caught in the bristles.\n\n" + prop_layout(same="the same brush"),
      "N-P08_shchetka_1.png", changed="васильковая ручка."),
    P("N-P09", "Машина мужчины (кадр 4)", "А",
      "Object: a compact crossover SUV in azure-blue metallic (#1A45D5), a generic modern design with no badges or "
      "emblems anywhere, light-grey alloy wheels, plain licence plates without any characters. A layer of fresh snow "
      "lies on the roof and bonnet, half brushed off on the driver's side.\n\n"
      + prop_layout("top-left — front view; top-right — rear view; bottom-left — left side view; bottom-right — "
                    "three-quarter front view", "the same car on a studio floor"),
      "N-P09_mashina_1.png", changed="лазурный металлик вместо графитового.",
      checks=["❗ ни эмблем, ни букв на номерах"]),
    P("N-P10", "Лопата-движок дворника (кадр 8)", "А",
      "Object: a wide snow pusher shovel of the kind Russian yard keepers use: a cornflower-blue plastic blade "
      "(#0F7DF5) about 75 cm wide with a galvanised metal strip along the bottom edge, a long wooden handle ending in "
      "a U-shaped metal crossbar grip with a black rubber cover; scuffed from use.\n\n"
      + prop_layout("top-left — front view of the blade; top-right — back view; bottom-left — side view; "
                    "bottom-right — three-quarter view", "the same shovel"),
      "N-P10_lopata_1.png", changed="васильковый ковш."),
    P("N-P11", "Панель вызова лифта со стрелками (кадр 11)", "А",
      "Object: a slim vertical elevator call panel in brushed graphite metal, about 12 × 30 cm, set into a wall of "
      "pale stone. One round brushed-steel push button in the lower half; above it a small square indicator window "
      "with two stacked up-pointing chevrons.\n\n"
      + prop_layout_free("top-left — front view, indicator off, the chevrons dark; top-right — front view, indicator "
                         "on: the two chevrons glow vivid lime green (#ADFC30) and a thin lime ring glows around the "
                         "button; bottom-left — side view showing the slim panel profile; bottom-right — "
                         "three-quarter view, indicator on"),
      "N-P11_panel_lifta_1.png", reuse="N-P11_panel_lifta_v1.png",
      checks=["❗ стрелки — двойные шевроны вверх; лайм только в подсветке"]),
    P("N-P12", "Авоська с мандаринами (кадры 12–13)", "А",
      "Object: a classic Russian string shopping bag (avoska) knitted from off-white cotton cord, with two long "
      "handles, filled with about fifteen bright tangerines, a few still with green leaves.\n\n"
      + prop_layout("top-left — front view, hanging by its handles; top-right — back view, hanging; bottom-left — "
                    "side view, hanging; bottom-right — three-quarter view, standing on the floor", "the same bag"),
      "N-P12_avoska_1.png", reuse="N-P12_avoska_v1.png"),
    P("N-P13", "Ёлка в сетке (реакция 1)", "Б",
      "Object: a freshly cut spruce about 180 cm tall, tightly wrapped in white plastic netting, the cut trunk end "
      "sticking out at the bottom, a few branches poking through the net.\n\n"
      + prop_layout("top-left — standing upright, front view; top-right — standing upright, back view; bottom-left "
                    "— lying on its side; bottom-right — three-quarter view, leaning", "the same wrapped tree"),
      "N-P13_yolka_v_setke_1.png", reuse="N-P13_yolka_v_setke_v1.png"),
    P("N-P14", "Термос (реакция 2)", "Б",
      "Object: a 1-litre stainless-steel thermos with a matte cornflower-blue body (#0F7DF5), a brushed-steel cup-lid "
      "and a stopper.\n\n"
      + prop_layout("top-left — front view, closed; top-right — back view, closed; bottom-left — side view, closed; "
                    "bottom-right — three-quarter view with the cup-lid off, standing beside the thermos, filled "
                    "with steaming tea", "the same thermos"),
      "N-P14_termos_1.png", changed="васильковый корпус."),
    P("N-P15", "Деревянные санки (реакция 7)", "Б",
      "Object: a classic Russian children's sled: a seat of light varnished wooden slats on bent steel runners "
      "painted cornflower blue (#0F7DF5), a folding push handle at the back, a thick natural rope tied to the "
      "front.\n\n" + prop_layout(same="the same sled on a studio floor"),
      "N-P15_sanki_1.png", reuse="N-P15_sanki_v1.png (если полозья на нём синие)"),
    P("N-P16", "Гирлянда (реакция 5)", "Б",
      "Object: a string of old-fashioned round warm-white light bulbs, about 5 m long, on a dark cable, the bulbs "
      "glowing softly.\n\n"
      + prop_layout_free("top-left — the garland loosely coiled; top-right — the garland hanging in two soft swags; "
                         "bottom-left — close-up of three bulbs on the cable; bottom-right — the garland held up in "
                         "a loose loop, three-quarter view"),
      "N-P16_girlyanda_1.png", reuse="N-P16_girlyanda_v1.png"),
    P("N-P17", "Снеговик (реакция 6)", "Б",
      "Object: a hand-made three-ball snowman about 120 cm tall, slightly lumpy snow, twig arms, coal eyes and a coal "
      "smile, a carrot nose stuck in crookedly at an angle, a sky-blue knitted scarf (#66A3FF) around its neck.\n\n"
      + prop_layout("top-left — front view; top-right — back view; bottom-left — side view showing the crooked "
                    "nose; bottom-right — three-quarter view", "the same snowman on a little snow"),
      "N-P17_snegovik_1.png", changed="небесный шарф на снеговике."),
]

# ── 5. Локации ──
LOCATIONS = [
    P("N-L01", "Опушка, вид на ЖК (кадр 1)", "А",
      "Images 1 and 2 show the residential complex; keep its architecture exactly — light-grey brick, graphite top "
      "floors, terracotta-red blocks, black window frames — but turn the season to deep winter.\n\n" + plate_text(
          "Point of view from inside the edge of a snowy spruce forest at a height of 1.5 m: heavy snow-laden spruce "
          "branches frame the shot on the left, the right and the top, soft in the foreground; through the opening, a "
          "wide snowy field, and on its far side the residential complex from images 1 and 2, crisp in the clean "
          "frosty air, roofs white with snow. Loose snow drifts in the air, lit from behind by the sun; long cool-blue "
          "shadows across the field; a clear pale-blue winter sky.", PLATE_EXT),
      "N-L01_opushka_1.png", refs=["REF-SS2-A", "REF-SS2-B"], changed="свет сбоку-сзади вместо золотого сияния."),
    P("N-L02", "Двор зимой (кадры 4–8, запасные реакции)", "А",
      "Image 1 shows the courtyard and image 2 the facades of the residential complex; keep the architecture and the "
      "playground exactly, but turn the season to winter.\n\n" + plate_text(
          "An eye-level view across the courtyard: the playground with its cylindrical wooden-slat towers and the "
          "stainless steel slide under snow caps, the orange rubber surface showing only in small patches; a tall "
          "spruce in the yard decorated with warm-white lights and baubles in cornflower blue, sky blue and lime; "
          "cleared paving paths with neat snowbanks; a cornflower-blue sled leaning against a wooden bench and a "
          "child's lime snow shovel stuck in a snowbank; a few snow-covered parked cars at the edge; the facades "
          "behind — light-grey brick with the two lower floors in graphite, black window frames, normal-size "
          "windows.", PLATE_EXT),
      "N-L02_dvor_1.png", refs=["REF-SS2-C", "REF-SS2-A"],
      changed="палитра в деталях двора: шары на ёлке, санки, детская лопатка; свет сбоку-сзади.",
      checks=["❗ ни катка, ни людей; окна обычные, не панорамные"]),
    P("N-L03", "Подъезд (кадр 9)", "А",
      "Image 1 shows the residential complex; keep its architecture — light-grey brick, graphite ground floors, "
      "black window frames — but in winter.\n\n" + plate_text(
          "A building entrance on the graphite ground floor, seen straight on from the path at shoulder height: a "
          "dark metal-framed glass door under a slim canopy with a spruce wreath tied with a cornflower-blue ribbon, "
          "three wide grey stone steps brushed clean of snow, neat snowbanks on both sides, warm light glowing "
          "through the glass from the bright lobby; above, light-grey brick with black window frames.", PLATE_EXT),
      "N-L03_podezd_1.png", refs=["REF-SS2-C"], changed="венок с васильковой лентой; свет сбоку-сзади."),
    P("N-L04", "Холл с лифтом (кадры 10–13, пэкшот)", "А", plate_text(
        "A bright modern residential lobby seen strictly frontally and symmetrically at chest height: a polished pale "
        "stone floor; in the right half of the frame the elevator — brushed-steel doors set in a wall of light oak "
        "panels, a slim brushed-graphite call panel to the right of the doors; the left half of the frame is a calm, "
        "empty wall of smooth pale ice-blue plaster (#DAEEFC), softly washed with light from above, with nothing on "
        "it.", PLATE_INT),
      "N-L04_holl_1.png", changed="светлый холл: бледный камень, светлый дуб, бледно-голубая стена вместо коричневого.",
      checks=["❗ левая половина — пустая бледно-голубая стена под титры", "❗ нет оранжево-коричневого «супа»"]),
    P("N-L05", "Кабина лифта (кадры 12–13)", "А", plate_text(
        "A strictly frontal, symmetric view at chest height into an open elevator cabin, the brushed-steel doors fully "
        "open: light oak veneer on three walls, a brushed-steel handrail at hip height, a soft neutral-white light "
        "panel in the ceiling, a pale stone floor.", PLATE_INT),
      "N-L05_kabina_1.png", changed="светлая кабина вместо тёмно-коричневой."),
]

# ── 6. Раскадровка ──
SB1 = board_text(
    "References: image 1 — the goat character (keep her exactly: tall and slender, sleek white coat, blue aviator "
    "sunglasses, lime scarf); image 2 — the forest edge with the view of the residential complex; image 3 — the "
    "courtyard; image 4 — the man; image 5 — his car; image 6 — his snow brush.",
    ["1", "2", "3", "4"],
    [
        "Point of view of someone 1.5 m tall standing inside the forest edge from image 2, 35 mm lens look: a slender "
        "goat foreleg — sleek short white coat, a small polished dark hoof — reaches in from the lower right and parts "
        "heavy snow-laden spruce branches; loose snow falls, backlit by the sun; through the gap, the snowy field and "
        "the residential towers far away, crisp in the frosty air.",
        "Low from behind at knee height, 50 mm lens look, framing only from the hooves to the waist of the goat from "
        "image 1 standing in deep forest snow: slim legs, sleek white coat, her short tail flicking snow off in a "
        "small puff that glows in the sunlight from behind; the fringed lime end of her scarf hangs down her back; "
        "spruce trunks soft in the background.",
        "Side view at hoof height, 50 mm lens look, only her legs from the knees down: two small dark hooves step out "
        "of deep forest snow onto the cleared grey paving of the courtyard path from image 3, walking from left to "
        "right past a low snowbank; kicked-up snow crystals lit from behind.",
        "The courtyard from image 3, a medium shot from the chest up at eye level, 50 mm lens look: on the right "
        "third of the frame the man from image 4 in his sky-blue parka brushes snow off the roof of the azure car from "
        "image 5 with the brush from image 6; his face takes about a third of the frame height; the brushed snow dust "
        "glows in the sun behind him. Caught mid-reaction: his eyes have just slid to the left of the camera and stay "
        "there; the brush has stopped mid-stroke; his brows lift a little and his lips part slightly; the rest of his "
        "face is still; no smile. Behind him, soft: the playground with wooden towers under snow, the spruce with "
        "blue and lime baubles, two children in bright snowsuits playing, the light-grey brick facades.",
    ], LOOK_EXT)

SB2 = board_text(
    "References: image 1 — the goat character (keep her exactly); image 2 — her packed moving box; image 3 — the "
    "courtyard; image 4 — the mother; image 5 — the yard keeper; image 6 — his snow shovel.",
    ["5", "6", "7", "8"],
    [
        "A ground-level insert, 85 mm lens look, very shallow depth of field: the goat's small dark hooves and slender "
        "white legs walk across the grey paving straight towards the camera; the nearest hoof is about to cover the "
        "lens; kicked-up snow crystals glow in the sun behind.",
        "At a child's eye height in the courtyard from image 3, a medium close two-shot, 50 mm lens look, both faces "
        "large in the frame: a boy of about six — round rosy cheeks, a cornflower-blue snowsuit, a white knitted hat "
        "with a lime pompom, lime mittens on a string — tugs the sleeve of the mother from image 4 and points just to "
        "the left of the camera; his face has opened up with real delight: eyebrows up, eyes wide and shining, a wide "
        "gap-toothed grin. The mother, half a beat behind him, has turned her head that way: her brows lift a little "
        "and her lower lids soften — the faintest smile only in her eyes, lips closed; her gloved hands are still "
        "straightening his hat. The sun behind them rims the hats and hair; their faces are softly lit by the snow.",
        "A close side view at box height, 85 mm lens look: the moving box from image 2 is carried past from left to "
        "right in the goat's slender white forelegs with small dark hooves — we see only the forelegs, the box and "
        "the lime fringe of her scarf; inside, the framed goat-family photo, the small spruce in its sky-blue pot, "
        "the white enamel mug with a cornflower rim and the lime yarn ball with wooden needles sway with the step; "
        "the courtyard soft behind.",
        "A medium shot from the waist up, 50 mm lens look: the yard keeper from image 5 in his azure work suit with "
        "lime reflective stripes keeps pushing the shovel from image 6 at the same steady pace while his eyes follow "
        "something just left of the camera; a perfectly flat, unbothered face — heavy lids, the moustache still, "
        "nothing moves but his eyes; a heap of snow grows in front of the cornflower-blue blade; sun from the side, "
        "his face readable.",
    ], LOOK_EXT)

SB3 = board_text(
    "References: image 1 — the goat carrying her box (keep her look and the box exactly); image 2 — the building "
    "entrance; image 3 and image 4 — the couple; image 5 — the lobby with the elevator; image 6 — the young man.",
    ["9", "10", "11", "12"],
    [
        "From behind at shoulder height, about 1.2 m behind the goat from image 1, 40 mm lens look, the goat centred: "
        "the back of her head with slim swept-back horns, her long elegant neck, the sleek white coat, the lime scarf "
        "end down her back, the top edge of the box she carries. Ahead, the entrance from image 2: the couple from "
        "images 3 and 4 have just stepped out mid-conversation and stop short, out of sync: she has stopped mid-word, "
        "her brows lifted, lips still parted; he, half a beat behind her, has turned his head, his face composed, "
        "lips closed, and holds the door open with a small, courteous gesture; no smiles. Warm light inside the "
        "doorway, sun from the side.",
        "A low side view from the knees down as the camera passes through the facade, 40 mm lens look: the left third "
        "of the frame is a dark blurred band — the cut edge of the wall right at the lens; beyond it the bright lobby "
        "from image 5 with its pale polished stone floor, light oak and pale ice-blue plaster; the goat's slender "
        "legs and small dark hooves step from left to right towards the elevator.",
        "Macro, 100 mm lens look: the slim graphite call panel in a pale stone wall; a small polished dark hoof at the "
        "end of a slender white foreleg presses the round steel button; above it two stacked up-chevrons glow vivid "
        "lime green. Very shallow depth of field.",
        "Strictly frontal and symmetric at chest height, 40 mm lens look: the elevator doors have slid open; inside "
        "the bright cabin — light oak, brushed steel, soft neutral-white light — on the right stands the young man "
        "from image 6 in his cornflower puffer with a string bag of tangerines; the goat from image 1 has stepped in "
        "and turned to face us, seen whole for the first time: tall, slender and graceful, blue aviator sunglasses, "
        "lime scarf, the box in her forelegs; calm and self-assured — lids a little lowered behind the blue lenses, "
        "the corners of her mouth lifted a fraction, chin a touch up, the rest of her face still. The young man has "
        "frozen mid-glance: his eyes turned sideways to her, brows lifted a little and drawn together, lips slightly "
        "parted, no smile; his shoulders stiff, the string bag motionless.",
    ], LOOK_ALL)

SB4 = single_text(
    "References: image 1 — the goat carrying her box; image 2 — the young man; image 3 — the lobby; image 4 — the "
    "elevator cabin. Keep all of them exactly.",
    "A wide, strictly frontal and symmetric view of the bright lobby from image 3 at chest height, 40 mm lens look: "
    "the open elevator (image 4) stands in the right half of the frame; inside it, full length and side by side, the "
    "tall, slender goat from image 1 — blue aviator sunglasses, lime knitted scarf, holding her moving box — and the "
    "young man from image 2 in his cornflower puffer with the string bag of tangerines. The goat nudges her "
    "sunglasses up her muzzle with one hoof, perfectly at ease, the corners of her mouth lifted a fraction; the "
    "young man stands stiffly, his eyes sliding sideways to her, brows a little raised, lips pressed together, no "
    "smile. The left half of the frame is a calm, empty wall of pale ice-blue "
    "plaster (#DAEEFC), softly washed with light from above, with nothing on it.",
    LOOK_INT)

SB5 = board_text(
    "References: image 1 — the courtyard; image 2 — the man with the spruce; image 3 — the grandmother; image 4 — the "
    "dog owner; image 5 — the beagle; image 6 — the thermos. Every still takes place in the courtyard from image 1; "
    "in every still the person looks at something just to the left of the camera that we never see.",
    ["R1", "R2", "R3", "R4"],
    [
        "By a parked car in the courtyard, 50 mm lens look: the man from image 2 with the net-wrapped spruce on his "
        "shoulder has stopped; the top of the tree still sways; his eyes follow something to the left of the camera "
        "and one corner of his mouth slowly lifts — barely.",
        "On a wooden bench, 85 mm lens look: the grandmother from image 3 holds the steaming cup-lid of the thermos "
        "from image 6; she has stopped it halfway to her mouth; the lines around her eyes deepen in a warm, "
        "knowing look, her lips barely curve; nothing else on her face moves.",
        "At low height on a snowy path, 50 mm lens look: the beagle from image 5 in its lime harness sits down and "
        "tilts its head to one side; the lime leash goes slack; above it, the owner from image 4 raises one eyebrow, "
        "the rest of her face perfectly still.",
        "On the playground swing, 50 mm lens look: a lanky boy of about fifteen with a deadpan face — azure puffer "
        "jacket, light-grey beanie, white wireless earbuds — keeps swinging, turns his head to follow something and "
        "pulls out one earbud; no smile.",
    ], LOOK_EXT)

SB6 = board_text(
    "References: image 1 — the courtyard and its buildings; image 2 — the woman; image 3 — her garland; image 4 — "
    "the snowman; image 5 — the sled. In every still the people look at something just to the left of the camera "
    "that we never see.",
    ["R5", "R6", "R7"],
    [
        "On a balcony of the light-grey brick building, seen at her eye level from the next balcony, 50 mm lens look: "
        "the woman from image 2 in her sky-blue sweater has frozen in the middle of hanging the garland from image 3 "
        "along the railing; she looks down to the left of the camera, lips parted, eyebrows slightly raised; the "
        "bulbs keep glowing.",
        "In the courtyard by the snowman from image 4 with its sky-blue scarf, 50 mm lens look: a girl of about six "
        "(sky-blue snowsuit, white knitted hat with ear flaps, lime mittens) and a boy of about seven (pale ice-blue "
        "snowsuit with cornflower trim, light-grey hat) both stare to the left of the camera, mouths open; without "
        "looking, the boy sticks the carrot nose into the snowman crooked.",
        "On a courtyard path, 50 mm lens look: a boy of about seven (azure snowsuit with light-grey knee patches, "
        "white knitted hat with a sky-blue stripe, cream scarf) pulling the sled from image 5 by its rope has stopped "
        "dead: eyes wide, mouth a small O; the sled rolls on and bumps into the back of his legs, and he doesn't "
        "look down.",
    ], LOOK_EXT, layout="stack")

STORYBOARD = [
    P("N-SB1", "Кадры 1–4", "А", SB1, "N-SB1_kadry_01-04_1.png",
      refs=["лист козы N-K01", "N-L01 опушка", "N-L02 двор", "N-K02 мужчина", "N-P09 машина", "N-P08 щётка"],
      checks=["❗ мужчина не улыбается: лёгкое недоумение", "❗ снег с фактурой, свет сбоку-сзади, не «золотая открытка»"]),
    P("N-SB2", "Кадры 5–8", "А", SB2, "N-SB2_kadry_05-08_1.png",
      refs=["лист козы N-K01", "N-P01 коробка", "N-L02 двор", "N-K04 мама", "N-K05 дворник", "N-P10 лопата"],
      note="Мальчик описан словами, его лист не прикладываем.",
      checks=["❗ кадр 7: коробку несёт коза (белые ноги с копытцами), а не мама",
              "❗ кадр 7: на фото в коробке семья коз",
              "мама с едва заметной улыбкой глазами, не позирует"]),
    P("N-SB3", "Кадры 9–12", "А", SB3, "N-SB3_kadry_09-12_1.png",
      refs=["N-K01B коза с коробкой", "N-L03 подъезд", "N-K06 мужчина ~50", "N-K07 женщина ~50", "N-L04 холл",
            "N-K08 парень"],
      checks=["❗ кадр 12: парень в лёгком недоумении, без улыбки", "❗ коза высокая и стройная, очки голубые",
              "пара у подъезда без улыбок"]),
    P("N-SB4", "Кадр 13, пэкшот", "А", SB4, "N-SB4_kadr_13_pekshot_1.png",
      refs=["N-K01B коза с коробкой", "N-K08 парень", "N-L04 холл", "N-L05 кабина"],
      checks=["❗ лифт и герои в правой половине, левая половина — пустая бледно-голубая стена",
              "❗ парень без улыбки", "❗ холл светлый, не коричневый"]),
    P("N-SB5", "Запасные реакции R1–R4", "Б", SB5, "N-SB5_reaktsii_1-4_1.png",
      refs=["N-L02 двор", "N-K09 мужчина с ёлкой", "N-K10 бабушка", "N-K11 хозяйка собаки", "N-K12 бигль",
            "N-P14 термос"],
      note="Подросток описан словами."),
    P("N-SB6", "Запасные реакции R5–R7", "Б", SB6, "N-SB6_reaktsii_5-7_1.png",
      refs=["N-L02 двор", "N-K14 женщина на балконе", "N-P16 гирлянда", "N-P17 снеговик", "N-P15 санки"],
      note="Дети описаны словами."),
]

SECTIONS = [
    ("3. Персонажи",
     "Формат персонажа (как в присланной сетке): слева большой портрет по плечи, справа два роста — анфас и со "
     "спины. Фон ровный серый.", CHARACTERS),
    ("4. Предметы",
     "Формат предмета (как в присланной сетке): 4 ячейки 2×2 на сером фоне — спереди, сзади, сбоку, три четверти. "
     "Там, где ракурсы другие, это сказано в промпте.\n\n**Порядок для коробки:** сначала N-P02…P05, потом N-P01 с "
     "ними в рефах, потом N-K01B.", PROPS),
    ("5. Локации (пустые фоны, без людей)",
     "Эти фоны станут референсом окружения для раскадровки и Seedance. **Дома точно как на рендерах, только зимой.**",
     LOCATIONS),
    ("6. Раскадровка",
     "Только из утверждённых листов. Каждый лист раскадровки — 4 кадра 2×2. Пэкшот (N-SB4) — один большой кадр.\n\n"
     "Общее для всех кадров:\n"
     "- люди смотрят **левее камеры**: коза за кадром рядом с объективом;\n"
     "- коза идёт **слева направо**;\n"
     "- до кадра 12 козу целиком не показываем.", STORYBOARD),
]


def HEADER(palette_table, export_names=None):
    instr = instructions(
    save_folder="Ролики 2027\\01 Новосёл\\Листы v2\\",
    hero_id="N-K01", hero_name="Коза",
    special_rules=["Без катка. Ёлка во дворе есть.",
                   "Козу в v2 генерируем **только по словам**, баннер с козой не прикладываем."],
    order_steps=[
        "**Шаг 2. Основа ролика (приоритет А).**\n"
        "1. Предметы для коробки: N-P02 фото (нужна выбранная коза), N-P03 ёлочка, N-P04 кружка, N-P05 клубок ♻️.\n"
        "2. N-P01 коробка: в рефах эти четыре предмета.\n"
        "3. N-K01B коза с коробкой.\n"
        "4. Люди N-K02…K08.\n"
        "5. Остальные предметы N-P06…P12 (♻️ где помечено).\n"
        "6. Локации N-L01…L05.\n\n"
        "Покажи все листы одной сводкой и дождись утверждения.",
        "**Шаг 3. Запасные реакции (приоритет Б).**\n"
        "- Сделай всё с пометкой **Б**. Помеченное ♻️ можно взять из v1.\n"
        "- Если ChatGPT упёрся в лимит генераций, остановись и сообщи, что готово, а что нет.",
        "**Шаг 4. Раскадровка.** Только из утверждённых листов: сначала N-SB1…SB4, потом N-SB5…SB6.",
    ],
    reuse_note="\n- Листы v1 лежат в папке v1. Помеченные ♻️ можно взять оттуда, если дизайнер их одобрил: спроси "
               "об этом в том же сообщении.")
    ps = photostyle()
    pal = palette_section(palette_table)
    sb = f"«{export_names['storyboard']}»" if export_names else "[`storyboard.md`](storyboard.md)"
    return f"""# «Новосёл»: промпты для ChatGPT, v3

Ролик застройщика «Развитие» для ЖК **Суворов-Сити 2**. YouTube, 16:9, 20 секунд. Версия v3 от 04.10.2026: игра актёров переписана по разбору эмоций в роликах Яндекса.

Это **набор инструкций для Claude в десктоп-приложении**: он генерирует картинки в ChatGPT через браузер дизайнера. Сценарий и раскадровка — {sb}.

## Что изменилось в v3

Изменилась только **раскадровка** (N-SB1…SB6). Листы персонажей, предметов и локаций остаются как в v2.
- Эмоции записаны **движениями лица**, а не словами «улыбается», «удивлён». Правила — в `video-research/06-emotions.md`.
- **Каждая реакция поймана посередине:** сначала глаза, потом рот. Улыбки по умолчанию с сомкнутыми губами. Большая эмоция одна — восторг мальчика.
- **Реакции снимаем ближе:** лицо занимает около трети высоты кадра (мужчина со щёткой — по грудь, мама с мальчиком — средний крупный, дворник — по пояс). Иначе мимика не читается.
- **Люди реагируют вразнобой:** в паре у подъезда сначала она, через полсекунды он.
- **Коза** спокойна и уверена: веки чуть опущены, уголки рта приподняты на долю.
- **Парень в лифте** застыл посреди взгляда: брови чуть вверх и к переносице, губы приоткрыты, плечи напряжены, без улыбки.

## Что изменилось в v2

- **Фотостиль как у Яндекса:**
  - живой свет сбоку-сзади с мягкой подсветкой лиц;
  - снег не выбит;
  - настоящая фактура кожи;
  - эмоции без позирования.
- **Палитра бренда в одежде и предметах.** Раньше люди были в тёмно-синем и чёрном, а лайм был только на козе.
- **Коза:**
  - высокая, стройная, изящная, с гладкой короткой шерстью;
  - очки-авиаторы с лазурной оправой и голубыми стёклами;
  - баннер с козой больше не прикладываем: он тянет лохматую козу в золотых очках.
- **Парень в лифте:** лёгкое недоумение, без улыбки.
- **Холл и лифт светлые:** бледный камень, светлый дуб, бледно-голубая стена под титры вместо коричневого.
- **Исправлены ошибки v1:**
  - в коробке теперь фото семьи коз, а не пейзаж: сначала делаем фото, потом коробку с ним в рефах;
  - на вставке 7 коробку несёт коза, а не мама.
- **♻️ Можно не перегенерировать** клубок, шарф, панель лифта, авоську, ёлку в сетке, гирлянду и санки, если листы v1 понравились.

{ps}
{pal}
{instr}
## 1. Референсы (файлы на компьютере дизайнера)

| Код | Что это | Как узнать файл |
|---|---|---|
| **REF-SS2-A** | Суворов-Сити 2, вечер | Вид с луга на закате: светло-серый кирпич, графитовые верхние этажи, терракотовые корпуса, тёплые окна, фонари |
| **REF-SS2-B** | Суворов-Сити 2, день | Вид с дороги: высокая башня из светлого кирпича с графитовым верхом, терракотовые корпуса, машины, деревья |
| **REF-SS2-C** | Суворов-Сити 2, двор | Двор сверху: оранжевое покрытие площадки, деревянные башни-цилиндры из реек, металлическая горка, плитка, парковка |
| **REF-SS2-D** | Суворов-Сити 2, квартал | Вид с высоты на весь квартал среди деревьев |

Баннер с козой («Авиапарк в Шилово») в v2 **не прикладываем**.

## 2. О ролике (контекст для генераций)

- **Герой** — прямоходящая белая коза, символ 2027 года. Она высокая, стройная и изящная, в очках-авиаторах с лазурной оправой и в лаймовом вязаном шарфе. Несёт коробку с вещами и переезжает в ЖК.
- Зритель видит только её глаза, хвост, копыта, коробку и спину, а реакции соседей — сдержанные и разные. **Целиком козу видно только в финале, в лифте.**
- **Картинка:**
  - солнечный морозный день, солнце сбоку-сзади, лица подсвечены снегом;
  - живая фактура, глубокие тени;
  - палитра бренда на одежде и в деталях двора, лайм — главный акцент на козе.
- **Пэкшот:** коза и парень в открытом лифте в **правой половине** кадра. Левая половина — пустая бледно-голубая стена под титры.
"""


FOOTER = """## 7. После раскадровки

Следующий этап — ключевые кадры (по одному на план) и промпты Seedance 2.0 для «Виви». Это делаем отдельно, после того как дизайнер утвердит раскадровку v2 и выберет реакции.
"""
