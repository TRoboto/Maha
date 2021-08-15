import itertools as it
from pprint import pprint

from maha.parsers.functions import parse_dimension
from maha.parsers.interfaces.enums import DurationUnit


def test_parse_numeral_wiki_arlang(wiki_arlang):
    numerals = parse_dimension(wiki_arlang, numeral=True)
    assert len(numerals) == 12
    assert numerals[0].value == 467000000
    assert numerals[-1].value == 29


def test_parse_numeral_wiki_arnumbers(wiki_arnumbers):
    numerals = parse_dimension(wiki_arnumbers, numeral=True)
    for d, e in zip(numerals[:8], it.cycle((178, 43, 1997))):
        assert d.value == e
    for d, e in zip(numerals[13:18], (65, 1992, 13, 1995)):
        assert d.value == e
    for d, e in zip(
        numerals[-17:-2], (311, 99, 5, 2, 11, 8, 311, 99, 5, 11, 311, 99, 5, 5, 11)
    ):
        assert d.value == e


def test_parse_duration_wiki_arnumbers(wiki_arnumbers):
    durations = parse_dimension(wiki_arnumbers, duration=True)
    assert len(durations) == 17

    for d, e in zip(durations[-6:], it.cycle((2, 11))):
        assert len(d.value) == 1
        assert d.value[0].unit == DurationUnit.HOURS
        assert d.value[0].value == e
