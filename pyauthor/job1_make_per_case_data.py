""" Exports make_per_case_data """

from py import my_html
from pyauthor.util import author
from pyauthor.job1_highlight import highlight


def make_per_case_data(record):
    return {
        "row": _make_row(record),
        "details": _make_details(record),
    }


def _make_row(record):
    hbhla = highlight(record, "bhla")
    hmam = highlight(record, "mam")
    if blha_q := record["bhla-q"]:
        assert blha_q == "(?)"
        bhla_and_q = [hbhla, " (?)"]
    else:
        bhla_and_q = [hbhla]
    bhla_and_mam = [*bhla_and_q, my_html.line_break(), hmam]
    hbo_attrs = {"lang": "hbo", "dir": "rtl"}
    return my_html.table_row(
        [
            # str(record["bhla-i"]),
            my_html.table_datum(bhla_and_mam, hbo_attrs),
            my_html.table_datum(record["cv"]),
            my_html.table_datum(record["what-is-weird"]),
        ]
    )


def _lc_full_page_anc(page):
    # E.g. page == "397B"
    href = f"https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F{page}.jpg"
    return my_html.anchor_h(f"LC page {page}", href)


def _maybe_img(record):
    if img_fname := record.get("img"):
        img_tag = my_html.img({"src": f"img/{img_fname}"})
        return [img_tag]
    return []


def _make_details(record):
    sep = " \N{EM DASH} "
    cv = record["cv"]
    uxlc_href = f"https://tanach.us/Tanach.xml?Job{cv}"
    uxlc_anc = my_html.anchor_h("UXLC", uxlc_href)
    cnvm = "c" + cv.replace(":", "v")
    mwd_href = f"https://bdenckla.github.io/MAM-with-doc/D3-Job.html#{cnvm}"
    mwd_anc = my_html.anchor_h("MwD", mwd_href)
    dpe = [uxlc_anc, sep, mwd_anc]
    if lcloc := record.get("lcloc"):
        page = lcloc["page"]
        line = lcloc["line"]
        column = lcloc["column"]
        dpe.append(sep)
        dpe.append(_lc_full_page_anc(page))
        dpe.append(f" (line {line}, col. {column})")
    if comment := record["comment"]:
        dpe.append(sep)
        dpe.append(comment)
    details_proper = my_html.para(dpe)
    return [
        author.table_c(_make_row(record)),
        details_proper,
        *_maybe_img(record),
        my_html.horizontal_rule(),
    ]
