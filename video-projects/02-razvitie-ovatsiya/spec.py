"""«Овация» (арт-квартал «Зарядье»): спецификация промптов для ChatGPT, v2 (04.10.2026).

Сборка: python3 video-projects/_kit/build_prompts.py
"""
from build_prompts import (FILM_SINGLE, animal_layout, board_text, person_layout, plate_text, prop_layout,
                           prop_layout_free, single_text)
from common_md import instructions, palette_section, photostyle

EXPORT = {"prompts": "Промпты_Развитие_Овация_v4.md", "storyboard": "Сториборд_Развитие_Овация_v4.md"}

# ── Свет и цвет ролика ──
LIGHT_EVE = (
    "Exteriors: winter blue hour just after sunset — a deep-blue sky and blue snow, warm 3000 K windows, lamps and "
    "street lights, gentle snowfall; warm lights behind and beside people draw a rim on hair and shoulders, while "
    "soft light from the front keeps every face readable."
)
LIGHT_HOME = (
    "Interiors: lived-in flats seen straight on like a dollhouse with the front wall removed; warm lamps in the "
    "room and the deep-blue evening in the window behind; a warm practical light behind or beside each person draws "
    "a rim on the hair, soft light from the front keeps the face readable; the cut walls and floor slabs are thick "
    "and deep black."
)
COLOUR = (
    "Colour: the evening blue and the brand blues in clothes and interiors — cornflower #0F7DF5, azure #1A45D5, "
    "sky blue #66A3FF, pale ice blue #DAEEFC — against warm lamplight, with lime #ADFC30 only as small bright "
    "accents, the brightest being the grandfather's bow tie; nobody wears black."
)
LOOK_HOME = f"{LIGHT_HOME} {COLOUR}"
LOOK_EVE = f"{LIGHT_EVE} {COLOUR}"
LOOK_ALL = f"{LIGHT_HOME} {LIGHT_EVE} {COLOUR}"
PLATE_EVE = (
    f"{FILM_SINGLE} Winter blue hour just after sunset: a deep-blue sky, blue snow, warm 3000 K windows and lamps, "
    "gentle snowfall; 35 mm lens look, about 47° horizontal field of view, level horizon."
)
PLATE_HOME = (
    f"{FILM_SINGLE} Warm lamps inside, the deep-blue snowy evening in the window; balanced colour, never "
    "orange-brown; 40 mm lens look, level horizon."
)


def P(id, title, prio, prompt, file, refs=None, checks=None, changed=None, reuse=None, note=None, runs=1):
    return dict(id=id, title=title, prio=prio, prompt=prompt, file=file, refs=refs, checks=checks,
                changed=changed, reuse=reuse, note=note, runs=runs)


def person(desc, who, pose="standing naturally, arms relaxed"):
    return f"{desc}\n\n{person_layout(who, pose)}"


