#!/usr/bin/env python3
import os

THEMES = {
    "dark": dict(
        bg="#0d1117", chrome="#161b22", border="#30363d",
        fg="#e6edf3", muted="#8b949e", dim="#6e7681",
        green="#3fb950", red="#ff5f56", yellow="#ffbd2e",
        g1="#ff7b35", g2="#f778ba", g3="#58a6ff",
        steam="#8b949e", cup="#ff7b35", shimmer="#ffffff", shimmer_op="0.055",
        levels=["#21262d", "#0e4429", "#006d32", "#26a641", "#39d353"], grid_op="0.75",
    ),
    "light": dict(
        bg="#ffffff", chrome="#f6f8fa", border="#d0d7de",
        fg="#1f2328", muted="#59636e", dim="#818b98",
        green="#1a7f37", red="#ff5f56", yellow="#e3b341",
        g1="#d4590a", g2="#bf3989", g3="#0969da",
        steam="#818b98", cup="#d4590a", shimmer="#0969da", shimmer_op="0.045",
        levels=["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"], grid_op="0.9",
    ),
}

MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

NAME = "Anas Mohamed"
PITCH = 30        
NAME_X = 46       
NAME_Y = 142        
CARET_W = 16

W, H = 880, 240


GRID_X, GRID_Y, GRID_STEP, GRID_CELL = 470, 66, 13, 9
GRID_COLS, GRID_ROWS = 12, 7


def contrib_grid(t: dict) -> str:
    """A miniature contribution graph filling the space beside the name.

    Levels come from a fixed integer hash so the pattern is stable across
    regenerations rather than reshuffling on every run.
    """
    cells = []
    for c in range(GRID_COLS):
        for r in range(GRID_ROWS):
            h = (c * 73856093) ^ (r * 19349663) ^ 0x5f3a
            lvl = [0, 0, 1, 1, 2, 2, 3, 3, 4][(h >> 3) % 9]
            x = GRID_X + c * GRID_STEP
            y = GRID_Y + r * GRID_STEP
            delay = c * 0.09 + r * 0.035
            cells.append(
                f'<rect class="cell" x="{x}" y="{y}" width="{GRID_CELL}" height="{GRID_CELL}" '
                f'rx="2" fill="{t["levels"][lvl]}" style="animation-delay:{delay:.2f}s"/>'
            )
    return "\n      ".join(cells)


