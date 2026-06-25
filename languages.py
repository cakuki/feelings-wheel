#!/usr/bin/env python3
"""Load language content from the per-language TOML files in languages/.

Each languages/<code>.toml holds one translation (see any existing file for the
shape). The 6 core emotions share one PALETTE (index aligns with each file's
emotion order). To add a language, drop in a new TOML file — no code changes.
"""
import os
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
LANG_DIR = os.path.join(HERE, "languages")

# Shared, in canonical order: Happy, Surprised, Angry, Scared, Sad, Calm.
PALETTE = ["#F4C430", "#E8833A", "#DB504A", "#9B6FB0", "#4F8FCB", "#56B27E"]


def _load():
    langs = {}
    for fn in sorted(os.listdir(LANG_DIR)):
        if not fn.endswith(".toml"):
            continue
        code = fn[:-len(".toml")]
        with open(os.path.join(LANG_DIR, fn), "rb") as f:
            data = tomllib.load(f)
        # Normalize the [[emotion]] tables into the shapes the rest of the code
        # expects. `leaves` (ring 3) is optional: a list of one [a, b] pair per
        # ring-2 feeling, so 6 cores x 4 feelings x 2 = 48 finest-grained words.
        data["cores"] = [(e["core"], e["feelings"]) for e in data["emotion"]]
        data["leaves_by_core"] = [e.get("leaves") for e in data["emotion"]]
        langs[code] = data
    return langs


LANGUAGES = _load()


def core_data(lang_code):
    """Return [(name, color, [feelings]), ...] for a language, with shared colors."""
    lang = LANGUAGES[lang_code]
    return [(name, PALETTE[i], feels) for i, (name, feels) in enumerate(lang["cores"])]


def leaf_data(lang_code):
    """Return [(color, [[a, b], ...]), ...] — the ring-3 leaf pairs per core.

    One inner list per core (same order/color as core_data), each holding 4
    [a, b] pairs aligned to that core's 4 ring-2 feelings. Returns None per core
    when the language hasn't supplied leaves yet.
    """
    lang = LANGUAGES[lang_code]
    return [(PALETTE[i], leaves) for i, leaves in enumerate(lang["leaves_by_core"])]


def has_leaves(lang_code):
    """True only if every core in the language has its ring-3 leaves filled in."""
    return all(lv for lv in LANGUAGES[lang_code]["leaves_by_core"])


def site(lang_code):
    """The [site] table of UI strings for the landing page (falls back to en)."""
    return LANGUAGES[lang_code].get("site", LANGUAGES["en"].get("site", {}))
