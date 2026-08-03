# codex-index-cam1753

A digital scholarship tool for locating Hebrew words on photographed pages of
Cambridge University Library MS Add. 1753 (Ketuvim) — μC. The current focus is the
Book of Job, though the infrastructure supports arbitrary biblical books.

A sibling repo, [`codex-index-aleppo`](https://github.com/bdenckla/codex-index-aleppo),
covers the same biblical text in the Aleppo Codex (μA). Both repos use quadrilateral
column geometry.

## Pipeline

1. **MAM-XML parsing** — `py_mam_xml/mam_xml_verses.py` extracts word lists from `MAM-XML/`
2. **Flat stream** — `gen_cam1753_flat_stream.py` combines explicit verse-range arguments with MAM-XML into per-page word streams; data in `cam1753-line-breaks/`
3. **Line-break annotation** — human-in-the-loop via `gen_cam1753_line_break_editor.py`; data in `cam1753-line-breaks/`
4. **Column coordinates** — `gen_col_quad_editor.py`; data in `cam1753-col-quads/`
5. **Word lookup** — `main_find_word_in_cam1753_images.py` ties it all together

## Conventions

- **Page IDs:** `{spread_number}{A|B}` — e.g. `0073A` (spread 73, left page), `0073B` (spread 73, right page)
- **Column numbering:** col 1 = right column (read first in RTL), col 2 = left column
- **Lines per column:** 26 — `LINES_PER_COL` in `py_cam1753_word_image/page.py`

## Docs

- [`doc/cam1753-line-break-task.md`](doc/cam1753-line-break-task.md) — the manuscript, its page images and their provenance, the column-quad data, and the marking task itself
- [`doc/reading-mam-simple.md`](doc/reading-mam-simple.md) — the MAM-simple XML format, verse extraction, versification traditions
- [`doc/mam-with-doc-urls.md`](doc/mam-with-doc-urls.md) — how to build a URL into the MAM-with-doc viewer (book codes, verse fragments)
