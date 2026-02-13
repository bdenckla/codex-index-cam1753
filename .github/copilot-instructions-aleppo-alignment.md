# Procedure: Manual Line-by-Line Alignment of Aleppo Codex Pages

## Goal

Align ground truth text (extracted from mam-xml) to the physical manuscript lines visible in an Aleppo Codex page image from mgketer.org.

## Inputs

- **Page index:** `C:\Users\BenDe\GitRepos\codex-index\aleppo\index-flat.json` — maps each Aleppo Codex leaf to a `[start_cv, end_cv]` text range. Key `"body"` contains the list; each entry has `de_leaf` (e.g., `"280r"`), `de_text_range` (e.g., `[["Job",37,9],["Job",38,30]]`), and `de_url`.
- **Ground truth text:** Extracted on the fly from MAM-XML via `pycmn/mam_xml_verses.py`.
- **Page image:** Screenshot from `https://www.mgketer.org/mikra/29/{chnu}/1/mg/106` (Job = book 29), saved to `.novc/`

## Outputs

- **Alignment file:** `py_uxlc_loc/aleppo_col_lines_{leaf}.py` — one file per leaf (e.g., `aleppo_col_lines_280r.py`), containing `COLUMN_1_LINES` and `COLUMN_2_LINES`.
- **Interactive alignment tool:** `.novc/aleppo_align_{leaf}_col{N}.html` — an HTML page for the user to visually align text to the image.

## Page Lookup

To find the leaf for a given chapter, or what text a leaf contains:

```python
import json
with open(r'C:\Users\BenDe\GitRepos\codex-index\aleppo\index-flat.json') as f:
    pages = json.load(f)['body']
job_pages = [p for p in pages if p['de_text_range'][0][0] == 'Job' or p['de_text_range'][1][0] == 'Job']
for p in job_pages:
    tr = p['de_text_range']
    print(f"  {p['de_leaf']:6s}  {tr[0][0]} {tr[0][1]}:{tr[0][2]}  –  {tr[1][0]} {tr[1][1]}:{tr[1][2]}")
```

Job pages (for reference):
```
270r  Ps 149:1  – Job 1:16      279r  Job 34:1  – Job 35:9
270v  Job 1:16  – Job 3:6       279v  Job 35:10 – Job 37:8 (cont.)
271r  Job 3:6   – Job 5:10      280r  Job 37:9  – Job 38:30
271v  Job 5:10  – Job 6:30      280v  Job 38:31 – Job 40:5
272r  Job 7:1   – Job 9:5       281r  Job 40:6  – Job 41:22
272v  Job 9:5   – Job 10:20     281v  Job 41:23 – Prov 1:8
273r  Job 10:20 – Job 13:2
273v  Job 13:2  – Job 14:21
274r  Job 14:22 – Job 16:12
274v  Job 16:13 – Job 19:6
275r  Job 19:7  – Job 20:26
275v  Job 20:27 – Job 22:13
276r  Job 22:13 – Job 24:14
276v  Job 24:15 – Job 27:16
277r  Job 27:16 – Job 29:14
277v  Job 29:14 – Job 31:6
278r  Job 31:7  – Job 32:7
278v  Job 32:8  – Job 33:33
```

## Procedure

### 1. Prepare the ground truth

Use the reusable extraction module `pycmn/mam_xml_verses.py`:

```python
from pycmn.mam_xml_verses import get_verses_in_range

verses = get_verses_in_range(
    r'C:\Users\BenDe\GitRepos\MAM-XML\out\xml-vtrad-mam\Job.xml',
    'Job', (37, 9), (38, 20),
)
```

This handles all special MAM-XML elements:
- `<text>`: plain text spans
- `<lp-legarmeih>`, `<lp-paseq>`: appends paseq (U+05C0) to preceding word
- `<kq>`: ketiv/qere — uses ketiv (`kq-k` child, unpointed) for manuscript alignment
- `<kq-trivial>`: uses `text` attribute (pointed)
- `<slh-word>`: suspended-letter word — uses `slhw-desc-0` (full pointed word)
- `<implicit-maqaf>`: no visible text, skipped
- `<spi-pe2>`, `<spi-samekh2>`: parashah breaks — returned as `parashah_after` field

Each verse dict contains:
- `cv`: chapter:verse string (e.g., `'37:9'`)
- `words`: list of maqaf-joined words
- `ketiv_indices`: indices of words that are ketiv (unpointed)
- `parashah_after`: `None`, `'{פ}'`, or `'{ס}'`

