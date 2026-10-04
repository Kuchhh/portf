#!/usr/bin/env python3
"""Собирает файлы-инструкции для ChatGPT (листы и раскадровка) из спецификаций роликов.

Запуск:
    python3 video-projects/_kit/build_prompts.py [--export ПАПКА]

Для каждой папки ролика со spec.py пишет gpt-prompts.md. С --export кладёт в ПАПКУ
копии с понятными именами (Промпты_…, Сториборд_…), ссылки внутри поправлены.

Общие блоки (раскладки листов, фотостиль, палитра) живут здесь, в одном месте:
правка блока меняет все промпты обоих роликов.
"""
import argparse
import importlib.util
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent  # video-projects/

# ── Палитра бренда (HEX сняты с картинки палитры, лайм и васильковый сверены с баннером) ──
PALETTE = [
    ("Зелёно-жёлтый (лайм)", "#ADFC30", "lime"),
    ("Васильковый", "#0F7DF5", "cornflower blue"),
    ("Лазурный", "#1A45D5", "azure"),
    ("Небесный", "#66A3FF", "sky blue"),
    ("«Синий» (на палитре — самый светлый голубой)", "#DAEEFC", "pale ice blue"),
    ("Светлый (без подписи)", "#F4F8FC", "near-white"),
]

CLEAN = "Clean image: no text, no letters, no labels, no logos, no watermarks."

# ── Общие блоки фотостиля ──
FILM = (
    "Each still is a real film frame, shot on an ARRI Alexa 35 with Cooke prime lenses and graded like a "
    "modern premium Russian TV commercial: photographic and alive, natural exposure, gentle highlight "
    "roll-off, deep but not crushed blacks, fine film grain, shallow depth of field with a soft but "
    "recognisable background, foreground layers where natural."
)
FILM_SINGLE = FILM.replace("Each still is", "It is")
PEOPLE = (
    "People are real, characterful and unglamorous, with natural skin texture; each face is caught in the "
    "middle of one small reaction, described below by what the brows, eyes and mouth do — never a posed "
    "expression; the eyes react first, the mouth follows; smiles are closed-lip and small unless stated; "
    "nobody looks into the lens unless stated; people around react out of sync, not together."
)


def person_layout(who, pose="standing naturally, arms relaxed"):
    if who in ("boy", "girl"):
        skin = "natural skin texture, real child proportions, flyaway hairs"
    else:
        skin = "natural skin texture with pores, fine lines and small imperfections, flyaway hairs"
    return (
        "Character reference sheet for a live-action TV commercial, 16:9 landscape. Layout: the left 45% of "
        "the sheet is a large head-and-shoulders portrait, face to camera; a thin black vertical line "
        f"separates it from the right part, where the same {who} stands full length twice at the same scale, "
        "with a little space above the head and below the feet — front view on the left, back view on the "
        f"right, {pose}. Seamless neutral mid-grey studio backdrop, soft light from a large softbox, a soft "
        f"contact shadow under the feet. Photographed like a real casting photo of a real {who}: {skin}, "
        "true-to-life fabrics with real creases, accurate garment colours, no retouching gloss. " + CLEAN
    )


def animal_layout(animal, portrait, views):
    return (
        "Animal reference sheet for a live-action TV commercial, 16:9 landscape. Layout: the left 45% of the "
        f"sheet is a large head portrait facing the camera, {portrait}; a thin black vertical line separates it "
        f"from the right part, where the same {animal} is shown full body twice at the same scale — {views}. "
        "Seamless neutral mid-grey studio backdrop, soft light from a large softbox, soft contact shadows. "
        f"Photographed like a real animal portrait: a real {animal}, true-to-life fur and natural colours. " + CLEAN
    )


DEFAULT_CELLS = (
    "top-left — front view; top-right — back view; bottom-left — side view; "
    "bottom-right — three-quarter view from slightly above"
)


def prop_layout(cells=None, same="the same object"):
    return (
        "Product reference sheet for a live-action TV commercial, 16:9 landscape, split into four equal cells by "
        f"thin white lines (a 2×2 grid). In every cell {same} on a seamless neutral mid-grey studio backdrop, soft "
        "even studio light, a soft contact shadow, centred and fully visible at the same scale: "
        f"{cells or DEFAULT_CELLS}. Photographed like a real product shot: true-to-life materials with real wear, "
        "accurate colours. Clean image: no text, no letters, no labels, no logos, no brand marks, no watermarks."
    )


def prop_layout_free(cells):
    """Четыре ячейки с разными состояниями предмета (шарф, гирлянда и т. п.)."""
    return (
        "Product reference sheet for a live-action TV commercial, 16:9 landscape, split into four equal cells by "
        "thin white lines (a 2×2 grid), every cell on a seamless neutral mid-grey studio backdrop with soft even "
        f"studio light and a soft contact shadow: {cells}. Photographed like a real product shot: true-to-life "
        "materials, accurate colours. Clean image: no text, no letters, no labels, no logos, no watermarks."
    )


def plate_text(desc, look):
    return (
        "Photorealistic location plate for a live-action TV commercial, 16:9 landscape, an empty scene with no "
        f"people.\n\n{desc}\n\n{look} " + "Clean image: no text, no letters, no numbers, no logos, no signs."
    )


