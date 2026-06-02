# Город ФМ — Remaining debt plan (cont-11, from inventory wf w9js8v96c)

> 108 remaining items across 12 waves. Grounded against live gorod-fm.html. Anchors DRIFT — re-grep before edit.

## Wave summary
G2 (40): retire --brand-cyan to zero — repoint 43 refs (rings/borders→blue-light, ≤14px text→accent-on-dark), delete alias LAST. G6 (10): anti-slop — flatten live multi-hue tints/gradients (taste-saved, track-history, ai-dock violet, artist orb) + delete dead particle/orb/scaleX/gradient CSS+markup. G7 (7): one focus color (--accent-on-dark) across all 3 ring populations + reduced-motion :active scale + sub-44px tap-area expands. DEFAULT_ROUTE (2): prod cold-start gate → first-timers land #/onboarding (high-risk control-flow) + stale comment. home (8): kill live cover-sampled hero glow + home-only mini-bar tint override + tokenize/hierarchy/markup-desync/height-guard. taste (13): demote dup blue CTA, saved-rows honesty gap, radii/hex/margins tokenize, green-meaning, hover/orb polish. discover (14): ASCII→SVG, map axis/nodes/canvas tokenize, section-title scale, 8pt spacing, ask-field states. track (11): hero cover size/shimmer/double-shadow, unify headings, eyebrow a11y, lyrics contrast, gaps, shared tab-label (med-risk), delete dead up-next/also+base gradient. artist (12): add material+one-column, remove inline tintFor, ghost-token tokenize+unify-reject, 8pt, meta contrast, stations grid, quiet demo badge, rank. onboarding (12): selected-bubble shadow+bg-layer (coordinate G6), dead hue code, one register «вы», collapse alt links, spark scaffold, glyphs→SVG, count/vec-fill, widths. recap_profile (11): tokenize, glyphs→SVG (share-card ▲), button-unify (#6d80ff collision), facet affordance, type ramp, profile width+padding clear mini-player, CLS reserve, share-card green, faux-bars, kicker-dot glow, card top-light. chrome (8): topbar brightness→bg, IA label/icon unify, sidebar row redesign (med-risk web+tv), wordmark no-recolor, dev-gate Карта флоу, tabbar split/indicator/player-route, scrim scroll-tie, theme-toggle copy.

