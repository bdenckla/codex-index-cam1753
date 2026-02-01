import re
from pycmn.my_utils import sl_map


EDITIONS = ("BHQ", "BHL", "DM", "WLC", "UXLC")


def _fill_in(nb_dict):
    full = {e: nb_dict.get(e) or "x" for e in EDITIONS}
    return full


def nb_pair(part):
    """Splits e.g. "xBHL" into ("BHL", "x")"""
    match = re.match(r"^([a-z]+)([A-Z].*)$", part)
    assert match is not None, f"part={part}"
    assert len(match.groups()) == 2
    lower, upper = match.groups()
    return upper, lower


def nb_dict(quirkrec):
    parts = quirkrec["qr-noted-by"].split("-")
    pairs = sl_map(nb_pair, parts)
    sparse_dict = dict(pairs)
    full_dict = _fill_in(sparse_dict)
    return full_dict