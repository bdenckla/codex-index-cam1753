from pyauthor_util import author
from pyauthor_util.job1_ov_and_de import make_example_row


def intro(ov_or_de):
    each = _VARIANTS[ov_or_de]
    return [
        author.para(_each(each)),
        author.table_c(make_example_row()),
        *_where(),
    ]


_VARIANTS = {
    "intro-overview": "Each entry below",
    "intro-details": "The header of each entry below",
    "intro-job2": "Each entry above",
}


def here_is(start, jda=None):
    out = [
        f"{start} some quirks in μL in the book of Job.",
    ]
    if jda is not None:
        jdae = [" For more details, see the ", jda]
        return out + jdae
    return out


def _each(each):
    return [f"{each} takes the following form:"]


def _where():
    return [
        author.para("Where:"),
        author.unordered_list(
            [
                "# (hash sign) (number sign) is a link to more details on this quirk",
                "μL-proposed is a proposed transcription of the Leningrad Codex",
                "consensus is the Masoretic consensus reading (or a good guess of it)",
                "c:v is the chapter and verse of the book of Job",
            ]
        ),
    ]