## Conflicts / resolutions
- FOCUS RING TOKEN: G2 wave repoints all cyan rings → --brand-blue-light, but G7-FOCUS-* wants ALL rings (incl global L216) → --accent-on-dark (#8094ff, AA-safe). The G2-cyan analyst chose --brand-blue-light; the G7 analyst says spec L74 mandates --accent-on-dark. RESOLUTION: run G2 first (retire cyan→blue-light, kills the dead alias), then G7 finalizes blue-light→accent-on-dark. Net: a fixer could collapse both and take cyan rings straight to --accent-on-dark, but do NOT touch intentional #fff-on-solid-blue rings (.onb-cta/.ai-send/.discover-*-play/etc).
- ALIAS DELETE ORDERING: G2-00 deletes --brand-cyan def. Must be LAST and AFTER both G2 ref-repoints AND any G7 step that still names --brand-cyan (G7-FOCUS-CYAN-CARD-FAMILY references the alias). Verify grep var(--brand-cyan)=0 before delete.
- ONBOARDING BG LAYERS: G6-6 (delete .onb-bg-particles) overlaps 2.6-P0-selected-shadow (which says drop ONE of bg-particles OR radial::after, not both). If G6-6 removes onb-bg-particles, the onboarding wave must KEEP the .onb-stage::after radial (don't delete both unintentionally → bare stage).
- WORDMARK RECOLOR: G2-03/G2-04 do a minimal cyan→--accent-on-dark repoint, but 2.8-P1d (and §2.6) say the wordmark should NOT recolor at ALL (opacity .85). Chrome wave 2.8-P1d supersedes — final state is no-recolor; G2 repoint is interim. .logo block is dead code (deleting it removes G2-03's target).
- PLAYER-MINI HOME TINT vs cont-11: 2.1-P0-player-mini-blue-tint deletes html[data-active-route=#/home] .player-mini blue !important wash. cont-11 rebuilt .player-mini as a flat 72px bar; this home-only override re-tints it. VERIFY against cont-11 player surface before removing (med risk). Mini-bar itself is excluded from scope per instructions — this is the route OVERRIDE, not the bar.
- --r-lg VALUE vs SPEC: discover (2.3-radius-vocab) wants map-stage=16px but --r-lg=14px; track (2.4-P1-hero-cover-size) wants cover radius→--r-lg(14). Reconcile the radius scale in §0 (is stage 16 a new --r-xl-ish step, or snap to 14?) before applying radius-vocab edits.
- --r-card / --brand-ghost-* MISSING TOKENS: spec references --r-card:13px (2.6-P1-onb-src-radius, 2.6-P2-ai-sparkle) and --brand-ghost-bg/--brand-ghost-border (2.5-P1-tokenize-rgba, 2.5-P2-unify-reject) but NEITHER exists in the file. Decide in §0: add them or use --r-lg(14)/existing alphas. Group the two artist ghost-token items together.
- raw #6d80ff vs canon #6477ff: 2.7-P1-button-unify — profile primary hover uses raw #6d80ff (L3138) which collides with --brand-blue-hover #6477ff; unify to the token.
- #/lives LIVE pill #ff3b30 red is genuinely off-palette (only blue UI / green growth allowed) but the route is an orphan (no nav link). Listed dropped_subsumed→G2-family as the only cheap worth-shipping dev-route fix; otherwise NA. .lives-card buttons are dead (data-station handler binds .home-station only) — convert to <article> if kept, else leave (NA).

## Ordered items

### Wave: G2

- **[G2-01] P0 · global · risk=low** — html accent-color cyan → blue-light
  - anchor: `accent-color: var(--brand-cyan);`
  - target: accent-color: var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L33 html{}. Repoint refs FIRST; alias def G2-00 deleted LAST.

- **[G2-02] P0 · global · risk=low** — Global :focus-visible ring (L216) cyan→blue-light
  - anchor: `outline: 3px solid var(--brand-cyan);`
  - target: outline: 3px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L216 global :focus-visible. NON-UNIQUE (~20×) — grep with global focus selector ~L213-217. CONFLICT: G7-FOCUS-GLOBAL wants --accent-on-dark here, not --brand-blue-light. Resolve in G7 wave (G7 re-targets all rings to --accent-on-dark AFTER G2 retires cyan). Do the cyan→blue swap here, then G7 corrects shade.

- **[G2-05] P0 · map(dev) · risk=low** — map badge background (L1526) cyan→blue-light
  - anchor: `        background: var(--brand-cyan);`
  - target: background: var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L1526 dev-gated #/map but ships CSS. Filled badge bg, large.

- **[G2-06] P0 · map(dev) · risk=low** — map badge border-color (L1528) cyan→blue-light
  - anchor: `        border-color: var(--brand-cyan);`
  - target: border-color: var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L1528. NON-UNIQUE border-color — grep near L1526 bg ref.

- **[G2-09] P0 · map(dev) · risk=low** — map focus ring (L1708) cyan→blue-light
  - anchor: `        outline: 3px solid var(--brand-cyan);`
  - target: outline: 3px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L1708 map focus-visible. NON-UNIQUE — region ~L1705-1710.

- **[G2-11] P0 · home · risk=med** — .home-hero-overline color (11px) cyan→accent-on-dark
  - anchor: `        color: var(--brand-cyan); ⏎         text-align: center; ⏎         text-shadow:`
  - target: color: var(--accent-on-dark);
  - token: --accent-on-dark
  - note: L3528, 11px/700 uppercase overline — small text → --accent-on-dark for AA.

- **[G2-13] P0 · home · risk=low** — home focus ring (L3646, 3px) cyan→blue-light
  - anchor: `        outline: 3px solid var(--brand-cyan);`
  - target: outline: 3px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L3646 home focus-visible. NON-UNIQUE 3px outline. G7 will re-shade to accent-on-dark.

- **[G2-15] P0 · home · risk=low** — home focus ring (L3719, 3px) cyan→blue-light
  - anchor: `        outline: 3px solid var(--brand-cyan);`
  - target: outline: 3px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L3719. NON-UNIQUE — region ~L3715-3720.

- **[G2-17] P0 · home · risk=low** — home focus ring (L4010, 3px) cyan→blue-light
  - anchor: `        outline: 3px solid var(--brand-cyan);`
  - target: outline: 3px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L4010. NON-UNIQUE — region ~L4006-4011.

- **[G2-20] P0 · home · risk=low** — focus ring (L4226, 3px) cyan→blue-light
  - anchor: `        outline: 3px solid var(--brand-cyan);`
  - target: outline: 3px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L4226. NON-UNIQUE — region ~L4222-4227.

- **[G2-21] P0 · library(dead) · risk=low** — library focus ring (L4379, 3px) cyan→blue-light
  - anchor: `        outline: 3px solid var(--brand-cyan);`
  - target: outline: 3px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L4379 library (redirected→taste, but ships). NON-UNIQUE — region ~L4375-4380.

- **[G2-23] P0 · library(dead) · risk=low** — .library-tile:hover box-shadow ring cyan→blue-light
  - anchor: `        box-shadow: 0 0 0 2px var(--brand-cyan), 0 8px 24px rgba(0, 0, 0, 0.5);`
  - target: box-shadow: 0 0 0 2px var(--brand-blue-light), 0 8px 24px rgba(0, 0, 0, 0.5);
  - token: --brand-blue-light
  - note: L4586 hover ring on cover.

- **[G2-24] P0 · library(dead) · risk=low** — .library-tile focus ring (L4590, 3px) cyan→blue-light
  - anchor: `        outline: 3px solid var(--brand-cyan); ⏎         outline-offset: 3px; ⏎         border-radius: 14px;`
  - target: outline: 3px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L4590 unique via border-radius:14px below.

- **[G2-26] P0 · library(dead) · risk=low** — library focus ring (L4717, 3px) cyan→blue-light
  - anchor: `        outline: 3px solid var(--brand-cyan);`
  - target: outline: 3px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L4717. NON-UNIQUE — region ~L4713-4718.

- **[G2-27] P0 · library(dead) · risk=low** — library focus ring (L4804, 3px) cyan→blue-light
  - anchor: `        outline: 3px solid var(--brand-cyan);`
  - target: outline: 3px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L4804. NON-UNIQUE — region ~L4800-4805.

- **[G2-29] P0 · favorites(dead) · risk=low** — favorites focus ring (L5260, 3px) cyan→blue-light
  - anchor: `        outline: 3px solid var(--brand-cyan);`
  - target: outline: 3px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L5260 favorites (redirected→taste). NON-UNIQUE — region ~L5256-5261.

- **[G2-30] P0 · favorites(dead) · risk=low** — favorites focus ring (L5299, 3px) cyan→blue-light
  - anchor: `        outline: 3px solid var(--brand-cyan);`
  - target: outline: 3px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L5299. NON-UNIQUE — region ~L5295-5300.

- **[G2-33] P0 · favorites(dead) · risk=low** — favorites focus ring (L5411, 3px) cyan→blue-light
  - anchor: `        outline: 3px solid var(--brand-cyan);`
  - target: outline: 3px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L5411. NON-UNIQUE — region ~L5407-5412.

- **[G2-35] P0 · track · risk=low** — track focus ring (L5684, 3px) cyan→blue-light
  - anchor: `        outline: 3px solid var(--brand-cyan);`
  - target: outline: 3px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L5684 (in dead up-next block, vanishes with 2.4-P2-dead-upnext-also). NON-UNIQUE.

- **[G2-37] P0 · track · risk=low** — track focus ring (L5884, 3px) cyan→blue-light
  - anchor: `        outline: 3px solid var(--brand-cyan);`
  - target: outline: 3px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L5884 (in dead history-plus/also block). NON-UNIQUE — region ~L5880-5885.

- **[G2-38] P0 · track · risk=low** — track focus ring (L5962, 3px) cyan→blue-light
  - anchor: `        outline: 3px solid var(--brand-cyan);`
  - target: outline: 3px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L5962 (dead .track-also-card). NON-UNIQUE — region ~L5958-5963.

- **[G2-40] P2 · carplay(dev) · risk=low** — CarPlay --player-accent override cyan→blue-light (or delete)
  - anchor: `        --player-accent: var(--brand-cyan);`
  - target: --player-accent: var(--brand-blue-light);  /* redundant vs L123 default — consider deleting line */
  - token: --brand-blue-light
  - note: L6306 [data-surface=carplay] UNIQUE. Matches L123 default → redundant override; delete preferred.

- **[G2-03] P1 · chrome · risk=low** — .logo:hover color cyan→accent-on-dark (DEAD .logo)
  - anchor: `      .logo:hover { ⏎         color: var(--brand-cyan);`
  - target: color: var(--accent-on-dark);
  - token: --accent-on-dark
  - note: L339. .logo is DEAD CODE (no class=logo in markup, per 2.8-P1d). §2.6/2.8 prefer NO recolor (opacity .85). Minimal G2 = repoint; full §2.8 chrome wave (2.8-P1d) decides delete-vs-opacity. Could delete whole .logo block.

- **[G2-04] P1 · chrome · risk=low** — .sidebar-logo:hover color cyan→accent-on-dark
  - anchor: `      .sidebar-logo:hover { ⏎         color: var(--brand-cyan);`
  - target: color: var(--accent-on-dark);
  - token: --accent-on-dark
  - note: L442. Live wordmark. Minimal G2 = repoint; chrome wave 2.8-P1d wants NO recolor (opacity .85) — final fix deferred there. CONFLICT-adjacent: pick one in chrome wave.

- **[G2-07] P1 · map(dev) · risk=med** — .map-internal-badge color (12px) cyan→accent-on-dark
  - anchor: `        color: var(--brand-cyan); ⏎         font-size: 12px;`
  - target: color: var(--accent-on-dark);
  - token: --accent-on-dark
  - note: L1604, 12px uppercase badge — small text AA → --accent-on-dark.

- **[G2-08] P1 · map(dev) · risk=low** — map border-color (L1698) cyan→blue-light
  - anchor: `        border-color: var(--brand-cyan);`
  - target: border-color: var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L1698 map card border. NON-UNIQUE — region ~L1690-1700.

- **[G2-10] P1 · map(dev) · risk=low** — map border-color (L1719) cyan→blue-light
  - anchor: `        border-color: var(--brand-cyan);`
  - target: border-color: var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L1719 map. NON-UNIQUE — region ~L1715-1720.

- **[G2-12] P1 · home · risk=low** — home track focus (L3639, 2px) cyan→blue-light
  - anchor: `        outline: 2px solid var(--brand-cyan);`
  - target: outline: 2px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L3639. NON-UNIQUE 2px (also L5714) — region ~L3635-3640.

- **[G2-14] P1 · home · risk=low** — .home-station-icon svg stroke cyan→blue-light
  - anchor: `        stroke: var(--brand-cyan); ⏎         fill: none;`
  - target: stroke: var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L3660 18px SVG icon stroke — visual → --brand-blue-light.

- **[G2-16] P1 · home · risk=low** — .home-tf-bar-fill blue→blue gradient → solid blue-light
  - anchor: `        background: linear-gradient(90deg, var(--brand-cyan), var(--brand-blue));`
  - target: background: var(--brand-blue-light);  /* solid per §1A; drops --brand-blue dep */
  - token: --brand-blue-light
  - note: L3877 progress fill. §1A wants SOLID fills — collapse 2-stop gradient.

- **[G2-18] P1 · home · risk=med** — .home-tf-open-player color (13px) cyan→accent-on-dark
  - anchor: `        font-size: 13px; ⏎         font-weight: 600; ⏎         color: var(--brand-cyan);`
  - target: color: var(--accent-on-dark);
  - token: --accent-on-dark
  - note: L4030, 13px button label → small text.

- **[G2-19] P1 · home · risk=med** — .home-tf-open-player:hover color (13px) cyan→accent-on-dark
  - anchor: `        background: rgba(81, 104, 252, 0.20); ⏎         color: var(--brand-cyan);`
  - target: color: var(--accent-on-dark);
  - token: --accent-on-dark
  - note: L4042 hover of same 13px button.

- **[G2-22] P1 · library(dead) · risk=med** — .library-eyebrow color (12px) cyan→accent-on-dark
  - anchor: `        text-transform: uppercase; ⏎         color: var(--brand-cyan); ⏎         margin: 0 0 12px;`
  - target: color: var(--accent-on-dark);
  - token: --accent-on-dark
  - note: L4466, 12px/700 eyebrow.

- **[G2-25] P1 · library(dead) · risk=med** — library eyebrow color (9px, L4683) cyan→accent-on-dark
  - anchor: `        font-size: 9px; ⏎         font-weight: 700; ⏎         letter-spacing: 0.1em; ⏎         text-transform: uppercase; ⏎         color: var(--brand-cyan);`
  - target: color: var(--accent-on-dark);
  - token: --accent-on-dark
  - note: L4683, 9px — smallest text, AA critical.

- **[G2-28] P1 · favorites(dead) · risk=med** — .favorites-eyebrow color (11px) cyan→accent-on-dark
  - anchor: `        font-size: 11px; ⏎         font-weight: 700; ⏎         letter-spacing: 0.10em; ⏎         text-transform: uppercase; ⏎         color: var(--brand-cyan); ⏎         margin: 0 0 12px; ⏎         line-height: 1;`
  - target: color: var(--accent-on-dark);
  - token: --accent-on-dark
  - note: L5180, 11px eyebrow.

- **[G2-31] P1 · favorites(dead) · risk=med** — .favorites-type-badge--track color cyan→accent-on-dark
  - anchor: `        background: rgba(81, 104, 252,0.15); ⏎         border: 1px solid rgba(81, 104, 252,0.30); ⏎         color: var(--brand-cyan);`
  - target: color: var(--accent-on-dark);
  - token: --accent-on-dark
  - note: L5357 pill badge text — unique via preceding rgba bg/border.

- **[G2-32] P1 · favorites(dead) · risk=low** — favorites icon-btn color (L5399) cyan→blue-light
  - anchor: `        background: var(--surf-glass-12); ⏎         border: none; ⏎         color: var(--brand-cyan); ⏎         cursor: pointer;`
  - target: color: var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L5399 tints icon glyph (not body text) → --brand-blue-light.

- **[G2-34] P1 · track · risk=med** — .track-eyebrow color (11px) cyan→accent-on-dark
  - anchor: `        letter-spacing: 0.12em; ⏎         text-transform: uppercase; ⏎         color: var(--brand-cyan); ⏎         margin: 0 0 24px; ⏎         text-align: center;`
  - target: color: var(--accent-on-dark);
  - token: --accent-on-dark
  - note: L5465 track eyebrow 11px. §2.4-P1-eyebrow ALSO needs aria-hidden removed on markup L8542 — handled in track wave (color swap here, a11y there).

- **[G2-36] P1 · track · risk=low** — track focus ring (L5714, 2px) cyan→blue-light
  - anchor: `        outline: 2px solid var(--brand-cyan);`
  - target: outline: 2px solid var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L5714 (dead up-next--current). NON-UNIQUE 2px (also L3639) — region ~L5710-5715.

- **[G2-39] P1 · track · risk=low** — outline-color cyan (L6205) → blue-light
  - anchor: `        outline-color: var(--brand-cyan);`
  - target: outline-color: var(--brand-blue-light);
  - token: --brand-blue-light
  - note: L6205 UNIQUE (only outline-color: ref).

- **[G2-00] P0 · global · risk=med** — DELETE --brand-cyan alias token def (do LAST)
  - anchor: `--brand-cyan:      #5168FC;   /* RETIRED → blue family (one-accent); legacy alias so var(--brand-cyan) refs resolve blue */`
  - target: DELETE line entirely (after all 43 refs repointed AND after G2-grep returns 0)
  - token: n/a (removal)
  - note: L88. MUST be the final G2 action — and ideally after G7 too if any G7 step still references the alias. Verify grep var(--brand-cyan)=0 before deleting. HIGH-RISK ordering gate: deleting early breaks every unconverted ref.

### Wave: G6

- **[G6-1] P0 · taste · risk=low** — Taste «Сохранённое» tint(): 2-hue HSL over-sat gradient → flat single tint
  - anchor: `return 'linear-gradient(135deg, hsl(' + hue + ',62%,30%), hsl(' + hue + ',70%,48%))';`
  - target: flat fill rgba(81,104,252,.18)+monogram OR single hue clamp 222-236 sat<=40% e.g. 'hsl('+hue+',38%,30%)'
  - token: --tint-blue-light-20 / hue222-236 sat<=40
  - note: L14444 tint() feeds live .taste-saved-tint (L14455). Only LIVE over-sat multi-hue placeholder. §2.2-P2-saved-tint-hsl is the same item (subsumed).

- **[G6-2] P0 · track · risk=low** — Track deep-dive history covers: 9 inline multi-hue gradients → flat tint+monogram
  - anchor: `class="track-history-cover" style="background: linear-gradient(135deg, #2c3e50, #4a6fa5);"`
  - target: flat color-mix(in oklab, var(--np-accent) 22%, #111318) OR var(--surface-1) + keep mono letters; delete all 9 inline gradients incl green #1a6b3a row
  - token: --surface-1 / color-mix(--np-accent 22%)
  - note: L8776-8903 (9 of 10 rows; L8889 already flat). LIVE история view. Subsumes 2.4-P0-history-covers AND 2.4-P0-history-cover-green (green #1a6b3a is growth-only, must go in same edit).

- **[G6-3] P1 · artist · risk=low** — Artist track-row cover: white radial-gradient orb ::after sheen → remove
  - anchor: `background:radial-gradient(110% 110% at 30% 25%, rgba(255,255,255,0.16), rgba(0,0,0,0.28));`
  - target: delete the ::after (or flat top-light linear-gradient(180deg,rgba(255,255,255,.06),transparent)); base .artist-track-cover already flat
  - token: --hairline top-light / remove
  - note: L4984 white-orb halo per row. Coupled with 2.5-P1-trackcovers which ALSO removes inline tintFor() at JS L14626 — see artist wave. Keep hero tintFor (L14643).

- **[G6-4] P1 · ai-dock · risk=low** — AI-dock header violet multi-hue gradient → single-accent flat
  - anchor: `background: linear-gradient(135deg, rgba(81, 104, 252, 0.18), rgba(139, 92, 246, 0.10));`
  - target: rgba(81,104,252,.14) OR color-mix(in oklab,var(--brand-blue-light) 14%,transparent) — drop violet rgba(139,92,246) stop
  - token: --tint-blue-light-20
  - note: L2834 .ai-dock-head. 2nd hue #8b5cf6 violates ONE-accent; live on any surface. Same violet dead in L2761/4616/5478.

- **[G6-11] P2 · player(verify) · risk=med** — Full-player history covers: 8 inline multi-hue gradients — VERIFY reachability
  - anchor: `<div class="player-history-item-cover" style="background: linear-gradient(135deg, #2c3e50, #4a6fa5);">LP</div>`
  - target: IF full-player history panel reachable → flat var(--surface-1)+mono (promotes to P1 live); ELSE delete L10189-10288
  - token: --surface-1 + monogram
  - note: L10189-10288. VERIFY-BEFORE-FIX: confirm full-player history surface is reachable in prod. If yes, same treatment as G6-2.

- **[G6-5] P2 · player(dead) · risk=low** — Delete dead .player-mini-art-placeholder--1/2/3 multi-hue gradients
  - anchor: `.player-mini-art-placeholder--2 { background: linear-gradient(135deg, #7b2d8b, #c43a6e); }`
  - target: delete L627-629 (and base L611 if unreferenced) — live mini bar uses real <img> L9935
  - token: n/a (delete dead CSS)
  - note: L627-629 purple/pink/green. Orphaned by cont-11 mini-bar (markup retired, palettes left). Confirm no other ref before deleting base.

- **[G6-6] P2 · home/onb(dead+live) · risk=low** — Delete .home-bg-particles (dead) + .onb-bg-particles blurred PNG fields
  - anchor: `background: url(assets/gorod-fm/home-bg-particles.png) center/cover no-repeat;`
  - target: delete .home-bg-particles CSS L1808 + markup L7605 (hidden .home-tiles); onboarding .onb-bg-particles CSS L2228 + markup L9307 → flat var(--home-bg-base)
  - token: --home-bg-base
  - note: Shared PNG. Home instance dead (hidden .home-tiles); onb instance LIVE if onboarding shown. Subsumes 2.1-P1-bg-particles (home half). NOTE: onb half overlaps 2.6-P0-selected-shadow which wants to drop ONE of bg-particles/radial::after — coordinate: if G6 deletes onb-bg-particles, keep the onb radial::after (or vice versa), not both gone unintentionally. CONFLICT flag.

- **[G6-7] P2 · home(dead) · risk=low** — Delete .home-featured-halo white/blue radial orb
  - anchor: `background: radial-gradient(50% 50% at 50% 45%, rgba(81, 104, 252, 0.07), transparent 72%);`
  - target: delete .home-featured-halo rule L1964 + markup L7714 (inside hidden .home-tiles)
  - token: n/a (delete dead orb)
  - note: L1971 blur(24px). cont-10 de-whited (now faint blue .07). Subsumes 2.1-P0-featured-halo PARTIAL (spec wants DELETE; dead anyway).

- **[G6-8] P2 · home/lib/fav(dead) · risk=low** — Delete rotated 900-weight scaleX(1.05) tile labels
  - anchor: `transform: rotate(-90deg) scaleX(1.05);`
  - target: delete dead rule sets (.home-tile-label L1958 + sibling scaleX/rotate L4433/5036/5135/5191); any surviving horizontal label → weight 700, sentence case, no scaleX
  - token: font-weight 700, no transform
  - note: L1958 inside hidden .home-tiles. Subsumes 2.1-P1-tile-labels (home half — but home-featured-title L2033-2037 scaleX fold-in is LIVE-ish; verify .home-tiles hidden covers it). scaleX also on .map-heading L1617 / .lives-title L5036 / .favorites-title L5191 (2.9 items) — global scaleX-purge here covers them.

- **[G6-9] P2 · library(dead) · risk=low** — Delete dead .library-tile-cover gradients + ::after shimmer + ad-slot gradient + cyan #1ecfe0 leak
  - anchor: `<div class="library-tile-cover library-tile-cover--album" style="background:linear-gradient(135deg,#0a2f70 0%,#0d74c4 45%,#1ecfe0 100%);">`
  - target: delete CSS L4610-4642 + 6 inline-gradient tiles L8148+ + .library-ad-slot gradient L4707
  - token: n/a (dead, redirected)
  - note: #/library folds to #/taste (L10743). Inline cyan #1ecfe0 (L8148) is also a retired-cyan leak; ::after shimmer L4640 white-orb slop. All dead but ships.

- **[G6-10] P2 · favorites(dead) · risk=low** — Delete dead .favorites-row-thumb (16 inline multi-hue gradients)
  - anchor: `<div class="favorites-row-thumb" aria-hidden="true" style="background:linear-gradient(135deg,#1a4fa0,#8b2da0)"></div>`
  - target: delete 16 inline-gradient thumbs L9046-9286
  - token: n/a (dead, redirected)
  - note: #/favorites folds to #/taste. purple/pink/green palettes. Dead but ships.

### Wave: G7

- **[G7-FOCUS-GLOBAL] P1 · global · risk=low** — Global :focus-visible (L215-219) → --accent-on-dark (one focus color)
  - anchor: `outline: 3px solid var(--brand-cyan);`
  - target: outline: 3px solid var(--accent-on-dark); outline-offset:2px (base @layer rule L215-219)
  - token: --accent-on-dark (#8094ff)
  - note: Spec L74 mandates ONE focus color=--accent-on-dark. CONFLICT with G2-02 which set this to --brand-blue-light; G7 supersedes (correct shade). Run G7 AFTER G2. Single source-of-truth for every unstyled control.

- **[G7-FOCUS-BLUELIGHT-FAMILY] P1 · global · risk=med** — ~30+ per-component focus rings --brand-blue-light → --accent-on-dark
  - anchor: `:focus-visible { outline: 3px solid var(--brand-blue-light); outline-offset: 2px; }`
  - target: replace var(--brand-blue-light)→var(--accent-on-dark) across family (keep offsets). Offenders: .why-row-reject,.why-pop-more,.home-ctx-card,.home-view-btn,.home-hero,.home-radio-why,.home-radio-like/.steer/.skip,.onb-alt,.resume-*,.onb-vec-btn/.onb-model-ghost/.onb-src,.ai-dock-btn,.ai-chip,.wave-chip,.ai-ribbon-why,.profile-cta/.profile-facet-lower,.taste-sonify/.ctx-chip/.taste-ctrl/.taste-saved-sum/.taste-saved-chip/.taste-sponsor-less,.discover-chip/.discover-near-card/.discover-dial-btn/.discover-map-node/.discover-ed-card,.artist-*,.track-why-fix/.track-neighbor
  - token: --accent-on-dark
  - note: --brand-blue-light on near-black=4.25:1 fails AA for thin ring. DO NOT touch #fff-on-solid-blue rings (.onb-cta/.ai-send/.discover-*-play intentional). Subsumes 2.7-P2-focus-visible (profile-cta/.profile-facet-lower) and many per-surface focus items. Re-grep family before bulk edit.

- **[G7-FOCUS-CYAN-CARD-FAMILY] P1 · global · risk=med** — ~22 card/tile/row focus rings literal --brand-cyan → --accent-on-dark
  - anchor: `outline: 3px solid var(--brand-cyan);`
  - target: var(--accent-on-dark). Rings still on cyan alias: .home-chip,.home-tile,.home-featured-play,.home-station(2px),.home-fab,.home-tf-action-btn,.podborki-chip,.podborki-tile,.library-chip/.library-tile(box-shadow 0 0 0 2px)/.library-ad-slot/.library-show-more,.favorites-chip/.favorites-row/.favorites-heart-btn,.track-up-next-card,.track-history-plus,.track-also-card,.map-card
  - token: --accent-on-dark
  - note: These overlap the G2 cyan-ring items (G2-13/15/17/20/etc set them to --brand-blue-light); G7 re-targets to --accent-on-dark — net: do G2 cyan→blue-light first, then G7 blue-light→accent-on-dark, OR collapse: in G7 take all rings straight to --accent-on-dark. Convert .library-tile box-shadow form → outline. .map-card dev-route low prio.

- **[G7-ACTIVE-SCALE-STANDARD] P1 · global · risk=med** — Add reduced-motion-gated :active{scale(.98)} across buttons/cards/rows; normalize 0.96→0.98
  - anchor: `.ai-chip:active { transform: scale(0.96); }`
  - target: one shared rule inside @media(prefers-reduced-motion:no-preference){ ...:active{transform:scale(.98)} } covering .home-chip/.home-tile/.home-ctx-card,.taste-ctrl/.taste-saved-chip,.discover-*,.library-*,.favorites-*,.artist-*,.track-*,.podborki-*; normalize existing 0.96 (.ai-chip)→.98
  - token: --lift / scale(.98), gate @media no-preference (spec L109)
  - note: Spec L72/L109/L172. Currently :active only on .onb-cta/.resume-go/.resume-build/.onb-model-go/.ai-chip/.home-fab and NONE gated. Subsumes 2.3-cta-hover-active (:active half), 2.5-P1-cta-active-shadow (:active half), 2.2/2.7 :active gaps. Re-grep selector list — many families. Define --lift:-2px token here too (used by discover hover).

- **[G7-HIT-TRACK-PLAY-SMALL] P0 · global · risk=low** — Small play buttons <44px → ::before tap-area expand (ai-track-play 30, discover-track-play 36, discover-dial-btn 36)
  - anchor: `.discover-track-play { flex: none; width: 36px; height: 36px; border-radius: 50%;`
  - target: keep visual; add position:relative + ::before{content:'';position:absolute;inset:-9px/-7px} for ≥44px tap. Also .ai-track-play L2930 (30px) and .discover-dial-btn L4290 (min-height:36px)
  - token: ::before{inset:-9px} (spec L166)
  - note: Spec L166 P0. Subsumes 2.3-track-play-44 (discover-track-play is the same control).

- **[G7-HIT-TASTE-CTRLS] P2 · taste · risk=low** — taste-pin (26px) + taste-ctrl (26px) + taste-saved-chip (40) → 44px hit area
  - anchor: `width: 26px; height: 26px; border-radius: 7px; flex-shrink: 0;`
  - target: keep 26px visual; position:relative + ::before{inset:-9px} (~44px). Both .taste-pin (L3388) and .taste-ctrl (L3402) share the 26px line — edit each block separately. taste-saved-chip min-height 40→44 (L3452 is 34→bump)
  - token: ::before{inset:-9px} (spec L160)
  - note: Subsumes 2.2-P2-hit-area entirely. Identical anchor on two selectors — target each block.

### Wave: DEFAULT_ROUTE

- **[G8-COLDSTART-GATE] P1 · boot · risk=med** — Prod cold-start: first-time visitor (no taste, never onboarded) lands #/onboarding not #/home
  - anchor: `var h = location.hash || ''; ⏎       if (h === '' || h === '#/map') location.hash = '#/home';`
  - target: In !dev branch of early G4 dev-gate IIFE (L7179-7180), before boot: var onb=false,tst=false; try{onb=!!localStorage.getItem('gorodfm_onboarded');tst=!!localStorage.getItem('gorodfm_taste');}catch(e){} if(h===''||h==='#/map'){location.hash=(!onb&&!tst)?'#/onboarding':'#/home';} Leave deep-links untouched.
  - token: n/a (control-flow)
  - note: HIGH-RISK: must NOT fire on explicit deep-links; returning users (either flag) keep #/home. Flags exist+durable (gorodfm_onboarded L12395, gorodfm_taste saveTaste). Early IIFE L7166-7181 is the real 'before savedRoute' site. #/onboarding in VALID_ROUTES L10718, not dev-gated. Net-new debt (no spec item).

- **[G8-BOOT-DEFAULT-COMMENT] P2 · boot · risk=low** — Fix stale boot() comment ('default #/map'); leave resolution chain
  - anchor: `var hashRoute    = routeFromHash(window.location.hash); ⏎         var savedRoute   = lsGet(LS_KEYS.lastRoute, null); ⏎         var initialRoute = hashRoute || (routeFromHash(savedRoute) ? savedRoute : DEFAULT_ROUTE);`
  - target: Keep resolution chain (early gate already decided). Fix misleading comment L11845-11846 'current hash -> saved last route -> default #/map' since prod DEFAULT_ROUTE is effectively #/home via early gate. Leave DEFAULT_ROUTE const='#/map' L10719 (dev-only path, never reached in prod).
  - token: n/a
  - note: PARTIAL — decision lives in early IIFE not here. Comment-only cleanup. Depends on G8-COLDSTART-GATE.

### Wave: home

- **[2.1-P0-hero-glow] P0 · home · risk=low** — Hero cover-sampled colored glow shadow → neutral depth
  - anchor: `0 24px 70px -16px rgba(0,0,0,0.65), 0 0 0 1px rgba(255,255,255,0.06), 0 18px 60px -20px var(--home-np)`
  - target: drop 3rd shadow layer (var(--home-np)); keep 0 12px 32px -12px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.06) (or --sh-3). Also drop matching hover layer 0 24px 70px -18px var(--home-np) at L2135
  - token: --sh-3 / rgba ladder
  - note: LIVE on DEFAULT surface: --home-np set by paintHero() L13355 from cover-sampled --np-accent — the forbidden cover-sampled glow. Two spots L2132 resting + L2135 hover. Highest-value home item.

- **[2.1-P0-player-mini-blue-tint] P0 · home · risk=med** — Delete route-specific !important blue player-mini tint on #/home
  - anchor: `html[data-active-route="#/home"] .player-mini { ⏎         background: var(--tint-blue-light-20) !important; ⏎       }`
  - target: Delete rule L2081-2083 so mini bar is cross-route consistent
  - token: n/a (delete)
  - note: CONFLICT with cont-11 flat mini-bar work — this !important wash re-tints it blue only on home, breaking the just-flattened bar. VERIFY against cont-11 player surface before removing. Spec L137 cross-route consistency.

- **[2.1-P1-raw-hero-tokens] P1 · home · risk=low** — Tokenize raw hero radii/bg/type (.home-radio hero + meta)
  - anchor: `border-radius: 20px; overflow: hidden; background: #111318;`
  - target: hero radius 20→--r-xl; bg #111318→--surface-0; title fs 22/15 (L2151-2152)+why 13+ctx-cap 11→§0 type ramp; tile radius 20px L1986→--r-xl
  - token: --r-xl / --surface-0 / --text-pri/sec/ter
  - note: L2131 hardcodes 20px+#111318 (both exist as tokens). Partly G1 remit; home not fully swept.

- **[2.1-P1-tile-labels-live] P1 · home · risk=med** — home-featured-title scaleX(1.05)+900 → 700, no scaleX (LIVE part)
  - anchor: `transform: rotate(-90deg) scaleX(1.05);`
  - target: home-featured-title L2033-2037 (font-weight 900 + scaleX 1.05) → weight 700, no scaleX, sentence case. Vertical .home-tile-label labels handled by G6-8 (dead .home-tiles).
  - token: font-weight 700, no transform
  - note: Most of 2.1-P1-tile-labels subsumed by G6-8 (dead tiles). RESIDUAL: home-featured-title is the live-ish piece + 8 tiles' data-label ALL-CAPS recase if .home-tiles ever shown. VERIFY .home-tiles truly hidden; if so this is dead too. Kept distinct from G6 because it's a weight/case fix not pure deletion.

- **[2.1-P1-control-hierarchy] P1 · home · risk=low** — Skip resting alpha .40→.55; Like/Steer hover add bg shift (not lift-only)
  - anchor: `.home-radio-like:hover, .home-radio-steer:hover { transform: translateY(-1px); }`
  - target: Skip resting rgba(255,255,255,0.40) L2167→~.55 (.85 hover); Like hover surface shift .06→.12; keep Steer the one filled primary; add bg change at L2164
  - token: n/a
  - note: L2164 hover = translateY only. Live radio controls.

- **[2.1-P2-hero-markup-fidelity] P2 · home · risk=med** — Hero art↔title desync: paintWhy() must also set hero-art src
  - anchor: `var hero=$('home-hero-btn'); if(hero && t && a) hero.setAttribute('aria-label','Открыть плеер: '+t.textContent+' — '+a.textContent);`
  - target: paintWhy() L14338 syncs title+artist+aria but NOT hero ART (stays static egor-krid.png L7571 while title→'Любимка'/Niletto). Make paintWhy() also set home-hero-art src to match named track
  - token: n/a
  - note: Real desync bug: initial DOM Egor Krid cover (L7571) vs Niletto title/artist/aria (L7570/7581/7582). Fidelity violation.

- **[2.1-P2-genre-chip-uppercase] P2 · home(dead) · risk=low** — Genre chips uppercase→sentence case, 17/500→15/600 + recase DOM labels
  - anchor: `letter-spacing: 0.02em; ⏎         text-transform: uppercase; ⏎         cursor: pointer;`
  - target: .home-chip L1845 → 15px/600 sentence case; recase DOM РОК/ДИСКО/ПОП L7615+ → Рок/Диско/Поп + aria-labels
  - token: n/a
  - note: In hidden .home-tiles view (dead-ish). Recase both CSS + literal DOM/aria.

- **[2.1-P2-hero-height-guard] P2 · home · risk=low** — Hero height guard for short/landscape (dvh clamp + overflow-y)
  - anchor: `width: min(360px, 78vw); aspect-ratio: 1 / 1;`
  - target: hero width:min(360px,78vw,42dvh) (L2130); .home-radio{overflow-y:auto} (L2103) so controls aren't clipped
  - token: n/a
  - note: Live radio. Square hero + 3-row bottom can clip controls on landscape.

### Wave: taste

- **[2.2-P1-two-blue-cta] P1 · taste · risk=low** — Demote «Открытый профиль» — two identical blue CTAs in hero
  - anchor: `class="taste-share-btn" href="#/profile" id="taste-open-profile"`
  - target: Открытый профиль → secondary: transparent bg + 1px var(--border-strong) + color var(--text-pri); keep Поделиться filled; soften share-btn shadow to 0 6px 18px rgba(81,104,252,.28)
  - token: --text-pri / --border-strong
  - note: L9478 reuses .taste-share-btn (filled blue) identical to L9470 — two equal-weight CTAs. Highest-value taste item, 1-line.

- **[2.2-P1-saved-rows-real] P1 · taste · risk=med** — Saved rows honesty gap: make interactive OR drop «Лайк здесь =» claim
  - anchor: `return '<div class="taste-saved-row" role="listitem">' +`
  - target: Make rows real (role=button, cursor:pointer, hover bg .05, focus ring, click→like/feed) OR drop the affordance + the «Лайк здесь = сигнал в вектор» lead L9566
  - token: --brand-blue-light (focus ring → see G7)
  - note: rowHtml L14454 emits static div; lead L9566 promises interactivity that doesn't exist. If made interactive, focus ring lands via G7 family. Honesty/fidelity gap.

- **[2.2-P1-radii] P1 · taste · risk=med** — 8 one-off radii → §0 scale
  - anchor: `border-radius: 24px; ⏎         overflow: hidden; ⏎         min-height: 280px;`
  - target: hero 24→--r-xl(20)/keep, group 16, streak/saved 16, saved-row 12, tint 9→--r-md, pin/ctrl 7→8, why 11→12
  - token: --r-xl/--r-lg/--r-md/--r-sm
  - note: PARTIAL. Hardcoded radii hero 24(L3293)/group 16(L3376)/streak 14(L3424)/saved 16(L3436)/saved-row 12(L3461)/tint 9(L3462)/pin 7(L3389)/ctrl 7(L3403)/why 11. Chips/rows already --r-pill.

- **[2.2-P1-hover-lift] P1 · taste · risk=low** — share-btn hover = lift-only → add bg/border/shadow
  - anchor: `.taste-share-btn:hover { transform: translateY(-2px); }`
  - target: add background:var(--brand-blue-hover) on hover, not transform-only
  - token: --brand-blue-hover
  - note: L3330 only translateY. (:active scale comes from G7-ACTIVE-SCALE.)

- **[2.2-P1-oneoff-hex] P1 · taste · risk=med** — Tokenize one-off hex/rgba (hero #14161c/#0c0d12, #eef0f6, #d6dbe8, alpha ladder)
  - anchor: `background: linear-gradient(160deg, #14161c 0%, #0c0d12 100%);`
  - target: tokenize #14161c/#0c0d12 (L3298 hero), #eef0f6 (L3397/3464 names), #d6dbe8 (L3405 ctrl), rgba(255,255,255,.04..10) ladder → §0 surface/text tokens
  - token: --surface-0..3 / --text-pri
  - note: Spec listed under G7 but it's tokenization (G1-ish); not a focus item. Kept on taste surface.

- **[2.2-P1-name-col-width] P1 · taste · risk=low** — Name column fixed 116px ellipsis → flexible
  - anchor: `color: #eef0f6; flex-shrink: 0; width: 116px; white-space: nowrap;`
  - target: flex:0 1 140px; min-width:96px (drop fixed 116px L3397 / mobile 92px L3509)
  - token: n/a (layout)
  - note: Long tags clipped (e.g. 'арена-рок').

- **[2.2-P2-green-meaning] P2 · taste · risk=low** — Green used for non-growth (−facet, ✓ учту) → split spans
  - anchor: `.taste-delta { font-family: 'Onest', sans-serif; font-size: 13px; font-weight: 600; color: var(--success, #34d399); }`
  - target: only «+» growth green; render «−арена-рок» + «✓ учту» in --text-sec/--accent-on-dark; split spans (L3333 colors whole string; JS L13183 sets ✓ учту green too)
  - token: --accent-on-dark / --text-sec
  - note: Green=growth only. Content L9482 '▲ +darkwave · −арена-рок'.

- **[2.2-P2-ctx-chip-glow] P2 · taste · risk=low** — ctx-chip active outer drop-glow → inset ring + fill only
  - anchor: `box-shadow: 0 0 0 1px rgba(81, 104, 252, 0.30), 0 6px 20px -8px var(--brand-blue-light);`
  - target: keep 1px inset ring + fill; drop outer colored 0 6px 20px -8px drop-glow (L3359)
  - token: --brand-blue-light
  - note: L3359 active ctx-chip.

- **[2.2-P2-streak-orb] P2 · taste · risk=low** — Streak pulsing orb → static / run-once
  - anchor: `animation: taste-streak-pulse 2.8s ease-in-out infinite;`
  - target: static growth glyph/ring OR run once on enter then settle (drop infinite pulse L3429/3431)
  - token: --ease-standard
  - note: reduced-motion disables (L3471) but default perpetual.

- **[2.2-P2-margins-8px] P2 · taste · risk=low** — Scattered margins → 8px grid
  - anchor: `margin-bottom: 28px; ⏎       } ⏎       .taste-wave`
  - target: snap to 8px; prefer .taste-stage>*+*{margin-top:24px}. Off-grid: hero 28(L3300), ctx-strip 28(L3336), foot 22(L3411), streak 4px 0 22px(L3423), group-title 14, mix 4/14/18/22/28
  - token: n/a
  - note: PARTIAL.

- **[2.2-P2-saved-tint-hsl] P2 · taste · risk=low** — (MERGED into G6-1) saved tint HSL gradient → flat
  - anchor: `var hue = 218 + h; return 'linear-gradient(135deg, hsl(' + hue + ',62%,30%), hsl(' + hue + ',70%,48%))';`
  - target: see G6-1 (same tint() at L14444)
  - token: --tint-blue-light-20
  - note: Listed for traceability — fully subsumed by G6-1; do NOT double-fix. (Kept as pointer, action happens in G6 wave.)

### Wave: discover

- **[2.3-glyph-svg] P1 · discover · risk=low** — «▶ Запустить как волну» ASCII glyph → inline play SVG
  - anchor: `id="discover-results-play" type="button">▶ Запустить как волну</button>`
  - target: inline play SVG + inline-flex;gap:8px (CSS already inline-flex L4260)
  - token: n/a (SVG)
  - note: L7801. Row buttons already SVG (L13436) — only this results-play CTA glyph remains.

- **[2.3-map-axis] P1 · discover · risk=med** — Map axis 10.5px --text-quat → 11px --text-sec, split anchored ends, +8px inset
  - anchor: `.discover-map-axis { position: absolute; font-family: 'Onest', sans-serif; font-size: 10.5px; font-weight: 600; letter-spacing: 0.03em; color: var(--text-quat);`
  - target: 11px, color var(--text-sec); split each axis top/bottom (left/right) anchored ends; +8px stage inset to clear rings
  - token: --text-sec
  - note: L4305. Combined strings L7792/7793 not split.

- **[2.3-section-title-scale] P1 · discover · risk=med** — Section titles 17/800 → shared .surface-section-title 19/700/-0.01em; reserve 800 for H2
  - anchor: `.discover-near-title { font-family: 'Onest', sans-serif; font-size: 17px; font-weight: 800; color: #fff; margin: 0 0 14px; }`
  - target: shared .surface-section-title 19px/700/-0.01em on .discover-near-title L4273/.discover-editorial-title L4282/.discover-map-title L4287; reserve 800 for .discover-title H2 L4236
  - token: type ramp
  - note: PARTIAL. Three dup weight-800 titles.

- **[2.3-8pt-spacing] P1 · discover · risk=med** — Normalize discover spacing to 8pt; .podborki-page flex column gap:32
  - anchor: `.discover-near { max-width: 1080px; margin: 26px auto 0; padding: 0 clamp(16px, 4vw, 28px); }`
  - target: .podborki-page flex column gap:32px; section margins on 8pt; title→content 16. Fix near 26(L4272)/editorial-title 30(L4282)/map-wrap 20(L4285)/ask 18(L4238)/title→content 14(L4273)
  - token: --s4/--s6
  - note: Ad-hoc off-grid margins.

- **[2.3-map-node-weights] P1 · discover · risk=med** — Map nodes 700/13→600/12; pill bg .85+blur(8px); dist=3 dots-only; connector globalAlpha .10
  - anchor: `.discover-map-node { position: absolute; transform: translate(-50%, -50%); display: inline-flex; align-items: center; gap: 6px; min-height: 44px; padding: 6px 12px 6px 8px; background: rgba(11, 12, 15, 0.72);`
  - target: 600/12px; bg rgba(11,12,15,.85)+backdrop-filter:blur(8px) (L4298); at dist=3 dots-only (labels on hover/focus); connector globalAlpha .10 (L13503)
  - token: one-off rgba
  - note: No blur, no dist=3 dots-only state (labels only hide via 560px media L4320).

- **[2.3-cta-hover] P1 · discover · risk=low** — Primary CTA hover bg+shadow (hover half; :active via G7)
  - anchor: `.discover-ask-go:hover { transform: translateY(-1px); }`
  - target: hover background:var(--brand-blue-hover)+shadow (L4249). --lift:-2px token + :active{scale(.98)} on CTA/chips/cards comes from G7-ACTIVE-SCALE.
  - token: --brand-blue-hover / --lift (G7)
  - note: --brand-blue-hover #6477ff exists L176 unused here. :active half subsumed by G7-ACTIVE-SCALE; this entry = hover-bg residual.

- **[2.3-radius-vocab] P1 · discover · risk=low** — Radius vocab → §0 (cards/stage --r-lg, track 12, pills 999)
  - anchor: `.discover-near-card { flex: none; width: 220px; text-align: left; padding: 16px; border-radius: 14px;`
  - target: cards/stage→--r-lg; pills→--r-pill. Hardcoded: near-card 14(L4276)/ed-card 14(L4311)/map-stage 16(L4295)/track 12(L4264). Reconcile --r-lg=14 vs stage 16 in §0 first.
  - token: --r-lg / --r-pill
  - note: PARTIAL. CONFLICT: --r-lg=14px but spec wants stage 16 — reconcile §0 before applying.

- **[2.3-tokenize-canvas] P1 · discover · risk=med** — Tokenize canvas colors via getComputedStyle (drop hardcoded #5168FC/#8094ff)
  - anchor: `mapCtx.strokeStyle='#5168FC'; mapCtx.globalAlpha=(r<=mapDist)?0.22:0.07;`
  - target: read --brand-blue-light/--accent-on-dark via getComputedStyle().getPropertyValue() once at draw time (L13497/13499/13503/13504)
  - token: --brand-blue-light / --accent-on-dark
  - note: drawMap() hardcodes canvas colors.

- **[2.3-ask-field-hover-focus] P1 · discover · risk=low** — ask-field :hover border + 3px focus ring; shorten placeholder to one example
  - anchor: `.discover-ask-field:focus-within { border-color: var(--brand-blue-light); }`
  - target: :hover{border-color rgba(255,255,255,.18)} + focus-within box-shadow 0 0 0 3px rgba(81,104,252,.25) (L4244); placeholder L7764 → one example
  - token: --brand-blue-light / new --focus-ring
  - note: Currently only focus-within border recolor.

- **[2.3-geometry-once] P2 · discover · risk=low** — Compute map geometry once: layout()→{cx,cy,R} shared by canvas+DOM
  - anchor: `var W=rect.width, H=rect.height, cx=W/2, cy=H/2, R=Math.min(W,H)/2 - 26;`
  - target: single layout() returning {cx,cy,R} consumed by drawMap() L13495 + renderNodes() L13511 (both '-26')
  - token: JS refactor
  - note: Geometry duplicated → drift risk (fidelity).

- **[2.3-fold-orientation] P2 · discover · risk=low** — Fold 3 orientation copies into one persistent explainer (keep «демо-карта»)
  - anchor: `<p class="discover-map-foot">Ты — в центре. Чем дальше узел, тем незнакомее. Известное затемнено.</p>`
  - target: single explainer; merge axis-label orientation (L7792-93) + foot (L7795) + dial-why (L7788); keep демо-карта tag L7781
  - token: --text-quat / --text-sec
  - note: PARTIAL. Three orientation copies coexist.

- **[2.3-empty-taste] P2 · discover · risk=low** — Empty-taste «Рядом»: dashed-border prompt OR «примерно» chip
  - anchor: `card.innerHTML = '<div class="discover-near-name">' + nb + '</div><div class="discover-near-dist">собери вкус в онбординге, чтобы точнее</div>';`
  - target: dashed-border onboarding prompt OR «примерно» chip distinguishing guessed vs personalized (L13472-13479)
  - token: --hairline (dashed)
  - note: Currently plain identical cards, no guessed signal.

- **[2.3-curator-color] P2 · discover · risk=low** — Curator byline --accent-on-dark → --text-sec (reserve blue for action)
  - anchor: `.discover-ed-curator { font-family: 'Onest', sans-serif; font-size: 11.5px; font-weight: 700; color: var(--accent-on-dark); margin-top: 10px; }`
  - target: color: var(--text-sec)
  - token: --text-sec
  - note: L4316 byline uses blue; should be neutral grey.

### Wave: track

- **[2.4-P1-hero-cover-size] P1 · track · risk=low** — Hero cover 480/280/600 → cap 360/280/440; radius 24→--r-lg
  - anchor: `.track-cover { ⏎         width: 480px; ⏎         height: 480px; ⏎         border-radius: 24px;`
  - target: desktop 360 (L5471-5472), TV 440 (L7062-7063 currently 600), mobile 280 (OK L7027); radius 24→var(--r-lg)
  - token: --r-lg (14px)
  - note: Base block L5470; 2nd block L5590 only restyles bg/shadow.

- **[2.4-P1-hero-cover-shimmer] P1 · track · risk=low** — Delete .track-cover::after radial shimmer
  - anchor: `/* Subtle radial shimmer on cover — not backdrop-filter (page rule) */ ⏎       .track-cover::after {`
  - target: delete entire ::after rule L5493-5499; depth from single shadow
  - token: n/a
  - note: rgba(81,104,252,.18) radial gloss. Borderline G6 (orb) but track-specific cover decoration — kept on track wave per 2.4 scope.

- **[2.4-P1-hero-cover-double-shadow] P1 · track · risk=low** — Hero cover double shadow → single neutral
  - anchor: `box-shadow: 0 40px 100px rgba(0,0,0,0.55), 0 0 64px -16px var(--track-tint);`
  - target: single 0 24px 60px -24px rgba(0,0,0,.6); drop 2nd tint-glow layer (effective shadow at 2nd block L5594 overrides base L5479)
  - token: n/a
  - note: Still two layers incl tint bloom.

- **[2.4-P1-section-headings] P1 · track · risk=low** — Unify section headings to one .track-why-title (19/600/-0.01em)
  - anchor: `.track-neighbors-heading { font-family: 'Onest', sans-serif; font-weight: 800; font-size: 18px; color: #fff; margin: 0; letter-spacing: -0.01em; }`
  - target: one style 19px/600/-0.01em + 14px bottom margin across .track-why-title (L5599 20/800), .track-vector-title (L5613 20/800), .track-neighbors-heading (L5624 18/800)
  - token: n/a
  - note: PARTIAL. Three near-dup headings, weight 800 exceeds 700/600 cap.

- **[2.4-P1-eyebrow-aria] P1 · track · risk=low** — Eyebrow: remove aria-hidden (a11y) + weight 700→600 + tracking .12→.08em
  - anchor: `<p class="track-eyebrow" aria-hidden="true">Сейчас играет · ГОРОД ПОП · 105.2 FM</p>`
  - target: remove aria-hidden on markup L8542 (carries real now-playing info); CSS L5459-5468 weight 700→600, letter-spacing .12em→.08em. Color cyan→accent-on-dark handled by G2-34.
  - token: --accent-on-dark (color via G2-34)
  - note: Color swap is G2-34 (subsumed). RESIDUAL here = the aria-hidden a11y bug + weight/tracking (NOT a cyan/token swap).

- **[2.4-P1-lyrics-contrast] P1 · track · risk=low** — Lyrics inactive #545454 (3.3:1) → rgba(235,235,245,.32)/600; active 700
  - anchor: `.track-lyric-line { ⏎         font-family: 'Onest', sans-serif; ⏎         font-size: 36px; ⏎         font-weight: 700; ⏎         color: #545454;`
  - target: inactive #545454→rgba(235,235,245,.32), weight 700→600 (L5773); active stays #fff bump to 700 (L5781-5783)
  - token: n/a
  - note: Low contrast inactive line.

- **[2.4-P1-action-row-gaps] P1 · track · risk=low** — action-row gap 44/24/60 → 32/20/44
  - anchor: `.track-action-row { ⏎         display: flex; ⏎         align-items: flex-start; ⏎         justify-content: center; ⏎         gap: 44px;`
  - target: desktop 44→32 (L5539), mobile 24→20 (L6997 & L7037), TV 60→44 (L7072)
  - token: n/a
  - note: Three declarations across base+responsive+surface.

- **[2.4-P1-tab-labels] P1 · track · risk=med** — Action-tab labels 15/400→12/500; internal gap 10→6 (SHARED selector)
  - anchor: `.player-action-tab span { ⏎         font-size: 15px; ⏎         font-weight: 400;`
  - target: .player-action-tab span L1238 fs 15→12 weight 400→500; .player-action-tab gap L1207 10→6
  - token: n/a
  - note: HIGH-RISK: .player-action-tab (L1203) SHARED with full-player overlay tabs — change touches both surfaces. Scope via .track-action-row modifier OR verify overlay still reads OK.

- **[2.4-P2-dead-trackcover-gradient] P2 · track · risk=low** — Delete superseded base .track-cover gradient/shadow/svg
  - anchor: `background: linear-gradient(135deg, #1a4fa0 0%, #7b2d8b 60%, #c43a6e 100%);`
  - target: delete dead gradient (L5478)/first box-shadow (L5479)/svg (L5484) in base .track-cover — overridden by 2nd block L5590+ (bg !important)
  - token: n/a
  - note: Pure dead-code (2nd block wins). Adjacent to G6 slop but track-local; kept on track wave.

- **[2.4-P2-dead-upnext-also] P2 · track · risk=low** — Delete unused .track-up-next-* / .track-also-* CSS + dead JS loops
  - anchor: `.track-up-next-card { ⏎         display: flex; ⏎         flex-direction: column; ⏎         align-items: center; ⏎         gap: 8px; ⏎         width: 140px;`
  - target: delete .track-up-next-* (L5639-5744), .track-also-* (L5907-6006), responsive refs L7018-7022 & L7057-7058; dead JS L10995/11008 (querySelector finds 0)
  - token: n/a
  - note: NOTE: this removes the blocks that G2-35/36/37/38 cyan-rings live in. ORDER: if doing both, do G2 cyan-swap OR just delete here — deleting makes those G2 items moot. Cover view renders why/vector/neighbors instead.

- **[2.4-P2-history-fake-durations] P2 · track · risk=low** — History fake identical 06:45 → varied durations + «демо-история» tag
  - anchor: `<div class="track-history-duration">06:45</div>`
  - target: vary 8 identical 06:45 (L8786..8885) to plausible 03:xx-04:xx; add <span class="demo-tag">демо-история</span> in history view header
  - token: n/a
  - note: Adds a kept-by-design демо tag (consistent with demo-vector). Last two rows already plausible.

### Wave: artist

- **[2.5-P1-trackcovers-tintfor] P1 · artist · risk=low** — Track-row covers: remove inline tintFor() in JS (::after handled by G6-3)
  - anchor: `'<span class="artist-track-cover" aria-hidden="true" style="background:'+tintFor(tr.t)+'">`
  - target: drop inline style=background:tintFor(tr.t) at JS L14626; set .artist-track-cover bg flat rgba(255,255,255,.06). The radial ::after (L4984) deletion is G6-3. Keep hero tintFor (L14643).
  - token: rgba(255,255,255,.06) / --surf-glass-06
  - note: 2.5-P1-trackcovers SPLIT: ::after orb → G6-3 (subsumed); inline JS tintFor removal is the RESIDUAL (edits render fn, not CSS). Hero tint stays.

- **[2.5-P1-material] P1 · artist · risk=low** — Add material: card OR top-hairline divider per .artist-section (pick one)
  - anchor: `.artist-section { padding:0 40px 40px; max-width:920px; margin:0 auto; }`
  - target: either card (rgba(255,255,255,.03)+1px var(--hairline)+--r-xl+padding 24 28) OR single top-hairline divider (border-top:1px solid var(--hairline)) between sibling sections — uniform across .artist-why+Топ треков+Станции
  - token: --hairline / --r-xl
  - note: L4902 bare padding — sections float structureless. (Listed subsumed_by G6 in source but it's material/layout not slop — kept on artist wave.)

- **[2.5-P1-onecolumn] P1 · artist · risk=low** — Align hero + sections to one column (same max-width + gutter)
  - anchor: `min-height: 320px; padding: 48px 40px;`
  - target: give .artist-hero inner content max-width:920px;margin:0 auto (or wrap inner 920 container) so name/CTAs left-align with section headings. Hero L4835-4841 has no max-width; sections L4902 capped 920 centered
  - token: 920px max-width + 40px gutter literals
  - note: Left edges mismatch (hero full-width vs 920 sections).

- **[2.5-P1-tokenize-rgba] P1 · artist · risk=med** — Tokenize raw rgba / introduce --brand-ghost-bg/--brand-ghost-border
  - anchor: `border:1px solid rgba(255,255,255,0.12); transition:background var(--t-fast)`
  - target: raw whites .06→--hairline-ish/.12→--border subtle/.14/.30→--border-strong/hover; brand alphas rgba(81,104,252,.10/.12/.30/.45)→NEW --brand-ghost-bg/--brand-ghost-border; rgba(0,0,0,.12) hero bg→token. L4915-4961, L4994-4997
  - token: --hairline / --border-strong / new --brand-ghost-bg/border
  - note: Do TOGETHER with 2.5-P2-unify-reject (both need the new --brand-ghost-* tokens). No such token exists yet.

- **[2.5-P1-rhythm-8pt] P1 · artist · risk=low** — Snap rhythm to 8pt (track-row gap 14→16, why-foot 18→24)
  - anchor: `display:flex; align-items:center; gap:14px; padding:10px 12px; min-height:56px;`
  - target: track-row gap 14→16 (L4968); .artist-why-foot margin-top 18→24 (L4954); optional hero-text gap 14→16 (L4864)
  - token: 8pt scale
  - note: Off-grid 14/18.

- **[2.5-P1-cta-active-shadow] P1 · artist · risk=low** — Primary CTA resting blue shadow + rows :active bg (scale via G7)
  - anchor: `.artist-action-primary:hover { filter:brightness(1.12); }`
  - target: add .artist-action-primary{box-shadow:0 8px 24px -8px rgba(81,104,252,.5)} resting; .artist-track-row:active/.artist-station-chip:active bg (--surf-glass-20). The :active{scale(.97)} is from G7-ACTIVE-SCALE (normalize .97→.98).
  - token: rgba(81,104,252,.5) shadow / --surf-glass-20
  - note: :active scale subsumed by G7-ACTIVE-SCALE; RESIDUAL = resting shadow + row active-bg. Add transform to transition for the G7 scale to animate.

- **[2.5-P1-meta-quat-to-sec] P1 · artist · risk=low** — Dense metadata --text-quat → --text-sec (AA)
  - anchor: `.artist-track-album { font-family:'Onest',sans-serif; font-size:13px; color:var(--text-quat);`
  - target: --text-quat→--text-sec on .artist-track-album (L4988)/.artist-track-dur (L4989)/.artist-station-freq (L5004)/.artist-why-prov (L4942); optional hover bump to --text-pri
  - token: --text-sec
  - note: Rank keeps quat (see rank item).

- **[2.5-P2-stations-grid] P2 · artist · risk=low** — Stations flex+fixed 260px → CSS grid auto-fill minmax(240px,1fr)
  - anchor: `.artist-stations { display:flex; flex-wrap:wrap; gap:12px; }`
  - target: display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px; remove width:260px from .artist-station-chip L4995; drop mobile width:100% L6899/6907 if grid handles
  - token: n/a (layout)
  - note: Ragged last row currently.

- **[2.5-P2-demo-badge-quiet] P2 · artist · risk=low** — «демо-вектор» loud blue pill → quiet 11px neutral caption
  - anchor: `.artist-why-demo {`
  - target: demote: 11px, --text-ter/--text-quat neutral, drop blue bg rgba(81,104,252,.12)+border+--r-pill+uppercase+cursor:default (L4912-4917); reposition as small caption under H2 (markup L8447). KEEP the word «демо-вектор».
  - token: --text-ter
  - note: KEEP-by-design label, only quiet styling.

- **[2.5-P2-unify-reject] P2 · artist · risk=med** — Unify two reject controls into one ghost-button, min-height 44
  - anchor: `.artist-why-reject {`
  - target: make .artist-why-reject (L4945, 32px) + .artist-why-not (L4955, 44px) share ONE ghost-button component (same padding/border/radius/min-height:44/pressed)
  - token: --brand-ghost-bg/border (shared) / min-height:44
  - note: Do with 2.5-P1-tokenize-rgba (shared new tokens). sub-44 tap on .artist-why-reject.

- **[2.5-P2-track-rank] P2 · artist · risk=low** — Track rank 24/900 → 15/600, width 24 centered
  - anchor: `font-size:24px; font-weight:900; color:var(--text-quat);`
  - target: .artist-track-rank → 15px/600/min-width:24px/text-align:center (was 24/900/min-width:30/right, L4974-4977). Color --text-quat stays (intended here).
  - token: --text-quat (kept)
  - note: PARTIAL. Heavy number competes with title.

### Wave: onboarding

- **[2.6-P0-selected-shadow] P0 · onboarding · risk=low** — Selected-bubble 4-layer neon shadow → clean ring; drop ONE bg layer (radial OR particles)
  - anchor: `0 0 28px rgba(81,104,252,0.6),`
  - target: .onb-bubble.is-selected (L2363-2369) → box-shadow: 0 0 0 2px var(--home-bg-base), 0 0 0 4px var(--brand-blue-light), 0 8px 24px rgba(0,0,0,.45) (drop the 0 0 28px neon glow). Also drop ONE of .onb-stage::after radial (L2238-2248) OR .onb-bg-particles (L2228-2236).
  - token: --brand-blue-light / --home-bg-base
  - note: CONFLICT with G6-6 (which deletes .onb-bg-particles). COORDINATE: if G6-6 removes onb-bg-particles, this item keeps the onb radial::after (don't drop both). Resolve in onboarding wave after G6 ran.

- **[2.6-P0-bubbles-deadcode] P0 · onboarding · risk=low** — Delete dead --hue setter + GENRE_HUE map + hashHue() (genre bubbles already flat)
  - anchor: `else { el.style.setProperty('--hue', d.hue != null ? d.hue : (GENRE_HUE[genre] != null ? GENRE_HUE[genre] : hashHue(d.t))); }`
  - target: visual P0 DONE (flat material L2345). Delete dead --hue setter L12067, GENRE_HUE map L11948-11952, hashHue() L11999-12003
  - token: n/a (dead-code removal)
  - note: PARTIAL — only slop-cleanup remains (adjacent to G6 but onboarding-local JS).

- **[2.6-P1-count-vecbar-accent] P1 · onboarding · risk=low** — Count number → --accent-on-dark; .onb-vec-fill gradient → solid blue-light
  - anchor: `.onb-vec-fill { height: 100%; border-radius: 4px; background: linear-gradient(90deg, var(--brand-blue-light), var(--accent-on-dark));`
  - target: (a) .onb-count #onb-count-n L2402 color --brand-blue-light→--accent-on-dark; (b) .onb-vec-fill L2654 gradient→solid background:var(--brand-blue-light). vec-pct already correct.
  - token: --accent-on-dark / --brand-blue-light
  - note: PARTIAL. vec-fill 2-stop gradient is slop (G6-adjacent) but onboarding-local; the count-color is a token fix.

- **[2.6-P1-header-scaffold] P1 · onboarding · risk=low** — Same header scaffold on 3 steps; add spark to #onb-import-pick + main
  - anchor: `<div class="onb-model-step" id="onb-import-pick" hidden> ⏎             <h2 class="onb-model-title">Откуда взять вкус?</h2>`
  - target: add <span class="onb-model-spark"> star badge before <h2> in #onb-import-pick (and main step); parse has spark--spin, main has kicker but no spark — unify static spark + optional kicker + h2
  - token: --tint-blue-light-20 / --brand-blue-light
  - note: Three inconsistent headers.

- **[2.6-P1-vec-glyphs-svg] P1 · onboarding · risk=low** — – + ✕ JS-injected text glyphs → 16px stroked SVGs
  - anchor: `'<button class="onb-vec-btn" type="button" data-act="down" aria-label="Меньше: '+esc(r.name)+'">–</button>'+`
  - target: replace –/+/✕ at L12477-12479 with 16px stroked SVGs (reuse #resume-close X path L9349); drop .onb-vec-btn--x font-size:15px L2666
  - token: currentColor stroke 16
  - note: JS render template edit (not markup). Glyph-imagery slop → G6-adjacent but onboarding-local.

- **[2.6-P1-onb-src-radius] P1 · onboarding · risk=low** — .onb-src radius 10 (--r-base) → 13 to match vec rows
  - anchor: `border: 1px solid rgba(255, 255, 255, 0.10); border-radius: var(--r-base);`
  - target: .onb-src L2704 → 13px to match .onb-vec-row (13px hardcoded L2648). Either add --r-card:13px applied to both, or set onb-src 13px directly
  - token: --r-card:13px (NEW, undefined) or --r-lg(14) closest
  - note: PARTIAL. CONFLICT: spec references --r-card twice but it does NOT exist in file — decide add-token vs use-existing in §0.

- **[2.6-P1-onb-title-weight] P1 · onboarding · risk=low** — .onb-title 900 → 800
  - anchor: `.onb-title { ⏎         font-family: 'Onest', sans-serif; ⏎         font-weight: 900;`
  - target: .onb-title L2274-2283 weight 900→800; keep clamp(28px,4vw,46px) + -0.01em
  - token: font-weight 800
  - note: h2 model-title already 800 (L2633).

- **[2.6-P2-one-register] P2 · onboarding · risk=low** — One register «вы» end-to-end (rewrite model/import «ты» copy)
  - anchor: `Демо: реальная история не загружается — соберём правдоподобный пример из выбранного сервиса. Ты увидишь и поправишь каждый пункт.`
  - target: «ты»→«вы» across import-pick sub L9417, onb-src-hint L9421, model kicker L9437, model title L9438, model prov L9439, import link L9337. Header/resume-modal already «вы».
  - token: n/a (copy)
  - note: Biggest copy inconsistency: header «вы» vs model/import flow «ты».

- **[2.6-P2-one-sheet] P2 · onboarding · risk=med** — Two stacked «или…» underlined links → ONE quiet «Другой способ собрать вкус» sheet
  - anchor: `или импортируй вкус из Last.fm · Яндекс · ВК`
  - target: footer L9333-9338 has TWO links (.onb-alt + .onb-alt--import). Collapse to ONE neutral «Другой способ собрать вкус» opening a small sheet (résumé + import). Remove text-decoration:underline (.onb-alt L2436) + accent on .onb-alt--import L2724 so CTA wins
  - token: --text-sec
  - note: Three competing actions under CTA.

- **[2.6-P2-vec-name-width] P2 · onboarding · risk=low** — .onb-vec-name fixed 116px → flex:1 1 auto, ellipsis, min-width:88
  - anchor: `.onb-vec-name { font-family: 'Onest', sans-serif; font-size: 15px; font-weight: 700; color: #fff; flex: none; min-width: 116px; }`
  - target: L2652 → flex:1 1 auto; min-width:88px; overflow:hidden;text-overflow:ellipsis;white-space:nowrap (drop flex:none/min-width:116px). Reconcile mobile L2731 (min-width:0;flex:1 1 100%)
  - token: n/a (layout)
  - note: Long names clip the bar.

- **[2.6-P2-ai-sparkle-calmer] P2 · onboarding · risk=low** — Optional: calmer brand mark for AI-sparkle; badge radius → --r-lg
  - anchor: `.onb-model-spark { ⏎         display: inline-flex; align-items: center; justify-content: center; ⏎         width: 42px; height: 42px; border-radius: 12px;`
  - target: .onb-model-spark L2637-2642 radius 12px→--r-lg(14)/--r-card; optionally swap 4-point star (M12 2l1.9 5.8…, L9355/9382/9391/9429, also .resume-spark) for calmer mark
  - token: --r-lg(14)
  - note: Lowest priority/optional. Off-scale radius.

### Wave: recap_profile

- **[2.7-P0-tokenize] P0 · recap_profile · risk=low** — Tokenize surfaces/radii/borders (raw #111318, raw radii, raw alphas)
  - anchor: `.profile-box { border-radius: 18px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.1); background: #111318; }`
  - target: bg→var(--surface-0); border→1px var(--hairline); radius 18→var(--r-xl)(20); recap-card 20px→--r-xl; profile-ad-strip 14→--r-lg. Raw #111318 at 3145/3178/3186; 5 raw radii + .06/.08/.10/.12/.16 alphas
  - token: --surface-0 / --hairline / --r-xl / --r-lg
  - note: --surface-0=#111318 so swap is 1:1, no visual change. (subsumed_by G1 per source, but no G1 wave exists — execute on this surface.)

- **[2.7-P0-glyphs] P0 · recap_profile · risk=med** — Glyph icons (✓ ▲ − → ←) → stroked SVG or strip
  - anchor: `var s = '<span class="grow">▲ +' + esc(d.plus.n) + '</span>';`
  - target: 14-16px stroked SVG up/down arrows + check, or strip; arrow-CTAs →/← icon-ize consistently. ▲/− in cardDeltaHTML 3931/3932, deltaText 3937/3938, renderDeltaList 14159/14164; ✓ 14043/14134; →/← 9584/9585/9620/9632/9655/13805/14205/14206
  - token: currentColor stroke SVG
  - note: The ▲ on the share-card PNG is the user-visible screenshot artifact — highest value here.

- **[2.7-P1-button-unify] P1 · recap_profile · risk=med** — Unify ONE button component + single --brand-blue-hover (drop raw #6d80ff); recap row = ONE primary
  - anchor: `.profile-cta--primary:hover { background: #6d80ff; }`
  - target: primary hover→var(--brand-blue-hover) (#6477ff); collapse .profile-cta/.recap-btn/.recap-btn--primary-alt → --primary/--secondary/--ghost; recap row = ONE primary (Сохранить), Скопировать→secondary neutral
  - token: --brand-blue-hover (#6477ff)
  - note: Raw #6d80ff L3138 COLLIDES with canon --brand-blue-hover #6477ff. recap-actions has two accent buttons side by side (3229-3236).

- **[2.7-P1-facet-affordance] P1 · recap_profile · risk=low** — .profile-facet row affordance: --r-md + hover/focus-within bg; lower-btn 28px
  - anchor: `.profile-facet { display: grid; grid-template-columns: 1fr auto; gap: 2px 12px; align-items: center; padding: 11px 0; border-top: 1px solid rgba(255, 255, 255, 0.06); }`
  - target: add border-radius:var(--r-md); padding 11px 12px; :hover,:focus-within{background:rgba(255,255,255,.04)}; .profile-facet-lower min 28px tall (currently ~26)
  - token: --r-md / --surf-hover
  - note: PARTIAL. Row has no hover/radius; button sub-28px. (focus-visible color → G7.)

- **[2.7-P1-type-ramp] P1 · recap_profile · risk=med** — Lock 6-step type ramp; headings 800→650-700; -0.01em on ≥22px
  - anchor: `.profile-section-h { font-family: 'Onest', sans-serif; font-size: 18px; font-weight: 800; color: #fff; margin: 26px 0 4px; }`
  - target: section-h/recap-h2/recap-title/profile-title weight 800→650-700; snap off-ramp 14.5/13.5/12.5/11.5/10.5 → 15/13/11; -0.01em on ≥22px
  - token: type-ramp scale
  - note: PARTIAL. All headings 800 (3176/3133/3205/3207); off-ramp sizes 3164/3177/3187/3237/3158/3183/3148.

- **[2.7-P1-columns-spacing] P1 · recap_profile · risk=low** — profile-stage width 1000→860 + bottom pad 64→96-120 (clear mini player)
  - anchor: `.profile-stage { max-width: 1000px; margin: 0 auto; padding: clamp(20px, 4vw, 44px) clamp(16px, 4vw, 40px) 64px; }`
  - target: max-width 1000→860; bottom padding 64→96-120 (clear .player-mini 72px); align gaps to 8pt. recap-stage (3199) already 680/120 — copy values
  - token: 8pt grid
  - note: Profile content sits behind 72px mini player.

- **[2.7-P1-reserve-space] P1 · recap_profile · risk=low** — Reserve intrinsic space for JS-injected blocks (no CLS)
  - anchor: `.recap-screen-bloom { margin: 0 auto; }`
  - target: .recap-screen-bloom{min-height:clamp(220px,60vw,300px)} (3242); #profile-facets (9606)/#recap-deltas (9665)/#profile-rejected (9615) reserve min-height; recap-card-word 2-line min-height
  - token: min-height clamp
  - note: Empty markup filled by JS → layout jump on first paint.

- **[2.7-P2-recap-card-toplight] P2 · recap_profile · risk=low** — recap-card add inset top-light + hairline .10
  - anchor: `.recap-card { position: relative; width: min(360px, 86vw); aspect-ratio: 1080 / 1920; margin: 0 auto; background: var(--bg-base); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px; overflow: hidden; box-shadow: 0 24px 60px -24px rgba(0, 0, 0, 0.7); }`
  - target: border .08→.10 (--hairline); box-shadow prepend inset 0 1px 0 rgba(255,255,255,.06) top-light
  - token: --hairline / inset top-light
  - note: Matches polish profile-box--open got (3159).

- **[2.7-P2-sharecard-green] P2 · recap_profile · risk=low** — Share-card: demote green delta to neutral name + small green «+»
  - anchor: `.recap-card-delta--hero .grow { color: var(--success, #34d399); }`
  - target: card delta name→--text-pri neutral; reserve green for ONLY a small '+' glyph (card=blue+neutrals). .grow at 3217/3220; screen-level .recap-delta-row.grow 3250 same
  - token: --text-pri / --success (+ only)
  - note: Green=growth only; full-word green over-uses it on the screenshotted card.

- **[2.7-P2-faux-bars] P2 · recap_profile · risk=low** — Faux competitor: 3 varied-width bars + diagonal lock hatch (reads 'redacted')
  - anchor: `.profile-faux-row { display: flex; align-items: center; gap: 10px; margin-bottom: 14px; }`
  - target: 3 rows (not 4, markup 9593-9596) varied widths (60/85/45%) + repeating-linear-gradient diagonal hatch so it reads 'redacted' not skeleton-loading
  - token: --text-ter hatch
  - note: Currently 4 identical full-width blurred rows = looks like loader.

- **[2.7-P2-kicker-dot-glow] P2 · recap_profile · risk=low** — Remove profile kicker-dot glow; one shared flat .gf-kicker-dot
  - anchor: `.profile-kicker-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--brand-blue-light); box-shadow: 0 0 10px var(--brand-blue-light); }`
  - target: drop box-shadow (L3132); unify to one flat .gf-kicker-dot shared with other kicker dots
  - token: --brand-blue-light (flat)
  - note: Same neon treatment P0 retired on profile-box. (subsumed_by G7 in source, but it's a glow not a focus ring — execute here.)

### Wave: chrome

- **[2.8-P1a] P1 · chrome · risk=low** — Drop filter:brightness() topbar search/account hovers → bg transition
  - anchor: `filter: brightness(1.15);`
  - target: .topbar-search:hover (L368) & .topbar-account:hover (L401) → bg transition to --surf-hover/--surf-active; drop filter. FAB brightness L1563 is dev-gated → leave
  - token: --surf-hover / --surf-active
  - note: Easy live fix.

- **[2.8-P1c] P1 · chrome · risk=med** — Unify IA labels: tabbar Главная/Подборки/Избранное → canon Волна/Открыть/Мой вкус + match icons
  - anchor: `data-route="#/podborki" ⏎       aria-label="Подборки"`
  - target: tabbar L10463-10514 labels → Волна/Открыть/Мой вкус(+Плеер); match sidebar icon per route (sidebar canon L7244-7268); resolve #/taste labeled «Избранное» dup
  - token: n/a
  - note: Same route must share word+icon. Sidebar already canon; tabbar diverges (house vs waveform, grid vs compass, heart vs target).

- **[2.8-P1b] P1 · chrome · risk=med** — Sidebar row geometry: vertical icon-over-text → horizontal flex rows
  - anchor: `flex-direction: column; ⏎         align-items: center; ⏎         justify-content: center; ⏎         gap: 10px; ⏎         padding: 12px 8px;`
  - target: .sidebar-item flex-direction:row;gap:12px;min-height:44px;padding:10px 12px; icons 34→22px/1.75 stroke; .sidebar-nav gap 28→4px (L449). Update web/tv surface overrides L6017/6173
  - token: --r-base
  - note: HIGH-RISK: full row redesign touching web+tv surface overrides. 80px rows currently. Separate from G7 (sidebar already ≥44px tall, not a hit-target failure).

- **[2.8-P1d] P1 · chrome · risk=low** — Wordmark must NOT recolor on hover → opacity .85 (resolve G2-03/04)
  - anchor: `.sidebar-logo:hover { ⏎         color: var(--brand-cyan);`
  - target: .sidebar-logo:hover (L442) → remove color shift, use opacity:.85 (G2-04 minimal-repointed it to --accent-on-dark; FINAL §2.6/§2.8 fix is no-recolor). .logo (L324-340) is DEAD CODE — delete whole block (covers G2-03).
  - token: n/a (opacity)
  - note: CONFLICT-resolution: G2-03/04 do minimal repoint; THIS chrome item is the canonical fix (no recolor). Do this AFTER G2 — supersedes the repoint. Deleting dead .logo block also removes G2-03's target.

- **[2.8-P2c] P2 · chrome · risk=low** — Dev-gate «Карта флоу» footer link (prod-hidden via G4)
  - anchor: `class="sidebar-item sidebar-item-internal"`
  - target: add «Карта флоу» link (L7273-7285, data-route=#/map) to html:not([data-dev="true"]) gate at L1399-1401 alongside theme-toggle (currently only hides via TWEAKS data-hide-flow-map)
  - token: n/a
  - note: Visible in prod today; fold into G4 prod gate.

- **[2.8-P2a] P2 · chrome · risk=med** — Tabbar split hover vs active + 3px top indicator + player route + label 10→11px
  - anchor: `.tabbar-item:hover, ⏎       .tabbar-item[aria-current="page"] { ⏎         color: var(--brand-blue-light);`
  - target: hover→--text-sec; active→--brand-blue-light/600 + 3px top ::after indicator (L1380-1383); add data-route to #tabbar-player-btn (L10503-10514) so exactly one active; .tabbar-item font-size 10→11 (L1370)
  - token: --text-sec / --brand-blue-light
  - note: Player tab has no data-route → never aria-current (loop L10783 matches [data-route] only).

- **[2.8-P2b] P2 · chrome · risk=low** — Topbar scrim scroll-tied (not static) + optional left contextual title
  - anchor: `background: linear-gradient( ⏎           180deg, ⏎           rgba(12, 11, 11, 0.72) 0%, ⏎           rgba(12, 11, 11, 0.0) 100% ⏎         );`
  - target: scrim (L314-318) → scroll-tied single fade-in on scroll; OR keep floating right cluster (already met) + optional left contextual page title
  - token: n/a
  - note: PARTIAL. Right-cluster branch satisfied; scrim is static constant.

- **[2.8-P2d] P2 · chrome(dev) · risk=low** — Theme toggle raw «Cinema / Warm» copy + dead warm target
  - anchor: `<span>Cinema / Warm</span>`
  - target: span L7308 → «Тема: Кино» (not raw EN); note warm theme retired G3 so applyTheme('warm') L11165 is dead state; map-chip «Cinema + Warm» L7334 stale
  - token: n/a
  - note: Dev-gated (only ?dev=1) → low. .bg-warm never rises (L292).