""" Exports gen_html_file and anchor """

from pyauthor.util import author
from pyauthor.common import D2_TITLE, d1v_anchor
from pyauthor.common import D2_H1_CONTENTS
from pyauthor.common import D2_FNAME


def gen_html_file(tdm_ch):
    author.assert_stem_eq(__file__, D2_FNAME)
    author.help_gen_html_file(tdm_ch, D2_FNAME, D2_TITLE, _CBODY)


_CPARA1 = [
    "This document discusses the BHQ edition of the Book of Job,",
    " focusing on its treatment of certain textual variants.",
    " Right now it consists merely of this",
    " ",
    d1v_anchor(),
]
_CBODY = [
    author.heading_level_1(D2_H1_CONTENTS),
    author.para(_CPARA1),
]