def board_text(refs_intro, labels, panels, look, layout="grid"):
    n = len(panels)
    words = {3: "three", 4: "four"}[n]
    if layout == "grid":
        frame = f"{words} film stills from the same live-action TV commercial in a 2×2 grid"
    else:  # stack
        frame = f"{words} film stills from the same live-action TV commercial stacked vertically in a portrait sheet"
    head = (
        f"Storyboard sheet: {frame}, each still 16:9, separated by thin white gutters, with a small white label "
        f"in the top-left corner of each still ({', '.join(labels)}) and no other text."
    )
    body = "\n\n".join(f"{lab} — {txt}" for lab, txt in zip(labels, panels))
    return f"{refs_intro}\n\n{head}\n\n{FILM} {look}\n\n{PEOPLE}\n\n{body}"


def single_text(refs_intro, desc, look):
    return (
        f"{refs_intro}\n\nA single film still — the final shot of a live-action TV commercial, 16:9 landscape.\n\n"
        f"{FILM_SINGLE} {look}\n\n{PEOPLE}\n\n{desc} Clean image: no text, no letters, no logos."
    )


# ── Сборка markdown ──

def render_item(it, stage_files):
    lines = []
    head = f"### {it['id']} · {it['title']} · {it['prio']}"
    if it.get("runs", 1) > 1:
        head += f" · {it['runs']} генерации"
    lines.append(head)
    lines.append("")
    refs = it.get("refs") or []
    if refs:
        lines.append("- **Рефы** (строго в этом порядке):")
        for i, r in enumerate(refs, 1):
            lines.append(f"  {i}. {r}")
    else:
        lines.append("- **Рефы:** без рефов.")
    lines.append(f"- **Файл:** `{it['file']}`")
    if it.get("changed"):
        lines.append(f"- **Что изменилось с v1:** {it['changed']}")
    if it.get("reuse"):
        lines.append(
            f"- ♻️ **Можно взять из v1:** `{it['reuse']}`, если дизайнер его одобрил. Тогда не генерируй. "
            "Иначе — генерация по промпту ниже."
        )
    if it.get("note"):
        lines.append(f"- {it['note']}")
    lines.append("")
    lines.append("```text")
    lines.append(it["prompt"].strip())
    lines.append("```")
    if it.get("checks"):
        lines.append("")
        lines.append("**Проверить:**")
        for c in it["checks"]:
            lines.append(f"- {c}")
    lines.append("")
    return "\n".join(lines)


def validate(spec):
    seen_ids, seen_files, errors = set(), set(), []
    for _, _, items in spec.SECTIONS:
        for it in items:
            if it["id"] in seen_ids:
                errors.append(f"повтор кода {it['id']}")
            seen_ids.add(it["id"])
            if it["file"] in seen_files:
                errors.append(f"повтор файла {it['file']}")
            seen_files.add(it["file"])
            refs = it.get("refs") or []
            if len(refs) > 6:
                errors.append(f"{it['id']}: рефов {len(refs)} > 6")
            used = [int(x) for x in re.findall(r"\bimages? (\d+)", it["prompt"], re.I)]
            used += [int(x) for x in re.findall(r"\bimages \d+ and (\d+)", it["prompt"], re.I)]
            used += [int(b) for a, b in re.findall(r"\bimages (\d+)[–-](\d+)", it["prompt"], re.I)]
            if used and max(used) > len(refs):
                errors.append(f"{it['id']}: в промпте image {max(used)}, а рефов {len(refs)}")
            if not refs and re.search(r"\bimage \d", it["prompt"], re.I):
                errors.append(f"{it['id']}: упомянут image, а рефов нет")
    if errors:
        sys.exit("Ошибки в спецификации:\n  " + "\n  ".join(errors))
    return len(seen_ids)


def palette_table():
    rows = ["| Цвет (как в палитре) | HEX | В промптах |", "|---|---|---|"]
    for name, hx, en in PALETTE:
        rows.append(f"| {name} | `{hx}` | {en} |")
    return "\n".join(rows)


def build(spec, export_names=None):
    n = validate(spec)
    parts = [spec.HEADER(palette_table(), export_names)]
    for title, intro, items in spec.SECTIONS:
        parts.append(f"## {title}\n")
        if intro:
            parts.append(intro.strip() + "\n")
        for it in items:
            parts.append(render_item(it, None))
        parts.append("---\n")
    parts.append(spec.FOOTER)
    return "\n".join(parts).rstrip() + "\n", n


def load_spec(path):
    s = importlib.util.spec_from_file_location(f"spec_{path.parent.name}", path)
    m = importlib.util.module_from_spec(s)
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    s.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", help="папка для копий с русскими именами")
    args = ap.parse_args()
    for spec_path in sorted(ROOT.glob("*/spec.py")):
        spec = load_spec(spec_path)
        md, n = build(spec)
        out = spec_path.parent / "gpt-prompts.md"
        out.write_text(md, encoding="utf-8")
        print(f"{out.relative_to(ROOT.parent)}: {n} промптов")
        if args.export:
            exp = pathlib.Path(args.export)
            exp.mkdir(parents=True, exist_ok=True)
            names = spec.EXPORT
            md_e, _ = build(spec, names)
            (exp / names["prompts"]).write_text(md_e, encoding="utf-8")
            sb = (spec_path.parent / "storyboard.md").read_text(encoding="utf-8")
            sb = sb.replace("[`gpt-prompts.md`](gpt-prompts.md)", f"«{names['prompts']}»")
            sb = re.sub(r"\[`video-research/director-style\.md`\]\([^)]*\)",
                        "`video-research/director-style.md` в репозитории", sb)
            (exp / names["storyboard"]).write_text(sb, encoding="utf-8")
            print(f"  → {names['prompts']}, {names['storyboard']}")


if __name__ == "__main__":
    main()
