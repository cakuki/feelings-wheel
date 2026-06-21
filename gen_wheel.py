#!/usr/bin/env python3
"""Generate a printable feeling wheel as SVG for a given language.

Usage:
    python3 gen_wheel.py [lang ...] [--outdir out]
Defaults to all languages into ./out/<lang>/wheel.svg
"""
import argparse
import math
import os

from languages import LANGUAGES, core_data

HERE = os.path.dirname(os.path.abspath(__file__))

CX, CY = 350, 350
R_CENTER = 90      # inner face circle
R_CORE = 178       # core ring outer edge
R_OUTER = 300      # outer ring outer edge
R_CORE_TEXT = (R_CENTER + R_CORE) / 2  # baseline radius for curved core labels
CORE_PAD = 16      # min px of clear space between a core label and each divider


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


def baseline_arc(r, a0, a1, flip):
    """An open arc to set curved text on. On the bottom half (flip) the arc is
    drawn in reverse so glyphs stay upright instead of hanging upside down."""
    start, end, sweep = (a1, a0, 0) if flip else (a0, a1, 1)
    x0, y0 = pol(CX, CY, r, start)
    x1, y1 = pol(CX, CY, r, end)
    return f"M {x0:.2f} {y0:.2f} A {r:.2f} {r:.2f} 0 0 {sweep} {x1:.2f} {y1:.2f}"


def build_svg(lang_code):
    lang = LANGUAGES[lang_code]
    data = core_data(lang_code)
    core_font = lang["core_font"]

    svg = ['<svg xmlns="http://www.w3.org/2000/svg" '
           'xmlns:xlink="http://www.w3.org/1999/xlink" '
           'viewBox="0 0 700 720" font-family="Nunito, Verdana, sans-serif">']
    defs = ['<defs>']
    svg.append('<rect x="0" y="0" width="700" height="720" fill="#FFFDF7"/>')

    n = len(data)
    core_span = 360 / n          # 60
    outer_span = core_span / 4   # 15

    for i, (core, color, feelings) in enumerate(data):
        a_start = i * core_span
        a_end = a_start + core_span
        a_mid = (a_start + a_end) / 2

        # outer ring (4 nuanced feelings), lighter shade, radial labels
        for j, feel in enumerate(feelings):
            oa0 = a_start + j * outer_span
            oa1 = oa0 + outer_span
            oam = (oa0 + oa1) / 2
            shade = lighten(color, 0.45)
            svg.append(f'<path d="{arc_segment(R_CORE, R_OUTER, oa0, oa1)}" '
                       f'fill="{shade}" stroke="#FFFDF7" stroke-width="2.5"/>')
            tr = (R_CORE + R_OUTER) / 2
            tx, ty = pol(CX, CY, tr, oam)
            rot = oam - 90  # along the radius (outward)
            if (oam % 360) > 180:  # left half -> flip so it's upright
                rot += 180
            fs = 15 if len(feel) <= 9 else (13 if len(feel) <= 13 else 11)
            svg.append(f'<text x="{tx:.2f}" y="{ty:.2f}" font-size="{fs}" '
                       f'font-weight="700" fill="#3a3a3a" text-anchor="middle" '
                       f'dominant-baseline="central" '
                       f'transform="rotate({rot:.2f} {tx:.2f} {ty:.2f})">{feel}</text>')

        # core ring (label curved along the arc, baseline follows the circle)
        svg.append(f'<path d="{arc_segment(R_CENTER, R_CORE, a_start, a_end)}" '
                   f'fill="{color}" stroke="#FFFDF7" stroke-width="3"/>')
        flip = 90 < (a_mid % 360) < 270  # bottom half -> reverse arc so text is upright
        pid = f"corepath{i}"
        defs.append(f'<path id="{pid}" fill="none" '
                    f'd="{baseline_arc(R_CORE_TEXT, a_start, a_end, flip)}"/>')
        svg.append(f'<text font-size="{core_font}" font-weight="800" fill="#ffffff" '
                   f'text-anchor="middle" dominant-baseline="central">'
                   f'<textPath href="#{pid}" xlink:href="#{pid}" startOffset="50%">'
                   f'{core}</textPath></text>')

    # center circle + prompt (3 lines, sized to stay inside the circle)
    line1, line2, line3 = lang["center"]
    svg.append(f'<circle cx="{CX}" cy="{CY}" r="{R_CENTER}" fill="#FFFDF7" '
               f'stroke="#cfc6b0" stroke-width="2"/>')
    svg.append(f'<text x="{CX}" y="{CY-22}" font-size="17" font-weight="800" '
               f'fill="#444" text-anchor="middle">{line1}</text>')
    svg.append(f'<text x="{CX}" y="{CY+1}" font-size="17" font-weight="800" '
               f'fill="#444" text-anchor="middle">{line2}</text>')
    svg.append(f'<text x="{CX}" y="{CY+25}" font-size="15" font-weight="800" '
               f'fill="#444" text-anchor="middle">{line3}</text>')

    defs.append('</defs>')
    svg.insert(1, "\n".join(defs))
    svg.append('</svg>')
    return "\n".join(svg)


def generate_svg(lang_code, outdir):
    out = os.path.join(outdir, lang_code)
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "wheel.svg")
    with open(path, "w") as f:
        f.write(build_svg(lang_code))
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("langs", nargs="*", default=list(LANGUAGES),
                    help="language codes (default: all)")
    ap.add_argument("--outdir", default=os.path.join(HERE, "out"))
    args = ap.parse_args()
    for code in (args.langs or list(LANGUAGES)):
        print("SVG:", generate_svg(code, args.outdir))


if __name__ == "__main__":
    main()
