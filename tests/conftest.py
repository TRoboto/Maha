from pathlib import Path

import pytest


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
def empty_file():
    return "sample_data/empty_file.txt"
