# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/hupo3661/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/hupo3661/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# The World Today — Tuesday 24 November 2026

A single picture that sums up the world news of Tuesday
24 November 2026, drawn as a clean newspaper front page
that stays readable even when shrunk to 300 pixels wide.

## What is on the page

- **Headline — Strait of Hormuz.** The United Nations counts
  25 seafarers killed around the vital waterway as the
  standoff over the strait deepens.
- **2 — India / Nepal.** India pledges $1.6 billion to help
  Nepal rebuild after the floods, and the two prime ministers
  flag off the new Saryu-Kamala Express train.
- **3 — Tech / Nvidia.** Jensen Huang returns as Nvidia chief,
  just 11 days after stepping down amid a "spy" controversy.
- **4 — Baltic / Gulf of Finland.** Russian cargo ship Sparta II
  catches fire after a drone attack off the coast of Finland.
- **5 — Football / AFCON 2025.** The Africa Cup title hangs on
  a court ruling: CAS decides Senegal's appeal against
  Morocco on Tuesday.
- **6 — Portugal / Lisbon.** Thousands march in Lisbon against
  the rising cost of living, as protests over prices spread.
- **Sport note.** The World Chess Championship opens in Geneva.

Sources shown on the picture itself: Reuters / AFP, Ukrinform
and The Straits Times.

## Run it

```sh
python3 main.py
```

- `render.py` draws `entry.png` (1024 x 1024) with Pillow and
  the DejaVu fonts. All text, colours and positions are fixed,
  so the drawing is deterministic.
- `main.py` is the program the platform runs. It copies the
  bundled `entry.png` byte for byte into the folder named by
  the `MAKEFUN_OUTPUT_DIR` environment variable (or `/output`
  when that variable is not set). Running it twice therefore
  gives exactly the same bytes both times.
- No network access is used anywhere.

## Rebuild the picture

```bash
python3 render.py
python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=7zv3mt0w&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