# ── 3. Персонажи ──
CHARACTERS = [
    P("O-K01", "Дедушка — главный герой (кадры 1, 11)", "А", person(
        "Character: a slim, upright Russian man of about 75 with a kind, dignified face: neatly combed white hair with "
        "a side parting, a trimmed white moustache, deep laugh lines, real age spots and wrinkles, bright attentive "
        "grey eyes. He has dressed up at home for a solemn occasion: a crisp white shirt, a vivid lime-green satin bow "
        "tie (#ADFC30), an azure wool cardigan (#1A45D5), buttoned, light-grey trousers with sharp creases, and worn "
        "brown leather house slippers. Expression: solemn and quietly proud; no smile, only a hint of warmth under "
        "the moustache.", "man"),
      "O-K01_dedushka_1.png", runs=3,
      changed="лазурный кардиган вместо графитового, светло-серые брюки.",
      checks=["❗ бабочка ярко-лаймовая, кардиган лазурный",
              "тапочки, а не туфли: в этом шутка",
              "не улыбается, торжественный"]),
    P("O-K02", "Молодая мама с младенцем (кадр 2)", "А", person(
        "Character: a Russian woman of about 30 with a gentle, tired-but-happy face, dark hair in a loose low "
        "ponytail, no make-up, in a soft pale ice-blue knitted lounge set (#DAEEFC) and thick cream socks. She carries "
        "a sleeping baby in a beige fabric sling on her chest: the baby's face is turned into her chest, so only a "
        "small sky-blue knitted hat (#66A3FF) and one round cheek are visible. Expression: calm and tender. From "
        "behind, the sling straps cross on her back.", "woman"),
      "O-K02_mama_1.png", changed="бледно-голубой домашний костюм, небесная шапочка младенца."),
    P("O-K03", "Подросток (кадр 3)", "А", person(
        "Character: a lanky boy of about fifteen with messy dark-blond hair and a bored, deadpan look. A "
        "cornflower-blue hoodie (#0F7DF5), light-grey sweatpants, white socks; large matte-white over-ear headphones "
        "without any logos hang around his neck.", "boy", "standing, hands in the hoodie pocket"),
      "O-K03_podrostok_1.png", note="Подросток — только по словам.", changed="васильковое худи, белые наушники."),
    P("O-K04", "Хозяйка с пирожками (кадр 4)", "А", person(
        "Character: a full-figured Russian woman of about 55 with a warm rosy face, chestnut hair in a short neat cut "
        "and small gold earrings. A cream blouse with rolled-up sleeves under an apron with cornflower-blue and white "
        "stripes (#0F7DF5), light-grey trousers, soft house shoes; sky-blue quilted oven mitts (#66A3FF) on both "
        "hands. Expression: restrained pride, lips pressed together in a small satisfied way.", "woman",
        "standing naturally, arms relaxed, the apron ties visible from behind"),
      "O-K04_khozyayka_1.png", changed="фартук в васильковую полоску, небесные прихватки."),
    P("O-K05", "Консьерж (кадр 5)", "А", person(
        "Character: a neat Russian woman of about 60 with a short silver bob and thin-rimmed glasses. An azure "
        "cardigan (#1A45D5) over a white blouse with a small round brooch, a light-grey knee-length skirt, low "
        "comfortable shoes. Expression: strict but kind, a barely visible smile in the eyes.", "woman"),
      "O-K05_konserzh_1.png", changed="лазурный кардиган, светло-серая юбка."),
    P("O-K06", "Мужчина с выбивалкой (кадр 6)", "А", person(
        "Character: a broad-shouldered Russian man of about 40 who has run outside for a minute: ruddy cheeks, a short "
        "dark beard, a light-grey knitted hat pushed back on his head, an open cornflower-blue puffer jacket "
        "(#0F7DF5) over a thick oatmeal knitted sweater, grey track trousers tucked into grey felt boots (valenki) with "
        "black rubber galoshes. In his right hand a twisted rattan carpet beater. Expression: focused, in rhythm.",
        "man"),
      "O-K06_muzhchina_kover_1.png", changed="васильковый пуховик, светло-серая шапка."),
    P("O-K07", "Девочка ~7 лет (кадр 7)", "А", person(
        "Character: a girl of about seven with rosy cheeks, freckles and a wide grin with one missing front tooth. A "
        "sky-blue one-piece winter snowsuit (#66A3FF), a white knitted hat with a big lime pompom (#ADFC30), white "
        "knitted mittens with a cornflower-blue pattern on a string, white snow boots. Expression: pure delight.",
        "girl"),
      "O-K07_devochka_1.png", note="Ребёнок — только по словам.", changed="небесный комбинезон, лаймовый помпон."),
    P("O-K08", "Мальчик ~7 лет (кадр 7)", "А", person(
        "Character: a boy of about seven with a round face, rosy cheeks and a light-brown fringe peeking out from "
        "under a pale ice-blue knitted hat (#DAEEFC). A cornflower-blue one-piece winter snowsuit (#0F7DF5) with pale "
        "ice-blue cuffs, lime knitted mittens on a string (#ADFC30), grey snow boots. Expression: a happy, slightly "
        "shy grin.", "boy"),
      "O-K08_malchik_1.png", note="Ребёнок — только по словам.", changed="васильковый комбинезон, лаймовые варежки."),
    P("O-K09", "Пёс (кадр 8)", "А",
      "Character: a medium-sized fluffy mixed-breed dog with a fox-like face: a ginger-and-white coat with a white "
      "chest, muzzle and paws, pointed ears, warm brown eyes, a big plumed tail curling over its back, a plain lime "
      "collar (#ADFC30) without tags. Happy and alert.\n\n"
      + animal_layout("dog", "alert and happy", "sitting, front view on the left; standing, left side profile with "
                                                "the tail clearly visible on the right"),
      "O-K09_pyos_1.png", changed="лаймовый ошейник."),
    P("O-K10", "Молодой мужчина с пакетами (кадр 9)", "А", person(
        "Character: a tall Russian man of about 28 with a short dark beard and a friendly, amused face. A sky-blue "
        "knitted beanie (#66A3FF), a long azure parka (#1A45D5), light-wash jeans, tan leather winter boots. In each "
        "hand a full canvas grocery tote bag with no prints — a natural one with a baguette and leeks sticking out, a "
        "cornflower-blue one with apples showing.", "man", "standing naturally, a bag in each hand"),
      "O-K10_paren_pakety_1.png", changed="лазурная парка, небесная шапка, один пакет васильковый."),
    P("O-K11", "Молодая женщина (кадр 9)", "А", person(
        "Character: a Russian woman of about 27 with laughing eyes, a warm open face and light-brown hair falling from "
        "under a white knitted hat. A long pale ice-blue puffer coat (#DAEEFC), a huge chunky cornflower-blue knitted "
        "scarf (#0F7DF5), light-grey mittens, white winter boots. Expression: about to laugh.", "woman"),
      "O-K11_devushka_1.png", changed="бледно-голубой пуховик, васильковый шарф."),
    P("O-K12", "Бабушка со спицами (A1)", "Б", person(
        "Character: a plump Russian woman of about 72 with silver hair in a bun and round glasses on a thin chain. A "
        "sky-blue knitted cardigan (#66A3FF) over a light-grey dress with a small muted floral print, thick grey "
        "woollen socks, felt house slippers. In her hands two wooden knitting needles with a piece of pale ice-blue "
        "knitting. Expression: peering over her glasses, a faint mischievous look.", "woman"),
      "O-K12_babushka_spitsy_1.png", changed="небесный кардиган, бледно-голубое вязание."),
    P("O-K13", "Лыжник (A2)", "Б", person(
        "Character: a lean, fit Russian man of about 60 with grey stubble and a weathered, cheerful face. A retro "
        "cross-country ski suit in cornflower blue and white (#0F7DF5) with a thin lime stripe on the sleeves "
        "(#ADFC30), a white knitted ski hat, black ski boots, thin light-grey gloves; a pair of light-grey ski poles "
        "in his hands. Expression: energetic, a broad satisfied grin.", "man", "standing, holding the poles"),
      "O-K13_lyzhnik_1.png", changed="васильково-белый лыжный костюм с лаймовой полоской."),
    P("O-K14", "Девочка со скрипкой (A3)", "Б", person(
        "Character: a girl of about nine with two neat braids and a serious, concentrated face. An azure dress "
        "(#1A45D5) over a white turtleneck, white tights, light-grey shoes. She holds a warm-brown violin under her "
        "chin and a bow in her right hand.", "girl", "standing, playing the violin"),
      "O-K14_devochka_skripka_1.png", note="Ребёнок — только по словам.", changed="лазурное платье."),
    P("O-K15", "Кот (A4)", "Б",
      "Character: a well-fed grey tabby cat with a white chest and white paws, green-gold eyes, a long striped tail, "
      "an expression of calm superiority.\n\n"
      + animal_layout("cat", "eyes half closed", "sitting, front view on the left; lying stretched out, left side "
                                                  "profile with the tail clearly visible on the right"),
      "O-K15_kot_1.png"),
]

