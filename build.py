#!/usr/bin/env python3
"""Build the feelings wheel for one or more languages and ring tiers.

    python3 build.py                 # all languages, all 3 tiers
    python3 build.py en de            # only these languages
    python3 build.py --tier 2         # only the 2-ring tier
    python3 build.py --no-pdf         # skip Chrome PDF/preview
    python3 build.py --package        # also write release bundles to dist/

Outputs land in out/<lang>/<tier>ring/: wheel.svg, index.html, and (if Chrome is
found) wheel.pdf + wheel-preview.png. Everything under out/ is gitignored.
"""
import argparse
import os
import shutil
import subprocess
import zipfile

from languages import LANGUAGES
from gen_wheel import generate_svg, tier_size, TIERS, TIER_DIR
from build_html import generate_html

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = "feelings-wheel"
ALIAS_TIER = 2  # the bare `feelings-wheel-<lang>.*` name points at this tier

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


def render_chrome(chrome, tier_dir, tier):
    html = os.path.join(tier_dir, "index.html")
    svg = os.path.join(tier_dir, "wheel.svg")
    size = tier_size(tier)
    # --no-sandbox is needed on most CI runners; harmless locally.
    common = [chrome, "--headless", "--disable-gpu", "--no-sandbox"]
    subprocess.run(common + ["--no-pdf-header-footer",
                   f"--print-to-pdf={os.path.join(tier_dir, 'wheel.pdf')}",
                   f"file://{html}"],
                   check=True, capture_output=True)
    subprocess.run(common + [f"--window-size={size},{size}",
                   "--force-device-scale-factor=2",
                   f"--screenshot={os.path.join(tier_dir, 'wheel-preview.png')}",
                   f"file://{svg}"],
                   check=True, capture_output=True)


def package(lang, tier, tier_dir, distdir):
    """Produce per-tier release downloadables: a standalone PDF and a zip
    bundling the PDF, SVG, preview, and printable HTML."""
    os.makedirs(distdir, exist_ok=True)
    base = f"{PROJECT}-{lang}-{tier}ring"
    pdf = os.path.join(tier_dir, "wheel.pdf")
    shutil.copyfile(pdf, os.path.join(distdir, f"{base}.pdf"))
    zip_path = os.path.join(distdir, f"{base}.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in ("wheel.pdf", "wheel.svg", "wheel-preview.png", "index.html"):
            src = os.path.join(tier_dir, name)
            if os.path.exists(src):
                z.write(src, f"{base}/{name}")
    if tier == ALIAS_TIER:  # keep old, un-suffixed links working
        shutil.copyfile(os.path.join(distdir, f"{base}.pdf"),
                        os.path.join(distdir, f"{PROJECT}-{lang}.pdf"))
        shutil.copyfile(zip_path, os.path.join(distdir, f"{PROJECT}-{lang}.zip"))
    return zip_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("langs", nargs="*", default=list(LANGUAGES))
    ap.add_argument("--tier", nargs="*", type=int, default=list(TIERS), choices=TIERS)
    ap.add_argument("--outdir", default=os.path.join(HERE, "out"))
    ap.add_argument("--no-pdf", action="store_true", help="skip Chrome PDF/preview")
    ap.add_argument("--package", metavar="DIR", nargs="?", const=os.path.join(HERE, "dist"),
                    help="also write per-tier downloadables to DIR (default: dist/)")
    args = ap.parse_args()

    chrome = None if args.no_pdf else find_chrome()
    if not args.no_pdf and not chrome:
        print("! Chrome not found — writing SVG/HTML only (open index.html to print).")
    if args.package and not chrome:
        ap.error("--package needs Chrome to render the PDFs")

    for code in (args.langs or list(LANGUAGES)):
        for tier in args.tier:
            generate_svg(code, tier, args.outdir)
            generate_html(code, tier, args.outdir)
            tier_dir = os.path.join(args.outdir, code, TIER_DIR[tier])
            line = f"✓ {code} ({LANGUAGES[code]['name']}) {TIER_DIR[tier]}: {tier_dir}/index.html"
            if chrome:
                render_chrome(chrome, tier_dir, tier)
                line += " + pdf"
            if args.package:
                package(code, tier, tier_dir, args.package)
                line += f" + {PROJECT}-{code}-{tier}ring.zip"
            print(line)


if __name__ == "__main__":
    main()
