"""Draw the one-page world news summary for Tuesday 24 November 2026.

Running this file creates entry.png next to it: a newspaper front
page with one lead story (a simple ship-and-waves graphic) and five
short numbered stories plus a sport note.  All text, colours and
coordinates are fixed, so the drawing is fully deterministic.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT_FILE = HERE / "entry.png"

W = 1024
H = 1024

PAPER = (250, 246, 236)
INK = (22, 22, 22)
GREY = (96, 92, 82)
RED = (178, 34, 34)
NAVY = (16, 58, 96)
AMBER = (198, 140, 28)
ALT = (240, 235, 220)
WHITE = (255, 255, 255)
CREAM = (255, 226, 140)

FONTS = Path("/usr/share/fonts/truetype/dejavu")
SANS = str(FONTS / "DejaVuSans.ttf")
SANS_B = str(FONTS / "DejaVuSans-Bold.ttf")
SERIF_B = str(FONTS / "DejaVuSerif-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_lines(draw, text, fnt, width):
    """Greedy word wrap into lines no wider than width pixels."""
    out = []
    cur = ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def para(draw, x, y, text, fnt, fill, width, step):
    for line in fit_lines(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def centre(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)


def lead_graphic(draw):
    """Strait of Hormuz: a small cargo ship on waves, dark navy panel."""
    x0, y0, x1, y1 = 52, 348, 972, 470
    draw.rounded_rectangle([x0, y0, x1, y1], radius=16, fill=NAVY)
    # hull
    draw.polygon([(96, 432), (260, 432), (238, 452), (118, 452)], fill=RED)
    # containers
    draw.rectangle([112, 404, 150, 432], fill=CREAM)
    draw.rectangle([156, 412, 194, 432], fill=WHITE)
    draw.rectangle([200, 404, 238, 432], fill=(120, 190, 210))
    # funnel
    draw.rectangle([216, 388, 238, 404], fill=INK)
    # waves, kept under the ship so they never touch the fact lines
    for yy in (456, 462):
        pts = []
        for xx in range(96, 288, 24):
            pts.append((xx, yy + (6 if (xx // 24) % 2 else -6)))
        draw.line(pts, fill=(120, 190, 210), width=3)
    facts = [
        "UN toll: 25 seafarers killed",
        "Around the Strait of Hormuz",
        "Diplomacy stalled as tensions rise",
    ]
    fy = y0 + 18
    ff = font(SANS_B, 24)
    for line in facts:
        draw.text((300, fy), line, font=ff, fill=CREAM)
        fy += 38


def brief(draw, top, num, tag, text):
    """One numbered story row."""
    if num % 2 == 0:
        draw.rectangle([36, top, 988, top + 90], fill=ALT)
    cx, cy = 80, top + 45
    draw.ellipse([cx - 25, cy - 25, cx + 25, cy + 25], fill=RED)
    bf = font(SANS_B, 27)
    label = str(num)
    lw = draw.textlength(label, font=bf)
    draw.text((cx - lw / 2, cy - 15), label, font=bf, fill=WHITE)
    draw.text((122, top + 6), tag, font=font(SANS_B, 23), fill=INK)
    para(draw, 122, top + 34, text, font(SANS, 23), INK, 846, 26)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([14, 14, W - 14, H - 14], outline=INK, width=3)
    centre(d, 32, "THE  WORLD  TODAY", font(SERIF_B, 34), INK)
    centre(d, 76, "Tuesday  24 November 2026", font(SANS_B, 46), RED)
    centre(d, 132, "The day's world news on one page",
           font(SANS, 23), GREY)
    d.rectangle([52, 166, 972, 172], fill=RED)
    d.text((52, 186), "1  \u2022  STRAIT OF HORMUZ",
           font=font(SANS_B, 25), fill=NAVY)
    para(d, 52, 216, "25 seafarers dead, UN counts the toll",
         font(SERIF_B, 42), INK, 920, 50)
    para(d, 52, 272,
         "The United Nations counts 25 seafarers killed around the "
         "vital waterway as the standoff over the strait deepens.",
         font(SANS, 24), INK, 920, 29)
    lead_graphic(d)
    stories = [
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
    ]
    y = 482
    for num, tag, text in stories:
        brief(d, y, num, tag, text)
        y += 90
    d.rectangle([52, y + 2, 972, y + 8], fill=AMBER)
    d.text((52, y + 16),
           "SPORT  \u2022  World Chess Championship opens in Geneva.",
           font=font(SANS_B, 23), fill=NAVY)
    d.text((52, 978),
           "Sources: Reuters  \u2022  AFP  \u2022  Ukrinform  \u2022  "
           "The Straits Times  \u2022  One page, no exaggeration.",
           font=font(SANS, 20), fill=GREY)
    return img


def main():
    page = build()
    page.save(OUT_FILE, format="PNG", optimize=True)
    print(f"wrote {OUT_FILE} ({OUT_FILE.stat().st_size} bytes)")
    print(
        f"diagnostic: rendered {OUT_FILE.name}: "
        f"{page.size[0]}x{page.size[1]}px, {OUT_FILE.stat().st_size} bytes",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