# ── 4. Предметы ──
PROPS = [
    P("O-P01", "Лаймовая бабочка дедушки (кадры 1, 11)", "А",
      "Object: a classic pre-tied bow tie in vivid lime-green satin (#ADFC30) with a soft sheen, a neat butterfly "
      "shape, on a thin black adjustable neck band with a small metal clasp.\n\n"
      + prop_layout("top-left — front view; top-right — back view with the band and clasp; bottom-left — side view; "
                    "bottom-right — three-quarter view", "the same bow tie"),
      "O-P01_babochka_1.png"),
    P("O-P02", "Стакан в подстаканнике (кадр 1)", "А",
      "Object: a faceted clear tea glass in an ornate nickel-silver tea-glass holder (podstakannik) with a curved "
      "handle and a simple geometric relief pattern, no emblems; the glass is two-thirds full of amber tea with a "
      "teaspoon in it.\n\n"
      + prop_layout("top-left — front view, handle on the right; top-right — back view, handle on the left; "
                    "bottom-left — side view with the handle facing the camera; bottom-right — three-quarter view from "
                    "slightly above", "the same glass in its holder"),
      "O-P02_podstakannik_1.png"),
    P("O-P03", "Противень с пирожками и прихватки (кадр 4)", "А",
      "Object: a dark metal baking tray with twelve golden, glossy, freshly baked Russian pirozhki in neat rows, a "
      "light dusting of flour on the tray rim, and a pair of sky-blue quilted oven mitts (#66A3FF).\n\n"
      + prop_layout("top-left — the tray seen from directly above with the mitts beside it; top-right — the tray from "
                    "the front at eye level; bottom-left — the tray from the side; bottom-right — the tray held in both "
                    "oven mitts, three-quarter view", "the same set"),
      "O-P03_pirozhki_1.png", changed="небесные прихватки."),
    P("O-P04", "Наушники подростка (кадр 3)", "А",
      "Object: large matte-white over-ear headphones with soft light-grey cushions and a plain padded headband, no "
      "logos anywhere.\n\n" + prop_layout(same="the same headphones"),
      "O-P04_naushniki_1.png", changed="белые вместо чёрных."),
    P("O-P05", "Настольный звонок консьержа (кадр 5)", "А",
      "Object: a classic chrome desk call bell with a polished dome and a small plunger on top, on a round black "
      "base.\n\n" + prop_layout(same="the same bell"),
      "O-P05_zvonok_1.png"),
    P("O-P06", "Ковёр (кадр 6)", "А",
      "Object: a wool carpet about 2 × 3 m with a traditional ornamental pattern in cornflower blue, azure, pale ice "
      "blue and cream, fringed short ends, a little worn.\n\n"
      + prop_layout_free("top-left — the carpet laid flat, seen from directly above; top-right — the carpet rolled "
                         "up; bottom-left — the carpet folded in half; bottom-right — the carpet lying flat, "
                         "three-quarter view at eye level"),
      "O-P06_kovyor_1.png", changed="орнамент в синих тонах палитры вместо бордового."),
    P("O-P07", "Выбивалка для ковра (кадр 6)", "А",
      "Object: a traditional carpet beater about 70 cm long, made of twisted rattan, with a looped pretzel-shaped "
      "head and a handle wrapped in rattan strips.\n\n" + prop_layout(same="the same carpet beater"),
      "O-P07_vybivalka_1.png"),
    P("O-P08", "Варежки на резинке (кадр 7)", "А",
      "Object: two pairs of children's knitted mittens, each pair joined by a long knitted string: one pair white "
      "with a cornflower-blue snowflake pattern (#0F7DF5), the other plain lime (#ADFC30); a few snowflakes stuck to "
      "the wool.\n\n"
      + prop_layout_free("top-left — both pairs laid flat, palms down; top-right — both pairs laid flat, palms up; "
                         "bottom-left — one mitten from the side; bottom-right — both pairs hanging by their strings, "
                         "three-quarter view"),
      "O-P08_varezhki_1.png", changed="белые с васильковым узором и лаймовые."),
    P("O-P09", "Пакеты с продуктами (кадр 9)", "А",
      "Object: two full canvas tote bags with no prints: a natural one with a long baguette and green leeks sticking "
      "out, and a cornflower-blue one (#0F7DF5) with red apples and a glass bottle of milk on top.\n\n"
      + prop_layout(same="the same two bags side by side on a studio floor"),
      "O-P09_pakety_1.png", changed="одна сумка васильковая."),
    P("O-P10", "Спицы с вязанием (A1)", "Б",
      "Object: two long wooden knitting needles holding a half-finished piece of pale ice-blue wool knitting "
      "(#DAEEFC), with a ball of the same yarn attached.\n\n" + prop_layout(same="the same knitting"),
      "O-P10_spitsy_1.png", changed="бледно-голубая пряжа."),
    P("O-P11", "Лыжи и палки (A2)", "Б",
      "Object: a pair of classic cross-country skis in a natural varnished wood finish with cornflower-blue bindings "
      "(#0F7DF5), and a pair of light-grey ski poles with leather wrist straps and small round baskets; no logos or "
      "graphics.\n\n"
      + prop_layout("top-left — skis and poles lying flat, seen from above; top-right — the underside of the skis; "
                    "bottom-left — side view, skis standing upright with the poles beside them; bottom-right — "
                    "three-quarter view, skis and poles leaning crossed", "the same skis and poles"),
      "O-P11_lyzhi_1.png", changed="васильковые крепления."),
    P("O-P12", "Скрипка и пюпитр (A3)", "Б",
      "Object: a warm-brown student violin with its bow, and a light-grey folding music stand holding a closed azure "
      "music folder (#1A45D5).\n\n"
      + prop_layout_free("top-left — the violin, front view, with the bow beside it; top-right — the violin, back "
                         "view; bottom-left — the violin, side view; bottom-right — the music stand with the folder, "
                         "three-quarter view"),
      "O-P12_skripka_1.png", changed="светло-серый пюпитр, лазурная папка."),
]

