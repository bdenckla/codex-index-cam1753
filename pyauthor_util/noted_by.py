import re
from pycmn.my_utils import sl_map


_DEFAULT = {
    "e:BHQ": "xBHQ",
    "e:BHL": "xBHL",
    "e:DM": "xDM",
    "e:WLC": "xWLC",
    "e:UXLC": "xUXLC",
}
EDITIONS = tuple(k for k in _DEFAULT.keys())


def nb_dict(quirkrec):
    parts = quirkrec["qr-noted-by"].split("-")
    pairs = sl_map(_nb_pair, parts)
    sparse_dict = dict(pairs)
    full_dict = _fill_in(sparse_dict)
    return full_dict


def x_uclc(quirkrec):
    nbd = nb_dict(quirkrec)
    return nbd["e:UXLC"] == "xUXLC"


def _fill_in(nb_dict):
    full = {e: nb_dict.get(e) or _DEFAULT[e] for e in EDITIONS}
    return full


def _nb_pair(part):
    """Turns e.g. "xBHL" into ("e:BHL", "xBHL")"""
    match = re.match(r"^([a-z]+)([A-Z].*)$", part)
    assert match is not None, f"part={part}"
    assert len(match.groups()) == 2
    _lower, upper = match.groups()
    return f"e:{upper}", part
