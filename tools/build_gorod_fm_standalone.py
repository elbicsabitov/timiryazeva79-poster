"""Build standalone single-file HTML for Город ФМ SPA.

Inlines all locally-referenced assets (PNG/JPG/SVG/WEBP) from
designs/assets/ as base64 data URIs, so the file is fully
self-contained for client delivery.

Rewrite targets:
  src="designs/assets/..."  →  src="data:<mime>;base64,..."
  src="assets/..."          →  src="data:<mime>;base64,..."
  url('assets/...')         →  url('data:<mime>;base64,...')
  url("assets/...")         →  url('data:<mime>;base64,...')
  JS string 'assets/...'   →  'data:<mime>;base64,...'

Google Fonts <link> stays external (CDN; inlining would bloat file
with ~200 KB of font data per weight that doesn't survive CORS anyway).

Gorod-FM v1 note: the file uses only CSS gradients + inline SVG for
visuals — no external image files ship at this stage. The script will
copy the source cleanly and prepend a notice comment. When real assets
arrive (GOROD-016), re-run to inline them automatically.

Usage:
    python tools/build_gorod_fm_standalone.py
"""
from __future__ import annotations

import base64
import mimetypes
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "designs"

SOURCE = "gorod-fm.html"
OUTPUT = "gorod-fm-standalone.html"

NOTICE_COMMENT = "<!-- standalone build — no local assets to inline; identical to source -->\n"

mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("image/avif", ".avif")


def _data_uri(rel_path: str) -> str | None:
    """Resolve *rel_path* relative to designs/ and return a data URI, or None if missing."""
    full = (DESIGNS / rel_path).resolve()
    if not full.exists():
        return None
    mime, _ = mimetypes.guess_type(str(full))
    mime = mime or "application/octet-stream"
    b64 = base64.b64encode(full.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


# ── regex patterns ──────────────────────────────────────────────────────────

# <img src="assets/..." />  or  <img src="designs/assets/..." />
_IMG_RE = re.compile(
    r"""(src=["'])(?:designs/)?(assets/[^"']+)(["'])""",
    re.IGNORECASE,
)

# CSS url('assets/...')  url("assets/...")  url(assets/...)
# also handles designs/assets/ prefix
_CSS_URL_RE = re.compile(
    r"""url\(\s*['"]?(?:designs/)?(assets/[^'")]+)['"]?\s*\)""",
    re.IGNORECASE,
)

# JS string literals  'assets/...'  "assets/..."
_JS_STR_RE = re.compile(
    r"""(["'])(?:designs/)?(assets/[^"']+\.(?:png|jpg|jpeg|webp|avif|gif|svg))(["'])""",
    re.IGNORECASE,
)


def _inline(html: str) -> tuple[str, list[str]]:
    """Return (rewritten_html, log_lines)."""
    cache: dict[str, str | None] = {}
    log: list[str] = []

    def _get(path: str) -> str | None:
        if path not in cache:
            cache[path] = _data_uri(path)
        return cache[path]

    def _img_sub(m: re.Match) -> str:
        path = m.group(2)
        data = _get(path)
        if data is None:
            log.append(f"MISSING: {path}")
            return m.group(0)
        return f"{m.group(1)}{data}{m.group(3)}"

    def _css_sub(m: re.Match) -> str:
        path = m.group(1)
        data = _get(path)
        if data is None:
            log.append(f"MISSING (css): {path}")
            return m.group(0)
        return f"url('{data}')"

    def _js_sub(m: re.Match) -> str:
        q1, path, q3 = m.group(1), m.group(2), m.group(3)
        data = _get(path)
        if data is None:
            log.append(f"MISSING (js): {path}")
            return m.group(0)
        return f"{q1}{data}{q3}"

    html = _IMG_RE.sub(_img_sub, html)
    html = _CSS_URL_RE.sub(_css_sub, html)
    html = _JS_STR_RE.sub(_js_sub, html)

    # Build per-asset summary from cache
    for path, data in cache.items():
        if data is not None:
            log.append(f"ok: {path} ({len(data) // 1024} KB b64)")

    return html, log


def main() -> int:
    src = DESIGNS / SOURCE
    if not src.exists():
        print(f"ERROR: source not found: {src}")
        return 1

    html = src.read_text(encoding="utf-8")
    out_html, log = _inline(html)

    # Determine whether any assets were actually inlined
    inlined_count = sum(1 for line in log if line.startswith("ok:"))

    if inlined_count == 0:
        # No local assets — prepend notice comment
        out_html = NOTICE_COMMENT + out_html

    dst = DESIGNS / OUTPUT
    dst.write_text(out_html, encoding="utf-8")

    size_in = src.stat().st_size
    size_out = dst.stat().st_size

    print(f"\n== {SOURCE} -> {OUTPUT} ==")
    if log:
        for line in log:
            print(f"  {line}")
    else:
        print(f"  (no local assets found to inline)")
    print(f"  Source: {size_in:,} bytes -> Standalone: {size_out:,} bytes")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
