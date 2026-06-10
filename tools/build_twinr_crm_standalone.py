"""Inline local assets into single-file HTML for twinr-liquid-glass and crm-glass.

Same pattern as build_kinolog_standalone.py:
  <img src="assets/..."> / url('assets/...') -> data URIs.
Google Fonts links stay external.

Writes:
  designs/twinr-liquid-glass-standalone.html
  designs/crm-glass-standalone.html
"""
import base64
import mimetypes
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DESIGNS = ROOT / "designs"

VARIANTS = ["twinr-liquid-glass.html", "crm-glass.html"]

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


def rewrite(html: str) -> tuple[str, list[str], list[str]]:
    inlined: list[str] = []
    missing: list[str] = []

    def img_sub(m: re.Match) -> str:
        path = m.group(2)
        data = inline_asset(path)
        if data is None:
            missing.append(path)
            return m.group(0)
        inlined.append(path)
        return f"{m.group(1)}{data}{m.group(3)}"

    def css_sub(m: re.Match) -> str:
        path = m.group(1)
        data = inline_asset(path)
        if data is None:
            missing.append(path)
            return m.group(0)
        inlined.append(path)
        return f"url('{data}')"

    html = IMG_RE.sub(img_sub, html)
    html = CSS_URL_RE.sub(css_sub, html)
    return html, inlined, missing


def main() -> None:
    for name in VARIANTS:
        src = DESIGNS / name
        out = DESIGNS / name.replace(".html", "-standalone.html")
        html = src.read_text(encoding="utf-8")
        patched, inlined, missing = rewrite(html)
        out.write_text(patched, encoding="utf-8")
        size_mb = out.stat().st_size / 1024 / 1024
        print(f"{out.name}: {size_mb:.2f} MB, inlined {len(inlined)} refs")
        for p in sorted(set(missing)):
            print(f"  MISSING: {p}")
        leftovers = re.findall(r"""(?:src=["']|url\(['"]?)assets/""", patched)
        if leftovers:
            print(f"  WARNING: {len(leftovers)} leftover asset refs")


if __name__ == "__main__":
    main()