# ── 5. Локации ──
LOCATIONS = [
    P("O-L01", "Дом в разрезе — «кукольный домик» (кадры 1–5)", "А",
      "Image 1 shows the residential quarter; use only the facade of the white-brick tower with graphite vertical "
      "bands for the outer edges of the building.\n\n"
      "Photorealistic architectural cut-away of a modern residential tower at winter blue hour, like a dollhouse with "
      "the whole front wall removed, portrait orientation 2:3, viewed perfectly straight on with a long lens, no "
      "perspective distortion, an empty scene with no people. Thick, deep-black section cuts of walls and floor slabs "
      "divide the building into rooms of equal height. Top floor, left: a cosy living room with pale ice-blue walls "
      "(#DAEEFC) — a caramel-brown leather armchair, a warm floor lamp, bookshelves, framed family photos, a small "
      "spruce with warm lights and baubles in blue and lime, oak parquet. Top floor, right: a nursery with sky-blue "
      "walls (#66A3FF), a white crib and a warm night lamp. One floor down, right: a teenager's room with azure walls "
      "(#1A45D5), a desk with a glowing monitor and a lime desk lamp (#ADFC30). Below that, right: a kitchen with white "
      "cabinets, an oak worktop, a cornflower-blue tiled backsplash (#0F7DF5) and a warm pendant lamp. Ground floor: "
      "a lobby with a pale stone floor, an oak concierge desk, a pale ice-blue wall and glass entrance doors on the "
      "right. The remaining rooms on the left are lived-in flats with warm light and walls in light, calm colours. "
      "Every room has one normal-size window in its back wall — black frame, white sill — with the snowy deep-blue "
      "evening outside. Warm interior light, deep true blacks in the cuts, gentle highlight roll-off, fine film grain. "
      "Clean image: no text, no letters, no numbers, no logos.",
      "O-L01_razrez_doma_1.png", refs=["REF-ZR-A"],
      changed="у каждой комнаты свой цвет из палитры вместо «тёплого» однотона.",
      checks=["❗ срезы стен и перекрытий густо-чёрные и толстые: это наши швы", "❗ людей нет",
              "окна обычного размера, не панорамные", "комнаты разного цвета из палитры, без оранжевого «супа»"]),
    P("O-L02", "Гостиная дедушки (кадры 1, 11)", "А",
      "Image 1 is the cut-away of the building; this is its top-floor living room on the left — keep the furniture and "
      "the colours exactly.\n\n" + plate_text(
          "The cosy top-floor living room seen strictly frontally and planimetrically through the removed front wall, at "
          "the eye height of a seated person: in the centre the caramel-brown leather armchair facing the camera, a "
          "small side table with a lace doily, a warm floor lamp just behind the armchair on the left, bookshelves and a "
          "wall of framed family photos, a small spruce with warm lights and blue and lime baubles in the corner, oak "
          "parquet, pale ice-blue walls (#DAEEFC); in the back wall a normal-size window with a black frame and a white "
          "sill, the snowy deep-blue evening outside. The thick black cut of the wall frames the right edge of the "
          "shot.", PLATE_HOME),
      "O-L02_gostinaya_1.png", refs=["O-L01 (утверждённый разрез)"], changed="бледно-голубые стены."),
    P("O-L03", "Двор зимним вечером (кадры 6–8)", "А",
      "Image 1 shows the buildings at ground level and image 2 the whole quarter from above; keep the architecture "
      "exactly, but turn it into a winter evening.\n\n" + plate_text(
          "An eye-level view across the car-free inner courtyard: the sports court lies under smooth untouched snow; "
          "the playground with curved wooden structures under snow caps, its shade sails taken down for winter; "
          "cleared paving paths lined with neat snowbanks; a spruce in the yard with warm lights and blue and lime "
          "baubles; a sky-blue sled by a bench; warm street lamps; behind, the towers from the references — brown-red "
          "brick with white window surrounds, beige-sand brick with black slatted boxes, white brick with graphite "
          "vertical bands — their normal-size windows glowing warm, and the black steel pergola with a glass roof by "
          "one of the entrances. No cars in the yard.", PLATE_EVE),
      "O-L03_dvor_1.png", refs=["REF-ZR-B", "REF-ZR-C"], changed="ёлка с синими и лаймовыми шарами, небесные санки.",
      checks=["❗ ни машин, ни людей, ни льда для катания"]),
    P("O-L04", "Деревянный мост вечером (кадры 9, 12)", "А",
      "Image 1 shows the wooden pedestrian bridge and the towers behind it; keep the architecture exactly, but turn "
      "it into a winter evening.\n\n" + plate_text(
          "The wooden pedestrian bridge with tall vertical timber slats of different heights on both sides and a plank "
          "deck with a thin layer of fresh snow, small warm lamps set low along the railing, looking along the bridge "
          "towards the towers — beige-sand brick with black slatted boxes and white brick with graphite vertical "
          "bands — their normal-size windows glowing warm.", PLATE_EVE),
      "O-L04_most_1.png", refs=["REF-ZR-A"]),
    P("O-L05", "Белая башня снизу (кадр 10)", "А",
      "Images 1 and 2 show the quarter; this is the white-brick tower with graphite vertical bands — keep its facade "
      "exactly, in winter at blue hour.\n\n" + plate_text(
          "A worm's-eye view from the snowy ground at the very foot of the white-brick tower, an ultra-wide lens about "
          "84° horizontal field of view, looking straight up the facade, which converges dramatically towards the "
          "deep-blue sky; the windows of the lower half glow warm, the upper floors are still dark; snowflakes fly "
          "towards the lens.", FILM_SINGLE + " Winter blue hour, deep-blue sky, warm windows."),
      "O-L05_bashnya_snizu_1.png", refs=["REF-ZR-A", "REF-ZR-B"]),
]

