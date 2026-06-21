# Duygu Çarkı 🎡

A printable Turkish **feeling wheel** (duygu çarkı) and matching monthly
**emotion tracker** (duygu takvimi), tuned for a 9–12 year old: 6 core emotions,
each surrounded by 4 nuanced feelings to grow emotional vocabulary.

## Regenerate the outputs

The PDF/SVG/HTML are **not** tracked in git — they're reproducible from these
two scripts. To rebuild everything:

```sh
python3 gen_wheel.py     # -> duygu-carki.svg
python3 build_html.py     # -> duygu-carki.html  (embeds the SVG, adds page 2)
```

Then produce a print-ready A4 PDF and a preview image — **both via Chrome**.
The core labels use SVG `<textPath>` (curved text), which `librsvg`/`rsvg-convert`
does **not** render, so don't use it for previews; Chrome (the PDF engine) does.

```sh
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# print-ready A4 PDF
"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="duygu-carki.pdf" "file://$PWD/duygu-carki.html"

# PNG preview of the wheel
"$CHROME" --headless --disable-gpu --window-size=700,720 \
  --screenshot="wheel-preview.png" "file://$PWD/duygu-carki.svg"
```

## Checking that labels fit (the feedback loop)

Guessing font sizes and squinting at the PNG is an open loop. `fit_check.js`
closes it: it reads the **real rendered geometry** of every label and reports any
that cross out of the ring (or circle) it belongs to.

1. Open `duygu-carki.html` in a browser.
2. In the DevTools console, paste `fit_check.js` and run `fitCheck()`
   (or run the same function via the Chrome DevTools MCP `evaluate_script`).
3. `{ ok: true, fails: [] }` means every label fits. Otherwise `fails` lists each
   offender: curved core labels report `padEach` (clear space to each divider;
   must be ≥ `CORE_PAD`), outer labels report `innerGap`/`outerGap`, and the center
   prompt reports `slack`. Adjust the relevant size in `gen_wheel.py` and re-run.

The six core labels are **curved along the arc** (`<textPath>`) at one uniform
size, `CORE_FONT`, picked so the longest word (*Korkmuş*) fills its wedge while
keeping `CORE_PAD` px of clear space from the dividers. Outer labels stay radial
and shrink by length.

## Customizing

All content lives at the top of `gen_wheel.py` in the `DATA` list —
edit the core emotions, their colors, or the four nuanced feelings under each.
`build_html.py` controls the page layout, the how-to text, and the 31-day tracker.

## Why not just download it from Scribd?

This started as a request to grab a paywalled, poorly-rated Scribd upload of a
generic feeling wheel. Generating our own gives a nicer, fully-editable result
we own and can reprint forever.
