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
MAX_DIM_SMALL = 360        # small thumbnails/avatars shown ≤84–120px → ~3× is plenty
LARGE_HINTS = ("bg", "particles", "featured", "hero", "backdrop")
# Thumbnail-class assets rendered small (library list circles 84px, fav avatars,
# onboarding artist bubbles). Capping these at MAX_DIM_SMALL keeps the standalone
# in the ~3–4 MB range without visible quality loss at their on-screen size.
SMALL_HINTS = ("library-artist-", "favs-artist-", "favs-group-", "favs-dj-")
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
            if any(name.startswith(h) for h in SMALL_HINTS):
                max_dim = MAX_DIM_SMALL
            elif any(h in name for h in LARGE_HINTS):
                max_dim = MAX_DIM_LARGE
            else:
                max_dim = MAX_DIM_DEFAULT
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


def _inline(html: str) -> tuple[str, list[str], set[str]]:
    """Return (rewritten_html, log_lines, statically_inlined_paths)."""
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

    inlined = {p for p, d in cache.items() if d is not None}
    return html, log, inlined


# ── runtime-asset interceptor (GOROD-OFFLINE) ─────────────────────────────────
# The static regexes above only catch assets referenced by *literal* strings in
# the source. Several images are built at RUNTIME by concatenating a base path
# with a data-driven filename, e.g.:
#     var ASSET = 'assets/gorod-fm/';
#     el.style.backgroundImage = 'url(' + ASSET + d.img + ')';          // onboarding bubbles
#     '<div style="background-image:url(assets/gorod-fm/library-artist-' + a.f + '.png)">'  // library
#     img.src = url;  /* where url is 'assets/gorod-fm/...' */
# Those strings don't exist verbatim in the HTML, so they can't be rewritten —
# in the standalone (opened with no assets/ folder next to it) they 404.
#
# Fix: emit, at the very TOP of <head> (before any app <script>), (a) a JS map of
# EVERY assets/gorod-fm/* file + assets/dusk-lake.jpg → its optimized data URI
# (reusing the same Pillow/WebP pipeline as static inlining, so size stays sane),
# and (b) a tiny interceptor that resolves any of those paths to its data URI for
# <img src> (property + setAttribute) AND JS-set CSS backgrounds (style.setProperty
# + background / backgroundImage setters). Every image then works fully offline.

# Folders whose every image file we want available to the runtime interceptor.
RUNTIME_ASSET_DIRS = ("gorod-fm",)
# Standalone single-file extras referenced by some glass skins.
RUNTIME_ASSET_EXTRA = ("dusk-lake.jpg",)
RUNTIME_IMG_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif", ".svg")


def _needs_runtime_map(filename: str, src_html: str) -> bool:
    """Does *filename* require a RUNTIME map entry (a ref the static pass can't reach)?

    The static rewriter (_inline) already turns every *literal* ``assets/...`` ref
    — <img src>, <style>/inline-style ``url(assets/...)``, and JS strings like
    ``img:'assets/gorod-fm/podborki-...png'`` — into a data URI. Those do NOT need
    a map entry. The interceptor map is for refs built at RUNTIME, which fall into
    two families the static pass cannot see:

      • bare-filename concat — ``var ASSET='assets/gorod-fm/'; … ASSET + d.img``
        where the data value is a *bare* filename, e.g. ``img:'genre-pop.jpg'`` →
        runtime path ``assets/gorod-fm/genre-pop.jpg`` (the literal has no
        ``assets/`` prefix, so the static JS-string regex skips it).
      • token concat — ``'library-artist-' + a.f + '.png'`` with ``{f:'a-studio'}``
        → ``library-artist-a-studio.png``.

    Returning True only for these keeps the map free of bytes the static pass
    already inlined elsewhere, and drops dead leftovers (unused ui-sprites, orphan
    covers) entirely — holding the standalone in the ~3–4 MB range.
    """
    # bare-filename concat: `img: 'genre-pop.jpg'` (quoted bare filename, no path)
    if re.search(r"""['"]""" + re.escape(filename) + r"""['"]""", src_html):
        # ensure it's used as a BARE value (the ASSET-prefixed concat), not only as
        # part of a full 'assets/gorod-fm/<file>' literal (which the static pass got)
        bare_hit = re.search(r"""(?<![\w/])""" + re.escape(filename) + r"""['"]""", src_html)
        full_lit = "assets/gorod-fm/" + filename
        # If it ONLY ever appears as a full literal, static inlining covered it.
        if bare_hit and not _only_full_literal(filename, full_lit, src_html):
            return True
    # token concat families (prefix literal present + token appears as a data value)
    stem = filename.rsplit(".", 1)[0]
    for prefix in ("library-artist-",):
        if stem.startswith(prefix) and prefix in src_html:
            token = stem[len(prefix):]
            if f"'{token}'" in src_html or f'"{token}"' in src_html:
                return True
    return False


