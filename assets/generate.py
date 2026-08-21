#!/usr/bin/env python3
import os

THEMES = {
    "dark": dict(
        bg="#0d1117", border="#30363d",
        fg="#e6edf3", muted="#8b949e",
        g1="#ff7b35", g2="#f778ba", g3="#58a6ff",
        arch="#1793d1",
        ansi=["#484f58", "#ff7b72", "#3fb950", "#d29922",
              "#58a6ff", "#bc8cff", "#39c5cf", "#b1bac4"],
    ),
    "light": dict(
        bg="#ffffff", border="#d0d7de",
        fg="#1f2328", muted="#59636e",
        g1="#d4590a", g2="#bf3989", g3="#0969da",
        arch="#1177ab",
        ansi=["#6e7781", "#cf222e", "#1a7f37", "#9a6700",
              "#0969da", "#8250df", "#1b7c83", "#8c959f"],
    ),
}

MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

W = 880  # H is derived from the logo height further down

# Straight out of `fastfetch --logo arch`, padded to a rectangle.
LOGO = [
    "                  -`                 ",
    "                 .o+`                ",
    "                `ooo/                ",
    "               `+oooo:               ",
    "              `+oooooo:              ",
    "              -+oooooo+:             ",
    "            `/:-:++oooo+:            ",
    "           `/++++/+++++++:           ",
    "          `/++++++++++++++:          ",
    "         `/+++ooooooooooooo/`        ",
    "        ./ooosssso++osssssso+`       ",
    "       .oossssso-````/ossssss+`      ",
    "      -osssssso.      :ssssssso.     ",
    "     :osssssss/        osssso+++.    ",
    "    /ossssssss/        +ssssooo/-    ",
    "  `/ossssso+/:-        -:/+osssso+-  ",
    " `+sso+:-`                 `.-/+oso: ",
    "`++:.                           `-/+/",
    ".`                                 `/",
]

TITLE = "anas@arch"
ROWS = [
    ("os",       "Arch Linux x86_64"),
    ("shell",    "zsh"),
    ("editor",   "Neovim"),
    ("langs",    "TypeScript, Rust"),
    ("frontend", "React, Next.js, Tailwind"),
    ("backend",  "Node, Postgres, Prisma"),
    ("work",     "software engineer, freelance"),
    ("building", "playercn & najmos & todo_cli"),
    ("learning", "Rust, cloud architecture"),
    ("where",    "Fayoum, Egypt"),
    ("web",      "anas-mohamed.vercel.app"),
]

# Everything sits on one terminal cell grid: the logo and the info block share a
# single font size and line step, the way real fastfetch output does. Sizing the
# ascii art separately is what makes these banners read as drawn rather than
# captured. A terminal cell is ~0.6em wide and ~1.2em tall; matching that ratio
# is what keeps the logo from looking stretched.
SIZE = 12
CELL, STEP = SIZE * 0.6, round(SIZE * 1.2)
TOP, PAD = 42, 36                                 # first baseline, card padding

_logo_w = len(LOGO[0]) * CELL
_key_w = (max(len(k) for k, _ in ROWS) + 2) * CELL
_val_w = max(len(v) for _, v in ROWS) * CELL
_gutter = 40                                      # logo column -> info column

LOGO_X = round((W - (_logo_w + _gutter + _key_w + _val_w)) / 2)
KEY_X = round(LOGO_X + _logo_w + _gutter)
VAL_X = round(KEY_X + _key_w)


def line_y(n: int) -> int:
    """Baseline of the nth output line."""
    return TOP + n * STEP


# fastfetch top-aligns the info block against line 1 of the logo.
LOGO_Y0 = TITLE_Y = line_y(0)
SEP_Y, ROW_Y0 = line_y(1), line_y(2)
SWATCH, SWATCH_STEP = 16, 20
SWATCH_Y = line_y(len(ROWS) + 3) - SWATCH + 3     # blank line, then the palette

H = line_y(len(LOGO) - 1) + PAD                   # logo is the taller column


def banner(t: dict) -> str:
    # xml:space="preserve" keeps the ascii art's leading spaces; the mono font
    # then does the column alignment for free.
    logo = "\n      ".join(
        f'<text class="mono art" xml:space="preserve" x="{LOGO_X}" '
        f'y="{LOGO_Y0 + i * STEP}">{line}</text>'
        for i, line in enumerate(LOGO)
    )

    info = "\n      ".join(
        f'<text class="mono key" x="{KEY_X}" y="{y}">{k}</text>'
        f'<text class="mono val" x="{VAL_X}" y="{y}">{v}</text>'
        for (k, v), y in ((r, ROW_Y0 + i * STEP) for i, r in enumerate(ROWS))
    )

    swatches = "\n      ".join(
        f'<rect x="{KEY_X + i * SWATCH_STEP}" y="{SWATCH_Y}" width="{SWATCH}" '
        f'height="{SWATCH}" rx="2" fill="{c}"/>'
        for i, c in enumerate(t["ansi"])
    )

    label = f"{TITLE}: " + ", ".join(v for _, v in ROWS)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">
  <title>Anas Mohamed, full-stack engineer</title>
  <style>
    .mono  {{ font-family: {MONO}; font-size: {SIZE}px; }}
    .art   {{ fill: {t['arch']};  font-weight: 700; }}
    .title {{ fill: {t['g1']};    font-weight: 700; }}
    .sep   {{ fill: {t['muted']}; }}
    .key   {{ fill: {t['g1']};    font-weight: 700; }}
    .val   {{ fill: {t['fg']}; }}
  </style>

  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14"
        fill="{t['bg']}" stroke="{t['border']}" stroke-width="1"/>

  <g>
      {logo}
  </g>

  <text class="mono title" x="{KEY_X}" y="{TITLE_Y}">{TITLE}</text>
  <text class="mono sep" x="{KEY_X}" y="{SEP_Y}">{'─' * len(TITLE)}</text>

  <g>
      {info}
  </g>

  <g>
      {swatches}
  </g>
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
