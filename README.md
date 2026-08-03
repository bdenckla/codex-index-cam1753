# codex-index-cam1753

A digital scholarship tool for locating Hebrew words on photographed pages of
Cambridge University Library MS Add. 1753 (Ketuvim) — μC. The current focus is the
Book of Job, though the infrastructure supports arbitrary biblical books.

A sibling repo, [`codex-index-aleppo`](https://github.com/bdenckla/codex-index-aleppo),
covers the same biblical text in the Aleppo Codex (μA). Both repos use quadrilateral
column geometry.

## Pipeline

1. **XML parsing** — `py_mam_xml/mam_xml_verses.py` extracts word lists from `MAM-XML/` (see [Data](#data))
2. **Flat stream** — `gen_cam1753_flat_stream.py` combines explicit verse-range arguments with those word lists into per-page word streams; data in `cam1753-line-breaks/`
3. **Line-break annotation** — human-in-the-loop via `gen_cam1753_line_break_editor.py`; data in `cam1753-line-breaks/`
4. **Column coordinates** — `gen_col_quad_editor.py`; data in `cam1753-col-quads/`
5. **Word lookup** — `main_find_word_in_cam1753_images.py` ties it all together

## Data

- **`MAM-XML/`** — a flat copy of the **`xml-vtrad-mam`** output of the sibling
  [`MAM-simple`](https://github.com/bdenckla/MAM-simple) repo: the mam vtrad, not `xml-vtrad-bhs`
  or `xml-vtrad-sef`. The directory name is that repo's *former* name, which it was renamed away
  from in its own `0c2ce6b`; `gen_cam1753_flat_stream.py` still spells it `MAM_XML_DIR`.
  [`MAM-simple-provenance.md`](MAM-simple-provenance.md) records which commit the copy came
  from, and records the source path as `MAM-simple/out/xml-vtrad-mam` — also pre-rename, since
  MAM-simple's `16b63e3` moved the `xml-vtrad-*` directories to that repo's root and turned
  `out/` into `misc/`.
- **`cam1753-pages/`**, **`cam1753-spreads/`** — page images and the two-page spreads they were
  split from; provenance in `cam1753-spreads-provenance.md`.
- **`cam1753-line-breaks/`**, **`cam1753-col-quads/`** — the generated flat streams with their
  human-annotated line breaks, and the column quadrilaterals.

## Conventions

- **Page IDs:** `{spread_number}{A|B}` — e.g. `0073A` (spread 73, left page), `0073B` (spread 73, right page)
- **Column numbering:** col 1 = right column (read first in RTL), col 2 = left column
- **Lines per column:** 26 — `LINES_PER_COL` in `py_cam1753_word_image/page.py`

## Docs

- [`doc/cam1753-line-break-task.md`](doc/cam1753-line-break-task.md) — the manuscript, its page images and their provenance, the column-quad data, and the marking task itself
- [`doc/reading-mam-simple.md`](doc/reading-mam-simple.md) — the vendored `MAM-XML/` snapshot and the reader over it; points at MAM-simple for the format itself
- [`doc/mam-with-doc-urls.md`](doc/mam-with-doc-urls.md) — how to build a URL into the MAM-with-doc viewer (book codes, verse fragments)
