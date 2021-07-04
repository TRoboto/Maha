import pytest

from maha.processors import FileProcessor, TextProcessor
from tests.processors.test_base_processor import TestBaseProcessor


class TestTextProcessor(TestBaseProcessor):
    __test__ = True

    @pytest.fixture()
    def processor(self, multiple_tweets: str):
        return TextProcessor.from_string(multiple_tweets, "\n")

    def test_set_lines_list(self, processor):
        newlines = ["hi", "مرحبا"]
        processor.set_lines(newlines)
        assert processor.lines == newlines

    def test_set_lines_text(self, processor):
        text = "hi مرحبا"
        processor.set_lines(text)
        assert len(processor.lines) == 1
        assert processor.text == text

    def test_from_string(self, multiple_tweets):
        processor = TextProcessor.from_string(multiple_tweets)
        assert isinstance(processor, TextProcessor)
        assert len(processor.lines) == 1

    def test_from_string_with_sep(self, multiple_tweets):
        processor = TextProcessor.from_string(multiple_tweets, "\n")
        assert isinstance(processor, TextProcessor)
        assert len(processor.lines) == 9

    def test_from_list(self, multiple_tweets):
        processor = TextProcessor.from_list(multiple_tweets.split("\n"))
        assert isinstance(processor, TextProcessor)
        assert len(processor.lines) == 9

    def test_drop_duplicates(self, processor):
        processor.lines.append(processor.lines[0])
        assert len(processor.lines) == 10
        processor.drop_duplicates()
        assert len(processor.lines) == 9


class TestFileProcessor(TestTextProcessor):
    @pytest.fixture()
    def processor(self, multiple_tweets_file):
        return FileProcessor(multiple_tweets_file)

    def test_init_raises_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            FileProcessor("invalid")

    def test_init_raise_empty_file(self, empty_file):
        with pytest.raises(ValueError):
            FileProcessor(empty_file)
