# Contributing

Thanks for helping more kids name their feelings! 💛

The most valuable contribution is **a new language**. You don't need to touch
any code — every translation is a single [TOML](https://toml.io) file in
[`languages/`](languages/).

## Add a language

1. Copy an existing file in `languages/` (e.g. `languages/en.toml`) to
   `languages/<code>.toml` (use the [ISO 639-1 code](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes),
   e.g. `it`, `pt`, `nl`) and translate the values. Keep the keys, and keep the
   6 emotions in the canonical order (Happy, Surprised, Angry, Scared, Sad, Calm)
   so they line up with the shared colors.
   - Prefer short, child-friendly **single words** for the 6 core emotions —
     they're curved inside a ring and long words have to shrink.
   - Give each core emotion 4 nuanced feelings (`feelings`) for ring 2, and one
     `[a, b]` pair of short fine-grained feelings per ring-2 feeling (`leaves`)
     for ring 3 — 48 leaves in all. Keep leaves to short single words.
   - Translate the `[site]` block too — that's the landing-page text shown when a
     visitor picks your language.
   - The comments in the file explain each field.
2. Build it (all three age tiers):
   ```sh
   python3 build.py xx           # your language code
   ```
3. **Verify the labels fit.** Open `out/xx/3ring/index.html` in a browser (the
   3-ring sheet is the tightest), open the DevTools console, paste `fit_check.js`,
   and run `fitCheck()`. You want `{ ok: true, fails: [] }`. If a core label
   fails, lower that language's `core_font` in its `.toml` and rebuild. (See the
   README for details.)
4. Regenerate the landing page so your language gets a download card:
   ```sh
   python3 build_site.py        # updates docs/index.html
   ```
   (Add a flag for your code in `build_site.py`'s `FLAGS`/`ORDER`.)
5. Open a pull request. CI builds every language; a release is cut when a
   maintainer pushes a version tag.

## Translation quality

These wheels are used with children, so natural, warm, age-appropriate wording
matters more than literal accuracy. Native-speaker review is very welcome —
if you spot an awkward term in an existing language, a PR fixing it is great.

## Code style

Pure Python standard library, no dependencies. Keep it that way if you can.
