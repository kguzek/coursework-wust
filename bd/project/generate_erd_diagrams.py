import re
from pathlib import Path

# pylint: disable=line-too-long


RELATIONSHIPS = [
    ("Posiada", "LINIA", "(1,1)", "TRASA", "(0,N)"),
    ("ObowiazujeW", "LINIA", "(1,1)", "ROZKLAD", "(0,N)"),
    ("Zawiera", "ROZKLAD", "(1,1)", "KURS", "(0,N)"),
    ("Realizuje", "TRASA", "(1,1)", "KURS", "(0,N)"),
    ("Obejmuje", "KURS", "(1,1)", "PRZYDZIAL", "(0,1)"),
    ("Wykonuje", "MOTORNICZY", "(1,1)", "PRZYDZIAL", "(0,N)"),
    ("Uzywa", "TRAMWAJ", "(1,1)", "PRZYDZIAL", "(0,N)"),
    ("ZawieraP", "TRASA", "(1,1)", "POSTOJ", "(0,N)"),
    ("NalezyDo", "PRZYSTANEK", "(1,1)", "POSTOJ", "(0,N)"),
    ("TworzyM", "MOTORNICZY", "(0,1)", "ZGLOSZENIE", "(0,N)"),
    ("TworzyD", "DYSPOZYTOR", "(0,1)", "ZGLOSZENIE", "(0,N)"),
    ("DotyczyK", "KURS", "(0,1)", "ZGLOSZENIE", "(0,N)"),
    ("DotyczyTr", "TRAMWAJ", "(0,1)", "ZGLOSZENIE", "(0,N)"),
    ("Nadzoruje", "ZARZADCA", "(0,N)", "DYSPOZYTOR", "(1,1)"),
]


def safe_filename(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def text_element(
    text: str, x: int, y: int, size: int = 18, weight: str = "normal"
) -> str:
    return (
        f'<text x="{x}" y="{y}" text-anchor="middle" '
        f'font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}">'
        f"{text}</text>"
    )


def create_svg(
    name: str, left_entity: str, left_card: str, right_entity: str, right_card: str
) -> str:
    width = 1000
    height = 260

    left_box = (60, 90, 220, 80)
    diamond_center = (500, 130)
    diamond_width = 220
    diamond_height = 110
    right_box = (720, 90, 220, 80)

    diamond_points = [
        (diamond_center[0], diamond_center[1] - diamond_height // 2),
        (diamond_center[0] + diamond_width // 2, diamond_center[1]),
        (diamond_center[0], diamond_center[1] + diamond_height // 2),
        (diamond_center[0] - diamond_width // 2, diamond_center[1]),
    ]
    diamond_points_str = " ".join(f"{x},{y}" for x, y in diamond_points)

    left_line_start = (left_box[0] + left_box[2], 130)
    left_line_end = (diamond_center[0] - diamond_width // 2, 130)
    right_line_start = (diamond_center[0] + diamond_width // 2, 130)
    right_line_end = (right_box[0], 130)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="white"/>

  <rect x="{left_box[0]}" y="{left_box[1]}" width="{left_box[2]}" height="{left_box[3]}" fill="#f7fbff" stroke="#111" stroke-width="2"/>
  {text_element(left_entity, left_box[0] + left_box[2] // 2, 138, 20, "bold")}

  <line x1="{left_line_start[0]}" y1="{left_line_start[1]}" x2="{left_line_end[0]}" y2="{left_line_end[1]}" stroke="#111" stroke-width="2"/>
  {text_element(left_card, (left_line_start[0] + left_line_end[0]) // 2, 105, 18, "bold")}

  <polygon points="{diamond_points_str}" fill="#fff8e8" stroke="#111" stroke-width="2"/>
  {text_element(name, diamond_center[0], 138, 18, "bold")}

  <line x1="{right_line_start[0]}" y1="{right_line_start[1]}" x2="{right_line_end[0]}" y2="{right_line_end[1]}" stroke="#111" stroke-width="2"/>
  {text_element(right_card, (right_line_start[0] + right_line_end[0]) // 2, 105, 18, "bold")}

  <rect x="{right_box[0]}" y="{right_box[1]}" width="{right_box[2]}" height="{right_box[3]}" fill="#f7fbff" stroke="#111" stroke-width="2"/>
  {text_element(right_entity, right_box[0] + right_box[2] // 2, 138, 20, "bold")}
</svg>
'''


def main() -> None:
    output_dir = Path("erd_diagrams")
    output_dir.mkdir(exist_ok=True)

    for index, relationship in enumerate(RELATIONSHIPS, start=1):
        name, left_entity, left_card, right_entity, right_card = relationship
        svg = create_svg(name, left_entity, left_card, right_entity, right_card)
        filename = f"ZWI_{index:03d}_{safe_filename(name)}.svg"
        (output_dir / filename).write_text(svg, encoding="utf-8")

    print(f"Wygenerowano {len(RELATIONSHIPS)} diagramow w katalogu: {output_dir}")


if __name__ == "__main__":
    main()
