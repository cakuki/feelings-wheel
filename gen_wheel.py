#!/usr/bin/env python3
"""Generate a printable Turkish 'Duygu Çarkı' (feeling wheel) as an SVG/HTML.
Designed for a 9–12 year old: 6 core emotions, each with 4 nuanced feelings.
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

CX, CY = 350, 350
R_CENTER = 90      # inner face circle
R_CORE = 178       # core ring outer edge
R_OUTER = 300      # outer ring outer edge

# (core name, base color, [4 nuanced feelings])
DATA = [
    ("Mutlu",   "#F4C430", ["Neşeli", "Heyecanlı", "Gururlu", "Minnettar"]),
    ("Şaşkın",  "#E8833A", ["Meraklı", "Hayran", "Kafası karışık", "Şok"]),
    ("Kızgın",  "#DB504A", ["Sinirli", "Öfkeli", "Kıskanç", "Engellenmiş"]),
    ("Korkmuş", "#9B6FB0", ["Endişeli", "Utangaç", "Tedirgin", "Panik"]),
    ("Üzgün",   "#4F8FCB", ["Yalnız", "Hayal kırıklığı", "Çaresiz", "Özlemli"]),
    ("Sakin",   "#56B27E", ["Huzurlu", "Rahat", "Güvende", "Memnun"]),
]

def lighten(hex_color, factor):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"

def pol(cx, cy, r, deg):
    a = math.radians(deg - 90)  # 0deg = top
    return cx + r * math.cos(a), cy + r * math.sin(a)

def arc_segment(r_in, r_out, a0, a1):
    x0o, y0o = pol(CX, CY, r_out, a0)
    x1o, y1o = pol(CX, CY, r_out, a1)
    x0i, y0i = pol(CX, CY, r_in, a0)
    x1i, y1i = pol(CX, CY, r_in, a1)
    large = 1 if (a1 - a0) > 180 else 0
    return (f"M {x0o:.2f} {y0o:.2f} "
            f"A {r_out:.2f} {r_out:.2f} 0 {large} 1 {x1o:.2f} {y1o:.2f} "
            f"L {x1i:.2f} {y1i:.2f} "
            f"A {r_in:.2f} {r_in:.2f} 0 {large} 0 {x0i:.2f} {y0i:.2f} Z")

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 720" font-family="Nunito, Verdana, sans-serif">')
svg.append('<rect x="0" y="0" width="700" height="720" fill="#FFFDF7"/>')

n = len(DATA)
core_span = 360 / n          # 60
outer_span = core_span / 4   # 15

for i, (core, color, feelings) in enumerate(DATA):
    a_start = i * core_span
    a_end = a_start + core_span
    a_mid = (a_start + a_end) / 2

    # outer ring (4 nuanced feelings), lighter shade
    for j, feel in enumerate(feelings):
        oa0 = a_start + j * outer_span
        oa1 = oa0 + outer_span
        oam = (oa0 + oa1) / 2
        shade = lighten(color, 0.45)
        svg.append(f'<path d="{arc_segment(R_CORE, R_OUTER, oa0, oa1)}" '
                   f'fill="{shade}" stroke="#FFFDF7" stroke-width="2.5"/>')
        # radial text, readable
        tr = (R_CORE + R_OUTER) / 2
        tx, ty = pol(CX, CY, tr, oam)
        rot = oam - 90  # align text along radius (outward)
        if (oam % 360) > 180:  # left half -> flip so it's upright
            rot += 180
        # font size adapts to label length
        fs = 15 if len(feel) <= 9 else (13 if len(feel) <= 13 else 11)
        svg.append(f'<text x="{tx:.2f}" y="{ty:.2f}" font-size="{fs}" '
                   f'font-weight="700" fill="#3a3a3a" text-anchor="middle" '
                   f'dominant-baseline="central" '
                   f'transform="rotate({rot:.2f} {tx:.2f} {ty:.2f})">{feel}</text>')

    # core ring
    svg.append(f'<path d="{arc_segment(R_CENTER, R_CORE, a_start, a_end)}" '
               f'fill="{color}" stroke="#FFFDF7" stroke-width="3"/>')
    tx, ty = pol(CX, CY, (R_CENTER + R_CORE) / 2, a_mid)
    rot = a_mid - 90
    if (a_mid % 360) > 180:
        rot += 180
    fs_core = 22 if len(core) <= 6 else 16  # shrink long names (e.g. Korkmuş) to fit the ring
    svg.append(f'<text x="{tx:.2f}" y="{ty:.2f}" font-size="{fs_core}" '
               f'font-weight="800" fill="#ffffff" text-anchor="middle" '
               f'dominant-baseline="central" '
               f'transform="rotate({rot:.2f} {tx:.2f} {ty:.2f})">{core}</text>')

# center circle + prompt (sized to stay inside the circle)
svg.append(f'<circle cx="{CX}" cy="{CY}" r="{R_CENTER}" fill="#FFFDF7" stroke="#cfc6b0" stroke-width="2"/>')
svg.append(f'<text x="{CX}" y="{CY-22}" font-size="17" font-weight="800" fill="#444" text-anchor="middle">Bugün</text>')
svg.append(f'<text x="{CX}" y="{CY+1}" font-size="17" font-weight="800" fill="#444" text-anchor="middle">nasıl</text>')
svg.append(f'<text x="{CX}" y="{CY+25}" font-size="15" font-weight="800" fill="#444" text-anchor="middle">hissediyorsun?</text>')

svg.append('</svg>')

svg_str = "\n".join(svg)
with open(os.path.join(HERE, "duygu-carki.svg"), "w") as f:
    f.write(svg_str)
print("SVG written, len:", len(svg_str))
