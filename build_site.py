#!/usr/bin/env python3
"""Generate the GitHub Pages landing page (docs/index.html) from languages.py.

The page starts with a language picker and 3 age bands (1/2/3-ring wheels).
Picking a language translates everything below the hero into that language and
points the downloads at the matching per-tier release assets. It always links to
the *latest* GitHub release, so it never goes stale.

Re-run after adding a language or rebuilding previews:  python3 build_site.py
(also copies out/<lang>/<tier>ring/wheel-preview.png into docs/img/)
"""
import json
import os
import shutil

from languages import LANGUAGES, site
from gen_wheel import TIERS, TIER_DIR

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "https://github.com/cakuki/feelings-wheel"
LATEST = f"{REPO}/releases/latest/download"

# Display order (English first) + a flag per language.
ORDER = ["en", "de", "es", "fr", "tr"]
FLAGS = {"en": "🇬🇧", "de": "🇩🇪", "es": "🇪🇸", "fr": "🇫🇷", "tr": "🇹🇷"}


def langs_in_order():
    return [c for c in ORDER if c in LANGUAGES] + \
           [c for c in LANGUAGES if c not in ORDER]


def copy_previews():
    """Copy the per-tier preview PNGs the build produced into docs/img/."""
    imgdir = os.path.join(HERE, "docs", "img")
    os.makedirs(imgdir, exist_ok=True)
    copied = 0
    for code in langs_in_order():
        for tier in TIERS:
            src = os.path.join(HERE, "out", code, TIER_DIR[tier], "wheel-preview.png")
            if os.path.exists(src):
                shutil.copyfile(src, os.path.join(imgdir, f"wheel-{code}-{tier}ring.png"))
                copied += 1
    return copied


def band_card(tier):
    """One age-band card. Initial text is English; JS swaps it per language."""
    s = site("en")
    return f"""\
      <article class="card">
        <div class="band">
          <span class="age" data-i18n="band{tier}_age">{s[f'band{tier}_age']}</span>
          <h3 data-i18n="band{tier}_name">{s[f'band{tier}_name']}</h3>
        </div>
        <a class="thumb" id="thumb{tier}" href="{LATEST}/feelings-wheel-en-{tier}ring.pdf">
          <img id="img{tier}" src="img/wheel-en-{tier}ring.png" loading="lazy"
               alt="{tier}-ring feelings wheel preview">
        </a>
        <p class="desc" data-i18n="band{tier}_desc">{s[f'band{tier}_desc']}</p>
        <div class="actions">
          <a class="btn" id="pdf{tier}" href="{LATEST}/feelings-wheel-en-{tier}ring.pdf"
             data-i18n="download_pdf">{s['download_pdf']}</a>
          <a class="btn ghost" id="zip{tier}" href="{LATEST}/feelings-wheel-en-{tier}ring.zip"
             data-i18n="download_zip">{s['download_zip']}</a>
        </div>
      </article>"""