def banner(t: dict) -> str:
    chars = []
    for i, ch in enumerate(NAME):
        if ch == " ":
            continue
        cx = NAME_X + i * PITCH + PITCH / 2
        delay = 0.55 + i * 0.075
        chars.append(
            f'<text class="ch" x="{cx:.0f}" y="{NAME_Y}" text-anchor="middle" '
            f'style="animation-delay:{delay:.3f}s">{ch}</text>'
        )
    glyphs = "\n      ".join(chars)

    caret_travel = len(NAME) * PITCH
    caret_x = NAME_X
    type_dur = len(NAME) * 0.075

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Anas Mohamed — full-stack engineer">
  <title>Anas Mohamed — full-stack engineer</title>
  <defs>
    <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{t['g1']}"/>
      <stop offset="55%" stop-color="{t['g2']}"/>
      <stop offset="100%" stop-color="{t['g3']}"/>
    </linearGradient>
    <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{t['shimmer']}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{t['shimmer']}" stop-opacity="{t['shimmer_op']}"/>
      <stop offset="100%" stop-color="{t['shimmer']}" stop-opacity="0"/>
    </linearGradient>
    <!-- userSpaceOnUse: a horizontal line has a zero-height bbox, which makes an
         objectBoundingBox gradient degenerate and the stroke disappear entirely. -->
    <linearGradient id="rule" gradientUnits="userSpaceOnUse"
                    x1="{NAME_X}" y1="0" x2="{NAME_X + 340}" y2="0">
      <stop offset="0%" stop-color="{t['g1']}"/>
      <stop offset="50%" stop-color="{t['g2']}"/>
      <stop offset="100%" stop-color="{t['g3']}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="card">
      <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14"/>
    </clipPath>
  </defs>

  <style>
    .mono {{ font-family: {MONO}; }}
    .prompt {{ fill: {t['green']}; font-size: 15px; font-weight: 700; }}
    .cmd    {{ fill: {t['fg']};    font-size: 15px; font-weight: 600; }}
    .tag    {{ fill: {t['dim']};   font-size: 12px; letter-spacing: .04em; }}
    .sub    {{ fill: {t['muted']}; font-size: 14.5px; }}
    .accent {{ fill: {t['g1']};    font-size: 14.5px; font-weight: 600; }}
    .accent2{{ fill: {t['g3']};    font-size: 14.5px; font-weight: 600; }}

    .ch {{
      font-family: {MONO}; font-size: 44px; font-weight: 800;
      fill: url(#name); opacity: 0;
      animation: pop .28s cubic-bezier(.2,.9,.3,1.4) forwards;
    }}
    @keyframes pop {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}

    .caret {{
      fill: {t['g3']};
      animation: travel {type_dur:.2f}s steps({len(NAME)},end) .55s both,
                 blink 1.05s steps(2,jump-none) {type_dur + .55:.2f}s infinite;
    }}
    @keyframes travel {{ from {{ transform: translateX(0); }} to {{ transform: translateX({caret_travel}px); }} }}
    @keyframes blink  {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}

    .cursor2 {{ fill: {t['fg']}; animation: blink 1.05s steps(2,jump-none) infinite; }}

    .fade   {{ opacity: 0; animation: fadein .6s ease forwards; }}
    @keyframes fadein {{ to {{ opacity: 1; }} }}

    .sweep  {{ animation: sweep 7s cubic-bezier(.4,0,.2,1) 1.4s infinite; }}
    @keyframes sweep {{ 0% {{ transform: translateX(-320px); }} 55%,100% {{ transform: translateX({W}px); }} }}

    .rule   {{ stroke-dasharray: 340; stroke-dashoffset: 340; animation: draw 1.6s ease-out .3s forwards; }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}

    .steam  {{ stroke: {t['steam']}; stroke-width: 2.5; stroke-linecap: round; fill: none; opacity: 0; }}
    .s1 {{ animation: rise 3.2s ease-out 0.2s infinite; }}
    .s2 {{ animation: rise 3.2s ease-out 1.2s infinite; }}
    .s3 {{ animation: rise 3.2s ease-out 2.2s infinite; }}
    @keyframes rise {{
      0%   {{ opacity: 0;   transform: translateY(6px)  scaleX(.85); }}
      25%  {{ opacity: .55; }}
      70%  {{ opacity: .18; }}
      100% {{ opacity: 0;   transform: translateY(-16px) scaleX(1.15); }}
    }}

    .grid {{ opacity: {t['grid_op']}; }}
    .cell {{ animation: ripple 4.5s ease-in-out infinite; }}
    @keyframes ripple {{
      0%, 55%, 100% {{ opacity: .30; }}
      22%           {{ opacity: 1; }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      .ch, .caret, .fade, .sweep, .rule, .steam, .cursor2, .cell {{ animation: none; opacity: 1; }}
      .caret {{ transform: translateX({caret_travel}px); }}
      .rule  {{ stroke-dashoffset: 0; }}
    }}
  </style>

  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="{t['bg']}"/>

    <!-- window chrome -->
    <rect width="{W}" height="36" fill="{t['chrome']}"/>
    <line x1="0" y1="36" x2="{W}" y2="36" stroke="{t['border']}" stroke-width="1"/>
    <circle cx="22" cy="18" r="5.5" fill="{t['red']}"/>
    <circle cx="42" cy="18" r="5.5" fill="{t['yellow']}"/>
    <circle cx="62" cy="18" r="5.5" fill="{t['green']}"/>
    <text class="mono tag" x="{W/2}" y="22" text-anchor="middle">anas@arch — ~/dev — zsh</text>

    <!-- $ whoami -->
    <g class="fade" style="animation-delay:.1s">
      <text class="mono prompt" x="24" y="82">❯</text>
      <text class="mono cmd" x="46" y="82">whoami</text>
    </g>

    <!-- typed name + caret -->
    <g>
      {glyphs}
      <rect class="caret" x="{caret_x}" y="{NAME_Y - 34}" width="{CARET_W}" height="42" rx="2"/>
    </g>

    <!-- underline rule -->
    <line class="rule" x1="{NAME_X}" y1="{NAME_Y + 16}" x2="{NAME_X + 340}" y2="{NAME_Y + 16}"
          stroke="url(#rule)" stroke-width="3" stroke-linecap="round"/>

    <!-- subtitle -->
    <g class="fade" style="animation-delay:1.7s">
      <text class="mono sub" x="{NAME_X}" y="184">
        <tspan class="accent">full-stack</tspan><tspan> engineer · </tspan><tspan class="accent2">rust</tspan><tspan> + </tspan><tspan class="accent2">typescript</tspan><tspan> · fayoum, egypt</tspan>
      </text>
    </g>

    <!-- trailing prompt -->
    <g class="fade" style="animation-delay:2.1s">
      <text class="mono prompt" x="24" y="214">❯</text>
      <rect class="cursor2" x="46" y="202" width="11" height="16" rx="1.5"/>
    </g>

    <!-- miniature contribution grid -->
    <g class="grid">
      {contrib_grid(t)}
    </g>

    <!-- coffee: "turning coffee into code" -->
    <g transform="translate(770,96)">
      <g class="steam s1"><path d="M0 0 C -5 -8, 5 -14, 0 -24"/></g>
      <g class="steam s2" transform="translate(16,2)"><path d="M0 0 C -5 -8, 5 -14, 0 -24"/></g>
      <g class="steam s3" transform="translate(32,0)"><path d="M0 0 C -5 -8, 5 -14, 0 -24"/></g>
      <g class="fade" style="animation-delay:2.4s">
        <path d="M-8 12 h48 v26 a14 14 0 0 1 -14 14 h-20 a14 14 0 0 1 -14 -14 z"
              fill="none" stroke="{t['cup']}" stroke-width="3" stroke-linejoin="round"/>
        <path d="M40 18 h9 a9 9 0 0 1 0 18 h-9" fill="none" stroke="{t['cup']}" stroke-width="3"/>
        <line x1="-16" y1="58" x2="48" y2="58" stroke="{t['cup']}" stroke-width="3" stroke-linecap="round" opacity=".55"/>
      </g>
    </g>

    <!-- light sweep -->
    <rect class="sweep" x="0" y="0" width="320" height="{H}" fill="url(#sweep)"/>
  </g>

  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{t['border']}" stroke-width="1"/>
</svg>
'''


def footer(t: dict) -> str:
    fw, fh = 880, 120
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{fw}" height="{fh}" viewBox="0 0 {fw} {fh}" role="img" aria-label="footer">
  <defs>
    <linearGradient id="fg1" gradientUnits="userSpaceOnUse" x1="40" y1="0" x2="840" y2="0">
      <stop offset="0%"   stop-color="{t['g1']}" stop-opacity="0"/>
      <stop offset="25%"  stop-color="{t['g1']}"/>
      <stop offset="60%"  stop-color="{t['g2']}"/>
      <stop offset="90%"  stop-color="{t['g3']}"/>
      <stop offset="100%" stop-color="{t['g3']}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <style>
    .mono {{ font-family: {MONO}; }}
    .line {{
      fill: none; stroke: url(#fg1); stroke-width: 2.5; stroke-linecap: round;
      stroke-dasharray: 1600; stroke-dashoffset: 1600;
      animation: draw 2.4s ease-out forwards;
    }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    .pulse {{ fill: {t['g2']}; animation: run 4.5s linear 1.2s infinite; }}
    @keyframes run {{
      0%   {{ transform: translateX(40px);  opacity: 0; }}
      8%   {{ opacity: 1; }}
      92%  {{ opacity: 1; }}
      100% {{ transform: translateX(840px); opacity: 0; }}
    }}
    .txt {{ fill: {t['muted']}; font-size: 13px; opacity: 0; animation: fadein .8s ease 1.6s forwards; }}
    .hl  {{ fill: {t['g2']}; font-weight: 700; }}
    @keyframes fadein {{ to {{ opacity: 1; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .line, .pulse, .txt {{ animation: none; opacity: 1; stroke-dashoffset: 0; }}
    }}
  </style>

  <path class="line" d="M40 46 H300 l14 -20 l16 40 l14 -20 H520 l12 -14 l14 28 l12 -14 H840"/>
  <circle class="pulse" cx="0" cy="46" r="4.5"/>
  <text class="mono txt" x="{fw/2}" y="84" text-anchor="middle">
    <tspan>❯ </tspan><tspan class="hl">git commit</tspan><tspan> -m "thanks for stopping by" &amp;&amp; </tspan><tspan class="hl">git push</tspan>
  </text>
</svg>
'''


def main() -> None:
    out = "/home/anas/projects/readme/assets"
    os.makedirs(out, exist_ok=True)
    for name, t in THEMES.items():
        with open(f"{out}/banner-{name}.svg", "w", encoding="utf-8") as f:
            f.write(banner(t))
        with open(f"{out}/footer-{name}.svg", "w", encoding="utf-8") as f:
            f.write(footer(t))
    print("wrote:", sorted(os.listdir(out)))


if __name__ == "__main__":
    main()
