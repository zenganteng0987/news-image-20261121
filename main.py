#!/usr/bin/env python3
"""Publish THE DAILY ATLAS — Saturday 21 November 2026.

The page itself (entry.png, 1024x1024) ships next to this file. This
program only publishes it: it checks the bundled image is present and is
a real PNG, copies it to the output directory, and verifies the copy
matches the original byte for byte (size and sha256).

Output directory: $MAKEFUN_OUTPUT_DIR when set, otherwise /output.
Python 3.13, standard library only, no network access. Running it
repeatedly produces a byte-identical output.
"""

import hashlib
import os
import shutil
import sys

# The first eight bytes of every PNG file.
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    # 1. The bundled image must exist next to this program.
    if not os.path.isfile(source):
        print(f"missing bundled image: {source}", file=sys.stderr)
        return 1

    # 2. It must be a PNG: check the 8-byte signature up front.
    with open(source, "rb") as handle:
        header = handle.read(len(PNG_SIGNATURE))
    if header != PNG_SIGNATURE:
        print(f"not a PNG file: {source}", file=sys.stderr)
        return 1

    # 3. Copy it to the output directory, creating it if needed.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, OUTPUT_NAME)
    shutil.copyfile(source, target)

    # 4. Verify the copy matches the original: same size, same sha256,
    #    and still a PNG (signature re-checked on the copy itself).
    source_size = os.path.getsize(source)
    target_size = os.path.getsize(target)
    if source_size != target_size:
        print(f"size mismatch: {source_size} != {target_size}", file=sys.stderr)
        return 1
    with open(target, "rb") as handle:
        copied_header = handle.read(len(PNG_SIGNATURE))
    if copied_header != PNG_SIGNATURE:
        print(f"copy is not a PNG file: {target}", file=sys.stderr)
        return 1
    if sha256_of(source) != sha256_of(target):
        print("sha256 mismatch after copy", file=sys.stderr)
        return 1

    print(f"published {OUTPUT_NAME} ({target_size} bytes) to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
