# HANDOFF — Город ФМ · cont-16 (2026-06-03) — Light theme **deferred secondary-route sweep**: ANALYSIS DONE, build paused

> **STATUS: PAUSED mid-task (no losses).** This session ran a 6-agent read-only audit of every secondary route's light-theme gaps and captured a **build-ready override spec**. **No edits were made to `gorod-fm.html`.** Working tree clean. Next session = execute the spec below (Edit → Chrome-verify → adversarial review → standalone regen).
>
> File: `designs/gorod-fm.html` (~15.8k lines, single-file SPA). Mirror: `designs/gorod-fm-standalone.html`. Server :8770 serves `designs/` (was up at pause).
> **Raw agent output (verbatim, do NOT re-run the workflow — it cost 537k tokens):** `docs/superpowers/cont-16-light-sweep-analysis.json` (6 routes, per-rule rationale + line hints).
> Disc: light theme needs `?dev=1`; re-grep anchors before editing (they drift); `?v=N` cache-bust; clean `gorodfm_*`/`gorod-fm.theme` LS after probe.

## Where cont-15 left it
13 commits local on `master` ahead of `origin/master` (HEAD `c6a192d`), **PUSH HELD until explicit `sync`**. cont-15 shipped light theme v1 (dark `cinema` byte-identical, dev-gated, prod forces cinema) + weight-cloud + ЛК + standalone. The light override block (search marker `LIGHT theme — per-surface overrides`, ~L7323-7397) only covers **main flows** (home/taste/discover/player/account). This task (cont-15 NEXT item **B**) finishes the **secondary routes**.

---

## 🔒 LOCKED DECISIONS (apply these; all reversible, all keep dark byte-identical)

1. **cover-mix-base seam (byte-identity method).** The dark `:root` currently defines `--cover-mix-base:#111318` (L179). If we wire the cover sites to `var(--cover-mix-base, #orig)` while that dark def exists, dark resolves to `#111318` for ALL sites → the `#191C24`/`#15171D` sites would shift (breaks byte-identity). **FIX: DELETE `--cover-mix-base:#111318;` from the dark `:root` (L179).** Then wire each site to `var(--cover-mix-base, <its-own-original-hex>)`:
   - dark → var undefined → falls back to its exact original hex → **byte-identical** ✓
   - light → `:root[light]` defines `--cover-mix-base:#FFFFFF` (L209) → all flip to white floor ✓
   - **KEEP** the player-scope `--cover-mix-base:#111318` (L7395) so player covers stay immersive-dark even in light.
2. **#/profile — `.profile-box--closed` STAYS DARK.** It is the deliberate "dead black box" rhetoric device (comment L3163-3164). All white-text overrides are **scoped to `.profile-box--open`** so the closed box keeps its correct white-on-dark label/faux-bars. (Agent confirmed: the cont-15 note "faux-bars flipped to ink" is **false** — no such rule exists and none is needed since closed stays dark.)
3. **#/recap — the 9:16 `.recap-card` STAYS DARK** (WYSIWYG with the PNG export, decision O3). Method = pin the dark palette back inside `.recap-card` scope (same technique as player chrome L7389). Only the page **chrome** + screen-level deltas/discovery-panel flip to light.
4. **#/track lyrics = paper-ink** (inactive→`--text-ter`, active→`--text-pri`). The track page is paper (no dark wrapper); only the album-art cover is immersive. (Alternative: immersive-dark lyrics panel — rejected as default; flip if Эльбик wants.)
5. **#/artist track-cover = deep-blue fill.** JS injects the cover bg INLINE as `var(--surface-1)` (L15182) → **white in light, white mono on it = invisible (a latent bug, light-only)**. FIX = change the inline value to `var(--brand-blue-light)` (white mono on deep blue = AA, dark-safe). Keep `.artist-track-mono` white.
6. **Chrome strategy = LIGHT-GLASS REPAINT** (topbar/sidebar/tabbar get a paper-glass bg so the now-dark-ink tokenized labels read). This is the Apple-day default (Apple Music light mode = light chrome). 🟡 **Эльбик may prefer the alternative** (keep chrome a permanent dark "cinema rail" via re-asserted dark tokens, zero-text-touch) — see Open Questions. Default shipped = light-glass.

