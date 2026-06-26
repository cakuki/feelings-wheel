"""Print-layout tests: the wheel must be horizontally centered and fit the page.

Two layers:

* test_svg_viewbox_centered_and_square — fast, no browser. Guards the SVG-side
  invariant: the viewBox is a square centered on the wheel's center, so the
  drawing sits in the middle of its own canvas for every tier.

* test_rendered_pages_centered_and_fit — the real thing. Renders each tier's
  print HTML in headless Chrome (the same tool the build uses for the PDF),
  screenshots it at A4 proportions, and measures where the colored wheel
  actually lands. Catches the bugs a text/size check can't: a wheel rendered
  left-aligned, or one wider than the page. Skipped if Chrome isn't installed.

The PDF and this screenshot come from the very same HTML + CSS, so a wheel that
is centered and fits here is centered and fits in the printed PDF.
"""
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gen_wheel import generate_svg, build_svg, TIERS, CX, CY  # noqa: E402
from build_html import generate_html  # noqa: E402
from build import find_chrome  # noqa: E402
from tests.png import load_png  # noqa: E402

# A4 portrait at 96dpi, with headroom so the wheel is inside the screenshot.
PAGE_W, PAGE_H = 800, 1180
LANG = "en"


def _saturation(r, g, b):
    return max(r, g, b) - min(r, g, b)


def colored_bbox(width, height, channels, raw, thresh=45):
    """Bounding box of the strongly-colored pixels — i.e. the wheel's wedges,
    ignoring the cream background, white page, and gray text."""
    minx, miny, maxx, maxy = width, height, -1, -1
    for y in range(0, height, 2):            # step 2: plenty for a bbox, ~4x faster
        row = y * width * channels
        for x in range(0, width, 2):
            i = row + x * channels
            if _saturation(raw[i], raw[i + 1], raw[i + 2]) > thresh:
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y
    if maxx < 0:
        return None
    return minx, miny, maxx, maxy


class TestSvgGeometry(unittest.TestCase):
    def test_svg_viewbox_centered_and_square(self):
        import re
        for tier in TIERS:
            svg = build_svg(LANG, tier)
            m = re.search(r'viewBox="([\d.\- ]+)"', svg)
            self.assertIsNotNone(m, f"tier {tier}: no viewBox")
            x, y, w, h = (float(v) for v in m.group(1).split())
            self.assertAlmostEqual(w, h, msg=f"tier {tier}: viewBox not square")
            # The viewBox must be centered on the wheel's center (CX, CY); an
            # off-center crop is exactly what makes a wheel look left-aligned.
            self.assertAlmostEqual(x + w / 2, CX, delta=0.6,
                                   msg=f"tier {tier}: viewBox not centered on CX")
            self.assertAlmostEqual(y + h / 2, CY, delta=0.6,
                                   msg=f"tier {tier}: viewBox not centered on CY")


@unittest.skipIf(find_chrome() is None, "Chrome not installed; skipping render test")
class TestRenderedLayout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chrome = find_chrome()
        cls.tmp = tempfile.mkdtemp(prefix="fw-layout-")
        for tier in TIERS:
            generate_svg(LANG, tier, cls.tmp)
            generate_html(LANG, tier, cls.tmp)

    def _screenshot(self, tier):
        from gen_wheel import TIER_DIR
        html = os.path.join(self.tmp, LANG, TIER_DIR[tier], "index.html")
        png = os.path.join(self.tmp, f"page-{tier}.png")
        subprocess.run(
            [self.chrome, "--headless", "--disable-gpu", "--no-sandbox",
             "--hide-scrollbars", f"--window-size={PAGE_W},{PAGE_H}",
             f"--screenshot={png}", f"file://{html}"],
            check=True, capture_output=True)
        return png

    def test_rendered_pages_centered_and_fit(self):
        for tier in TIERS:
            with self.subTest(tier=tier):
                w, h, ch, raw = load_png(self._screenshot(tier))
                box = colored_bbox(w, h, ch, raw)
                self.assertIsNotNone(box, f"tier {tier}: no wheel found in render")
                minx, _, maxx, _ = box
                center = (minx + maxx) / 2
                page_center = w / 2

                # Horizontally centered (catches the left-aligned 1-ring bug).
                self.assertLess(
                    abs(center - page_center), w * 0.02,
                    f"tier {tier}: wheel off-center "
                    f"(center {center:.0f}px vs page {page_center:.0f}px)")

                # Fits the page with a real margin on both sides (catches the
                # 3-ring overflow, which clips at the window edge).
                self.assertGreater(minx, w * 0.03,
                                   f"tier {tier}: wheel touches/overflows left edge")
                self.assertLess(maxx, w * 0.97,
                                f"tier {tier}: wheel touches/overflows right edge")


if __name__ == "__main__":
    unittest.main(verbosity=2)