**Key points:**
- Read from `xml-vtrad-mam/` (MAM's native versification).
- For Aleppo alignment, only **ketiv** matters — it's the unpointed text visible in the manuscript's main column.
- **Do NOT use the mam-for-sefaria CSV** — it contains HTML entities and parashah markers that would need stripping.

### 2. Get the page image

Take a screenshot from mgketer.org and copy it to `.novc/`:

```powershell
Get-ChildItem "$env:USERPROFILE\OneDrive\Pictures\Screenshots" | Sort-Object LastWriteTime -Descending | Select-Object -First 3 Name, LastWriteTime
Copy-Item "$env:USERPROFILE\OneDrive\Pictures\Screenshots\<latest>.png" ".novc/aleppo_{leaf}_col{N}_page.png"
```

### 3. Generate the interactive alignment HTML

Use the reusable module `pycmn/aleppo_align_html.py`. Create a thin column-specific script in `.novc/`:

```python
"""Generate alignment HTML for leaf NNNx Column M."""
import sys
sys.path.insert(0, r'C:\Users\BenDe\GitRepos\book-of-job')

from pycmn.aleppo_align_html import generate_alignment_html

MAM_XML = r'C:\Users\BenDe\GitRepos\MAM-XML\out\xml-vtrad-mam\Job.xml'

generate_alignment_html(
    out_path=r'.novc\aleppo_align_{leaf}_colM.html',
    image_path='aleppo_{leaf}_colM_page.png',
    title='Leaf NNNx, Job X:Y–A:B, Column M (right/left column)',
    column_var='COLUMN_M_LINES',
    xml_path=MAM_XML,
    book='Job',
    verse_range=((X, Y), (A, B)),
    lead_in_words=['...'],  # words from prev column, or omit if starts at verse boundary
    lead_in_skip=1,         # how many words to skip from first verse
)
```

The generated HTML includes:
- **Left panel (RTL):** All ground truth words as clickable elements, split at maqaf (U+05BE) boundaries.
- **Right panel:** The page image.
- **Ketiv words** styled in gold.
- **Parashah markers** (`{פ}`, `{ס}`) shown inline as clickable orange pseudo-words.
- **Click a word** to toggle it as the last word on a manuscript line (turns green with line number).
- **Copy to Clipboard** exports the `COLUMN_{N}_LINES` Python list.

#### Parashah markers

Petuxah (`{פ}`) and setumah (`{ס}`) breaks from the MAM-XML appear inline as clickable words. When a parashah break causes a blank line in the manuscript, click the last real word of the line before it, then click the `{פ}`/`{ס}` marker itself. The exported line will contain `"{פ}"` (not an empty string).

#### Mid-verse continuation across pages

When a column starts mid-verse, pass `lead_in_words` (the words already on the previous column) and `lead_in_skip` (how many words to skip from the first verse). The lead-in words render grayed out with a "(prev col)" label and are not clickable.

### 4. User aligns text to image

The user opens the HTML in a browser, loads the image, and clicks the last word/segment of each manuscript line. When finished, clicks **Copy to Clipboard** and pastes the result.

### 5. Record the alignment

Replace the `COLUMN_{N}_LINES` list in `py_uxlc_loc/aleppo_col_lines_{leaf}.py` with the pasted output.

## Line Break Heuristics

- Early verses in Job's poetic sections often fit **one verse per line**.
- Longer verses (especially prose-like ones such as v10, v19, v20) often span **two lines**.
- When a verse spills, the break often falls at an etnachta or other major accent.
- Lines can also break at a maqaf (the maqaf is the last character on the line).

## Naming Conventions

- **Screenshot:** `.novc/aleppo_{leaf}_col{N}_page.png` (e.g., `aleppo_280r_col1_page.png`)
- **Alignment HTML:** `.novc/aleppo_align_{leaf}_col{N}.html` (e.g., `aleppo_align_280r_col1.html`)
- **Python output file:** `py_uxlc_loc/aleppo_col_lines_{leaf}.py` (e.g., `aleppo_col_lines_280r.py`) with `COLUMN_1_LINES` and `COLUMN_2_LINES`
- Each Aleppo page has two columns: column 1 = right, column 2 = left.
- The `{leaf}` identifier (e.g., `279r`, `280v`) comes from the Aleppo Codex index (`codex-index/aleppo/index-flat.json`).

## Completed Alignments

- **Leaf 279r** (Job 34:1–35:9): `py_uxlc_loc/aleppo_col_lines_279r.py`
  - Column 1: Job 34:1–23, 28 lines
  - Column 2: Job 34:24–35:9, 28 lines
- **Leaf 279v** (Job 35:10–37:8): `py_uxlc_loc/aleppo_col_lines_279v.py`
  - Column 1: Job 35:10–36:18 (partial), 28 lines
  - Column 2: Job 36:18 (cont.)–37:8, 28 lines
- **Leaf 280r** (Job 37:9–38:30): `py_uxlc_loc/aleppo_col_lines_280r.py`
  - Column 1: Job 37:9 (cont.)–38:6, 28 lines (line 21 = `"{פ}"` pe break)
  - Column 2: Job 38:7–38:30, 28 lines
