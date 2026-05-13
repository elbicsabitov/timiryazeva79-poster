#!/usr/bin/env python3
"""Build standalone single-file HTML for RU.TV landing variants.

Inlines all referenced assets (PNG/JPG/SVG) from designs/assets/rutv/ as base64
data URIs. Output sits next to source as <stem>-standalone.html.

Usage:
    python tools/build_rutv_landing_standalone.py
"""
from __future__ import annotations

import base64
import mimetypes
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "designs"
ASSETS_DIR = DESIGNS / "assets" / "rutv"

VARIANTS = [
    "rutv-landing.html",          # production-best
    "rutv-landing-figma.html",    # Figma 1-в-1
]

# match: assets/rutv/<file> referenced inside url('...'), src="...", img src="...", style background-image, etc.
ASSET_REF = re.compile(
    r"""(?P<prefix>(?:url\(\s*['"]?|src=['"]|content=['"]))(?P<path>assets/rutv/[^'")]+)(?P<suffix>['"]?\)?['"]?)""",
    re.IGNORECASE,
)


def asset_to_data_uri(rel_path: str) -> str | None:
    decoded = urllib.parse.unquote(rel_path)
    fp = DESIGNS / decoded
    if not fp.exists():
        print(f"  ! asset missing: {decoded}", file=sys.stderr)
        return None
    mime, _ = mimetypes.guess_type(fp.name)
    if mime is None:
        mime = "application/octet-stream"
    data = base64.b64encode(fp.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def inline(html: str) -> tuple[str, dict[str, int]]:
    cache: dict[str, str] = {}
    stats = {"hits": 0, "unique": 0, "missed": 0}

    def repl(m: re.Match[str]) -> str:
        ref = m.group("path")
        stats["hits"] += 1
        if ref not in cache:
            data_uri = asset_to_data_uri(ref)
            if data_uri is None:
                stats["missed"] += 1
                return m.group(0)
            cache[ref] = data_uri
            stats["unique"] += 1
        return f"{m.group('prefix')}{cache[ref]}{m.group('suffix')}"

    new_html = ASSET_REF.sub(repl, html)
    return new_html, stats


def main() -> int:
    if not ASSETS_DIR.exists():
        print(f"assets dir not found: {ASSETS_DIR}", file=sys.stderr)
        return 1

    for variant in VARIANTS:
        src = DESIGNS / variant
        if not src.exists():
            print(f"  - skip (not found): {variant}", file=sys.stderr)
            continue
        dst = src.with_name(src.stem + "-standalone.html")
        html = src.read_text(encoding="utf-8")
        out, stats = inline(html)
        dst.write_text(out, encoding="utf-8")
        size_in_kb = len(out.encode("utf-8")) / 1024
        print(f"  + {variant} -> {dst.name}  "
              f"({size_in_kb:.1f} KB | {stats['unique']} unique assets | "
              f"{stats['hits']} refs | {stats['missed']} missed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