# ── 6. Раскадровка ──
SB1 = board_text(
    "References: image 1 — the grandfather (keep him exactly, with his lime bow tie and azure cardigan); image 2 — "
    "his living room; image 3 — the young mother with the baby; image 4 — the woman in the striped apron; image 5 — "
    "her tray of pirozhki and oven mitts; image 6 — the cut-away of the whole building, showing where each room is.",
    ["1", "2", "3", "4"],
    [
        "The living room from image 2, strictly frontal like a dollhouse, a medium shot, 40 mm lens look, his face "
        "about a third of the frame height: the grandfather from image 1 sits upright in the caramel leather "
        "armchair, a glass of tea in a metal holder on the side table; chin slightly lifted, a steady solemn gaze "
        "just below the camera as if at a TV; his lips press into a straight line under the moustache; he claps "
        "slowly and evenly; no smile. The floor lamp behind his shoulder "
        "draws a warm rim on his white hair; soft light from the TV in front keeps his face readable.",
        "Same floor, the next flat to the right: the left edge of the frame is a thick black band — the cut of the "
        "wall between the flats. The sky-blue nursery: the young mother from image 3 rocks the sleeping baby in the "
        "sling; hearing the clapping through the wall, she glances at the wall — a beat later the corners of her mouth "
        "lift a little, lips closed — and taps two fingers into her palm without a sound; the baby sleeps on. The night lamp beside her warms her hair; her face is softly lit.",
        "One floor down: the top edge of the frame is a thick black band — the cut of the floor slab. The azure "
        "teenager's room with a lime desk lamp: a lanky boy of about fifteen with messy dark-blond hair, in a "
        "cornflower-blue hoodie and big white over-ear headphones with one ear cup slid off, sits at his desk; eyes "
        "still on the monitor, he gives two dry claps; a perfectly flat face, nothing moves but his hands. The monitor lights his face from the front, the lime "
        "lamp rims his hair.",
        "Another floor down, a black slab band at the top: the white kitchen with the cornflower-blue tiles; the woman "
        "from image 4 holds the tray from image 5 in her sky-blue oven mitts, sets it down and claps the mitts "
        "together; a small puff of flour glitters in the light of the pendant lamp; she presses her lips together to "
        "hold back a proud smile, and the corners lift anyway.",
    ], LOOK_HOME)

