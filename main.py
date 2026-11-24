"""Entry point for the make.fun news-image task (24 November 2026).

The finished picture already sits next to this file as entry.png
(it is drawn by render.py).  This program only writes those exact
bytes to the output folder, so running it twice always produces
exactly the same file.  It never touches the network.
"""

import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def target_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    folder = Path(out_dir) if out_dir else Path("/output")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.png"


def main():
    data = SOURCE.read_bytes()
    target = target_path()
    target.write_bytes(data)
    print(f"wrote {target} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
