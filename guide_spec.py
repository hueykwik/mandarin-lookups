"""
Canonical study-guide blueprint shared by BOTH Mandarin guides.

This lives in the mandarin-lookups repo because it is the one place reachable by
both worlds: the local listening guide (mandarin_study_guide.py) imports it, and
the cloud reading-brief routine clones this repo into its sandbox and reads it.
Edit the blueprint here once → both guides change.

The two guides differ only in their *source* (an audio transcript segment vs a
news article) and their *wrapper* (a .md file header vs an email header). Those
stay guide-specific. Everything between them — Background, vocabulary, grammar,
questions — comes from render_spec() below so the two outputs look like siblings.

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
# Illustrative-image marker sub-spec (embedded in the blueprint below).
# The model only TAGS items; embed_images() resolves markers to real photos.
# ---------------------------------------------------------------------------

IMAGE_MARKER_RULES = """\
### Image markers (concrete, visual items only)

Some items are best understood by seeing them. For those — and ONLY those — emit an
image marker on its OWN line, immediately after the entry it illustrates:

    {{IMG|傳統字詞|short english gloss}}

for example:  {{IMG|龍鬚糖|dragon's beard candy}}

The marker is replaced later with a real photo, or removed if none is found, so:
- First field = the Traditional term; second field = a short concrete English gloss.
  Both are used as image-search queries, so make the gloss specific (a night-market
  food, not just "candy").
- Emit a marker ONLY for concrete, visually distinctive, usually culture-specific
  things: foods and dishes, physical objects and tools, games and activities, places
  and landmarks, animals, plants, garments. These may appear in the Cultural &
  Contextual Notes and/or in the Key Vocabulary entries.
- NEVER emit one for abstract words, feelings, qualities, states, verbs, or grammar —
  anything a photo would not clarify (e.g. 心態, 糾結, 算是, 體驗). When unsure, omit.
- At most 3 markers in the whole guide; pick the items where a picture helps most.
  One marker per item, never repeat an item."""


# ---------------------------------------------------------------------------
# The blueprint. __SLOTS__ are filled by render_spec via str.replace (no .format,
# so literal braces in examples are safe).
# ---------------------------------------------------------------------------

_BLUEPRINT = """\
## Background & Context

2–4 short paragraphs, **written in English**, giving the reader what they need to
understand this __SOURCE__: who the key people/orgs are, what the broader story is,
why it matters — context a non-specialist B2/C1 reader would NOT get from the
__SOURCE__ alone. (Chinese terms may be cited inline, but the explanation itself is
in English.) If the __SOURCE__ is from a Mainland source and the reader is
Taiwan-oriented (or vice versa), put cross-strait register notes here.

### Cultural & Contextual Notes
- **{term in characters}** ({pinyin}): 1–2 sentence English explanation — only for
  terms whose meaning relies on context the __SOURCE__ assumes.
- … (3–6 bullets, only as many as actually useful)

For any bullet naming a concrete, visually distinctive item (a food, object, place,
game, garment), add an image marker on its own line right under that bullet — see
"Image markers" in the Key Vocabulary section below.

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

__IMAGE_RULES__

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

## Summary

### Overview
2–3 sentences on the topic and main points of this __SOURCE__.

### Key Themes
Bullet list of 4–6 main ideas or topics covered.

### Learner Notes
- Estimated HSK level and TOCFL band for this content
- What to focus on while __SOURCE_VERB__
- Any particularly useful phrases for everyday conversation

---

## Comprehension Questions (3–4 questions)

Fewer but harder. Each question MUST require having actually engaged with THIS
__SOURCE__ by __SOURCE_VERB__ — test specific details, claims, examples, or the
chain of reasoning that appear ONLY in the source itself. A learner who skimmed
the Vocabulary, Grammar, and Summary sections of this guide but skipped the actual
__SOURCE_VERB__ should NOT be able to answer. Therefore: do NOT ask about anything
already stated in the Summary/Key Themes, and do NOT ask for definitions of the
vocab words. Favour questions that hinge on a specific stated detail, a speaker's
stated reason or opinion, a number/name/sequence, or an inference that requires
following the actual content. Write each in Chinese with pinyin only — no answer here.

1. **Question in Chinese** (Pīnyīn)
2. **Question in Chinese** (Pīnyīn)

## Discussion Questions (4–5 questions)

Open-ended questions connecting the content to the learner's own life or opinions,
for speaking practice. Write each in Chinese with pinyin, then add 2–3 Chinese
sentence starters to scaffold the answer.

1. **Question in Chinese** (Pīnyīn)
   *Sentence starters:* 我覺得… / 在我的經驗裡… / 我認為…

---

## Answer Key

Answers to the Comprehension Questions above, with a brief Chinese answer and a
paragraph/quote reference (for listening guides, include the timestamp, e.g. `(@ 4:32)`).

1. Answer to question 1.
2. Answer to question 2."""


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
    return (
        _BLUEPRINT
        .replace("__NEAR_SYNONYM_RULES__", NEAR_SYNONYM_RULES)
        .replace("__IMAGE_RULES__", IMAGE_MARKER_RULES)
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
# Illustrative images: resolve {{IMG|term|gloss}} markers to real photo URLs.
# Sources: Wikimedia Commons (precise) then Openverse (broad) — no API key.
# Fails safe: any network/import/parse error, or no confident match, drops the
# marker so a guide never ships a broken image or a leftover token.
# ---------------------------------------------------------------------------

_IMG_MARKER = re.compile(r'\{\{IMG\s*\|\s*([^|{}]+?)\s*\|\s*([^{}]*?)\s*\}\}')
_IMG_UA = {"User-Agent": "mandarin-study-guide/1.0 (personal language study)"}
_IMG_CACHE = {}  # term|gloss -> (url, source, page) or None; dedupes across parts


# Document scans and vector logos are rendered to .jpg/.png thumbnails by
# Commons, so the extension in the *path* is what gives them away, not the
# thumbnail's own suffix.
_IMG_BAD_EXT = (".pdf", ".djvu", ".tif", ".tiff", ".svg")
_IMG_STOPWORDS = {
    "a", "an", "the", "of", "for", "with", "and", "or", "in", "on", "to",
    "small", "large", "big", "little", "type", "style", "kind", "used", "like",
}


def _img_ok(url: str) -> bool:
    """Reject document scans and non-photos before trusting a search hit.

    Commons renders PDF/DjVu page scans as `...djvu.jpg` thumbnails — those are
    the magazine/newspaper false positives (a 1912 pulp magazine called *The
    Black Cat* matched "freeze-dried cat treats"), and SVGs are almost always
    logos rather than photos of a thing.
    """
    u = url.lower()
    return u.startswith("http") and not any(e in u for e in _IMG_BAD_EXT)


def _content_tokens(text: str) -> list[str]:
    return [t for t in re.split(r"[^a-z0-9]+", (text or "").lower())
            if len(t) >= 3 and t not in _IMG_STOPWORDS]


def _stem(tok: str) -> str:
    return tok[:-1] if len(tok) > 3 and tok.endswith("s") else tok


def _matches_gloss(title: str, gloss: str) -> bool:
    """True when `title` names the thing the gloss is about.

    Commons full-text search has no relevance floor: it happily returns any file
    whose description mentions *one* query word, which is how "freeze-dried cat
    treats" landed a magazine cover on the strength of "cat". The head noun of
    the gloss (its last content word) is the thing being illustrated, so require
    that specific word in the file title — "cat" alone is not enough, "treats"
    is.
    """
    toks = _content_tokens(gloss)
    if not toks:
        return False
    title_toks = {_stem(t) for t in _content_tokens(title)}
    if _stem(toks[-1]) in title_toks:
        return True
    # Glosses ending in a generic head ("...cage enclosure") would otherwise
    # drop a good match, so two agreeing words also clear the bar. One shared
    # word never does — that is exactly the "cat" coincidence being guarded
    # against.
    return len(title_toks & {_stem(t) for t in toks}) >= 2


def _matches_term(title: str, term: str) -> bool:
    """CJK queries only count when the title actually carries the term.

    Commons matched 貓條 to a *Puss in Boots* logo through a single shared
    character, so partial-character overlap is worthless here.
    """
    return bool(term) and term in (title or "")


def _commons(query, timeout, accept):
    import requests
    r = requests.get(
        "https://commons.wikimedia.org/w/api.php",
        params={
            "action": "query", "format": "json", "generator": "search",
            "gsrnamespace": 6, "gsrsearch": query, "gsrlimit": 5,
            "prop": "imageinfo", "iiprop": "url", "iiurlwidth": 360,
        }, headers=_IMG_UA, timeout=timeout)
    pages = (r.json().get("query", {}) or {}).get("pages", {}) or {}
    for p in sorted(pages.values(), key=lambda p: p.get("index", 999)):
        ii = (p.get("imageinfo") or [{}])[0]
        thumb, page = ii.get("thumburl"), ii.get("descriptionurl")
        title = re.sub(r"^File:", "", p.get("title") or "")
        if thumb and _img_ok(thumb) and accept(title):
            return thumb, "Wikimedia Commons", page or thumb
    return None


def _openverse(query, timeout, accept):
    import requests
    r = requests.get(
        "https://api.openverse.org/v1/images/",
        params={"q": query, "page_size": 5}, headers=_IMG_UA, timeout=timeout)
    for d in r.json().get("results", []) or []:
        thumb = d.get("thumbnail") or d.get("url")
        tags = " ".join(t.get("name", "") for t in (d.get("tags") or [])
                        if isinstance(t, dict))
        title = f"{d.get('title') or ''} {tags}"
        if thumb and _img_ok(thumb) and accept(title):
            page = d.get("foreign_landing_url") or d.get("url") or thumb
            return thumb, (d.get("source") or "Openverse"), page
    return None


def _resolve_image(term, gloss, timeout=10.0):
    """Return (url, source, page) for the first hit that survives the relevance
    gate, else None.

    Openverse goes first: it indexes CC-licensed *photographs*, while Commons is
    a mixed archive where book scans and film logos outrank the actual object.
    The English gloss is queried before the Traditional term because both APIs
    are English-indexed — the CJK term is a long-shot pass at culture-specific
    items, and only counts when it appears in the file's own title.

    Every candidate is checked against the query before it is returned; a marker
    with no relevant match resolves to nothing, which drops the image. No image
    beats a wrong image in a study guide.
    """
    key = f"{term}|{gloss}"
    if key in _IMG_CACHE:
        return _IMG_CACHE[key]
    attempts = []
    if gloss:
        gate = lambda title: _matches_gloss(title, gloss)  # noqa: E731
        attempts += [(_openverse, gloss, gate), (_commons, gloss, gate)]
    if term:
        gate = lambda title: _matches_term(title, term)  # noqa: E731
        attempts += [(_commons, term, gate), (_openverse, term, gate)]
    result = None
    try:
        for source, query, accept in attempts:
            result = source(query, timeout, accept)
            if result:
                break
    except Exception:
        result = None  # network down / sandbox block / bad JSON / no requests → skip
    _IMG_CACHE[key] = result
    return result


def embed_images(markdown: str, max_images: int = 3) -> str:
    """Replace {{IMG|term|gloss}} markers with real Markdown images.

    Each marker resolves to a Wikimedia Commons / Openverse photo plus a small
    attribution caption; markers with no confident match — or any past the
    per-guide cap — are removed. Emits plain `![alt](url)` markdown, which
    Obsidian renders directly and the email routine converts to <img>.
    Idempotent: a second pass finds no markers and is a no-op.
    """
    used = 0

    def repl(m):
        nonlocal used
        term, gloss = m.group(1).strip(), m.group(2).strip()
        if used >= max_images:
            return ""
        hit = _resolve_image(term, gloss)
        if not hit:
            return ""
        used += 1
        url, source, page = hit
        alt = f"{term} — {gloss}" if gloss else term
        return f"![{alt}]({url})\n*image: [{source}]({page})*"

    return _IMG_MARKER.sub(repl, markdown)
