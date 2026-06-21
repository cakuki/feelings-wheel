# Contributing

Thanks for helping more kids name their feelings! 💛

The most valuable contribution is **a new language**. You don't need to touch
the geometry or layout code — everything translatable lives in `languages.py`.

## Add a language

1. Copy an existing entry in `languages.py` (e.g. `"en"`) and translate it.
   Keep the 6 core emotions in the canonical order (Happy, Surprised, Angry,
   Scared, Sad, Calm) so they line up with the shared `PALETTE`.
   - Prefer short, child-friendly **single words** for the 6 core emotions —
     they're curved inside a ring and long words have to shrink.
   - Give each core emotion 4 nuanced feelings for the outer ring.
2. Build it:
   ```sh
   python3 build.py xx           # your language code
   ```
3. **Verify the labels fit.** Open `out/xx/index.html` in a browser, open the
   DevTools console, paste `fit_check.js`, and run `fitCheck()`. You want
   `{ ok: true, fails: [] }`. If a core label fails, lower that language's
   `core_font` in `languages.py` and rebuild. (See the README for details.)
4. Open a pull request. CI builds every language; a release is cut when a
   maintainer pushes a version tag.

## Translation quality

These wheels are used with children, so natural, warm, age-appropriate wording
matters more than literal accuracy. Native-speaker review is very welcome —
if you spot an awkward term in an existing language, a PR fixing it is great.

## Code style

Pure Python standard library, no dependencies. Keep it that way if you can.
