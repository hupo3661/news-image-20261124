"""Ship the finished news image to the make.fun output folder.

The artwork itself is produced by ``render.py`` and stored beside this
file as ``entry.png``.  This entry point is deliberately boring: it
sanity-checks those bytes as a PNG, then copies them verbatim to the
destination folder, so repeated runs always deliver the identical
file.  Nothing here talks to the network.
"""

import os
import struct
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SOURCE_IMAGE = SCRIPT_DIR / "entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
# The entry image is a fixed asset with a known rough weight; the size
# window below exists to catch a truncated, swapped or corrupt file
# before it gets copied anywhere.
SMALLEST_OK_BYTES = 10_000
LARGEST_OK_BYTES = 5_000_000
IHDR_LABEL_AT = slice(12, 16)
DIMENSIONS_AT = slice(16, 24)
HEADER_MIN_BYTES = 24


def resolve_destination():
    """Work out where the copy should land and make sure the folder exists.

    The ``MAKEFUN_OUTPUT_DIR`` environment variable wins when set;
    otherwise the copy goes to ``/output``.
    """
    requested = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    folder = Path(requested) if requested else Path("/output")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.png"


def ensure_source_present():
    """Refuse to continue when the source image file is not on disk."""
    if not SOURCE_IMAGE.is_file():
        raise SystemExit(f"{SOURCE_IMAGE} is missing, refusing to copy")


def ensure_png_signature(payload):
    """Refuse bytes that do not start with the eight-byte PNG signature."""
    if not payload.startswith(PNG_SIGNATURE):
        raise SystemExit(f"{SOURCE_IMAGE} is not a PNG file, refusing to copy")


def ensure_plausible_size(payload):
    """Refuse payloads whose byte count falls outside the expected window."""
    if not SMALLEST_OK_BYTES <= len(payload) <= LARGEST_OK_BYTES:
        raise SystemExit(
            f"{SOURCE_IMAGE} has unexpected size {len(payload)} bytes "
            f"(expected {SMALLEST_OK_BYTES}-{LARGEST_OK_BYTES}), "
            "refusing to copy"
        )


def read_ihdr_dimensions(payload):
    """Pull the pixel dimensions out of the IHDR chunk and vet them.

    The chunk label must sit at its fixed offset and both dimensions
    must be positive; anything else means the file is not the intact
    image we expect, so the run aborts with a clear message.
    """
    if len(payload) < HEADER_MIN_BYTES or payload[IHDR_LABEL_AT] != b"IHDR":
        raise SystemExit(f"{SOURCE_IMAGE} has no IHDR chunk, refusing to copy")
    width, height = struct.unpack(">II", payload[DIMENSIONS_AT])
    if width <= 0 or height <= 0:
        raise SystemExit(
            f"{SOURCE_IMAGE} has invalid dimensions {width}x{height}, "
            "refusing to copy"
        )
    return width, height


def validate_payload(payload):
    """Run every sanity check over the source bytes, in a fixed order.

    On success a one-line diagnostic goes to stderr and the image
    dimensions are returned; on failure the run exits via SystemExit
    with the reason instead of copying a suspect file.
    """
    ensure_source_present()
    ensure_png_signature(payload)
    ensure_plausible_size(payload)
    width, height = read_ihdr_dimensions(payload)
    print(
        f"validated {SOURCE_IMAGE.name}: {width}x{height}px, "
        f"{len(payload)} bytes",
        file=sys.stderr,
    )
    return width, height


def run():
    """Validate the source image, then copy its bytes to the destination."""
    payload = SOURCE_IMAGE.read_bytes()
    validate_payload(payload)
    destination = resolve_destination()
    destination.write_bytes(payload)
    print(f"wrote {destination} ({len(payload)} bytes)")


if __name__ == "__main__":
    run()
