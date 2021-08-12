from pathlib import Path

import pytest

from maha.parsers import EXPRESSION_DURATION, EXPRESSION_NUMERAL


@pytest.fixture()
def simple_text_input():
    return " 1. بِسْمِ،اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ In the name of Allah,Most Gracious, Most Merciful. "


@pytest.fixture()
def multiple_tweets(multiple_tweets_file: Path):
    return multiple_tweets_file.open(encoding="utf8").read()


@pytest.fixture()
def multiple_tweets_file():
    return Path("sample_data/tweets.txt")


@pytest.fixture()
def surah_al_ala_file():
    return Path("sample_data/surah_al-ala.txt")


@pytest.fixture()
def surah_al_ala_processed_file():
    return Path("sample_data/surah_al-ala_processed.txt")


@pytest.fixture()
def empty_file():
    return "sample_data/empty_file.txt"


@pytest.fixture(scope="session", autouse=True)
def compile_parse_expressions():
    EXPRESSION_DURATION.compile_expressions()
    EXPRESSION_NUMERAL.compile_expressions()
