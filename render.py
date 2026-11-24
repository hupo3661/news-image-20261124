"""Renderer for a single-page world-news poster dated 24 November 2026.

Executing this module produces ``entry.png`` beside it.  The page is
assembled from small declarative tables below -- masthead lines, the
lead story, its fact panel and the numbered briefs -- and one drawing
pass walks those tables in order, so the output stays reproducible.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# --- locations ---------------------------------------------------------
MODULE_DIR = Path(__file__).resolve().parent
TARGET_PATH = MODULE_DIR / "entry.png"
TYPE_DIR = Path("/usr/share/fonts/truetype/dejavu")
TYPE_PLAIN = str(TYPE_DIR / "DejaVuSans.ttf")
TYPE_STRONG = str(TYPE_DIR / "DejaVuSans-Bold.ttf")
TYPE_SERIF_STRONG = str(TYPE_DIR / "DejaVuSerif-Bold.ttf")

# --- geometry and palette ----------------------------------------------
CANVAS_W = 1024
CANVAS_H = 1024
MARGIN_LEFT = 52
CONTENT_RIGHT = 972
CONTENT_WIDTH = 920

COLOUR_PAGE = (250, 246, 236)
COLOUR_TEXT = (22, 22, 22)
COLOUR_MUTED = (96, 92, 82)
COLOUR_ACCENT = (178, 34, 34)
COLOUR_PANEL = (16, 58, 96)
COLOUR_RULE_GOLD = (198, 140, 28)
COLOUR_ROW_SHADE = (240, 235, 220)
COLOUR_BRIGHT = (255, 255, 255)
COLOUR_PALE_GOLD = (255, 226, 140)
COLOUR_SEA = (120, 190, 210)

# --- copy tables ---------------------------------------------------------
# Each masthead entry: (vertical position, wording, typeface, size, colour).
MASTHEAD_LINES = (
    (32, "THE  WORLD  TODAY", TYPE_SERIF_STRONG, 34, COLOUR_TEXT),
    (76, "Tuesday  24 November 2026", TYPE_STRONG, 46, COLOUR_ACCENT),
    (132, "The day's world news on one page", TYPE_PLAIN, 23, COLOUR_MUTED),
)

LEAD_KICKER = "1  \u2022  STRAIT OF HORMUZ"
LEAD_HEADLINE = "25 seafarers dead, UN counts the toll"
LEAD_SUMMARY = (
    "The United Nations counts 25 seafarers killed around the "
    "vital waterway as the standoff over the strait deepens."
)

# Fact lines printed inside the lead panel, top to bottom.
PANEL_FACTS = (
    "UN toll: 25 seafarers killed",
    "Around the Strait of Hormuz",
    "Diplomacy stalled as tensions rise",
)
PANEL_BOX = (52, 348, 972, 470)

# Numbered briefs below the lead: (number, section label, body copy).
BRIEF_ROWS = (
    (2, "INDIA \u2014 NEPAL",
     "India pledges $1.6 billion to help Nepal rebuild after the "
     "floods, and the two prime ministers flag off the new "
     "Saryu-Kamala Express train."),
    (3, "TECH \u2014 NVIDIA",
     "Jensen Huang returns as Nvidia chief, just 11 days after "
     "stepping down amid a 'spy' controversy."),
    (4, "BALTIC \u2014 GULF OF FINLAND",
     "Russian cargo ship Sparta II catches fire after a drone "
     "attack off the coast of Finland."),
    (5, "FOOTBALL \u2014 AFCON 2025",
     "The Africa Cup title hangs on a court ruling: CAS decides "
     "Senegal's appeal against Morocco on Tuesday."),
    (6, "PORTUGAL \u2014 LISBON",
     "Thousands march in Lisbon against the rising cost of "
     "living, as protests over prices spread."),
)
BRIEF_FIRST_TOP = 482
BRIEF_ROW_HEIGHT = 90

SPORT_LINE = "SPORT  \u2022  World Chess Championship opens in Geneva."
FOOTER_LINE = (
    "Sources: Reuters  \u2022  AFP  \u2022  Ukrinform  \u2022  "
    "The Straits Times  \u2022  One page, no exaggeration."
)


def load_typeface(path, size):
    """Return a TrueType face for ``path`` at ``size`` points."""
    return ImageFont.truetype(path, size)


def wrap_copy(draw, wording, face, max_width):
    """Split ``wording`` greedily so no line exceeds ``max_width``."""
    lines = []
    pending = ""
    for token in wording.split():
        candidate = token if not pending else pending + " " + token
        if draw.textlength(candidate, font=face) <= max_width:
            pending = candidate
        else:
            if pending:
                lines.append(pending)
            pending = token
    if pending:
        lines.append(pending)
    return lines


def stamp_paragraph(draw, left, top, wording, face, colour, max_width, leading):
    """Draw wrapped copy starting at (left, top); return the next free y."""
    cursor_y = top
    for line in wrap_copy(draw, wording, face, max_width):
        draw.text((left, cursor_y), line, font=face, fill=colour)
        cursor_y += leading
    return cursor_y


def stamp_centred(draw, top, wording, face, colour):
    """Draw one line centred horizontally on the canvas."""
    text_w = draw.textlength(wording, font=face)
    draw.text(((CANVAS_W - text_w) / 2, top), wording, font=face, fill=colour)


def paint_lead_panel(draw):
    """Paint the navy lead panel: ship shapes, wave lines and fact copy."""
    box_left, box_top, box_right, box_bottom = PANEL_BOX
    draw.rounded_rectangle(
        [box_left, box_top, box_right, box_bottom], radius=16, fill=COLOUR_PANEL
    )
    # Ship silhouette: hull first, then its stacked cargo and funnel.
    draw.polygon(
        [(96, 432), (260, 432), (238, 452), (118, 452)], fill=COLOUR_ACCENT
    )
    cargo_blocks = (
        ([112, 404, 150, 432], COLOUR_PALE_GOLD),
        ([156, 412, 194, 432], COLOUR_BRIGHT),
        ([200, 404, 238, 432], COLOUR_SEA),
    )
    for block_box, block_colour in cargo_blocks:
        draw.rectangle(block_box, fill=block_colour)
    draw.rectangle([216, 388, 238, 404], fill=COLOUR_TEXT)
    # Two zig-zag wave strokes sit low in the panel, clear of the facts.
    for wave_y in (456, 462):
        wave_points = []
        for wave_x in range(96, 288, 24):
            offset = 6 if (wave_x // 24) % 2 else -6
            wave_points.append((wave_x, wave_y + offset))
        draw.line(wave_points, fill=COLOUR_SEA, width=3)
    fact_face = load_typeface(TYPE_STRONG, 24)
    fact_y = box_top + 18
    for fact in PANEL_FACTS:
        draw.text((300, fact_y), fact, font=fact_face, fill=COLOUR_PALE_GOLD)
        fact_y += 38


def paint_brief_row(draw, top, number, label, body):
    """Paint one numbered brief: optional shading, badge, label and body."""
    if number % 2 == 0:
        draw.rectangle(
            [36, top, 988, top + BRIEF_ROW_HEIGHT], fill=COLOUR_ROW_SHADE
        )
    badge_cx, badge_cy = 80, top + 45
    draw.ellipse(
        [badge_cx - 25, badge_cy - 25, badge_cx + 25, badge_cy + 25],
        fill=COLOUR_ACCENT,
    )
    badge_face = load_typeface(TYPE_STRONG, 27)
    numeral = str(number)
    numeral_w = draw.textlength(numeral, font=badge_face)
    draw.text(
        (badge_cx - numeral_w / 2, badge_cy - 15),
        numeral,
        font=badge_face,
        fill=COLOUR_BRIGHT,
    )
    draw.text(
        (122, top + 6), label,
        font=load_typeface(TYPE_STRONG, 23), fill=COLOUR_TEXT,
    )
    stamp_paragraph(
        draw, 122, top + 34, body,
        load_typeface(TYPE_PLAIN, 23), COLOUR_TEXT, 846, 26,
    )


def assemble_page():
    """Compose the whole poster and return it as an RGB image."""
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), COLOUR_PAGE)
    pen = ImageDraw.Draw(canvas)

    pen.rectangle(
        [14, 14, CANVAS_W - 14, CANVAS_H - 14], outline=COLOUR_TEXT, width=3
    )
    for line_top, line_text, line_path, line_size, line_colour in MASTHEAD_LINES:
        stamp_centred(
            pen, line_top, line_text,
            load_typeface(line_path, line_size), line_colour,
        )
    pen.rectangle([52, 166, 972, 172], fill=COLOUR_ACCENT)

    # Lead story block, in reading order: kicker, headline, summary, panel.
    pen.text(
        (MARGIN_LEFT, 186), LEAD_KICKER,
        font=load_typeface(TYPE_STRONG, 25), fill=COLOUR_PANEL,
    )
    stamp_paragraph(
        pen, MARGIN_LEFT, 216, LEAD_HEADLINE,
        load_typeface(TYPE_SERIF_STRONG, 42), COLOUR_TEXT, CONTENT_WIDTH, 50,
    )
    stamp_paragraph(
        pen, MARGIN_LEFT, 272, LEAD_SUMMARY,
        load_typeface(TYPE_PLAIN, 24), COLOUR_TEXT, CONTENT_WIDTH, 29,
    )
    paint_lead_panel(pen)

    # The briefs share one vertical rhythm; the sport strip follows them.
    row_top = BRIEF_FIRST_TOP
    for row_number, row_label, row_body in BRIEF_ROWS:
        paint_brief_row(pen, row_top, row_number, row_label, row_body)
        row_top += BRIEF_ROW_HEIGHT
    pen.rectangle(
        [MARGIN_LEFT, row_top + 2, CONTENT_RIGHT, row_top + 8],
        fill=COLOUR_RULE_GOLD,
    )
    pen.text(
        (MARGIN_LEFT, row_top + 16), SPORT_LINE,
        font=load_typeface(TYPE_STRONG, 23), fill=COLOUR_PANEL,
    )
    pen.text(
        (MARGIN_LEFT, 978), FOOTER_LINE,
        font=load_typeface(TYPE_PLAIN, 20), fill=COLOUR_MUTED,
    )
    return canvas


def run():
    """Render the poster, save it as PNG and report what was written."""
    poster = assemble_page()
    poster.save(TARGET_PATH, format="PNG", optimize=True)
    byte_count = TARGET_PATH.stat().st_size
    print(f"wrote {TARGET_PATH} ({byte_count} bytes)")
    print(
        f"diagnostic: rendered {TARGET_PATH.name}: "
        f"{poster.size[0]}x{poster.size[1]}px, {byte_count} bytes",
        file=sys.stderr,
    )


if __name__ == "__main__":
    run()
