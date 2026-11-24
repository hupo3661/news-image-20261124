"""Entry point for the make.fun news-image task (24 November 2026).

The finished picture already sits next to this file as entry.png
(it is drawn by render.py).  This program only writes those exact
bytes to the output folder, so running it twice always produces
exactly the same file.  It never touches the network.
"""

import os
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
# The finished entry image is a fixed asset: guard against a truncated,
# swapped or corrupt file being copied to the output folder unnoticed.
MIN_PNG_BYTES = 10_000
MAX_PNG_BYTES = 5_000_000


def target_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    folder = Path(out_dir) if out_dir else Path("/output")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.png"


def validate_png(data):
    """Check the source image exists as a sane PNG before copying it.

    Verifies the PNG signature, a plausible file size, and that the IHDR
    chunk carries positive pixel dimensions. Any failure aborts with a
    clear message instead of silently shipping a broken entry image.
    """
    if not SOURCE.is_file():
        raise SystemExit(f"{SOURCE} is missing, refusing to copy")
    if not data.startswith(PNG_MAGIC):
        raise SystemExit(f"{SOURCE} is not a PNG file, refusing to copy")
    if not MIN_PNG_BYTES <= len(data) <= MAX_PNG_BYTES:
        raise SystemExit(
            f"{SOURCE} has unexpected size {len(data)} bytes "
            f"(expected {MIN_PNG_BYTES}-{MAX_PNG_BYTES}), refusing to copy"
        )
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise SystemExit(f"{SOURCE} has no IHDR chunk, refusing to copy")
    width, height = struct.unpack(">II", data[16:24])
    if width <= 0 or height <= 0:
        raise SystemExit(
            f"{SOURCE} has invalid dimensions {width}x{height}, refusing to copy"
        )
    print(
        f"validated {SOURCE.name}: {width}x{height}px, {len(data)} bytes",
        file=sys.stderr,
    )
    return width, height


def main():
    data = SOURCE.read_bytes()
    validate_png(data)
    target = target_path()
    target.write_bytes(data)
    print(f"wrote {target} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
