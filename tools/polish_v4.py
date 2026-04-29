"""Production polish pass v4: spacing rhythm + Apple HIG fix + cards + footer."""
from pathlib import Path

p = Path(r'C:\Users\elbics\Desktop\design-project\designs\showcase-aggregator.html')
s = p.read_text(encoding='utf-8')

REPLACEMENTS = [

# ── 1. Sidebar mini-player UX: hide big play, show only on hover ─────
('''.sb-mini-play {
  position: absolute;
  inset: 0;
  display: grid; place-items: center;
  z-index: 2;
}
.sb-mini-play-btn {
  width: 56px; height: 56px;
  border-radius: 50%;
  background: var(--accent);
  color: white;
  display: grid; place-items: center;
  box-shadow: 0 8px 20px rgba(255,31,75,0.5);
  transition: transform var(--t-fast);
}
.sb-mini-player:hover .sb-mini-play-btn { transform: scale(1.08); }
.sb-mini-play-btn svg { width: 22px; height: 22px; fill: currentColor; margin-left: 3px; }''',

'''.sb-mini-play {
  position: absolute;
  inset: 0;
  display: grid; place-items: center;
  z-index: 2;
  opacity: 0;
  background: rgba(0,0,0,0.32);
  transition: opacity var(--t-fast);
}
.sb-mini-player:hover .sb-mini-play { opacity: 1; }
.sb-mini-play-btn {
  width: 52px; height: 52px;
  border-radius: 50%;
  background: var(--accent);
  color: white;
  display: grid; place-items: center;
  box-shadow: 0 8px 20px rgba(0,0,0,0.5);
  transition: transform var(--t-fast);
}
.sb-mini-player:hover .sb-mini-play-btn { transform: scale(1.08); }
.sb-mini-play-btn svg { width: 20px; height: 20px; fill: currentColor; margin-left: 3px; }'''),

# ── 2. Apple sidebar active: subtle white tint вместо красного pill ──
('''.sb-item[aria-current="page"] {
  background: var(--accent);
  color: white;
  font-weight: 600;
}''',

'''.sb-item[aria-current="page"] {
  background: var(--accent);
  color: white;
  font-weight: 600;
}
[data-style="apple"] .sb-item[aria-current="page"] {
  background: rgba(255,255,255,0.10);
  color: var(--text-primary);
  position: relative;
}
[data-style="apple"] .sb-item[aria-current="page"]::before {
  content: "";
  position: absolute;
  left: -8px; top: 50%; transform: translateY(-50%);
  width: 3px; height: 22px;
  background: var(--accent);
  border-radius: 2px;
}'''),

# ── 3. Vertical rhythm ─────────────────────────────────────────
('.row-section { margin-bottom: 38px; }',
 '.row-section { margin-bottom: 56px; }\n.row-section:last-of-type { margin-bottom: 32px; }'),

('padding: 0 var(--content-pad) 60px;',
 'padding: 0 var(--content-pad) 96px;'),

# ── 4. Hero overlay: padding/gap/z-index ───────────────────────
('''.hero-card-overlay {
  position: absolute; inset: 0;
  display: flex; flex-direction: column; justify-content: flex-end;
  padding: 36px 44px;
  gap: 14px;
}''',

'''.hero-card-overlay {
  position: absolute; inset: 0;
  display: flex; flex-direction: column; justify-content: flex-end;
  padding: 44px 52px;
  gap: 18px;
  z-index: 2;
}
@media (max-width: 1100px) { .hero-card-overlay { padding: 32px 28px; gap: 14px; } }'''),

# Hero meta gap
('''.hero-card-meta {
  display: flex; align-items: center; gap: 10px;
  font-size: 13px;
  color: rgba(255,255,255,0.85);
}''',
'''.hero-card-meta {
  display: flex; align-items: center; gap: 14px; flex-wrap: wrap;
  font-size: 13px;
  color: rgba(255,255,255,0.85);
}'''),

# Hero title
('''.hero-card-title {
  font-size: clamp(28px, 3.5vw, 48px);
  font-weight: 800;
  letter-spacing: -0.02em;
  color: white;
  max-width: 720px;
  line-height: 1.05;
}''',
'''.hero-card-title {
  font-size: clamp(28px, 3.5vw, 52px);
  font-weight: 800;
  letter-spacing: -0.022em;
  color: white;
  max-width: 720px;
  line-height: 1.04;
  text-shadow: 0 2px 18px rgba(0,0,0,0.45);
}'''),

# Hero card overlay gradient stronger
('''.hero-card-bg::after {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(135deg, transparent 0%, rgba(0,0,0,0.0) 40%, rgba(0,0,0,0.6) 100%);
}''',
'''.hero-card-bg::after {
  content: "";
  position: absolute; inset: 0;
  background:
    linear-gradient(180deg, transparent 30%, rgba(0,0,0,0.78) 100%),
    linear-gradient(90deg, rgba(0,0,0,0.45) 0%, transparent 55%);
}'''),

# Hero card pseudo-overlay для дынами image bg
('''.hero-card {
  flex: 0 0 88%;
  scroll-snap-align: start;
  position: relative;
  border-radius: var(--r-xl);
  overflow: hidden;
  aspect-ratio: 21 / 8;
  min-height: 320px;
  max-height: 520px;
  background: var(--hero-grad, linear-gradient(135deg,#FF1F4B 0%,#FF8A3D 60%,#FFD83D 100%));
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-lg);
  transition: transform var(--t-mid);
}
.hero-card:hover { transform: scale(1.005); }''',

'''.hero-card {
  flex: 0 0 88%;
  scroll-snap-align: start;
  position: relative;
  border-radius: var(--r-xl);
  overflow: hidden;
  aspect-ratio: 21 / 8;
  min-height: 340px;
  max-height: 540px;
  background-color: #1a1a1a;
  background-size: cover;
  background-position: center;
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-lg);
  transition: transform var(--t-mid);
}
.hero-card::before {
  content: "";
  position: absolute; inset: 0;
  background:
    linear-gradient(180deg, transparent 30%, rgba(0,0,0,0.82) 100%),
    linear-gradient(90deg, rgba(0,0,0,0.55) 0%, transparent 60%);
  z-index: 1;
}
.hero-card:hover { transform: scale(1.005); }'''),

# ── 5. Apple cards: solid bg ────────────────────────────────────
('''[data-style="apple"] .card-tv {
  background: var(--glass-bg-weak);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}''',

'''[data-style="apple"] .card-tv {
  background: rgba(28,28,30,0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}'''),

('''[data-style="apple"] .card-news {
  background: rgba(28,28,30,0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}''',

'''[data-style="apple"] .card-news {
  background: rgba(28,28,30,0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}'''),

# ── 6. Chart row spacing + dividers ────────────────────────────
('''.chart-row {
  display: grid;
  grid-template-columns: 56px 56px 1fr auto;
  gap: 16px;
  align-items: center;
  padding: 10px 14px;
  border-radius: var(--r-md);
  cursor: pointer;
  transition: background var(--t-fast);
}
.chart-row:hover { background: var(--glass-bg-weak); }''',

'''.chart-row {
  display: grid;
  grid-template-columns: 56px 56px 1fr auto;
  gap: 16px;
  align-items: center;
  padding: 14px 14px;
  border-radius: var(--r-md);
  cursor: pointer;
  transition: background var(--t-fast);
  position: relative;
}
.chart-row + .chart-row::before {
  content: "";
  position: absolute;
  top: 0; left: 84px; right: 14px;
  height: 1px;
  background: var(--glass-border);
  opacity: 0.5;
}
.chart-row:hover { background: var(--glass-bg-weak); }
.chart-row:hover + .chart-row::before { opacity: 0; }
.chart-row:hover::before { opacity: 0; }'''),

# ── 7. Hero carousel scroll padding ────────────────────────────
('''.hero-track {
  display: flex; gap: 20px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  padding-bottom: 8px;
}''',

'''.hero-track {
  display: flex; gap: 22px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  padding-bottom: 12px;
  scroll-padding-left: var(--content-pad);
  margin: 0 calc(var(--content-pad) * -1);
  padding-left: var(--content-pad);
  padding-right: var(--content-pad);
}'''),

# ── 8. Player shadow polished ──────────────────────────────────
('box-shadow: 0 -10px 30px rgba(0,0,0,0.4);',
 'box-shadow: 0 -8px 24px rgba(0,0,0,0.32);'),

# ── 9. Sidebar item полировка ─────────────────────────────────
('''.sb-item {
  display: flex; align-items: center; gap: 12px;
  padding: 11px 14px;
  border-radius: var(--r-md);
  color: var(--text-secondary);
  font-size: 14.5px;
  font-weight: 500;
  cursor: pointer;
  text-align: left;
  width: 100%;
  transition: background var(--t-fast), color var(--t-fast);
  position: relative;
}''',

'''.sb-item {
  display: flex; align-items: center; gap: 14px;
  padding: 12px 16px;
  border-radius: var(--r-md);
  color: var(--text-secondary);
  font-size: 14.5px;
  font-weight: 500;
  cursor: pointer;
  text-align: left;
  width: 100%;
  transition: background var(--t-fast), color var(--t-fast);
  position: relative;
  min-height: 44px;
}'''),

# ── 10. Topbar spacing ─────────────────────────────────────────
('''.topbar {
  position: sticky; top: 0; z-index: 30;
  display: flex; align-items: center; gap: 18px;
  padding: 18px 0;''',

'''.topbar {
  position: sticky; top: 0; z-index: 30;
  display: flex; align-items: center; gap: 20px;
  padding: 20px 0 18px;'''),

# ── 11. Tweaks button typography ──────────────────────────────
('''.tweaks-btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 16px;
  border-radius: var(--r-pill);
  color: var(--text-secondary);
  transition: background var(--t-fast), color var(--t-fast);
}''',

'''.tweaks-btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 18px;
  border-radius: var(--r-pill);
  color: var(--text-secondary);
  transition: background var(--t-fast), color var(--t-fast);
  font-family: var(--font-sans);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: -0.005em;
  min-height: 38px;
}'''),

# ── 12. Chip selected — bolder ─────────────────────────────────
('''.chip[aria-pressed="true"] {
  background: var(--text-primary);
  color: var(--bg-base);
  border-color: transparent;
}''',

'''.chip[aria-pressed="true"] {
  background: var(--text-primary);
  color: var(--bg-base);
  border-color: transparent;
  font-weight: 600;
}'''),

# ── 13. Schedule cells ─────────────────────────────────────────
('''.schedule-cell {
  padding: 12px 14px;
  border-radius: var(--r-md);
  color: white;
  font-size: 13.5px;
  font-weight: 600;
  text-align: center;
  cursor: pointer;
  transition: transform var(--t-fast), filter var(--t-fast);
  letter-spacing: -0.005em;
  min-height: 44px;
  display: grid; place-items: center;
}''',

'''.schedule-cell {
  padding: 12px 14px;
  border-radius: var(--r-md);
  color: white;
  font-size: 13.5px;
  font-weight: 600;
  text-align: center;
  cursor: pointer;
  transition: transform var(--t-fast), filter var(--t-fast), box-shadow var(--t-fast);
  letter-spacing: -0.005em;
  min-height: 48px;
  display: grid; place-items: center;
  text-shadow: 0 1px 4px rgba(0,0,0,0.25);
}'''),

('.schedule-cell:hover { transform: scale(1.04); filter: brightness(1.1); }',
 '.schedule-cell:hover { transform: scale(1.04); filter: brightness(1.12); box-shadow: 0 6px 20px rgba(0,0,0,0.35); }'),

# ── 14. Sb-recent polish ───────────────────────────────────────
('''.sb-recent {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 12px;
  border-radius: var(--r-md);
  background: var(--glass-bg-weak);
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: background var(--t-fast), color var(--t-fast);
}''',

'''.sb-recent {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 14px;
  border-radius: var(--r-md);
  background: var(--glass-bg-weak);
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: background var(--t-fast), color var(--t-fast);
  min-height: 44px;
}'''),

# ── 15. Footer cleanup ──────────────────────────────────────────
('''.app-footer {
  margin-top: 8px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  padding: 24px 0;
  border-top: 1px solid var(--glass-border);
}''',

'''.app-footer {
  margin-top: 16px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  padding: 32px 0 20px;
  border-top: 1px solid var(--glass-border);
}'''),

('''.footer-bottom {
  font-size: 12px;
  color: var(--text-tertiary);
  display: flex; gap: 14px; flex-wrap: wrap;
  padding: 12px 0;
}''',

'''.footer-bottom {
  font-size: 12px;
  color: var(--text-tertiary);
  display: flex; gap: 18px; flex-wrap: wrap;
  padding: 16px 0 8px;
}'''),

# ── 16. Partner plates ──────────────────────────────────────────
('''.partners {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 14px;
  margin-top: 20px;
  margin-bottom: 28px;
}''',

'''.partners {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-top: 4px;
}'''),

# ── 17. Card-radio meta ────────────────────────────────────────
('''.card-radio-meta {
  position: absolute;
  bottom: 14px; left: 14px; right: 14px;
  display: flex; align-items: center; justify-content: space-between;
  z-index: 2;
}''',

'''.card-radio-meta {
  position: absolute;
  bottom: 16px; left: 16px; right: 16px;
  display: flex; align-items: end; justify-content: space-between;
  gap: 12px;
  z-index: 2;
}'''),

# ── 18. Card-clip-meta ─────────────────────────────────────────
('''.card-clip-meta {
  position: absolute;
  bottom: 12px; left: 14px; right: 14px;
  z-index: 2;
}''',

'''.card-clip-meta {
  position: absolute;
  bottom: 14px; left: 16px; right: 16px;
  z-index: 2;
}'''),

# ── 19. Search placeholder ─────────────────────────────────────
('  <input type="search" placeholder="Каналы, станции, исполнители, треки…" aria-label="Поиск">',
 '  <input type="search" placeholder="Найти канал, станцию, исполнителя или клип" aria-label="Поиск">'),

# ── 20. Schedule grid widths ────────────────────────────────────
('''.schedule-row {
  display: grid;
  grid-template-columns: 100px repeat(7, 1fr);
  gap: 10px;
  align-items: center;
  margin-bottom: 8px;
}''',

'''.schedule-row {
  display: grid;
  grid-template-columns: 110px repeat(7, 1fr);
  gap: 10px;
  align-items: center;
  margin-bottom: 10px;
}'''),

('''.schedule-head {
  display: grid;
  grid-template-columns: 100px repeat(7, 1fr);
  gap: 10px;
  margin-bottom: 12px;
  padding-left: 10px;
}''',

'''.schedule-head {
  display: grid;
  grid-template-columns: 110px repeat(7, 1fr);
  gap: 10px;
  margin-bottom: 14px;
  padding-left: 10px;
}'''),

# ── 21. Apple sidebar более solid ──────────────────────────────
('''[data-style="apple"] .sidebar {
  background: rgba(0,0,0,0.55);
  backdrop-filter: blur(40px);
  -webkit-backdrop-filter: blur(40px);
}''',

'''[data-style="apple"] .sidebar {
  background: rgba(0,0,0,0.78);
  backdrop-filter: blur(40px) saturate(1.4);
  -webkit-backdrop-filter: blur(40px) saturate(1.4);
}'''),

# ── 22. Live badge polish ──────────────────────────────────────
('''.live-badge {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 5px 11px 5px 9px;
  background: var(--live-dot);
  color: white;
  border-radius: var(--r-pill);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
}''',

'''.live-badge {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 5px 12px 5px 9px;
  background: var(--live-dot);
  color: white;
  border-radius: var(--r-pill);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  box-shadow: 0 4px 12px rgba(255,92,92,0.35);
}'''),

]

count = 0
for old, new in REPLACEMENTS:
    if old in s:
        s = s.replace(old, new)
        count += 1
    else:
        print(f'NOT FOUND: {old[:60]}...')

p.write_text(s, encoding='utf-8')
print(f'applied {count}/{len(REPLACEMENTS)} replacements')
