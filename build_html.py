#!/usr/bin/env python3
"""Wrap a generated wheel SVG in a print-ready A4 HTML, localized per language.

Page 1 is always the wheel. Page 2 is the monthly feelings tracker, which we
include only from tier 2 up — the youngest (1-ring) sheet is just the wheel.

Usage:
    python3 build_html.py [lang ...] [--tier 1 2 3] [--outdir out]
Reads out/<lang>/<tier>ring/wheel.svg, writes .../index.html
"""
import argparse
import os

from languages import LANGUAGES, core_data
from gen_wheel import TIERS, TIER_DIR

HERE = os.path.dirname(os.path.abspath(__file__))

# Tiers that get the second-page monthly tracker (the 1-ring sheet stays a
# single page — the calendar is too much for the youngest age band).
CALENDAR_TIERS = {2, 3}

CSS = """
  @page { size: A4; margin: 12mm; }
  * { box-sizing: border-box; }
  body { margin: 0; font-family: 'Nunito', 'Segoe UI', Verdana, sans-serif; color: #333; }
  .page { width: 186mm; min-height: 263mm; margin: 0 auto; padding: 4mm 0;
          display: flex; flex-direction: column; align-items: center;
          page-break-after: always; }
  .page:last-child { page-break-after: auto; }
  h1 { font-size: 26px; margin: 2mm 0 0; color: #2b2b2b; text-align: center; }
  .sub { font-size: 13px; color: #777; margin: 1mm 0 3mm; text-align: center; }
  .wheel { width: 165mm; max-width: 100%; }
  .howto { font-size: 12.5px; color: #555; max-width: 165mm; margin-top: 3mm;
           line-height: 1.5; }
  .howto b { color: #333; }
  .legend { display: flex; flex-wrap: wrap; gap: 6px 14px; justify-content: center;
            margin: 3mm 0 4mm; }
  .chip { font-size: 13px; font-weight: 700; display: inline-flex; align-items: center; }
  .chip i { width: 13px; height: 13px; border-radius: 50%; display: inline-block;
            margin-right: 5px; border: 1px solid rgba(0,0,0,.15); }
  .grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; width: 165mm; }
  .day { border: 1.5px solid #e3ddcb; border-radius: 9px; aspect-ratio: 1 / 1;
         display: flex; flex-direction: column; align-items: center;
         justify-content: center; background: #FFFDF7; }
  .day .num { font-size: 12px; font-weight: 800; color: #999; align-self: flex-start;
              margin: 4px 0 0 6px; }
  .dot { width: 26px; height: 26px; border-radius: 50%; border: 2px dashed #cfc6b0;
         margin-top: 2px; }
  .note { font-size: 11.5px; color: #888; margin-top: 4mm; max-width: 165mm;
          text-align: center; }
"""


def calendar_page(lang_code):
    lang = LANGUAGES[lang_code]
    legend = "".join(
        f'<span class="chip"><i style="background:{color}"></i>{name}</span>'
        for name, color, _ in core_data(lang_code)
    )
    boxes = "".join(
        f'<div class="day"><span class="num">{d}</span><span class="dot"></span></div>'
        for d in range(1, 32)
    )
    return f"""
  <section class="page">
    <h1>{lang["cal_title"]}</h1>
    <div class="sub">{lang["cal_subtitle"]}</div>
    <div class="legend">{legend}</div>
    <div class="grid">{boxes}</div>
    <div class="note">{lang["month_label"]}: ____________  •  {lang["cal_note"]}</div>
  </section>"""


def build_html(lang_code, svg, tier=2):
    lang = LANGUAGES[lang_code]
    cal = calendar_page(lang_code) if tier in CALENDAR_TIERS else ""
    return f"""<!DOCTYPE html>
<html lang="{lang_code}">
<head>
<meta charset="utf-8">
<title>{lang["title"]} — {lang["name"]} ({tier})</title>
<style>{CSS}</style>
</head>
<body>
  <section class="page">
    <h1>{lang["title"]}</h1>
    <div class="sub">{lang["subtitle"]}</div>
    <div class="wheel">{svg}</div>
    <div class="howto"><b>{lang["howto_title"]}</b> {lang["howto_body"]}</div>
  </section>
{cal}
</body>
</html>
"""


def generate_html(lang_code, tier, outdir):
    out = os.path.join(outdir, lang_code, TIER_DIR[tier])
    with open(os.path.join(out, "wheel.svg")) as f:
        svg = f.read()
    path = os.path.join(out, "index.html")
    with open(path, "w") as f:
        f.write(build_html(lang_code, svg, tier))
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("langs", nargs="*", default=list(LANGUAGES))
    ap.add_argument("--tier", nargs="*", type=int, default=list(TIERS), choices=TIERS)
    ap.add_argument("--outdir", default=os.path.join(HERE, "out"))
    args = ap.parse_args()
    for code in (args.langs or list(LANGUAGES)):
        for tier in args.tier:
            print("HTML:", generate_html(code, tier, args.outdir))


if __name__ == "__main__":
    main()
