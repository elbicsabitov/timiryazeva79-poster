# Paws.kz Figma Design Tokens

Источник: FigMCP `dev` file (2026-04-24). Полный design system (132 секции, Walker/Owner/Authorization/Chat/Tutorials flows).

## Palette

### Primary — Orange (основной бренд)
| Token | Light | Dark |
|-------|-------|------|
| Primary/01 | `#FF9500` | `#FFAA33` |
| Primary/02 | `#FFBF66` | `#FFBF66` |
| Primary/03 | `#FFEACC` | `#1F222A` |
| Primary/04 | `#FFEACC` | `#35383F` |

### Gradients
- **Orange (основной):** `#FF9500 → #FFBF66` @ 196° — главный CTA, акценты
- **Orange Light:** тот же, opacity 0.08 — фон карточек/hero
- **Blue:** `#246BFD → #6F9EFF`
- **Green:** `#4ADE80 → #73FFA6`
- **Yellow:** `#FACC15 → #FFE580`
- **Red:** `#FF4D67 → #FF8A9B`

### Alerts & Status
- Success `#4ADE80` · Warning `#FACC15` · Error `#F75555`
- System Blue: `#007AFF` light / `#0A84FF` dark

### Gray scale (Material-style)
| Step | Light | Dark |
|------|-------|------|
| 01 | `#212121` | `#FFFFFF` |
| 02 | `#424242` | `#EEEEEE` |
| 03 | `#616161` | `#E0E0E0` |
| 04 | `#757575` | `#BDBDBD` |
| 05 | `#9E9E9E` | `#BDBDBD` |
| 06 | `#BDBDBD` | `#9E9E9E` |
| 07 | `#E0E0E0` | `#616161` |
| 08 | `#EEEEEE` | `#424242` |
| 09 | `#FFFFFF` | `#212121` |

### Backgrounds
- Dark: Primary `#181A20` · Secondary `#1F222A` · Tertiary `#35383F`
- Light: Primary `#FFFFFF` · Secondary `#FFFFFF` · Tertiary `#FAFAFA`

## Typography

**Primary:** Inter (H1-H6, все body)
**Secondary:** Roboto (только H2)

| Style | Font | Weight | Size | Line-height |
|-------|------|--------|------|-------------|
| H1/bold | Inter | Bold | 48 | 110% |
| H2/bold | **Roboto** | Bold | 40 | 110% |
| H3/bold | Inter | Bold | 32 | 110% |
| H4/bold | Inter | Bold | 24 | 120% |
| H5/bold | Inter | Bold | 20 | 120% |
| H6/bold | Inter | Bold | 18 | 120% |
| body/xxlarge | Inter | Reg/Semi | 20 | 120% |
| body/xlarge | Inter | Reg/Med/Semi/Bold | 18 | 140% |
| body/large | Inter | Reg/Med/Semi/Bold | 16 | 140% |
| body/medium | Inter | Reg/Med/Semi/Bold | 14 | 140% |
| body/small | Inter | Reg/Med/Bold | 12 | — |
| body/xsmall | Inter | Reg/Med/Semi/Bold | 10 | — |

## Shadows

### Card (нейтральные)
```css
/* Card/Shadow 1 - основной */
box-shadow: 0 4px 60px rgba(4, 6, 15, 0.08);

/* Card/Shadow 2 - лёгкий */
box-shadow: 0 4px 60px rgba(4, 6, 15, 0.05);

/* Card/Shadow 3 - большой подъём */
box-shadow: 0 20px 100px rgba(4, 6, 15, 0.08);
```

### Button (оранжевые — brand lift)
```css
/* Button/Shadow 1 */
box-shadow: 4px 8px 24px rgba(255, 149, 0, 0.25);

/* Button/Shadow 2 */
box-shadow: 4px 12px 32px rgba(255, 149, 0, 0.20);

/* Button/Shadow 3 - самый яркий */
box-shadow: 4px 16px 32px rgba(255, 149, 0, 0.20);
```

## Grid

12-column, center-aligned, max 1200px:
| Breakpoint | Cols | Gutter | Section (col-width) |
|------------|------|--------|---------------------|
| 1200-max | 12 | 40 | 60 |
| 960-1200 | 12 | 20 | 60 |
| 640-960 | 8 | 20 | 60 |
| 480-640 | 6 | 20 | 60 |
| 320-480 | 4 | 20 | 60 |

## Cross-check с live-сайтом paws.kz

Живой paws.kz использует **более агрессивный оранжевый `#eb6400`** как кнопки (чем Figma `#FF9500`) и `#fff0db` как cream-фон. Это более насыщенный вариант. Для нового лендинга:

- **Figma-токены** = основной источник (Inter, `#FF9500`, warm shadow)
- **Live `#eb6400`** = допустимая альтернатива для кнопок если нужно "более нажимное" ощущение
- Heading font-weight на живом сайте `800`, в Figma `Bold` (обычно 700) — можно использовать любой

## Применение в CSS

```css
:root {
  /* Brand */
  --paws-orange: #FF9500;
  --paws-orange-hover: #FFAA33;
  --paws-orange-soft: #FFBF66;
  --paws-orange-tint: #FFEACC;
  --paws-gradient: linear-gradient(196deg, #FF9500, #FFBF66);
  --paws-gradient-soft: linear-gradient(196deg, rgba(255,149,0,.08), rgba(255,191,102,.08));

  /* Neutrals (light theme) */
  --text-primary: #212121;
  --text-secondary: #424242;
  --text-tertiary: #616161;
  --text-muted: #9E9E9E;
  --divider: #E0E0E0;
  --surface-soft: #EEEEEE;
  --bg: #FFFFFF;
  --bg-soft: #FAFAFA;

  /* Status */
  --success: #4ADE80;
  --warning: #FACC15;
  --error: #F75555;
  --info: #007AFF;

  /* Shadows */
  --shadow-card: 0 4px 60px rgba(4, 6, 15, .08);
  --shadow-card-hover: 0 20px 100px rgba(4, 6, 15, .08);
  --shadow-btn: 4px 8px 24px rgba(255, 149, 0, .25);
  --shadow-btn-hover: 4px 16px 32px rgba(255, 149, 0, .20);

  /* Typography */
  --font-body: 'Inter', system-ui, sans-serif;
  --font-display: 'Inter', system-ui, sans-serif;

  /* Grid */
  --container-max: 1200px;
  --gutter-desktop: 40px;
  --gutter-tablet: 20px;
}
```
