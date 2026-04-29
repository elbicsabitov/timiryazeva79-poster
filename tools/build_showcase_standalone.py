"""Inline assets для showcase-aggregator standalone.

Same pattern as build_kinolog_standalone.py — base64 inline для assets/*.
Google Fonts остаются external (нужен интернет, но это OK).
"""
import base64
import mimetypes
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DESIGNS = ROOT / "designs"

VARIANTS = ["showcase-aggregator.html"]

mimetypes.add_type("image/webp", ".webp")


def inline_asset(rel_path: str) -> str | None:
    full = (DESIGNS / rel_path).resolve()
    if not full.exists():
        return None
    mime, _ = mimetypes.guess_type(str(full))
    mime = mime or "application/octet-stream"
    b64 = base64.b64encode(full.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


IMG_RE = re.compile(r'''(src=["'])(assets/[^"']+)(["'])''')
CSS_URL_RE = re.compile(r"""url\(\s*['"]?(assets/[^'")]+)['"]?\s*\)""")


def rewrite(html: str):
    inlined = []

    def img_sub(m):
        path = m.group(2)
        data = inline_asset(path)
        if data is None:
            inlined.append(f"MISSING: {path}")
            return m.group(0)
        inlined.append(f"ok: {path} ({len(data) // 1024} KB b64)")
        return f"{m.group(1)}{data}{m.group(3)}"

    def css_sub(m):
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
    for name in VARIANTS:
        src = DESIGNS / name
        if not src.exists():
            print(f"skip: {src} not found")
            continue
        html = src.read_text(encoding="utf-8")
        patched, log = rewrite(html)
        out = DESIGNS / name.replace(".html", "-standalone.html")
        out.write_text(patched, encoding="utf-8")
        print(f"\n== {name} -> {out.name} ==")
        for line in log:
            print(f"  {line}")
        print(f"  size: {src.stat().st_size:,} -> {out.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