SB2 = board_text(
    "References: image 1 — the concierge; image 2 — the cut-away of the building (its ground-floor lobby); image 3 — "
    "the man with the carpet beater; image 4 — the carpet; image 5 — the courtyard; image 6 — the dog.",
    ["5", "6", "7", "8"],
    [
        "The ground-floor lobby from image 2 seen frontally, 40 mm lens look: the concierge from image 1 in her azure "
        "cardigan, behind the oak desk, taps a chrome desk bell twice and gives one short approving nod, lips pressed, eyes warm; through the "
        "glass entrance doors behind her, the blue winter courtyard. The right edge of the frame is a dark blurred "
        "band — the cut of the facade wall right at the lens.",
        "The car-free courtyard from image 5 at blue hour, 35 mm lens look: the man from image 3 — open "
        "cornflower-blue puffer, oatmeal sweater, grey felt boots — beats the blue-patterned carpet from image 4, laid "
        "flat on the snow, with his rattan carpet beater; snow dust rises and glitters in the warm lamp light behind "
        "him; behind, the snowy playground and towers with warm windows. A lamp in front keeps his face readable: "
        "focused, eyes on the carpet, a satisfied half-smile just appearing at one corner of his mouth.",
        "At a child's eye height in the same courtyard, 50 mm lens look: two children of about seven face the camera "
        "and clap their mittens — a girl in a sky-blue snowsuit and a white hat with a lime pompom, with freckles and "
        "a missing front tooth, laughing for real, eyes crinkled almost shut; a boy in a cornflower-blue snowsuit, a pale ice-blue "
        "hat and lime mittens, a beat behind her, grinning shyly — the biggest emotion of the film; snow bursts off the mittens like confetti in the lamp light.",
        "A ground-level insert, 85 mm lens look: the dog from image 6 in its lime collar sits on the snow, its plumed "
        "tail sweeping the snow from side to side like a wiper; snow sparkles in the lamplight behind it.",
    ], LOOK_ALL)