---

## 🧱 BUILD-READY SPEC

### Step 0 — seam edit (1 deletion + 12 call-site rewrites)
- **DELETE** L179 `--cover-mix-base: #111318;` from dark `:root` (the seam-tokens comment block ~L177-179; keep `--accent-text` line).
- L5790 `.track-cover`: `…22%, #111318)` → `…22%, var(--cover-mix-base, #111318))` (keep `!important`).
- L5826 `.track-neighbor-cover`: `…20%, #191C24)` → `…20%, var(--cover-mix-base, #191C24))`.
- **9 inline** `.track-history-cover` (L8941, 8955, 8969, 8983, 8997, 9011, 9025, 9040, 9068): `…20%, #15171D)` → `…20%, var(--cover-mix-base, #15171D))`. (L9054 already uses `var(--surface-1)` — leave; it's fixed by the `.track-history-cover` color override.)
- **1 inline** `.artist-track-cover` (L15182): `style="background:var(--surface-1)"` → `style="background:var(--brand-blue-light)"`.

### Step 1 — append override rules to the light block
Insert **after the player-chrome block (after L7397 `}`), before the ЛК comment (L7399)**, inside the same `<style>`. All selectors already `html[data-theme="light"]`-scoped (UNLAYERED → beats `@layer components`). **Re-grep each base line before trusting the hint — anchors drift.**

**— #/track —**
```css
html[data-theme="light"] .track-title,
html[data-theme="light"] .track-why-title,
html[data-theme="light"] .track-vector-title,
html[data-theme="light"] .track-neighbors-heading,
html[data-theme="light"] .track-why-text b,
html[data-theme="light"] .track-vector-k,
html[data-theme="light"] .track-neighbor-title,
html[data-theme="light"] .track-cover-mono,
html[data-theme="light"] .track-neighbor-mono,
html[data-theme="light"] .track-history-cover,
html[data-theme="light"] .track-lyric-line[data-active] { color: var(--text-pri); }
html[data-theme="light"] .track-cover-mono { text-shadow: none; }
html[data-theme="light"] .track-artist,
html[data-theme="light"] .track-why-text,
html[data-theme="light"] .track-vector-why,
html[data-theme="light"] .track-neighbor-artist { color: var(--text-sec); }
html[data-theme="light"] .track-lyric-line { color: var(--text-ter); }   /* see OQ: bump to --text-sec if AA-as-content required */
html[data-theme="light"] .track-why-row,
html[data-theme="light"] .track-neighbor { background: var(--surface-1); border-color: var(--hairline); }
html[data-theme="light"] .track-neighbor:hover { background: var(--surf-hover); border-color: var(--brand-blue-light); }
html[data-theme="light"] .track-why-fix { border-color: var(--border-strong); color: var(--text-sec); }
html[data-theme="light"] .track-why-fix:hover { color: var(--text-pri); border-color: var(--brand-blue-light); }
html[data-theme="light"] .track-vector-bar { background: var(--surf-active); }
html[data-theme="light"] .track-history-row { border-bottom-color: var(--divider); }
html[data-theme="light"] .track-scrubber-wrap .player-progress { background: var(--surf-active); }  /* shared player rail rendered on paper here */
```

**— #/profile (scope text flips to `--open`; closed box stays dark) —**
```css
html[data-theme="light"] .profile-title,
html[data-theme="light"] .profile-section-h,
html[data-theme="light"] .profile-ad-text b,
html[data-theme="light"] .profile-box--open .profile-box-label,
html[data-theme="light"] .profile-box--open .profile-facet-name { color: var(--text-pri); }
html[data-theme="light"] .profile-box--open { background: var(--surface-1); border-color: var(--hairline); box-shadow: var(--sh-2); }
html[data-theme="light"] .profile-panel,
html[data-theme="light"] .profile-ad-strip { background: var(--surface-1); border-color: var(--hairline); box-shadow: var(--sh-1); }
html[data-theme="light"] .profile-box--open .profile-box-tag { color: var(--accent-text); }
html[data-theme="light"] .profile-box--open .profile-facet { border-top-color: var(--divider); }
html[data-theme="light"] .profile-box--open .profile-facet-bar { background: var(--surf-active); }
html[data-theme="light"] .profile-cta--ghost,
html[data-theme="light"] .profile-box--open .profile-facet-lower { border-color: var(--border-strong); color: var(--text-sec); }
html[data-theme="light"] .profile-cta--ghost:hover,
html[data-theme="light"] .profile-box--open .profile-facet-lower:hover { color: var(--text-pri); border-color: var(--text-pri); }
html[data-theme="light"] .profile-rej-chip { color: var(--text-sec); border-color: var(--border-strong); text-decoration-color: var(--text-ter); }
```

**— #/artist (cover bg fixed inline in Step 0; here = borders + nothing else needs text flip, body uses tokens) —**
```css
html[data-theme="light"] .artist-action-secondary,
html[data-theme="light"] .artist-why-item,
html[data-theme="light"] .artist-station-chip { border-color: var(--hairline); }
html[data-theme="light"] .artist-why-reject,
html[data-theme="light"] .artist-why-not { border-color: var(--border-strong); }
html[data-theme="light"] .artist-why-reject:hover,
html[data-theme="light"] .artist-why-not:hover { color: var(--text-pri); border-color: var(--border-strong); }
```
*(Do NOT add the `.artist-track-mono` override — Step 0's inline→blue fix makes white-on-blue correct.)*

**— #/podborki (GALLERY IS DEAD CODE — skip `.podborki-*`; live route = «Открыть» discover surface, mostly already patched) —**
```css
html[data-theme="light"] .discover-input { color: var(--text-pri); }              /* typed search text, was #fff */
html[data-theme="light"] .discover-track-why b { color: var(--accent-text); }     /* was #cdd4f5 pale lavender */
html[data-theme="light"] .discover-map-node.is-known { background: var(--surf-hover); border-color: var(--border-strong); }
```
⚠️ **VERIFY first:** L7365 may already contain `.discover-ask-go:focus-visible { outline-color: var(--accent-on-dark); }`. If present, the `#fff` focus ring is already fixed — **don't duplicate**. (Confirmed-uncovered: `.discover-input`, `.discover-track-why b`, `.discover-map-node.is-known`.)
🟡 Out-of-CSS-scope (flag only): the taste-map `<canvas id="discover-map">` is painted by JS with dark-theme RGBs → may need a JS-side light palette to stay legible. Not part of this CSS sweep.

**— #/lives + #/recap-chrome —**
```css
html[data-theme="light"] .lives-card { border-color: var(--hairline); }
/* recap CARD pinned dark (stays = PNG export O3) */
html[data-theme="light"] .recap-card {
  --bg-base:#0B0C0F; --surface-0:#111318; --surface-1:#15171D; --surface-2:#1B1E26; --surface-3:#23262F;
  --text-pri:#FFFFFF; --text-sec:rgba(255,255,255,.62); --text-ter:rgba(255,255,255,.40); --text-quat:rgba(235,235,245,.60);
  --accent-on-dark:#8094ff; --accent-text:#8094ff; --success:#34d399; --brand-blue-light:#5168FC;
}
/* recap CHROME flips */
html[data-theme="light"] .recap-btn--ghost { border-color: var(--border-strong); }
html[data-theme="light"] .recap-btn--ghost:hover { border-color: var(--text-pri); }
html[data-theme="light"] .recap-delta-row.fade .recap-delta-name { color: var(--text-ter); }
html[data-theme="light"] .recap-discovery-panel { border-color: var(--hairline); background: var(--surface-2); }
```
🟡 `.lives-live-pill` (#ff3b30 red + #fff) does NOT break in light (white-on-red legible) → leave. The red being off single-accent is a **separate** token-correctness flag, out of scope here.

**— Shared chrome (LIGHT-GLASS REPAINT default — see OQ for the dark-rail alternative) —**
```css
html[data-theme="light"] .topbar { background: linear-gradient(180deg, rgba(250,250,247,.82) 0%, rgba(250,250,247,0) 100%); border-bottom: 1px solid var(--hairline); }
html[data-theme="light"] .topbar-account:hover { background: var(--surf-active); }
html[data-theme="light"] .sidebar { background: rgba(255,255,255,.72); border-right: 1px solid var(--hairline); }
html[data-theme="light"] .sidebar-item[aria-current="page"] { background: var(--tint-blue-light-20); box-shadow: inset 3px 0 0 var(--brand-blue-light); }
html[data-theme="light"] .mobile-tabbar { background: rgba(255,255,255,.92); border-top: 1px solid var(--hairline); }
html[data-theme="light"] .home-fab { color: var(--text-pri); border-color: var(--border-strong); box-shadow: var(--sh-2); }
html[data-theme="light"] .home-fab:hover { background: var(--surf-active); box-shadow: var(--sh-3); }
html[data-theme="light"] .tweaks { background: rgba(255,255,255,.94); color: var(--text-pri); }  /* dev-only, low priority */
```
✅ **Leave white (self-paint own dark glass, theme correctly):** `.why-pop`, `.ai-dock`+children, `.ai-launcher` (blue fill), `.ai-ribbon`, `.np-transition`/`.np-transition-card` (TwinrTransition — flat `#111318`, NOT a color-mix site), `.account-backdrop` scrim. These are intentional immersive-dark moments (player-chrome family).

---

## ⚠️ Latent bugs found (light-only; prod forces cinema so not client-visible, but fix while here)
- **#/artist track-cover**: white mono on white cover in light TODAY (inline `var(--surface-1)`). Step 0 fixes it.
- **#/track history row L9054**: `var(--surface-1)` cover + `rgba(255,255,255,.7)` mono = white-on-white in light TODAY. The `.track-history-cover { color: var(--text-pri) }` override fixes it.

## 🟡 Open questions for Эльбик (build NOT blocked — defaults shipped, reversible)
1. **Chrome strategy**: light-glass repaint (default, Apple-day) vs permanent dark "cinema rail" (re-assert dark tokens on topbar/sidebar/tabbar, zero-text-touch). If dark-rail wanted, the chrome CSS block above is replaced by a re-assert-dark scope like the player block.
2. **#/track lyrics**: paper-ink (default) vs immersive-dark lyrics panel.
3. **#/lives red pill**: retint `#ff3b30`→blue/neutral in BOTH themes (separate single-accent pass, not light-sweep).
4. `--text-ter` lyrics ≈3.0:1 on paper — fine for decorative 36px de-emphasized type; bump inactive→`--text-sec` (≈4.7:1) if it must be AA-as-content.
5. Standing gates: GOROD-029 positioning · GOROD-030 licences.

## ✅ Next-session execution order
1. Step 0 seam + inline edits (re-grep all anchors first). 2. Step 1 append override blocks. 3. `node .scratch/check_scripts.cjs` (all `<script>` blocks). 4. Chrome :8770 `?dev=1` → switch to light → walk #/track, #/profile, #/artist, #/podborki, #/lives, #/recap; confirm **dark byte-identical** (toggle back, diff a screenshot/spot-check). 5. Adversarial multi-lens review workflow (dark-regression / light-completeness / honesty). 6. Fold fixes. 7. Regen standalone `python tools/build_gorod_fm_standalone.py`. 8. Update DEBT/RESUME/handoff. **PUSH still held until `sync`.**

## Task list (TaskCreate IDs, all pending)
#1 seam · #2 #/track · #3 #/profile+#/artist · #4 #/podborki+#/lives+#/recap-chrome+shared · #5 verify+review+standalone (blocked by 1-4).

## Artefacts
- **`docs/superpowers/cont-16-light-sweep-analysis.json`** — verbatim 6-agent audit (every rule + rationale + exact line hints + leaveWhite justifications + openQuestions).
- Analysis workflow: `woi5kyh7a` (6 agents, 537k tokens). Script: `…/workflows/scripts/gorod-fm-light-sweep-analysis-wf_9e650818-72d.js`.
- Builder: `tools/build_gorod_fm_standalone.py`. Script-check: `.scratch/check_scripts.cjs`.
- cont-15 handoff: `docs/superpowers/HANDOFF-gorod-fm-cont-15.md`. Light spec: `SPEC-gorod-fm-light-theme.md`.
