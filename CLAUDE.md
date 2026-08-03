# CLAUDE.md

What this repo is, its pipeline and its page/column conventions are in [README.md](README.md);
the longer references are in [`doc/`](doc/). Only what an assistant gets wrong without being
told is below.

## The interactive editors need a local HTTP server, started separately

They will not work from a `file://` URL, and none of them starts a server for itself — each
expects one to be running already, at a port it hardcodes:

| Editor | Server to start first |
|---|---|
| `gen_col_quad_editor.py`, `gen_cam1753_line_break_editor.py` | `python -m http.server 8119` from the repo root (they load `http://localhost:8119/cam1753-pages/...`) |
| `main_find_word_in_cam1753_images.py` | `python -m http.server 8753 -d .novc` (`SERVER_PORT` in that script) |

`file://` fails for two separate reasons, so neither is fixable by adjusting the page: the
image loads cross-origin, and `navigator.clipboard` / `canvas.toBlob()` need a secure context.
Plain `http://localhost` counts as a secure context in every major browser, so no TLS is needed.
A static, read-only HTML file that does none of that opens fine as a file.

## Hebrew combining marks are in this project's own order, not Unicode's

Never run `unicodedata.normalize` (NFC, NFD, or any other form) over Hebrew text here. NFC
reorders combining marks and destroys the order this project deliberately keeps. The order, and
the authoritative implementation, are `give_std_mark_order` in `mb_cmn/uni_denorm.py` — byte-identical
to `../MAM-basics/py/mb_cmn/uni_denorm.py`, which is where it is maintained;
`check_mark_order.py` checks a tree against it and is wired into
`check_all.py`. When two Hebrew strings that should be equal do not match, put both through
`give_std_mark_order` rather than normalizing.
