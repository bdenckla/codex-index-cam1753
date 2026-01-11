from pyauthor.util import author
from pyauthor.job1_make_per_case_data import make_example_row

def intro(expanding, each, jda=None):
    return [
        author.para(here_is(expanding, jda)),
        author.para(the_row(each)),
        author.table_c(make_example_row()),
    ]


def here_is(expanding, jda=None):
    out = [
        f"Here is a table {expanding} upon the entries for the book of Job",
        " in BHL Appendix A.",
    ]
    if jda is not None:
        jdae = [" For more details, see the ", jda, "."]
        return out + jdae
    return out


def the_row(each):
    return [
        f"{each} entry below takes the following form:"
    ]
