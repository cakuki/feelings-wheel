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
        # Normalize the [[emotion]] tables into the (name, [feelings]) shape the
        # rest of the code expects.
        data["cores"] = [(e["core"], e["feelings"]) for e in data["emotion"]]
        langs[code] = data
    return langs


LANGUAGES = _load()


def core_data(lang_code):
    """Return [(name, color, [feelings]), ...] for a language, with shared colors."""
    lang = LANGUAGES[lang_code]
    return [(name, PALETTE[i], feels) for i, (name, feels) in enumerate(lang["cores"])]
