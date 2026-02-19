# cam1753 Line-Break Marking Task

## Manuscript

Cambridge University Library, MS Add. 1753 (Ketuvim). Images downloaded from archive.org (item `ketuvim-cambridge-ms-add-1753-images`, zip `Ketuvim_Cambridge_MS_Add_1753_jp2.zip`, scale=2, server `ia800901.us.archive.org`).

## Page Images

- **28 individual pages** in `cam1753-pages/` (0072B.jpg through 0086A.jpg, approx 2200x3040 px)
- Split from two-page spreads in `cam1753-spreads/` (archive pages 77-90)
- Naming: archive page N → left=recto(A) of leaf N-4, right=verso(B) of leaf N-5
- Provenance documented in `cam1753-pages-provenance.md`

## Column Quad Data

- **28 JSON files** in `cam1753-col-quads/` — manually defined bounding quadrilaterals
- Col1 = RIGHT column (read first in RTL), Col2 = LEFT column
- Each has `rel` (0-1 normalized) and `px` coordinates for corners tl/tr/bl/br
- 26 weighted line-boxes per column: top box 1.5x (ascenders), bottom box 1.25x (descenders), 24 normal
- Generated via `gen_col_quad_editor.py` (interactive HTML editor, serves images via localhost:8119)

## Sibling Aleppo Codex Workflow

The repo already has a line-break workflow for Aleppo Codex pages in `py_ac_loc/`:
- `gen_lb_flat_stream.py` — generates word-level flat stream JSON for a page
- `gen_line_break_editor.py` — interactive HTML editor: click last word of each line, export
- `line-breaks/*.json` — saved line-break data
- `MAM-XML/*.xml` — text source (Westminster Leningrad / MAM markup)

A similar workflow should be adapted for cam1753, using the quad data for column cropping.

## Local HTTP Server

HTML editors that load page images need `http://localhost:8119/` serving the repo root. Start with:
```
python -m http.server 8119
```
Run in background. Required because browsers block `file://` cross-origin image loads in SVG/canvas.

## Status

- [x] Download and split page images (28 pages)
- [x] Column quad data for all 28 pages
- [ ] Identify text source / word stream for cam1753 pages (what biblical books/chapters are on these pages?)
- [ ] Build line-break editor adapted for cam1753
- [ ] Mark line breaks for all 28 pages
