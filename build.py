#!/usr/bin/env python3
"""Build the feeling wheel for one or more languages.

    python3 build.py            # all languages
    python3 build.py en de       # only these
    python3 build.py --no-pdf    # skip PDF/preview rendering

Outputs land in out/<lang>/: wheel.svg, index.html, and (if Chrome is found)
wheel.pdf + wheel-preview.png. Everything under out/ is gitignored.
"""
import argparse
import os
import shutil
import subprocess

from languages import LANGUAGES
from gen_wheel import generate_svg
from build_html import generate_html

HERE = os.path.dirname(os.path.abspath(__file__))

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    shutil.which("google-chrome"),
    shutil.which("chromium"),
    shutil.which("chrome"),
]


def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and os.path.exists(c):
            return c
    return None


def render_chrome(chrome, lang_dir):
    html = os.path.join(lang_dir, "index.html")
    svg = os.path.join(lang_dir, "wheel.svg")
    common = [chrome, "--headless", "--disable-gpu"]
    subprocess.run(common + ["--no-pdf-header-footer",
                   f"--print-to-pdf={os.path.join(lang_dir, 'wheel.pdf')}",
                   f"file://{html}"],
                   check=True, capture_output=True)
    subprocess.run(common + ["--window-size=700,720",
                   f"--screenshot={os.path.join(lang_dir, 'wheel-preview.png')}",
                   f"file://{svg}"],
                   check=True, capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("langs", nargs="*", default=list(LANGUAGES))
    ap.add_argument("--outdir", default=os.path.join(HERE, "out"))
    ap.add_argument("--no-pdf", action="store_true", help="skip Chrome PDF/preview")
    args = ap.parse_args()

    chrome = None if args.no_pdf else find_chrome()
    if not args.no_pdf and not chrome:
        print("! Chrome not found — writing SVG/HTML only (open index.html to print).")

    for code in (args.langs or list(LANGUAGES)):
        generate_svg(code, args.outdir)
        generate_html(code, args.outdir)
        lang_dir = os.path.join(args.outdir, code)
        line = f"✓ {code} ({LANGUAGES[code]['name']}): {lang_dir}/index.html"
        if chrome:
            render_chrome(chrome, lang_dir)
            line += "  + wheel.pdf"
        print(line)


if __name__ == "__main__":
    main()
