"""Add Light theme variant + final Apple polish."""
from pathlib import Path

p = Path(r'C:\Users\elbics\Desktop\design-project\designs\showcase-aggregator.html')
s = p.read_text(encoding='utf-8')

# ── 1. Add Light theme tokens ─────────────────────────────────────────
LIGHT_THEME = '''
/* =========================================================================
   LIGHT STYLE — Apple Music Light / Apple TV+ Light HIG
   ========================================================================= */
[data-style="light"] {
  --bg-base: #f5f5f7;
  --bg-overlay: rgba(245,245,247,0.85);
  --backdrop-image: none;

  --glass-bg: rgba(255,255,255,0.92);
  --glass-bg-strong: #ffffff;
  --glass-bg-weak: rgba(0,0,0,0.04);
  --glass-border: rgba(0,0,0,0.08);
  --glass-rim: rgba(0,0,0,0.16);
  --glass-blur: 24px;
  --glass-blur-strong: 40px;

  --accent: var(--brand-red);
  --accent-hover: var(--brand-red-hot);
  --accent-soft: rgba(227,0,51,0.10);
  --on-accent: #ffffff;

  --text-primary: #1d1d1f;
  --text-secondary: #515154;
  --text-tertiary: #86868b;

  --live-dot: #E30033;
  --shadow-lg: 0 20px 50px rgba(0,0,0,0.10), 0 4px 14px rgba(0,0,0,0.06);
  --shadow-md: 0 8px 24px rgba(0,0,0,0.08);
}
[data-style="light"] body { background: var(--bg-base); }
[data-style="light"] .app-backdrop { background: var(--bg-base); }
[data-style="light"] .app-backdrop::after { display: none; }

[data-style="light"] .sidebar {
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(24px) saturate(1.4);
  -webkit-backdrop-filter: blur(24px) saturate(1.4);
  border-right: 1px solid var(--glass-border);
}
[data-style="light"] .sb-item[aria-current="page"] {
  background: var(--accent-soft);
  color: var(--accent);
  font-weight: 600;
}
[data-style="light"] .sb-item[aria-current="page"]::before {
  content: "";
  position: absolute;
  left: -8px; top: 50%; transform: translateY(-50%);
  width: 3px; height: 22px;
  background: var(--accent);
  border-radius: 2px;
}
[data-style="light"] .topbar {
  background: linear-gradient(180deg, rgba(245,245,247,0.92), rgba(245,245,247,0));
}
[data-style="light"] .tb-search,
[data-style="light"] .tb-icon-btn {
  background: rgba(0,0,0,0.05);
  border: 0;
}
[data-style="light"] .tb-search:hover,
[data-style="light"] .tb-icon-btn:hover {
  background: rgba(0,0,0,0.08);
}

[data-style="light"] .card-tv,
[data-style="light"] .card-news {
  background: #ffffff;
  border: 1px solid var(--glass-border);
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  box-shadow: var(--shadow-md);
}
[data-style="light"] .card-tv:hover,
[data-style="light"] .card-news:hover {
  background: #ffffff;
  box-shadow: var(--shadow-lg);
}
[data-style="light"] .card-radio-disc,
[data-style="light"] .card-genre,
[data-style="light"] .card-mood,
[data-style="light"] .card-clip-thumb,
[data-style="light"] .card-dj-art,
[data-style="light"] .card-artist-avatar {
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-md);
}

[data-style="light"] .chip {
  background: rgba(0,0,0,0.06);
  border: 0;
  color: var(--text-secondary);
}
[data-style="light"] .chip:hover { background: rgba(0,0,0,0.10); color: var(--text-primary); }
[data-style="light"] .chip[aria-pressed="true"] {
  background: var(--text-primary);
  color: white;
}

[data-style="light"] .btn-primary {
  background: #1d1d1f;
  color: white;
}
[data-style="light"] .btn-primary:hover { background: #000; }
[data-style="light"] .btn-secondary {
  background: rgba(255,255,255,0.5);
  color: white;
  border: 1px solid rgba(255,255,255,0.4);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

[data-style="light"] .player {
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(40px) saturate(1.6);
  -webkit-backdrop-filter: blur(40px) saturate(1.6);
  border-top: 1px solid var(--glass-border);
}
[data-style="light"] .pl-btn-play {
  background: #1d1d1f;
  color: white;
}
[data-style="light"] .pl-btn-play:hover { background: var(--accent); color: white; }

[data-style="light"] .tweaks {
  background: rgba(255,255,255,0.92);
  border: 1px solid var(--glass-border);
}

[data-style="light"] .schedule {
  background: #ffffff;
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-md);
}

[data-style="light"] .partner {
  background: #ffffff;
  border: 1px solid var(--glass-border);
}
[data-style="light"] .partner:hover { background: rgba(0,0,0,0.02); }

[data-style="light"] .sb-recent {
  background: rgba(0,0,0,0.04);
}
[data-style="light"] .sb-recent:hover { background: rgba(0,0,0,0.08); color: var(--text-primary); }

[data-style="light"] .chart-rank {
  color: var(--accent);
}

[data-style="light"] .row-link {
  color: var(--accent);
}

[data-style="light"] .card-news-tag {
  color: var(--accent);
}

[data-style="light"] .pl-btn:hover {
  background: rgba(0,0,0,0.06);
}

[data-style="light"] .tb-avatar {
  border: 0;
}

[data-style="light"] .player-volume input[type=range] {
  background: rgba(0,0,0,0.12);
}
[data-style="light"] .player-volume input[type=range]::-webkit-slider-thumb {
  background: #1d1d1f;
}

'''

# Insert before the RESET section
marker = '/* =========================================================================\n   RESET'
s = s.replace(marker, LIGHT_THEME + marker)

# ── 2. Update Tweaks panel HTML — add Light button ───────────────────
old_tweaks = '''<div class="tweaks" role="region" aria-label="Стиль оформления">
  <div class="tweaks-row">
    <button class="tweaks-btn" data-style-target="glass" aria-pressed="true">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 8a7 7 0 1 1 14 0v8a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4V8z"/><path d="M8 12h8" opacity="0.5"/></svg>
      Liquid Glass
    </button>
    <button class="tweaks-btn" data-style-target="apple" aria-pressed="false">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.05 20.28c-.98.95-2.05.86-3.08.4-1.09-.47-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.4C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.53 4.08zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/></svg>
      Apple
    </button>
  </div>
</div>'''

new_tweaks = '''<div class="tweaks" role="region" aria-label="Стиль оформления">
  <div class="tweaks-row">
    <button class="tweaks-btn" data-style-target="glass" aria-pressed="true">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 8a7 7 0 1 1 14 0v8a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4V8z"/><path d="M8 12h8" opacity="0.5"/></svg>
      Glass
    </button>
    <button class="tweaks-btn" data-style-target="apple" aria-pressed="false">
      <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.05 20.28c-.98.95-2.05.86-3.08.4-1.09-.47-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.4C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.53 4.08zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/></svg>
      Apple Dark
    </button>
    <button class="tweaks-btn" data-style-target="light" aria-pressed="false">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>
      Light
    </button>
  </div>
</div>'''

s = s.replace(old_tweaks, new_tweaks)

# ── 3. Update body color — добавить условие для light ─────────────────
# (already handled in LIGHT_THEME via [data-style="light"] body)

p.write_text(s, encoding='utf-8')
print('Light theme added')
