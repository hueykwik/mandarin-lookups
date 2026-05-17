"""
HSK / TOCFL lookups with Traditional ↔ Simplified normalization.

Used by both ~/code/mandarin-tools/mandarin_brief.py and
mandarin_study_guide.py to inject authoritative level data into prompts
instead of letting the model guess.

Data sources (all in ~/code/zhongwen/data/):
  - hsk_levels.json   — HSK 2.0 (2010 Hanban), 4,993 words, levels 1–6
  - hsk3_levels.json  — HSK 3.0 (2021), 11,092 words across bands 1–6 and 7-9
  - tocfl_levels.json — Taiwan TOCFL, 14,736 words, ints 1–6 (A1–C2)
  - cedict_ts.u8      — CC-CEDICT, used only to build a TC↔SC map
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

_DATA_DIR = Path(__file__).parent / "data"

_TOCFL_LABEL = {1: "A1", 2: "A2", 3: "B1", 4: "B2", 5: "C1", 6: "C2"}
# Level 7 in tocfl_levels.json is a noisy overflow bucket (5k+ entries
# including common A2–B1 words). Treat as unlabeled rather than misreport.


def _load_json(name: str) -> dict:
    p = _DATA_DIR / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


@lru_cache(maxsize=1)
def _hsk2() -> dict[str, int]:
    return _load_json("hsk_levels.json")


@lru_cache(maxsize=1)
def _hsk3() -> dict[str, str]:
    return _load_json("hsk3_levels.json")


@lru_cache(maxsize=1)
def _tocfl() -> dict[str, int]:
    return _load_json("tocfl_levels.json")


@lru_cache(maxsize=1)
def _script_map() -> tuple[dict[str, str], dict[str, str]]:
    """
    Return (trad_to_simp, simp_to_trad) built from CC-CEDICT.
    Each CEDICT line: `TRAD SIMP [pinyin] /defs/`.
    """
    trad_to_simp: dict[str, str] = {}
    simp_to_trad: dict[str, str] = {}
    cedict = _DATA_DIR / "cedict_ts.u8"
    if not cedict.exists():
        return {}, {}
    with cedict.open(encoding="utf-8") as fh:
        for line in fh:
            if not line or line.startswith("#"):
                continue
            parts = line.split(" ", 2)
            if len(parts) < 2:
                continue
            trad, simp = parts[0], parts[1]
            # First mapping wins — CEDICT lists more common forms first.
            trad_to_simp.setdefault(trad, simp)
            simp_to_trad.setdefault(simp, trad)
    return trad_to_simp, simp_to_trad


def _candidates(word: str) -> list[str]:
    """Return [word, alternate-script form] without duplicates."""
    t2s, s2t = _script_map()
    forms = [word]
    if word in t2s and t2s[word] not in forms:
        forms.append(t2s[word])
    if word in s2t and s2t[word] not in forms:
        forms.append(s2t[word])
    return forms


def lookup(word: str) -> dict:
    """
    Return {hsk2: int|None, hsk3: str|None, tocfl: str|None} for *word*.
    Tries Traditional and Simplified forms via CEDICT before giving up.
    """
    hsk2 = hsk3 = tocfl_band = None
    for form in _candidates(word):
        if hsk2 is None:
            hsk2 = _hsk2().get(form)
        if hsk3 is None:
            hsk3 = _hsk3().get(form)
        if tocfl_band is None:
            tocfl_band = _tocfl().get(form)
        if hsk2 and hsk3 and tocfl_band:
            break
    return {
        "hsk2": hsk2,
        "hsk3": hsk3,
        "tocfl": _TOCFL_LABEL.get(tocfl_band) if tocfl_band else None,
    }


def lookup_many(words) -> dict[str, dict]:
    """Batch convenience — returns {word: lookup(word)} preserving input order."""
    return {w: lookup(w) for w in dict.fromkeys(words)}


# ---------------------------------------------------------------------------
# Text scan
# ---------------------------------------------------------------------------

import re as _re

# Runs of contiguous CJK characters (no spaces — Chinese has none anyway).
_CJK_RUN_RE = _re.compile(r"[㐀-鿿]+")
_MAX_WORD_LEN = 4


def find_words_with_levels(text: str) -> list[tuple[str, dict]]:
    """
    Scan *text* for 2-to-4 character substrings that have a hit in HSK 3.0
    or TOCFL. Greedy longest-match: at each starting position, try length 4,
    then 3, then 2; first hit wins and we advance past it. This avoids
    emitting both 政策 and 政策性 when only one is in the dicts.

    Returns [(word, lookup_info), …] in first-seen order, deduplicated.
    """
    seen: dict[str, dict] = {}
    out: list[tuple[str, dict]] = []
    for run in _CJK_RUN_RE.findall(text):
        i = 0
        while i < len(run):
            advanced = False
            for L in range(min(_MAX_WORD_LEN, len(run) - i), 1, -1):
                w = run[i : i + L]
                if w in seen:
                    i += L
                    advanced = True
                    break
                info = lookup(w)
                if info["hsk3"] is not None or info["tocfl"] is not None:
                    seen[w] = info
                    out.append((w, info))
                    i += L
                    advanced = True
                    break
            if not advanced:
                i += 1
    return out


# ---------------------------------------------------------------------------
# Prompt helper
# ---------------------------------------------------------------------------

def format_lookup_table(text: str) -> str:
    """
    Scan *text* and return a Markdown table of HSK 3.0 + TOCFL levels for
    every matching word. Returns "" if nothing hits.
    """
    rows = [
        f"| {w} | {info['hsk3'] or '—'} | {info['tocfl'] or '—'} |"
        for w, info in find_words_with_levels(text)
    ]
    if not rows:
        return ""
    return "\n".join(["| Word | HSK 3.0 | TOCFL |", "|------|---------|-------|", *rows])


if __name__ == "__main__":
    # Smoke test
    sample = (
        "[0:00] 今天我們來討論台灣的政府政策。\n"
        "[0:15] 持續發展是很重要的議題。\n"
        "[0:30] 我希望能夠釐清這個概念。\n"
        "[0:45] 做生意需要繁體字和簡體字都會。"
    )
    print(format_lookup_table(sample))
