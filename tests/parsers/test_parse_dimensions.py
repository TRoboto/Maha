from maha.parsers.functions import parse_dimension


def test_parse_numeral_wiki(wiki_arlang):
    numerals = parse_dimension(wiki_arlang, numeral=True)
    assert len(numerals) == 12
    assert numerals[0].value == 467000000
    assert numerals[-1].value == 29
