# Feelings Wheel 🎡

A free, printable **feelings wheel** and matching **monthly emotion tracker**
to help kids name what they feel — in their own language.

Six core emotions in the middle, each surrounded by four more nuanced feelings,
so a child can move from "happy" to *grateful*, or "angry" to *frustrated*. Print
it, put it on the fridge, and use it together.

<p align="center">
  <img src="assets/preview-en.png" alt="English feelings wheel" width="48%">
  <img src="assets/preview-tr.png" alt="Turkish feelings wheel" width="48%">
</p>

## ⬇️ Download &amp; print

Grab your language from the [**latest release**](../../releases/latest):

- `feelings-wheel-<lang>.pdf` — ready-to-print A4 (2 pages: wheel + tracker)
- `feelings-wheel-<lang>.zip` — the same, plus SVG, preview image, and HTML

Open the PDF and print at 100% / "Actual size" on A4. That's it — no account,
no paywall, free forever.

**Available languages:** 🇬🇧 English · 🇩🇪 Deutsch · 🇪🇸 Español · 🇫🇷 Français · 🇹🇷 Türkçe

Want yours? [Adding a language](CONTRIBUTING.md) is a small, welcome PR.

## How to use it with your child

1. Find the core emotion in the middle that feels closest right now.
2. Move outward to a more specific feeling in the same color.
3. Say it out loud and talk about *when* you felt it. There's no wrong feeling.
4. On the second page, color one circle a day to see the week's mood at a glance.

## Build from source

Pure Python standard library — no dependencies. You only need **Python 3** and
**Google Chrome** (used to render the PDF and preview).

```sh
python3 build.py                 # all languages -> out/<lang>/
python3 build.py en de            # only these
python3 build.py --package        # also write release bundles to dist/
python3 build.py --no-pdf         # SVG + HTML only (skip Chrome)
```

Each language produces `out/<lang>/`: `wheel.svg`, `index.html` (print this from a
browser if you don't want the PDF step), `wheel.pdf`, and `wheel-preview.png`.

For pixel-identical output everywhere, the project pins the open-source
[**Nunito**](https://fonts.google.com/specimen/Nunito) font. Install it once so
your local build matches the released PDFs (CI does the same automatically):

```sh
# macOS
curl -fsSL -o ~/Library/Fonts/Nunito.ttf \
  "https://github.com/google/fonts/raw/main/ofl/nunito/Nunito%5Bwght%5D.ttf"
# Linux
mkdir -p ~/.fonts && curl -fsSL -o ~/.fonts/Nunito.ttf \
  "https://github.com/google/fonts/raw/main/ofl/nunito/Nunito%5Bwght%5D.ttf" && fc-cache -f
```

## How it works

| File | Role |
|------|------|
| `languages.py` | all per-language content (emotions, feelings, UI text) + shared color palette |
| `gen_wheel.py` | draws the wheel SVG (arc geometry, curved labels) |
| `build_html.py` | wraps the SVG in a print-ready A4 HTML + the monthly tracker |
| `build.py` | orchestrates SVG → HTML → PDF/preview, and packages release bundles |
| `fit_check.js` | browser-measured check that every label fits its wedge |

The six core labels are curved along the ring with SVG `<textPath>` (flipping on
the bottom half so they stay upright). Because different languages have different
word lengths, each language sets a `core_font` size so its longest word fills the
wedge without crowding the dividers.

### Keeping labels inside the lines (the feedback loop)

Rather than eyeballing font sizes, `fit_check.js` measures the **real rendered
geometry** of every label in the browser and reports anything that overflows.
Open `out/<lang>/index.html`, paste `fit_check.js` in the DevTools console, and
run `fitCheck()` — `{ ok: true, fails: [] }` means everything fits. Run it after
any change to wording or geometry.

## Releases

Pushing a `v*` tag triggers [CI](.github/workflows/release.yml) to rebuild every
language and publish a GitHub Release with the per-language downloadables
attached. Pull requests build all languages as a check.

## Credits

- Concept based on the classic emotion-wheel work of **Robert Plutchik** and
  **Gloria Willcox**.
- Typeface: [**Nunito**](https://fonts.google.com/specimen/Nunito) by Vernon
  Adams et al., under the SIL Open Font License.

## License

[MIT](LICENSE) — use it, remix it, print a thousand of them. If it helps a kid,
it's done its job. 💛
