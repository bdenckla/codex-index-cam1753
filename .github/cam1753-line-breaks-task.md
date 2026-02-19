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
- [x] Identify text on pages: Ps 149:7 through end of Job (page 0085B). Page 0086A is past Job — ignore it. 27 pages total: 0072B through 0085B.
- [x] Build flat stream generator (`gen_cam1753_flat_stream.py`)
- [x] Build line-break editor (`gen_cam1753_line_break_editor.py`) with blank-line feature
- [ ] Mark line breaks for all 27 pages (0072B through 0085B)

### Pages completed

| Page   | Start verse       | End verse (fragment) |
|--------|-------------------|----------------------|
| 0072B  | Ps 149:7          | Job 1:16 (mid)       |
| 0073A  | (in progress)     |                      |

## Procedure: Marking Line Breaks Page by Page

### First page (bootstrapping)

1. User identifies the starting verse (e.g. `Ps 149:7`) and a generous ending verse.
2. Generate the flat stream:
   ```
   .venv\Scripts\python.exe gen_cam1753_flat_stream.py 0072B Ps 149:7 Job 2:10
   ```
3. Generate and open the editor (always start with col 1):
   ```
   .venv\Scripts\python.exe gen_cam1753_line_break_editor.py 0072B 1
   Start-Process ".novc\cam1753_lb_editor_0072B_col1.html"
   ```
4. In the editor: right-click the actual first word on the page to set page-start (if the flat stream includes earlier words from the same verse). Click the last word of each line to mark line-ends. Click line numbers to add blank lines (for masorah notes, inter-book gaps, etc. — any line without verse content). Use the col toggle to switch between columns.
5. Click **Export** → paste directly into `cam1753-line-breaks/<page_id>.json`.
6. **Do NOT** paste the exported JSON into the chat window — that causes Unicode NFC normalization of Hebrew text.

### Subsequent pages (chaining)

1. Generate the flat stream with `--chain`, which reads the previous page\u2019s JSON and starts at the next word:
   ```
   .venv\Scripts\python.exe gen_cam1753_flat_stream.py 0073A --chain 0072B Job 4:10
   ```
   This auto-detects whether the previous page ended mid-verse (generates a `verse-fragment-start`) or at a verse boundary (starts at next full verse). The end verse (`Job 4:10`) should be generous — extra verses at the end are harmless.
2. Generate and open the editor:
   ```
   .venv\Scripts\python.exe gen_cam1753_line_break_editor.py 0073A 1
   Start-Process ".novc\cam1753_lb_editor_0073A_col1.html"
   ```
3. Mark line breaks, export, paste into file (same as bootstrapping steps 4-6).

### Important notes

- **Never overwrite a line-breaks JSON file** that already has marked data without backing it up first. The flat stream generator writes to the same file.
- **Always use `.venv\Scripts\python.exe`** — never bare `python`.
- **Never use `python -c "..."`** one-liners — always create a script in `.novc/` per the general copilot instructions.
- The editor loads images from `http://localhost:8119/cam1753-pages/` — the local HTTP server must be running.
- Col 1 = right column (read first), Col 2 = left column. The editor has a toggle button to switch.
- "Blank lines" are lines without verse content (masorah notes, decorations between books, etc.), not necessarily visually empty.

## Key Files

| File | Purpose |
|------|---------|
| `gen_cam1753_flat_stream.py` | Generate flat-stream JSON for a page (manual or `--chain` mode) |
| `gen_cam1753_line_break_editor.py` | Generate interactive HTML editor for marking line breaks |
| `cam1753-line-breaks/*.json` | Line-break data per page (flat stream + markers) |
| `cam1753-col-quads/*.json` | Column bounding quad data (used by editor for image cropping) |
| `cam1753-pages/*.jpg` | Individual page images |
| `py_ac_loc/mam_xml_verses.py` | MAM-XML verse extraction (shared with Aleppo workflow) |
| `py_ac_loc/MAM-XML/*.xml` | Hebrew Bible text source |
