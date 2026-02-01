from pyauthor_util.noted_by import nb_dict
from pycmn.my_utils import dv_map


def _bhq_and_t3o(quirkrec):
    """t3o: the three others (BHL, DM, & WLC)"""
    nbd = nb_dict(quirkrec)
    t30 = nbd["e:BHL"], nbd["e:DM"], nbd["e:WLC"]
    return nbd["e:BHQ"], t30


def _startswith_n(part):
    return part.startswith("n")


def _startswith_x(part):
    return part.startswith("x")


def _foobhq_and_n3(foobhq, quirkrec):
    bhq, t3o = _bhq_and_t3o(quirkrec)
    return bhq == foobhq and any(_startswith_n(part) for part in t3o)


def _foobhq_and_x3(foobhq, quirkrec):
    bhq, t3o = _bhq_and_t3o(quirkrec)
    return bhq == foobhq and all(_startswith_x(part) for part in t3o)


def _nbhq_and_n3(quirkrec):
    return _foobhq_and_n3("nBHQ", quirkrec)


def _nbhq_and_x3(quirkrec):
    return _foobhq_and_x3("nBHQ", quirkrec)


def _xbhq_and_n3(quirkrec):
    return _foobhq_and_n3("xBHQ", quirkrec)


def _tbhq_and_n3(quirkrec):
    return _foobhq_and_n3("tBHQ", quirkrec)


def _tbhq_and_zwd(quirkrec):
    nbd = nb_dict(quirkrec)
    return nbd["e:WLC"] == "zdexiWLC"

    
def _tbhq_and_zwm(quirkrec):
    nbd = nb_dict(quirkrec)
    return nbd["e:WLC"] == "zmiscWLC"

def _xbhq_and_nuxlc(quirkrec):
    nbd = nb_dict(quirkrec)
    return nbd["e:UXLC"] == "nUXLC"


def _tbhq_and_zuxlc(quirkrec):
    nbd = nb_dict(quirkrec)
    return nbd["e:UXLC"] == "zUXLC"


def _filter(quirkrecs, filter_fn):
    return list(filter(filter_fn, quirkrecs))


_FILTER_FNS = {
    "nbhq_and_x3": _nbhq_and_x3,
    "nbhq_and_n3": _nbhq_and_n3,
    "xbhq_and_n3": _xbhq_and_n3,
    "tbhq_and_n3": _tbhq_and_n3,
    "tbhq_and_zwd": _tbhq_and_zwd,
    "tbhq_and_zwm": _tbhq_and_zwm,
    "xbhq_and_nuxlc": _xbhq_and_nuxlc,
    "tbhq_and_zuxlc": _tbhq_and_zuxlc,
}
# nbhq: noted (as a quirk) in BHQ
# xbhq: not noted (as a quirk) in BHQ
# n3, noted (as a quirk) in one of "the three"
# x3: not noted (as a quirk) in one of "the three"
# zw (zmiscWLC): noted (as consensus) by WLC (combined with MAM):
#     flagged as a change in WLC relative to BHS, e.g. a bracket-c or bracket-v note.
#     comparison with MAM revealed that it is a change back towards consensus,
#     i.e. this is BHS/BHQ proposing a quirk that is not in μL (according to WLC at least)


def get_qr_groups(quirkrecs):
    groups = dv_map((_filter, quirkrecs), _FILTER_FNS)
    return groups
