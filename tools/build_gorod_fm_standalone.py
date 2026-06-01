"""Build standalone single-file HTML for Город ФМ SPA.

Inlines all locally-referenced assets (PNG/JPG/SVG/WEBP) from
designs/assets/ as base64 data URIs, so the file is fully
self-contained for client/investor delivery.

Rewrite targets:
  src="designs/assets/..."  →  src="data:<mime>;base64,..."
  src="assets/..."          →  src="data:<mime>;base64,..."
  url('assets/...')         →  url('data:<mime>;base64,...')
  url("assets/...")         →  url('data:<mime>;base64,...')
  JS string 'assets/...'   →  'data:<mime>;base64,...'

Google Fonts <link> stays external (CDN; inlining would bloat file
with ~200 KB of font data per weight that doesn't survive CORS anyway).

── Image optimization (added 2026-06-02, GOROD-032) ──────────────────────────
The Figma-exported source PNGs are full-fidelity originals (e.g. a tile photo
ships at 4096×2731 / 10.9 MB). Inlining them verbatim produced a **71 MB**
standalone — unshippable to an investor. So, *only while inlining*, raster
images are downscaled to a sane on-screen size and re-encoded as WebP, keeping
whichever (optimized vs original) is smaller. The source asset files on disk are
NEVER modified — they remain Figma-fidelity for the eventual Next.js production
handoff. Set OPTIMIZE = False to ship pixel-identical originals.

Gorod-FM v1 note: the v1 file used only CSS gradients + inline SVG — no external
images. The v2/AI-product file (this build) references real Figma photo tiles.

Usage:
    python tools/build_gorod_fm_standalone.py
"""
from __future__ import annotations

import base64
import mimetypes
import re
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "designs"

SOURCE = "gorod-fm.html"
OUTPUT = "gorod-fm-standalone.html"

NOTICE_COMMENT = "<!-- standalone build — no local assets to inline; identical to source -->\n"

# ── image optimization config ────────────────────────────────────────────────
OPTIMIZE = True            # downscale + WebP re-encode raster images while inlining
MAX_DIM_DEFAULT = 800      # tiles/covers: ~2× their on-screen size (≈245–373px in Figma)
MAX_DIM_LARGE = 1600       # full-bleed backgrounds / featured heroes keep more detail
LARGE_HINTS = ("bg", "particles", "featured", "hero", "backdrop")
WEBP_QUALITY = 82

mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("image/avif", ".avif")

# Per-asset optimization savings, populated by _data_uri (path -> (orig_bytes, final_bytes)).
_SAVINGS: dict[str, tuple[int, int]] = {}


def _optimize_image(full: Path) -> tuple[bytes, str] | None:
    """Downscale + WebP-encode *full*. Return (bytes, mime) or None if not optimizable.

    Returns None for anything Pillow can't open (SVGs-as-.png, icon sprites, etc.),
    so the caller falls back to the raw bytes unchanged.
    """
    try:
        from PIL import Image
    except Exception:
        return None
    try:
        resample = Image.Resampling.LANCZOS  # Pillow ≥ 9.1
    except AttributeError:  # pragma: no cover - very old Pillow
        resample = Image.LANCZOS
    try:
        with Image.open(full) as im:
            im.load()
            name = full.name.lower()
            max_dim = MAX_DIM_LARGE if any(h in name for h in LARGE_HINTS) else MAX_DIM_DEFAULT
            w, h = im.size
            scale = min(1.0, max_dim / max(w, h))
            if scale < 1.0:
                im = im.resize((max(1, round(w * scale)), max(1, round(h * scale))), resample)
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGBA" if ("A" in im.getbands()) else "RGB")
            buf = BytesIO()
            im.save(buf, format="WEBP", quality=WEBP_QUALITY, method=6)
            return buf.getvalue(), "image/webp"
    except Exception:
        return None


def _data_uri(rel_path: str) -> str | None:
    """Resolve *rel_path* relative to designs/ and return a data URI, or None if missing."""
    full = (DESIGNS / rel_path).resolve()
    if not full.exists():
        return None
    raw = full.read_bytes()
    mime, _ = mimetypes.guess_type(str(full))
    mime = mime or "application/octet-stream"

    if OPTIMIZE and mime.startswith("image/") and mime != "image/svg+xml":
        opt = _optimize_image(full)
        if opt is not None and len(opt[0]) < len(raw):
            _SAVINGS[rel_path] = (len(raw), len(opt[0]))
            raw, mime = opt

    b64 = base64.b64encode(raw).decode("ascii")
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
            opt = ""
            if path in _SAVINGS:
                o, n = _SAVINGS[path]
                opt = f"  [opt {o // 1024}->{n // 1024} KB, -{100 * (o - n) // o}%]"
            log.append(f"ok: {path} ({len(data) // 1024} KB b64){opt}")

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
    if _SAVINGS:
        saved = sum(o - n for o, n in _SAVINGS.values())
        print(f"  image optimization: {len(_SAVINGS)} images, {saved / 1024 / 1024:.1f} MB saved")
    print(f"  Source: {size_in:,} bytes -> Standalone: {size_out:,} bytes")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
