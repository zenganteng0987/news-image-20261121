#!/usr/bin/env python3
"""THE DAILY ATLAS — Saturday 21 November 2026 (news-image-20261121, V2).

Entry program: publishes the pre-composed front page (entry.png, 1024x1024,
50 verified Saturday stories) by copying it to the output directory.

The image was composed programmatically with PIL from a pool of 50 stories,
each confirmed against two independent sources: NATO chief Rutte arriving
in Poland on Saturday as Poland asks for more Eastern Sentry assets
(F-35s and AWACS, no Article 4 move), Wall Street sliding into correction,
GTA 6 taking $3.79bn on day one, the UK-EU summit signing three deals,
COP31 still deadlocked in overtime, Cyclone Akvan weakening over Odisha,
Anthropic shares sliding on day two, the Palisades fire defendant found
guilty, Bayer's $7.25bn Roundup deal approved, Denmark foiling a Russian
murder plot, Gupta jailed 19 years 7 months in the Pannun plot, US
sanctions on Iran's "oil guardians", the Senate passing an energy bill
62-33, India declaring 720/9 — a record team total in New Zealand — and an
Anthropic researcher CLAIMING a proof of the Riemann hypothesis (NOT
independently verified), plus 35 further Saturday stories in the ALSO list.

Python 3.13, standard library only, no network access.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
TARGET = OUTPUT_DIR / "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not SOURCE.is_file():
        print(f"missing bundled image: {SOURCE}", file=sys.stderr)
        return 1
    with open(SOURCE, "rb") as handle:
        head = handle.read(len(PNG_MAGIC))
    if head != PNG_MAGIC:
        print("bundled image is not a PNG (bad 8-byte signature)", file=sys.stderr)
        return 1
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    if SOURCE.stat().st_size != TARGET.stat().st_size:
        print("output copy size does not match the bundled image", file=sys.stderr)
        return 1
    source_hash = sha256_of(SOURCE)
    target_hash = sha256_of(TARGET)
    if source_hash != target_hash:
        print("output copy sha256 does not match the bundled image", file=sys.stderr)
        return 1
    print(f"published {TARGET} "
          f"({TARGET.stat().st_size} bytes, "
          f"sha256 {target_hash[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
