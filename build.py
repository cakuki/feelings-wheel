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
import zipfile

from languages import LANGUAGES
from gen_wheel import generate_svg
from build_html import generate_html

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = "feelings-wheel"

CHROME_CANDIDATES = [
    os.environ.get("CHROME"),  # explicit override (used in CI)
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    shutil.which("google-chrome"),
    shutil.which("google-chrome-stable"),
    shutil.which("chromium"),
    shutil.which("chromium-browser"),
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
    # --no-sandbox is needed on most CI runners; harmless locally.
    common = [chrome, "--headless", "--disable-gpu", "--no-sandbox"]
    subprocess.run(common + ["--no-pdf-header-footer",
                   f"--print-to-pdf={os.path.join(lang_dir, 'wheel.pdf')}",
                   f"file://{html}"],
                   check=True, capture_output=True)
    subprocess.run(common + ["--window-size=700,720",
                   f"--screenshot={os.path.join(lang_dir, 'wheel-preview.png')}",
                   f"file://{svg}"],
                   check=True, capture_output=True)


def package(lang, lang_dir, distdir):
    """Produce per-language release downloadables: a standalone PDF and a zip
    bundling the PDF, SVG, preview, and printable HTML."""
    os.makedirs(distdir, exist_ok=True)
    pdf = os.path.join(lang_dir, "wheel.pdf")
    shutil.copyfile(pdf, os.path.join(distdir, f"{PROJECT}-{lang}.pdf"))
    zip_path = os.path.join(distdir, f"{PROJECT}-{lang}.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in ("wheel.pdf", "wheel.svg", "wheel-preview.png", "index.html"):
            src = os.path.join(lang_dir, name)
            if os.path.exists(src):
                z.write(src, f"{PROJECT}-{lang}/{name}")
    return zip_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("langs", nargs="*", default=list(LANGUAGES))
    ap.add_argument("--outdir", default=os.path.join(HERE, "out"))
    ap.add_argument("--no-pdf", action="store_true", help="skip Chrome PDF/preview")
    ap.add_argument("--package", metavar="DIR", nargs="?", const=os.path.join(HERE, "dist"),
                    help="also write per-language downloadables to DIR (default: dist/)")
    args = ap.parse_args()

    chrome = None if args.no_pdf else find_chrome()
    if not args.no_pdf and not chrome:
        print("! Chrome not found — writing SVG/HTML only (open index.html to print).")
    if args.package and not chrome:
        ap.error("--package needs Chrome to render the PDFs")

    for code in (args.langs or list(LANGUAGES)):
        generate_svg(code, args.outdir)
        generate_html(code, args.outdir)
        lang_dir = os.path.join(args.outdir, code)
        line = f"✓ {code} ({LANGUAGES[code]['name']}): {lang_dir}/index.html"
        if chrome:
            render_chrome(chrome, lang_dir)
            line += "  + wheel.pdf"
        if args.package:
            package(code, lang_dir, args.package)
            line += f"  + {PROJECT}-{code}.zip"
        print(line)


if __name__ == "__main__":
    main()