def _only_full_literal(filename: str, full_lit: str, src_html: str) -> bool:
    """True if *filename* appears ONLY inside the full 'assets/gorod-fm/<file>' literal.

    Such a file was fully handled by static inlining and needs no map entry. If the
    bare filename also appears standalone (an ``ASSET + d.img`` data value), it is a
    runtime ref and must be mapped.
    """
    # Count quoted-bare occurrences NOT immediately preceded by 'assets/gorod-fm/'.
    for m in re.finditer(re.escape(filename), src_html):
        start = m.start()
        preceding = src_html[max(0, start - 16):start]
        if not preceding.endswith("assets/gorod-fm/"):
            return False  # found a bare/standalone usage → not only-full-literal
    return True


def _build_asset_map(
    skip: set[str] | None = None, src_html: str = ""
) -> tuple[dict[str, str], list[str]]:
    """Map runtime-referenced assets' FULL path -> optimized data URI.

    Keys are exactly what the runtime produces, e.g. 'assets/gorod-fm/genre-pop.jpg'
    (note `var ASSET='assets/gorod-fm/'`, so resolve by the full concatenated path).
    Reuses _data_uri → same downscale + WebP optimization as static inlining.

    *skip* lists paths already inlined statically (literal <img>/CSS/JS-string refs).
    Those are excluded so their bytes appear only ONCE in the file — the runtime
    interceptor only needs the assets the static pass cannot reach (bare-filename
    `ASSET + d.img` concats, `library-artist-` concats, `img.src = url`, etc.).
    Only files actually reachable from *src_html* are included (see _is_referenced).
    """
    skip = skip or set()
    amap: dict[str, str] = {}
    log: list[str] = []
    skipped = 0
    unref = 0
    for sub in RUNTIME_ASSET_DIRS:
        d = DESIGNS / "assets" / sub
        if not d.is_dir():
            continue
        for f in sorted(d.iterdir()):
            if not f.is_file() or f.suffix.lower() not in RUNTIME_IMG_EXTS:
                continue
            rel = f"assets/{sub}/{f.name}"
            if rel in skip:
                skipped += 1
                continue
            if src_html and not _needs_runtime_map(f.name, src_html):
                unref += 1
                continue
            uri = _data_uri(rel)
            if uri:
                amap[rel] = uri
    for name in RUNTIME_ASSET_EXTRA:
        rel = f"assets/{name}"
        if rel in skip:
            skipped += 1
            continue
        if (DESIGNS / rel).exists():
            uri = _data_uri(rel)
            if uri:
                amap[rel] = uri
    log.append(f"runtime asset map: {len(amap)} files inlined for interceptor "
               f"({skipped} already static-inlined; {unref} unreferenced/dead-leftover skipped)")
    return amap, log


