# mandarin-lookups

Authoritative HSK / TOCFL level lookups with Traditional ↔ Simplified
normalization. Used by a daily Mandarin reading brief routine and a
listening study guide generator, so the model copies real levels instead
of guessing.

## Usage

```python
from lookups import format_lookup_table, lookup

# Markdown table of every 2-4 char Chinese substring with a HSK 3.0 or TOCFL hit
print(format_lookup_table("今天我們來討論台灣的政府政策。"))

# Single-word lookup
lookup("政府")  # {'hsk2': 4, 'hsk3': '4', 'tocfl': 'B2'}
```

## Data

- `data/hsk3_levels.json` — HSK 3.0 (2021), 17,346 forms (both scripts).
  Built from [ivankra/hsk30](https://github.com/ivankra/hsk30).
- `data/hsk_levels.json` — HSK 2.0 (Hanban 2010), 4,993 forms.
- `data/tocfl_levels.json` — Taiwan TOCFL, 14,736 forms. **Note:** level 7
  is a noisy overflow bucket and is treated as unlabeled by `lookup()`.
- `data/cedict_ts.u8` — [CC-CEDICT](https://cc-cedict.org/), used only to
  build a Traditional ↔ Simplified normalization map. Licensed CC BY-SA 4.0.

## Routines

- `routines/reading_brief.md` — the full prompt for the **daily Mandarin
  reading-brief cloud routine**, kept here as the single source of truth. The
  Claude Code routine config is just a thin bootstrap that locates this cloned
  repo, reads this file, and follows it — so edit the prompt **here**, commit,
  and the next run picks it up (no pasting into the routine UI). Topic keywords
  and Google News query terms live in Steps 1–2 of that file.

## License

Data files retain their upstream licenses. `lookups.py` is MIT.
