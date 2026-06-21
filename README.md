# Feelings Wheel 🎡 (Duygu Çarkı / Gefühlsrad)

A printable, **multi-language** feeling wheel and matching monthly emotion
tracker, tuned for a 9–12 year old: 6 core emotions, each surrounded by 4 nuanced
feelings to grow emotional vocabulary. Ships with **English, German, and Turkish**.

## Build

Everything is generated into `out/<lang>/` and is reproducible — only the
generators are tracked in git (see Layout). Build with one command:

```sh
python3 build.py            # all languages
python3 build.py en de       # only these
python3 build.py --no-pdf    # SVG + HTML only (skip Chrome PDF/preview)
```

Each language produces `out/<lang>/`:
`wheel.svg`, `index.html`, `wheel.pdf` (print-ready A4), `wheel-preview.png`.

The PDF and preview are rendered with **Chrome** (auto-detected). The core labels
use SVG `<textPath>` (curved text), which `librsvg`/`rsvg-convert` does **not**
render — so previews go through Chrome too, the same engine that makes the PDF.

To print: open `out/<lang>/index.html` in a browser and Print → Save as PDF, or
just use the generated `wheel.pdf`.

## Adding or editing a language

All translatable content lives in `languages.py`:

- `PALETTE` — the 6 shared core colors (order: Happy, Surprised, Angry, Scared,
  Sad, Calm). Colors are the same across languages.
- `LANGUAGES["xx"]` — one entry per language with the 6 core names + their 4
  feelings, plus all UI strings (title, subtitle, center prompt, how-to, calendar).
- `core_font` — the uniform curved-label size for that language, chosen so its
  longest core word fills the wedge with `CORE_PAD` px of clearance. Tune it with
  the fit-check loop below (German needed 17, English 20, Turkish 21).

The layout/geometry code (`gen_wheel.py`, `build_html.py`) is language-agnostic.

## Checking that labels fit (the feedback loop)

Guessing font sizes and squinting at a PNG is an open loop. `fit_check.js` closes
it: it reads the **real rendered geometry** of every label and reports any that
cross out of the ring (or circle) it belongs to.

1. Open `out/<lang>/index.html` in a browser.
2. In the DevTools console, paste `fit_check.js` and run `fitCheck()`
   (or run the same function via the Chrome DevTools MCP `evaluate_script`).
3. `{ ok: true, fails: [] }` means every label fits. Otherwise `fails` lists each
   offender: curved core labels report `padEach` (clear space to each divider;
   must be ≥ `CORE_PAD`), outer labels report `innerGap`/`outerGap`, the center
   prompt reports `slack`. Adjust `core_font` in `languages.py` (or wedge geometry
   in `gen_wheel.py`) and rebuild. **Run this for every language after edits.**

The six core labels are curved along the arc (`<textPath>`), flipping on the
bottom half so they stay upright. Outer labels stay radial and shrink by length.

## Layout

| File | Role | Tracked |
|------|------|---------|
| `languages.py` | all per-language content + shared palette | ✅ |
| `gen_wheel.py` | builds the wheel SVG (geometry) | ✅ |
| `build_html.py` | wraps SVG in A4 HTML + monthly tracker | ✅ |
| `build.py` | orchestrates SVG→HTML→PDF/preview per language | ✅ |
| `fit_check.js` | browser-measured label-fit check | ✅ |
| `out/<lang>/…` | generated svg/html/pdf/png | ❌ (`out/.gitignore`) |

## Why not just download it from Scribd?

This started as a request to grab a paywalled, poorly-rated Scribd upload of a
generic feeling wheel. Generating our own gives a nicer, fully-editable,
multi-language result we own and can reprint forever.
