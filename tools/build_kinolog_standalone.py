"""Inline all local assets into single-file HTML for client-facing delivery.

Rewrites:
  <img src="assets/..."> → <img src="data:image/...;base64,...">
  url('assets/...')      → url('data:image/...;base64,...')

Google Fonts <link> stays external (works everywhere with internet).

Writes three standalone variants into designs/:
  kinolog-paws-standalone.html
  kinolog-glass-standalone.html
  kinolog-material-standalone.html
"""
import base64
import mimetypes
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DESIGNS = ROOT / "designs"

VARIANTS = ["kinolog-paws.html", "kinolog-glass.html", "kinolog-material.html"]

# Allow common webp/png/jpg in our asset tree
mimetypes.add_type("image/webp", ".webp")


def inline_asset(rel_path: str) -> str | None:
    """Resolve relative path against designs/ and return data-URI."""
    full = (DESIGNS / rel_path).resolve()
    if not full.exists():
        return None
    mime, _ = mimetypes.guess_type(str(full))
    mime = mime or "application/octet-stream"
    b64 = base64.b64encode(full.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


# Match src="assets/..." or src='assets/...'
IMG_RE = re.compile(r'''(src=["'])(assets/[^"']+)(["'])''')
# CSS url('assets/...') / url("assets/...") / url(assets/...)
CSS_URL_RE = re.compile(r"""url\(\s*['"]?(assets/[^'")]+)['"]?\s*\)""")


def rewrite(html: str) -> tuple[str, list[str]]:
    """Inline all asset refs, return patched html + list of what was inlined."""
    inlined: list[str] = []

    def img_sub(m: re.Match) -> str:
        path = m.group(2)
        data = inline_asset(path)
        if data is None:
            inlined.append(f"MISSING: {path}")
            return m.group(0)
        inlined.append(f"ok: {path} ({len(data) // 1024} KB b64)")
        return f"{m.group(1)}{data}{m.group(3)}"

    def css_sub(m: re.Match) -> str:
        path = m.group(1)
        data = inline_asset(path)
        if data is None:
            inlined.append(f"MISSING (css): {path}")
            return m.group(0)
        inlined.append(f"ok (css): {path} ({len(data) // 1024} KB b64)")
        return f"url('{data}')"

    html = IMG_RE.sub(img_sub, html)
    html = CSS_URL_RE.sub(css_sub, html)
    return html, inlined


def main():
    for src_name in VARIANTS:
        src = DESIGNS / src_name
        if not src.exists():
            print(f"skip: {src} not found")
            continue
        html = src.read_text(encoding="utf-8")
        patched, log = rewrite(html)
        out_name = src_name.replace(".html", "-standalone.html")
        out = DESIGNS / out_name
        out.write_text(patched, encoding="utf-8")
        size_in = src.stat().st_size
        size_out = out.stat().st_size
        print(f"\n== {src_name} -> {out_name} ==")
        for line in log:
            print(f"  {line}")
        print(f"  size: {size_in:,} -> {size_out:,} bytes ({size_out / 1024 / 1024:.2f} MB)")


if __name__ == "__main__":
    main()
