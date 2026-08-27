"""
Canonical study-guide blueprint shared by BOTH Mandarin guides.

This lives in the mandarin-lookups repo because it is the one place reachable by
both worlds: the local listening guide (mandarin_study_guide.py) imports it, and
the cloud reading-brief routine clones this repo into its sandbox and reads it.
Edit the blueprint here once → both guides change.

The two guides differ only in their *source* (an audio transcript segment vs a
news article) and their *wrapper* (a .md file header vs an email header). Those
stay guide-specific. Everything between them — level, background, vocabulary,
grammar, the summarise-it prompt and its answer key — comes from render_spec()
below so the two outputs look like siblings.

Public API:
    render_spec(source_noun, source_quote, vocab_target, grammar_target) -> str
    annotate_synonym_levels(markdown) -> str
    NEAR_SYNONYM_RULES  (the synonym-block sub-spec, embedded in the blueprint)
"""

import re
import sys
from pathlib import Path

# Self-locating: find the sibling lookups.py whether local or in the cloud clone.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lookups import lookup  # noqa: E402


# ---------------------------------------------------------------------------
# Near-synonym discrimination sub-spec (embedded in the blueprint below).
# ---------------------------------------------------------------------------

NEAR_SYNONYM_RULES = """\
After the table, for each word give (a) the header line, (b) an example sentence
with full sentence-level pinyin, and (c) a near-synonym discrimination block.
Repeat the English definition in the header line (italics) so the reader need not
scroll back to the table:

**傳統字** (pīnyīn) — *English definition (same as the Definition column)* — HSK N · TOCFL X
> 完整中文例句。
> Wánzhěng Zhōngwén lìjù.
> Full English translation.

**近義詞 / When to use which:**
- **vs 近義詞A (pīnyīn):** how 近義詞A differs — its typical object/collocation,
  register, and scope — and when to pick it over the headword (and vice versa).
- **vs 近義詞B (pīnyīn):** …

Rules for the near-synonym block:
- Include it ONLY when the word has genuinely confusable near-synonyms a B2/C1
  learner would mix up. Skip it for proper nouns, narrow technical terms, or words
  with no real confusable synonym — do NOT force distant synonyms.
- 1–3 bullets, each contrasting ONE near-synonym. Anchor each distinction in
  something concrete: the typical object/collocation (符合標準 vs 滿足需求),
  register (formal/colloquial/written), or scope (abstract vs physical).
- Always give the synonym's pīnyīn in parentheses, e.g. 開幕 (kāimù). HSK/TOCFL
  levels for the synonyms are added automatically afterwards — do NOT add them
  yourself.
- Flag Taiwan vs Mainland preference when relevant (e.g. 運營 is CN-favoured;
  TW often says 營運). Use Traditional characters in the headwords."""


# ---------------------------------------------------------------------------
# The blueprint. __SLOTS__ are filled by render_spec via str.replace (no .format,
# so literal braces in examples are safe).
# ---------------------------------------------------------------------------

