#!/usr/bin/env python3
"""Generate a printable feelings wheel as SVG for a language and a ring tier.

Three tiers (how many rings around the hub):
    1  core feelings only            ages 4–9   (early readers)
    2  core + nuanced feelings       ages 9–12  (the classic wheel)
    3  core + nuanced + fine feelings ages 12+  (the full map, 48 leaves)

Usage:
    python3 gen_wheel.py [lang ...] [--tier 1 2 3] [--outdir out]
Writes out/<lang>/<tier>ring/wheel.svg
"""
import argparse
import math
import os

from languages import LANGUAGES, core_data, leaf_data

HERE = os.path.dirname(os.path.abspath(__file__))

CX, CY = 350, 350
R_CENTER = 90      # inner face circle
R_CORE = 178       # core ring outer edge
R_OUTER = 300      # ring-2 (nuanced) outer edge
R_LEAF = 408       # ring-3 (fine / leaves) outer edge
R_CORE_TEXT = (R_CENTER + R_CORE) / 2  # baseline radius for curved core labels
CORE_PAD = 16      # min px of clear space between a core label and each divider
MARGIN = 14        # blank px between the outermost ring and the viewBox edge

TIERS = (1, 2, 3)
TIER_DIR = {1: "1ring", 2: "2ring", 3: "3ring"}


def tier_radius(tier):
    return {1: R_CORE, 2: R_OUTER, 3: R_LEAF}[tier]


def tier_size(tier):
    """Side length (px) of the square viewBox/canvas that fits this tier."""
    return int(round(2 * (tier_radius(tier) + MARGIN)))


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


def radial_label(svg, text, r_in, r_out, a0, a1, fs, color="#3a3a3a"):
    """A label centered in a wedge, reading outward along the radius."""
    am = (a0 + a1) / 2
    tr = (r_in + r_out) / 2
    tx, ty = pol(CX, CY, tr, am)
    rot = am - 90
    if (am % 360) > 180:  # left half -> flip so it's upright
        rot += 180
    svg.append(f'<text x="{tx:.2f}" y="{ty:.2f}" font-size="{fs}" '
               f'font-weight="700" fill="{color}" text-anchor="middle" '
               f'dominant-baseline="central" '
               f'transform="rotate({rot:.2f} {tx:.2f} {ty:.2f})">{text}</text>')


def build_svg(lang_code, tier=2):
    lang = LANGUAGES[lang_code]
    data = core_data(lang_code)
    leaves = leaf_data(lang_code)
    core_font = lang["core_font"]

    size = tier_size(tier)
    vb_min = CX - size / 2  # == CY - size/2 (centered)
    vb = f"{vb_min:.0f} {vb_min:.0f} {size} {size}"

    svg = ['<svg xmlns="http://www.w3.org/2000/svg" '
           'xmlns:xlink="http://www.w3.org/1999/xlink" '
           f'viewBox="{vb}" width="{size}" height="{size}" '
           'font-family="Nunito, Verdana, sans-serif">']
    defs = ['<defs>']
    svg.append(f'<rect x="{vb_min:.0f}" y="{vb_min:.0f}" width="{size}" '
               f'height="{size}" fill="#FFFDF7"/>')

    n = len(data)
    core_span = 360 / n          # 60
    outer_span = core_span / 4   # 15  (one ring-2 feeling)
    leaf_span = outer_span / 2   # 7.5 (one ring-3 leaf)

    for i, (core, color, feelings) in enumerate(data):
        a_start = i * core_span
        a_end = a_start + core_span
        a_mid = (a_start + a_end) / 2

        # ring 2 — 4 nuanced feelings (tiers 2 and 3)
        if tier >= 2:
            for j, feel in enumerate(feelings):
                oa0 = a_start + j * outer_span
                oa1 = oa0 + outer_span
                shade = lighten(color, 0.45)
                svg.append(f'<path d="{arc_segment(R_CORE, R_OUTER, oa0, oa1)}" '
                           f'fill="{shade}" stroke="#FFFDF7" stroke-width="2.5"/>')
                fs = 15 if len(feel) <= 9 else (13 if len(feel) <= 13 else 11)
                radial_label(svg, feel, R_CORE, R_OUTER, oa0, oa1, fs)

        # ring 3 — 2 fine "leaf" feelings under each ring-2 feeling (tier 3)
        if tier >= 3 and leaves[i][1]:
            _, pairs = leaves[i]
            for j, pair in enumerate(pairs):
                for k, leaf in enumerate(pair):
                    la0 = a_start + j * outer_span + k * leaf_span
                    la1 = la0 + leaf_span
                    shade = lighten(color, 0.62)
                    svg.append(f'<path d="{arc_segment(R_OUTER, R_LEAF, la0, la1)}" '
                               f'fill="{shade}" stroke="#FFFDF7" stroke-width="2"/>')
                    fs = 12 if len(leaf) <= 8 else (11 if len(leaf) <= 11 else 10)
                    radial_label(svg, leaf, R_OUTER, R_LEAF, la0, la1, fs)

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


def generate_svg(lang_code, tier, outdir):
    out = os.path.join(outdir, lang_code, TIER_DIR[tier])
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "wheel.svg")
    with open(path, "w") as f:
        f.write(build_svg(lang_code, tier))
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("langs", nargs="*", default=list(LANGUAGES),
                    help="language codes (default: all)")
    ap.add_argument("--tier", nargs="*", type=int, default=list(TIERS),
                    choices=TIERS, help="ring tiers to build (default: 1 2 3)")
    ap.add_argument("--outdir", default=os.path.join(HERE, "out"))
    args = ap.parse_args()
    for code in (args.langs or list(LANGUAGES)):
        for tier in args.tier:
            print("SVG:", generate_svg(code, tier, args.outdir))


if __name__ == "__main__":
    main()
