""" Exports gen_html_file and anchor """

from pyauthor_util import author
from pyauthor.common import D2_TITLE, d1v_anchor
from pyauthor.common import D2_H1_CONTENTS
from pyauthor.common import D2_FNAME
from py import my_html


def gen_html_file(tdm_ch):
    author.assert_stem_eq(__file__, D2_FNAME)
    author.help_gen_html_file(tdm_ch, D2_FNAME, D2_TITLE, _CBODY)


def num_range(start, stop):
    return f"{start}\N{THIN SPACE}\N{EN DASH}\N{THIN SPACE}{stop}"


_CPARA10 = [
    "Like many students of Tanakh,",
    " I started out in the cult of $BHS.",
    #
    [" I thought $BHS was", " ", my_html.bold("the")],
    " definitive edition.",
    #
    " Unlike many students of Tanakh,",
    " I eventually soured on $BHS, for the following reasons:"]
    #
_C_LIST_ITEMS_AFTER_PARA10 = [
   "It often fails to accurately transcribe μL (the Leningrad Codex).",
   #
   "It often fails to note where μL disagrees with other manuscripts.",
   #
   "It cites other manuscripts using an outdated emphasis on quantity over quality."
 ]
_CPARA11 = [
    "My first candidate for a $BHS alternative was $BHQ (Biblia Hebraica Quinta).",
    " (Though I had soured on $BHS, I still hadn’t fully escaped its cult.)"
]
_CPARA12 = [
    "But I soon soured on $BHQ as well."
    #
    " One obvious problem is that $BHQ will not be complete for many years.",
    #
    " Perhaps more importantly, I found that $BHQ still suffers from some of the",
    " same problems as $BHS.",
    #
    " Although $BHQ now emphasizes manuscript quality over quantity,",
    " the other two problems listed above remain, albeit to a lesser degree.",
]
_CPARA13 = [
    "As I continued my search for better editions, I found editions that do much better.",
    #
    " This made me even more disappointed with $BHQ, in retrospect.",
    #
    " I can see why something like a fresh transcription of μL was beyond the scope of $BHQ.",
    #
    " But I can’t see why $BHQ would neglect the work already done in other editions.",
    #
    " These other editions include the following:",
]
_C_LIST_ITEMS_AFTER_PARA13 = [
    f"דעת מקרא (Breuer et al., {num_range(1970, 2003)})",
    "$BHL (Dotan, 2001)",
]
_CPARA14 = [
    "The first volume of $BHQ (Megilloth) came out in 2004.",
    #
    " The חמש מגילות volume of דעת מקרא came long before, in 1990.",
    #
    " Even Dotan’s $BHL was available in plenty of time to be used in all volumes of $BHQ.",
    #
    " Before his death, Dotan was even a consultant for $BHQ.",
    #
    " What’s more, his $BHL is even used as a source in at least some volumes of $BHQ.",
    #
    " So it is particularly puzzling that his $BHL, in particular its monumental Appendix A,"
    " was not used (or was not thoroughly used) in $BHQ.",
]
_CPARA15 = [
    "Although it may already be clear, at this point I should mention that",
    " my purposes are narrowly focused on the Masoretic text.",
    " Thus I am not concerned with",
    " the many parts of $BHQ that deal with the following:",
]
_C_LIST_ITEMS_AFTER_PARA15 = [
    "sources in languages other than Hebrew",
    "non-Masoretic (e.g. unpointed) Hebrew sources",
    "Masorah magna and parva",
    "the meaning of the text",
]
_CPARA16 = [
    "For all I know, these parts of $BHQ are of the highest quality, and improve greatly on $BHS.",
    " But these parts are not my concern.",
]
_CPARA17 = [
    "Having criticized $BHQ in general terms,",
    " I will now review the specifics of the $BHQ Book of Job.",
    #
    " As of now, it is the latest volume of $BHQ to be published.",
    #
    " Right now the review consists merely of this",
    " ",
    d1v_anchor(),
]
_CBODY = [
    author.heading_level_1(D2_H1_CONTENTS),
    author.para(_CPARA10),
    author.ordered_list(_C_LIST_ITEMS_AFTER_PARA10),
    author.para(_CPARA11),
    author.para(_CPARA12),
    author.para(_CPARA13),
    author.unordered_list(_C_LIST_ITEMS_AFTER_PARA13),
    author.para(_CPARA14),
    author.para(_CPARA15),
    author.unordered_list(_C_LIST_ITEMS_AFTER_PARA15),
    author.para(_CPARA16),
    author.para(_CPARA17),
]