_BLUEPRINT = """\
## Level

- **Estimated level:** HSK ~N · TOCFL ~X _(estimated)_
- **What makes it hard:** one line — speed, accent, register, density of domain
  vocabulary, number of speakers, whatever actually applies to this __SOURCE__.
- **What to focus on while __SOURCE_VERB__:** one line.

---

## Background & Context

The goal is a *gist*: enough for the reader to know what this __SOURCE__ is about
before __SOURCE_VERB__, and nothing more. Write in English. Hard limits:

- **2–4 sentences total**, not paragraphs. No scene-setting, no history lesson,
  no restating what the __SOURCE__ itself will say.
- **If the __SOURCE__ explains it, skip it.** Only supply context the __SOURCE__
  assumes the audience already has.
- Name the speakers/participants and the topic in one clause; do not profile them.
- If the __SOURCE__ is from a Mainland source and the reader is Taiwan-oriented
  (or vice versa), add one short register note here.

### Terms Assumed, Not Explained
- **{term in characters}** ({pinyin}): one sentence, English.
- … 0–5 bullets. Include a term ONLY if the __SOURCE__ uses it as known background
  and never explains it, and a B2/C1 Taiwan-oriented learner would plausibly not
  know it. If the __SOURCE__ defines or unpacks the term itself, leave it out —
  the reader should meet it there. Skip the whole section if nothing qualifies.

---

## Key Vocabulary (__VOCAB_TARGET__)

Choose the most useful or challenging words from this __SOURCE__. Prioritise words a
B2/C1 learner has likely NOT yet mastered (HSK 4–6 / TOCFL B1–C1 plus post-HSK
domain vocabulary central to the topic). Skip particles and the most basic words
(的, 了, 是, 有, 在). Stay within the range above — do not pad with marginal words.

| Traditional | Simplified | Pinyin | Part of Speech | Definition | HSK 3.0 | TOCFL |
|-------------|------------|--------|----------------|------------|---------|-------|
| 傳統字 | 简体字 | pīnyīn | noun/verb/adj/etc. | English meaning | 4 | B2 |

**HSK 3.0 column** — copy levels verbatim from the LEVEL LOOKUP TABLE provided
above the prompt. Bands are 1–6 plus "7-9" (advanced). Write "—" for any word not
in the table — do not guess from your own knowledge.
**TOCFL column** — copy levels verbatim from the LEVEL LOOKUP TABLE (A1–C2). Write
"—" for any word not in the table.

__NEAR_SYNONYM_RULES__

### Words Used in Unexpected Senses

Optional — include 0–3 entries, or skip the section entirely if nothing qualifies.
These are items where a familiar character/word carries a sense the reader may not
have seen (e.g. 把握 normally "to grasp," here "to seize [an opportunity]").

- **{trad}** ({pinyin}) — usual sense: {gloss}; in this __SOURCE__: {gloss + 1-line context}

---

## Key Grammar Patterns (__GRAMMAR_TARGET__)

Prioritise patterns at HSK 4–6 / TOCFL B1–C1 that ACTUALLY appear in this __SOURCE__,
over textbook patterns it merely permits. Skip elementary patterns unless used in a
notably advanced or idiomatic way. Fewer high-quality patterns beat padding.

### Pattern N: [Name]
**Structure:** [formula, e.g. Subject + 把 + Object + Verb + 了]
**Level:** HSK ~N · TOCFL ~X _(estimated — no authoritative grammar level list)_
**Frequency:** ★★★★★ [brief label] | [register: spoken / written / formal / colloquial / literary]
**Usage:** [2–3 sentences on when and why this pattern is used, with any nuance for this __SOURCE__'s register]
**From __SOURCE_QUOTE__:** *直接引用原文。* / Pīnyīn. / English translation.
  ALWAYS include all three parts on this line: the verbatim 原文 sentence, its full
  pinyin, AND an English translation of that sentence — never omit the translation.
**Examples** (Chinese / full pinyin / English):
1. 中文例句。/ Pīnyīn. / English.
2. 中文例句。/ Pīnyīn. / English.

Star ratings: ★★★★★ constant in everyday Chinese · ★★★★ very common · ★★★ common ·
★★ less common / formal / situational · ★ rare / literary.

---

## After __SOURCE_VERB_CAP__

Reproduce this section verbatim — do not add questions of your own:

__SOURCE_CN__
__SOURCE_CN_PY__

*(Summarise the main points in Chinese from memory, then compare against the
answer key at the bottom.)*

---

## Answer Key

This is the ONLY place the main points appear — there is no overview, summary, or
key-themes section earlier in the guide, and Background & Context must not preview
them. The reader writes their own summary first, then compares against this.

### Overview
2–3 sentences in English on the topic and how the __SOURCE__ develops it.

### Main Points
4–6 bullets covering the substance the reader should have caught. Each bullet: the
point in one sentence, plus a reference (for listening guides, a timestamp such as
`(@ 4:32)`; for reading guides, a short 原文 quote). Include any specific number,
name, or claim that carries the argument.

### Easy to Miss
0–3 bullets: details a learner __SOURCE_VERB__ at speed most likely dropped — an
aside, a reversal, a stated reason behind an opinion, a joke that carries meaning."""


# The single summarise-it question, in Chinese + pinyin, per source type.
_SOURCE_CN = {
    "segment": (
        "用中文總結這一段的主要內容。講者說到哪些重點？",
        "Yòng Zhōngwén zǒngjié zhè yí duàn de zhǔyào nèiróng. Jiǎngzhě shuō dào nǎxiē zhòngdiǎn?",
    ),
    "article": (
        "用中文總結這篇文章的主要內容。作者說到哪些重點？",
        "Yòng Zhōngwén zǒngjié zhè piān wénzhāng de zhǔyào nèiróng. Zuòzhě shuō dào nǎxiē zhòngdiǎn?",
    ),
}


