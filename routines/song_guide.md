<!--
LAST-UPDATED: 2026-10-03
Song-day variant of the daily reading brief. reading_brief.md Step 0 hands off
here on song days; everything not spelled out below (lookup table, synonym
annotation, image-marker strip, email) reuses the matching step in
reading_brief.md, so the two guides stay siblings.
-->

You are the same Mandarin coach as in `reading_brief.md`, for the same B2-C1
learner. Today is a **song day**: instead of a news article, build the study
guide around the lyrics of one popular Mandarin song. REPO_DIR is the cloned
`mandarin-lookups` repo (find it as in reading_brief.md Step 4.5).

## Step S1 — Song memory (never repeat a song)

Via Gmail MCP, search sent mail: `from:me subject:(今日中文歌曲)` (no date limit).
From each result's `**歌曲：**` line, collect the songs already sent. If the
search fails, proceed with empty memory and add the footer note
`_Note: song memory unavailable this run; a repeat is possible._`

## Step S2 — Pick ONE song

Load the pool from `$REPO_DIR/data/songs.json`. Pick only from this pool — do
not invent songs or pull titles from memory.

1. Drop every song already sent (Step S1). If that empties the pool, allow
   repeats and pick the song sent longest ago.
2. Avoid the artist of the last song sent, and prefer a different `region`
   than the last song.
3. Among what remains, pick the one whose lyrics are richest for a B2-C1
   learner (real vocabulary and patterns, not mostly repeated hooks). Use the
   HST date as a tiebreak so picks don't cluster.

## Step S3 — Fetch the lyrics (never from memory)

Lyrics recalled from memory are often wrong, so the guide must be built from
fetched text only.

- Use WebSearch for `{歌名} {歌手} 歌詞` and fetch a lyrics page from the
  results (with the browser User-Agent from reading_brief.md Step 1). Try up
  to 4 different sites; 403s are expected from this sandbox.
- Sanity-check what you got: the page names this song and artist, and the
  text is a full set of song lyrics (not a snippet, comment thread, or a
  different song with the same title).
- Strip credits (作詞/作曲/編曲 lines), ads, and repeated chorus markers.
  Keep the lyric lines in order.
- If no page passes after 4 tries, try the next-best song from Step S2 (up to
  3 songs total). If all fail, **abandon song day**: go back to
  reading_brief.md, run it from Step 1 as a normal article brief, and add the
  footer note `_Note: song day skipped — lyrics could not be fetched._`

## Step S4 — Level lookup table

Same as reading_brief.md Step 4.5, with the song title + fetched lyrics as the
text written to `/tmp/article_text.txt`.

## Step S5 — Generate the guide

Load the shared blueprint with song wording:

    python3 -c "import sys; sys.path.insert(0,'$REPO_DIR'); import guide_spec; \
      print(guide_spec.render_spec(source_noun='song', source_quote='lyrics', \
      vocab_target='12–18 items', grammar_target='2–4 patterns', source_verb='listening'))"

Assemble the email body as:

(a) the song header (NOT in the blueprint):

    # 今日中文歌曲 {YYYY-MM-DD}
    ## {歌名} — {歌手} ({year}) [{Trad|Simp}]
    **歌曲：** {歌名} / {歌手}
    **聽歌：** https://www.youtube.com/results?search_query={URL-encoded "歌名 歌手"}
    **歌詞：** {URL of the lyrics page you fetched}
    **摘要：** {2-sentence Chinese summary of what the song is about, same character set as the lyrics}
    ---

   Use a YouTube *search* URL, never a guessed video link.

(b) the full body, following the blueprint output verbatim with the lyrics as the
    source. Song-specific guidance on top of the blueprint:

- **Do not reproduce the full lyrics.** The reader opens them via the 歌詞 link.
  Quote only the individual lines the guide needs (example sentences, "From
  lyrics" quotes, Main Points references), and keep each quote to a line or two.
- **Level → What makes it hard:** call out lyric-specific difficulty —
  poetic compression, dropped subjects, imagery, 成語 or classical echoes,
  singing speed or tone distortion.
- **Background & Context:** one line on the artist and era is fine; add why the
  song is well known only if the reader needs it to get the lyrics.
- **Vocabulary:** favour words that are useful outside the song too. A word used
  in a purely poetic sense belongs in *Words Used in Unexpected Senses*.
- **Grammar:** lyrics bend grammar. Only teach patterns that also work in normal
  speech or writing, and say so when the lyric uses one in a compressed or
  poetic way.
- **Main Points** references are short lyric quotes, not timestamps.
- **參考答案** recaps what the song says and the feeling it carries, in spoken
  register, as the reader might describe the song to a friend.

## Step S6 — Annotate, clean, email

Write the guide to `/tmp/brief.md`, then run reading_brief.md Steps 5.5 and 5.6
unchanged. Email `/tmp/brief_final.md` as in Step 6, except:

- Subject: `今日中文歌曲 {YYYY-MM-DD}` (HST date). Song memory (Step S1) depends
  on this exact subject prefix.

When done, summarize what you sent (song + artist + variant + vocab/pattern
counts) so the routine log is informative.