SB3 = board_text(
    "References: image 1 — the wooden bridge; image 2 — the young man with grocery bags; image 3 — the young woman; "
    "image 4 — the white goat character from our previous film (keep her exactly: tall and slender, blue aviator "
    "sunglasses, lime scarf); image 5 — the white-brick tower from below; image 6 — the grandfather (keep him "
    "exactly, with his lime bow tie and azure cardigan).",
    ["9", "9b", "10", "11"],
    [
        "The wooden bridge from image 1, tall timber slats blurred in the foreground, 50 mm lens look: the young couple "
        "from images 2 and 3 have stopped; she — pale ice-blue coat, cornflower-blue scarf — claps in her mittens and "
        "laughs into her scarf, eyes crinkling; he — azure parka, sky-blue beanie — hands full with two grocery bags, taps the bags "
        "together, one eyebrow up, amused. Small warm lamps low along the railing light their faces softly from the "
        "front; the windows behind glow warm.",
        "The same shot, and at the far end of the bridge the tall, slender white goat from image 4 — blue aviator "
        "sunglasses, lime knitted scarf — claps her front hooves.",
        "A worm's-eye view from the snowy ground at the foot of the tower from image 5, ultra-wide lens: its windows "
        "are lighting up one by one, floor after floor upward, the wave of warm light nearly at the top; snowflakes "
        "fly towards the lens; deep-blue sky.",
        "The grandfather's living room again, strictly frontal: the grandfather from image 6 now stands, straightening "
        "his lime bow tie in the middle of a final clap, chin lifting a little, with one small dignified nod straight into the lens; warmth in the eyes, "
        "the mouth stays still, no smile. "
        "The floor lamp rims his hair, soft light keeps his face readable, the snowy blue window behind him.",
    ], LOOK_ALL)

SB4 = single_text(
    "References: image 1 — the wooden bridge at winter blue hour; image 2 — the bridge and the towers in the original "
    "render; image 3 — the whole quarter from above. Keep the architecture exactly.",
    "A wide view from the wooden bridge at winter blue hour, 40 mm lens look: the tall timber slats lead the eye to "
    "the right, where the towers of the quarter — the white-brick tower with graphite vertical bands and its "
    "beige-sand brick neighbour — stand in the right half of the frame with warm glowing windows; far below, tiny "
    "figures of residents in bright blue snowsuits and coats in the snowy courtyard; gentle snowfall. The left half "
    "of the frame is a calm, empty deep-blue evening sky above dark snow-covered park trees, with nothing in it.",
    LOOK_EVE)

SB5 = board_text(
    "References: image 1 — the grandmother; image 2 — her knitting; image 3 — the skier; image 4 — his skis and "
    "poles; image 5 — the cat; image 6 — the cut-away of the building, for the look of the rooms.",
    ["A1", "A2", "A3", "A4"],
    [
        "A cosy room of the building from image 6 seen frontally like a dollhouse, a thick black slab band along the "
        "top edge, 40 mm lens look: the grandmother from image 1 in an armchair taps her knitting needles from image 2 "
        "together like applause, peering over her glasses with a faint mischievous look. A lamp beside her rims her "
        "silver hair.",
        "The snowy park of the quarter, a ski track between birches, warm park lamps, 50 mm lens look: the skier from "
        "image 3 has stopped on his skis from image 4 and taps his ski poles together above his head, grinning. A "
        "lamp lights his face softly from the front.",
        "A small room of the same building, seen frontally, 50 mm lens look: a girl of about nine with two neat braids, "
        "in an azure dress over a white turtleneck, stands at a light-grey music stand and plays a short solemn "
        "fanfare on a violin, eyes shut with concentration. A warm desk lamp lights her face from the front.",
        "A windowsill with the snowy blue evening outside, 85 mm lens look: the cat from image 5 lies on the sill with "
        "half-closed eyes, its tail thumping the sill in rhythm. Warm room light on its face from the front.",
    ], LOOK_ALL)

STORYBOARD = [
    P("O-SB1", "Кадры 1–4", "А", SB1, "O-SB1_kadry_01-04_1.png",
      refs=["лист дедушки O-K01", "O-L02 гостиная", "O-K02 мама", "O-K04 хозяйка", "O-P03 пирожки", "O-L01 разрез"],
      note="Подросток описан словами.",
      checks=["❗ дедушка не улыбается, торжественный", "❗ комнаты разных цветов палитры, не оранжевые"]),
    P("O-SB2", "Кадры 5–8", "А", SB2, "O-SB2_kadry_05-08_1.png",
      refs=["O-K05 консьерж", "O-L01 разрез", "O-K06 мужчина с выбивалкой", "O-P06 ковёр", "O-L03 двор", "O-K09 пёс"],
      note="Дети описаны словами."),
    P("O-SB3", "Кадры 9, 9б, 10, 11", "А", SB3, "O-SB3_kadry_09-11_1.png",
      refs=["O-L04 мост", "O-K10 молодой мужчина", "O-K11 молодая женщина", "лист козы N-K01 v2 из «Новосёла»",
            "O-L05 башня снизу", "лист дедушки O-K01"],
      note="Если лист козы v2 из «Новосёла» ещё не утверждён, сделай этот лист позже.",
      checks=["❗ кадр 11: дедушка стоит, кивает в объектив, без улыбки"]),
    P("O-SB4", "Кадр 12, пэкшот", "А", SB4, "O-SB4_kadr_12_pekshot_1.png",
      refs=["O-L04 мост", "REF-ZR-A", "REF-ZR-C"],
      checks=["❗ дома в правой половине; левая половина — пустое небо под титры"]),
    P("O-SB5", "Запасные варианты A1–A4", "Б", SB5, "O-SB5_varianty_A1-A4_1.png",
      refs=["O-K12 бабушка", "O-P10 спицы", "O-K13 лыжник", "O-P11 лыжи", "O-K15 кот", "O-L01 разрез"],
      note="Девочка описана словами."),
]