def _head_injection(asset_map: dict[str, str]) -> str:
    """Return a <script> resolving runtime assets/... refs to inlined data URIs.

    Must be placed at the very TOP of <head>, before any app script, so the
    prototype patches are in force the instant app code starts assigning
    img.src / element.style.background.
    """
    # json.dumps keeps the (already URL-safe base64) data URIs intact and escaped.
    # ensure_ascii=True (default) is LOAD-BEARING: this script is injected at the very
    # top of <head>, BEFORE <meta charset>, so any non-ASCII byte could mis-decode and
    # silently truncate the script. Keep the whole injection strictly 7-bit ASCII.
    import json

    payload = json.dumps(asset_map, separators=(",", ":"), ensure_ascii=True)
    script = (
        "<script>(function(){\n"
        "  // GOROD-OFFLINE: resolve runtime-built assets/... refs to inlined data URIs.\n"
        f"  var MAP = {payload};\n"
        "  // Match any assets/gorod-fm/... or assets/dusk-lake.jpg occurrence (with or\n"
        "  // without a leading designs/ or ./), optionally wrapped in url(...) / quotes.\n"
        "  function lookup(p){\n"
        "    if(p==null) return p;\n"
        "    var s=String(p);\n"
        "    // direct hit\n"
        "    if(MAP[s]) return MAP[s];\n"
        "    // strip ./ or designs/ prefix\n"
        "    var k=s.replace(/^\\.?\\//,'').replace(/^designs\\//,'');\n"
        "    if(MAP[k]) return MAP[k];\n"
        "    return null;\n"
        "  }\n"
        "  // Rewrite a CSS value that may contain url(assets/...) -> url(data:...).\n"
        "  function rewriteCss(v){\n"
        "    if(v==null) return v;\n"
        "    var s=String(v);\n"
        "    if(s.indexOf('assets/')===-1) return v;\n"
        "    return s.replace(/url\\(\\s*(['\\\"]?)((?:\\.\\/|designs\\/)?assets\\/[^'\\\")]+)\\1\\s*\\)/g,\n"
        "      function(m,q,path){ var d=lookup(path); return d? ('url(\"'+d+'\")') : m; });\n"
        "  }\n"
        "  // Rewrite a plain src-like value (may be a bare path or a url(...) wrap).\n"
        "  function rewriteSrc(v){\n"
        "    if(v==null) return v;\n"
        "    var s=String(v);\n"
        "    if(s.indexOf('assets/')===-1) return v;\n"
        "    if(s.indexOf('url(')!==-1) return rewriteCss(s);\n"
        "    var d=lookup(s); return d!=null? d : v;\n"
        "  }\n"
        "  // (1) <img>.src property get/set\n"
        "  try{\n"
        "    var imgProto=HTMLImageElement.prototype;\n"
        "    var srcDesc=Object.getOwnPropertyDescriptor(imgProto,'src')\n"
        "      || Object.getOwnPropertyDescriptor(HTMLElement.prototype,'src');\n"
        "    if(srcDesc&&srcDesc.set){\n"
        "      Object.defineProperty(imgProto,'src',{\n"
        "        configurable:true, enumerable:srcDesc.enumerable,\n"
        "        get:function(){ return srcDesc.get.call(this); },\n"
        "        set:function(v){ srcDesc.set.call(this, rewriteSrc(v)); }\n"
        "      });\n"
        "    }\n"
        "  }catch(e){}\n"
        "  // (2) setAttribute('src',...) on <img> (and 'srcset' best-effort single-url)\n"
        "  try{\n"
        "    var setAttr=Element.prototype.setAttribute;\n"
        "    Element.prototype.setAttribute=function(name,value){\n"
        "      if(name && /^src$/i.test(name)){ value=rewriteSrc(value); }\n"
        "      else if(name && /^srcset$/i.test(name)){ value=rewriteSrc(value); }\n"
        "      return setAttr.call(this,name,value);\n"
        "    };\n"
        "  }catch(e){}\n"
        "  // (3) CSSStyleDeclaration.setProperty (covers style.setProperty('background-image',...))\n"
        "  try{\n"
        "    var setProp=CSSStyleDeclaration.prototype.setProperty;\n"
        "    CSSStyleDeclaration.prototype.setProperty=function(prop,value,prio){\n"
        "      if(value!=null && /background/i.test(String(prop))){ value=rewriteCss(value); }\n"
        "      return setProp.call(this,prop,value,prio);\n"
        "    };\n"
        "  }catch(e){}\n"
        "  // (4) JS-set CSS backgrounds: el.style.background = 'url(assets/...)'.\n"
        "  //     In Blink the per-property accessors (backgroundImage/background/cssText)\n"
        "  //     live on the *instance*, not CSSStyleDeclaration.prototype, so wrapping\n"
        "  //     the prototype setter never fires. Instead we observe the resulting\n"
        "  //     inline `style` attribute mutation and rewrite it in place. This also\n"
        "  //     catches static markup `style=\"background-image:url(assets/...)\"`.\n"
        "  var rewriting=false;\n"
        "  function fixStyleAttr(el){\n"
        "    if(!el || el.nodeType!==1) return;\n"
        "    var sa=el.getAttribute && el.getAttribute('style');\n"
        "    if(!sa || sa.indexOf('assets/')===-1) return;\n"
        "    var fixed=rewriteCss(sa);\n"
        "    if(fixed!==sa){ rewriting=true; try{ el.setAttribute('style', fixed); } finally { rewriting=false; } }\n"
        "  }\n"
        "  function fixSrcAttr(el){\n"
        "    if(!el || el.nodeType!==1 || !el.getAttribute) return;\n"
        "    ['src','srcset'].forEach(function(a){\n"
        "      var v=el.getAttribute(a);\n"
        "      if(v && v.indexOf('assets/')!==-1 && v.indexOf('data:')!==0){\n"
        "        var f=rewriteSrc(v); if(f!==v) el.setAttribute(a,f);\n"
        "      }\n"
        "    });\n"
        "  }\n"
        "  function sweep(root){\n"
        "    if(!root || !root.querySelectorAll) return;\n"
        "    var nodes=root.querySelectorAll('[style*=\"assets/\"]');\n"
        "    for(var i=0;i<nodes.length;i++) fixStyleAttr(nodes[i]);\n"
        "    var imgs=root.querySelectorAll('img[src*=\"assets/\"],img[srcset*=\"assets/\"],source[srcset*=\"assets/\"]');\n"
        "    for(var j=0;j<imgs.length;j++) fixSrcAttr(imgs[j]);\n"
        "    if(root.getAttribute) { fixStyleAttr(root); fixSrcAttr(root); }\n"
        "  }\n"
        "  try{\n"
        "    var mo=new MutationObserver(function(muts){\n"
        "      if(rewriting) return;\n"
        "      for(var i=0;i<muts.length;i++){\n"
        "        var m=muts[i];\n"
        "        if(m.type==='attributes'){\n"
        "          if(m.attributeName==='style') fixStyleAttr(m.target);\n"
        "          else if(m.attributeName==='src'||m.attributeName==='srcset') fixSrcAttr(m.target);\n"
        "        } else if(m.type==='childList'){\n"
        "          for(var a=0;a<m.addedNodes.length;a++){ var n=m.addedNodes[a];\n"
        "            if(n.nodeType===1){ fixStyleAttr(n); fixSrcAttr(n); sweep(n); } }\n"
        "        }\n"
        "      }\n"
        "    });\n"
        "    function startObs(){ if(document.documentElement) mo.observe(document.documentElement,{subtree:true,childList:true,attributes:true,attributeFilter:['style','src','srcset']}); }\n"
        "    startObs();\n"
        "  }catch(e){}\n"
        "  // Sweep-based safety net. The MutationObserver can miss content rendered\n"
        "  // long after load (SPA routes build their DOM on navigation, e.g. the\n"
        "  // #/onboarding bubble field and #/library artist grid set backgrounds via\n"
        "  // `el.style.backgroundImage = 'url(' + ASSET + d.img + ')'`). So we ALSO:\n"
        "  //   - sweep on every route change (hashchange / popstate),\n"
        "  //   - run a short bounded interval sweep to catch async/late renders,\n"
        "  //   - sweep at the usual lifecycle points.\n"
        "  function sweepDoc(){ try{ sweep(document); }catch(e){} }\n"
        "  sweepDoc();\n"
        "  if(document.addEventListener){\n"
        "    document.addEventListener('DOMContentLoaded', sweepDoc);\n"
        "    window.addEventListener('load', sweepDoc);\n"
        "    window.addEventListener('hashchange', function(){ sweepDoc(); setTimeout(sweepDoc,80); setTimeout(sweepDoc,300); });\n"
        "    window.addEventListener('popstate', function(){ sweepDoc(); setTimeout(sweepDoc,80); setTimeout(sweepDoc,300); });\n"
        "  }\n"
        "  // bounded recurring sweep: every 200ms for ~12s after start, then stop.\n"
        "  var _n=0, _iv=setInterval(function(){ sweepDoc(); if(++_n>60) clearInterval(_iv); }, 200);\n"
        "})();</script>\n"
    )
    # Guard: the injection MUST be pure ASCII (see ensure_ascii note above).
    assert script.isascii(), "head injection contains non-ASCII bytes (would mis-decode before <meta charset>)"
    return script