def build_html():
    codes = langs_in_order()
    i18n = {c: site(c) for c in codes}
    langs = [{"code": c, "name": LANGUAGES[c]["name"], "flag": FLAGS.get(c, "🏳️")}
             for c in codes]
    s = site("en")
    options = "\n".join(
        f'        <option value="{c}">{FLAGS.get(c, "")} {LANGUAGES[c]["name"]}</option>'
        for c in codes)
    cards = "\n".join(band_card(t) for t in TIERS)
    flagbar = " ".join(FLAGS.get(c, "") for c in codes)

    tmpl = TEMPLATE
    repl = {
        "__REPO__": REPO,
        "__LATEST__": LATEST,
        "__COUNT__": str(len(codes)),
        "__FLAGBAR__": flagbar,
        "__OPTIONS__": options,
        "__CARDS__": cards,
        "__JSON_I18N__": json.dumps(i18n, ensure_ascii=False),
        "__JSON_LANGS__": json.dumps(langs, ensure_ascii=False),
        "__PICK_LANGUAGE__": s["pick_language"],
        "__PICK_AGE__": s["pick_age"],
        "__PRINT_HINT__": s["print_hint"],
        "__HOW_TITLE__": s["how_title"],
        "__HOW1__": s["how1"], "__HOW2__": s["how2"],
        "__HOW3__": s["how3"], "__HOW4__": s["how4"],
        "__OSS_TITLE__": s["oss_title"], "__OSS_BODY__": s["oss_body"],
        "__BTN_GITHUB__": s["btn_github"], "__BTN_CONTRIBUTE__": s["btn_contribute"],
        "__BTN_IDEAS__": s["btn_ideas"],
        "__FOOTER_MADE__": s["footer_made"], "__FOOTER_LATEST__": s["footer_latest"],
    }
    for k, v in repl.items():
        tmpl = tmpl.replace(k, v)
    return tmpl


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Feelings Wheel — free printable emotion wheel for kids</title>
  <meta name="description" content="A free, printable feelings wheel and monthly
  emotion tracker to help kids name what they feel. Pick your language and your
  child's age, and download a ready-to-print PDF.">
  <meta property="og:title" content="Feelings Wheel 🎡">
  <meta property="og:description" content="Free printable feelings wheel for kids,
  in __COUNT__ languages and 3 age levels.">
  <meta property="og:type" content="website">
  <meta property="og:image" content="img/wheel-en-2ring.png">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🎡</text></svg>">
  <style>
    :root {
      --bg: #FFFDF7; --ink: #2b2b2b; --muted: #6b6256; --line: #e7e0cf;
      --accent: #4F8FCB; --accent-ink: #fff; --card: #fff;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0; background: var(--bg); color: var(--ink);
      font-family: 'Nunito', -apple-system, 'Segoe UI', system-ui, sans-serif;
      line-height: 1.6;
    }
    a { color: var(--accent); }
    .wrap { max-width: 1000px; margin: 0 auto; padding: 0 20px; }
    header { text-align: center; padding: 56px 20px 8px; }
    h1 { font-size: clamp(2rem, 6vw, 3rem); margin: 0 0 8px; font-weight: 800; }
    .tagline { font-size: 1.15rem; color: var(--muted); max-width: 40ch;
               margin: 0 auto 6px; }
    .langbar { font-size: 1.4rem; letter-spacing: 4px; margin: 14px 0 0; }
    main { padding: 16px 0 8px; }
    .picker { text-align: center; margin: 18px auto 8px; }
    .picker label { font-weight: 800; font-size: 1.1rem; margin-right: 8px; }
    .picker select {
      font: inherit; font-weight: 700; padding: 10px 14px; border-radius: 12px;
      border: 2px solid var(--line); background: #fff; color: var(--ink); cursor: pointer;
    }
    h2.section { text-align: center; margin: 26px 0 6px; font-size: 1.5rem; }
    .grid { display: grid; gap: 22px; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }
    .card { background: var(--card); border: 1px solid var(--line); border-radius: 18px;
            padding: 16px; text-align: center; box-shadow: 0 2px 10px rgba(120,100,60,.06);
            display: flex; flex-direction: column; }
    .band .age { display: inline-block; background: #f3edda; color: var(--muted);
                 font-weight: 800; font-size: .85rem; padding: 3px 10px; border-radius: 999px; }
    .card h3 { margin: 8px 0 10px; font-size: 1.3rem; }
    .thumb { display: block; border-radius: 12px; overflow: hidden; background: #FFFDF7; }
    .thumb img { width: 100%; height: auto; display: block; aspect-ratio: 1 / 1;
                 object-fit: contain; }
    .desc { font-size: .95rem; color: var(--muted); margin: 12px 4px; flex: 1; }
    .actions { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; }
    .btn { display: inline-block; background: var(--accent); color: var(--accent-ink);
           text-decoration: none; font-weight: 700; padding: 10px 16px; border-radius: 999px;
           border: 2px solid var(--accent); }
    .btn.ghost { background: transparent; color: var(--accent); }
    .btn:hover { filter: brightness(1.05); }
    a:focus-visible, .thumb:focus-visible, select:focus-visible {
      outline: 3px solid #f0a; outline-offset: 3px; }
    .hint { text-align: center; color: var(--muted); font-size: .95rem; margin: 16px auto; max-width: 60ch; }
    .how { margin: 30px auto; max-width: 62ch; background: #fff; border: 1px solid var(--line);
           border-radius: 18px; padding: 8px 28px; }
    .how ol { padding-left: 1.2em; }
    .contribute { text-align: center; margin: 40px 0; }
    .contribute .btn { margin: 6px; }
    footer { text-align: center; color: var(--muted); padding: 30px 20px 50px;
             border-top: 1px solid var(--line); margin-top: 30px; font-size: .95rem; }
    @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <h1>Feelings Wheel 🎡</h1>
      <p class="tagline">A free, printable wheel that helps kids name what they
      feel — in their own language, at their own age.</p>
      <p class="langbar" aria-hidden="true">__FLAGBAR__</p>
    </div>
  </header>

  <main class="wrap">
    <div class="picker">
      <label for="lang" data-i18n="pick_language">__PICK_LANGUAGE__</label>
      <select id="lang" aria-label="Choose your language">
__OPTIONS__
      </select>
    </div>

    <h2 class="section" data-i18n="pick_age">__PICK_AGE__</h2>
    <section class="grid" aria-label="Download by age">
__CARDS__
    </section>

    <p class="hint" data-i18n="print_hint">__PRINT_HINT__</p>

    <section class="how" aria-labelledby="how-title">
      <h2 id="how-title" data-i18n="how_title">__HOW_TITLE__</h2>
      <ol>
        <li data-i18n="how1">__HOW1__</li>
        <li data-i18n="how2">__HOW2__</li>
        <li data-i18n="how3">__HOW3__</li>
        <li data-i18n="how4">__HOW4__</li>
      </ol>
    </section>

    <section class="contribute" aria-labelledby="contribute-title">
      <h2 id="contribute-title" data-i18n="oss_title">__OSS_TITLE__</h2>
      <p data-i18n="oss_body">__OSS_BODY__</p>
      <a class="btn" href="__REPO__" data-i18n="btn_github">__BTN_GITHUB__</a>
      <a class="btn ghost" href="__REPO__/blob/main/CONTRIBUTING.md" data-i18n="btn_contribute">__BTN_CONTRIBUTE__</a>
      <a class="btn ghost" href="__REPO__/issues" data-i18n="btn_ideas">__BTN_IDEAS__</a>
    </section>
  </main>

  <footer>
    <p><span data-i18n="footer_made">__FOOTER_MADE__</span> ·
       <a href="__REPO__">cakuki/feelings-wheel</a> ·
       <a href="__REPO__/blob/main/LICENSE">MIT</a></p>
    <p data-i18n="footer_latest">__FOOTER_LATEST__</p>
  </footer>

  <script>
    const I18N = __JSON_I18N__;
    const LANGS = __JSON_LANGS__;
    const LATEST = "__LATEST__";
    const TIERS = [1, 2, 3];

    function apply(code) {
      const t = I18N[code] || I18N.en;
      const name = (LANGS.find(l => l.code === code) || {}).name || code;
      document.documentElement.lang = code;
      document.querySelectorAll('[data-i18n]').forEach(el => {
        const k = el.getAttribute('data-i18n');
        if (t[k] != null) el.innerHTML = t[k];
      });
      TIERS.forEach(tier => {
        const pdf = `${LATEST}/feelings-wheel-${code}-${tier}ring.pdf`;
        const zip = `${LATEST}/feelings-wheel-${code}-${tier}ring.zip`;
        document.getElementById('pdf' + tier).href = pdf;
        document.getElementById('zip' + tier).href = zip;
        document.getElementById('thumb' + tier).href = pdf;
        const img = document.getElementById('img' + tier);
        img.src = `img/wheel-${code}-${tier}ring.png`;
        img.alt = `${tier}-ring feelings wheel in ${name}`;
      });
    }

    const sel = document.getElementById('lang');
    sel.addEventListener('change', e => apply(e.target.value));

    // Default to the visitor's browser language when we have it.
    const guess = (navigator.language || 'en').slice(0, 2).toLowerCase();
    const start = I18N[guess] ? guess : 'en';
    sel.value = start;
    apply(start);
  </script>
</body>
</html>
"""


def main():
    docs = os.path.join(HERE, "docs")
    os.makedirs(docs, exist_ok=True)
    n = copy_previews()
    path = os.path.join(docs, "index.html")
    with open(path, "w") as f:
        f.write(build_html())
    print(f"Site written: {path}  ({n} preview images)")


if __name__ == "__main__":
    main()