SECTIONS = [
    ("3. Персонажи",
     "Формат персонажа (как в присланной сетке): слева большой портрет по плечи, справа два роста — анфас и со "
     "спины. Фон ровный серый.", CHARACTERS),
    ("4. Предметы",
     "Формат предмета (как в присланной сетке): 4 ячейки 2×2 на сером фоне — спереди, сзади, сбоку, три четверти. "
     "Там, где ракурсы другие, это сказано в промпте.", PROPS),
    ("5. Локации (пустые фоны, без людей)",
     "Эти фоны станут референсом окружения для раскадровки и Seedance. **Дома точно как на рендерах «Зарядья», "
     "только зимой и вечером.** Порядок: сначала O-L01 (разрез), потом O-L02 с ним в рефах.", LOCATIONS),
    ("6. Раскадровка",
     "Только из утверждённых листов. Каждый лист раскадровки — 4 кадра 2×2. Пэкшот (O-SB4) — один большой кадр.\n\n"
     "Общее для всех кадров:\n"
     "- камера едет **вправо и вниз** по дому, во дворе вправо;\n"
     "- лица читаются, контровой свет рисует силуэт;\n"
     "- лайм — самый яркий акцент на бабочке дедушки.", STORYBOARD),
]


def HEADER(palette_table, export_names=None):
    instr = instructions(
        save_folder="Ролики 2027\\02 Овация\\Листы\\",
        hero_id="O-K01", hero_name="Дедушка",
        special_rules=["Двор без машин. Спортплощадка под ровным снегом, катка нет.",
                       "Лист козы для пасхалки 9б берём из «Новосёла» (N-K01 v2, утверждённый)."],
        order_steps=[
            "**Шаг 2. Основа ролика (приоритет А).**\n"
            "1. Люди O-K02…K11.\n"
            "2. Предметы O-P01…P09.\n"
            "3. Локации: сначала O-L01 (разрез), потом O-L02 с ним в рефах, потом O-L03…L05.\n\n"
            "Покажи все листы одной сводкой и дождись утверждения.",
            "**Шаг 3. Запасные варианты (приоритет Б).**\n"
            "- Сделай всё с пометкой **Б**.\n"
            "- Если ChatGPT упёрся в лимит генераций, остановись и сообщи, что готово, а что нет.",
            "**Шаг 4. Раскадровка.** Только из утверждённых листов: сначала O-SB1…SB4, потом O-SB5.",
        ])
    ps = photostyle()
    pal = palette_section(palette_table)
    sb = f"«{export_names['storyboard']}»" if export_names else "[`storyboard.md`](storyboard.md)"
    return f"""# «Овация»: промпты для ChatGPT, v4

Ролик застройщика «Развитие» для **арт-квартала «Зарядье»**. YouTube, 16:9, 20 секунд, финальная фраза **«Лучший застройщик года»**. Версия v4 от 04.10.2026: игра актёров по разбору эмоций (v3), цвет и фотостиль по пяти стилевым референсам дизайнера (v4).

Это **набор инструкций для Claude в десктоп-приложении**: он генерирует картинки в ChatGPT через браузер дизайнера. Сценарий и раскадровка — {sb}.

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

{ps}
{pal}
{instr}
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
"""


FOOTER = """## 7. После раскадровки

Следующий этап — ключевые кадры (по одному на план) и промпты Seedance 2.0 для «Виви». Это делаем отдельно, после того как дизайнер утвердит раскадровку и выберет варианты.
"""


# v4: стилевые референсы (цвет и свет)
for _sec in SECTIONS:
    for _it in _sec[2]:
        _it['style'] = {'O-L01': 'REF-STYLE-A', 'O-L02': 'REF-STYLE-E', 'O-SB1': 'REF-STYLE-A', 'O-SB2': 'REF-STYLE-A', 'O-SB3': 'REF-STYLE-C', 'O-SB5': 'REF-STYLE-A'}.get(_it['id'])
