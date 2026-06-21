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

Then produce a print-ready A4 PDF (and an optional preview image):

```sh
# PDF via headless Chrome
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="duygu-carki.pdf" "file://$PWD/duygu-carki.html"

# PNG preview of just the wheel (needs librsvg: `brew install librsvg`)
rsvg-convert -w 900 duygu-carki.svg -o wheel-preview.png
```

## Customizing

All content lives at the top of `gen_wheel.py` in the `DATA` list —
edit the core emotions, their colors, or the four nuanced feelings under each.
`build_html.py` controls the page layout, the how-to text, and the 31-day tracker.

## Why not just download it from Scribd?

This started as a request to grab a paywalled, poorly-rated Scribd upload of a
generic feeling wheel. Generating our own gives a nicer, fully-editable result
we own and can reprint forever.