def main() -> int:
    src = DESIGNS / SOURCE
    if not src.exists():
        print(f"ERROR: source not found: {src}")
        return 1

    html = src.read_text(encoding="utf-8")
    out_html, log, inlined = _inline(html)

    # Inject the runtime-asset interceptor at the very top of <head>, before any
    # app script, so img.src / style.background assignments resolve offline.
    #
    # NOTE: we do NOT skip statically-inlined paths here. A path inlined once in a
    # literal <img src> can STILL be produced at RUNTIME by a bare-filename concat
    # (e.g. home-featured-egor-krid.png appears both as <img src="assets/..."> AND
    # as `ASSET + 'home-featured-egor-krid.png'` in the onboarding data). The latter
    # 404s without a map entry, so every *referenced* file must be in the map.
    # Dead leftover assets (unused ui-sprites, orphan covers) are still dropped via
    # _needs_runtime_map to keep the file in the ~3–4 MB range.
    asset_map, map_log = _build_asset_map(src_html=html)
    log = map_log + log
    injection = _head_injection(asset_map)
    head_m = re.search(r"<head[^>]*>", out_html, re.IGNORECASE)
    if head_m:
        idx = head_m.end()
        out_html = out_html[:idx] + "\n" + injection + out_html[idx:]
    else:  # no <head> — fall back to start of document
        out_html = injection + out_html

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