def render_spec(
    source_noun: str = "segment",
    source_quote: str = "transcript",
    vocab_target: str = "15–22 items",
    grammar_target: str = "3–5 patterns",
    source_verb: str = "listening",
) -> str:
    """Return the filled study-guide blueprint.

    Listening: render_spec("segment", "transcript", ..., source_verb="listening")
    Reading:   render_spec("article", "article",   ..., source_verb="reading")
    """
    cn, cn_py = _SOURCE_CN.get(source_noun, ("內容", "nèiróng "))
    return (
        _BLUEPRINT
        .replace("__NEAR_SYNONYM_RULES__", NEAR_SYNONYM_RULES)
        .replace("__SOURCE_VERB_CAP__", source_verb.capitalize())
        .replace("__SOURCE_CN_PY__", cn_py)
        .replace("__SOURCE_CN__", cn)
        .replace("__VOCAB_TARGET__", vocab_target)
        .replace("__GRAMMAR_TARGET__", grammar_target)
        .replace("__SOURCE_QUOTE__", source_quote)
        .replace("__SOURCE_VERB__", source_verb)
        .replace("__SOURCE__", source_noun)
    )


# ---------------------------------------------------------------------------
# Post-processor: stamp HSK 3.0 / TOCFL levels onto the synonyms.
# Runs on the rendered markdown of EITHER guide.
# ---------------------------------------------------------------------------

_CJK = r'一-鿿'
_TONE_MARKS = 'āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ'
_PAREN = re.compile(rf'([{_CJK}]{{1,6}})(\s*)\(([^)]+)\)')


def _is_pinyin(content: str) -> bool:
    """True only for romanised pinyin — requires a tone-marked vowel and no CJK.

    The tone-mark requirement keeps English glosses like 'match, be consistent
    with' from being mistaken for pinyin.
    """
    if re.search(rf'[{_CJK}]', content):
        return False
    return any(c in _TONE_MARKS for c in content)


def _level_suffix(word: str) -> str:
    r = lookup(word)
    parts = []
    if r.get("hsk3"):
        parts.append(f"HSK {r['hsk3']}")
    if r.get("tocfl"):
        parts.append(f"TOCFL {r['tocfl']}")
    return " · ".join(parts)


def annotate_synonym_levels(markdown: str) -> str:
    """Inject HSK 3.0 / TOCFL levels into the synonym parentheticals.

    Scoped to the "Key Vocabulary" section's bullet lines so it never touches
    grammar patterns, summaries, or headword rows. Idempotent and safe on words
    with no level ('if they exist').
    """

    def annotate_line(line: str) -> str:
        def repl(m: re.Match) -> str:
            word, sp, content = m.group(1), m.group(2), m.group(3)
            if not _is_pinyin(content) or "HSK" in content or "TOCFL" in content:
                return m.group(0)
            suf = _level_suffix(word)
            return f"{word}{sp}({content}, {suf})" if suf else m.group(0)
        return _PAREN.sub(repl, line)

    out, in_vocab = [], False
    for ln in markdown.split("\n"):
        if ln.startswith("## Key Vocab"):
            in_vocab = True
        elif ln.startswith("## Key Grammar"):
            in_vocab = False
        if in_vocab and ln.startswith("- "):
            ln = annotate_line(ln)
        out.append(ln)
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Legacy image markers.
#
# Guides used to embed photos resolved from Wikimedia Commons / Openverse via
# {{IMG|term|gloss}} markers. The images were rarely worth their space — an
# abstract term would be illustrated with a photo of whatever object it was
# named after — so the blueprint no longer asks for them. This stripper stays
# as a safety net: if a model emits a marker out of habit, it is removed rather
# than shipped as a raw {{IMG|...}} token in the middle of a study guide.
# ---------------------------------------------------------------------------

_IMG_MARKER = re.compile(r'\{\{IMG\s*\|\s*([^|{}]+?)\s*\|\s*([^{}]*?)\s*\}\}')


def strip_image_markers(markdown: str) -> str:
    """Remove any leftover {{IMG|term|gloss}} markers, including a trailing newline.

    Idempotent: text with no markers is returned unchanged.
    """
    return re.sub(r'[ \t]*' + _IMG_MARKER.pattern + r'[ \t]*\n?', '', markdown)
