import pathlib

import pytest

from maha.constants import EMPTY
from maha.processors import StreamFileProcessor, StreamTextProcessor
from tests.processors.test_base_processor import TestBaseProcessor


class TestStreamTextProcessor(TestBaseProcessor):
    __test__ = True

    @pytest.fixture()
    def processor(self, multiple_tweets: str):
        return StreamTextProcessor(multiple_tweets.split("\n"))

    def get_processed_lines(self, proc):
        return list(proc.process())[0]

    def get_processed_text(self, proc):
        return "\n".join(self.get_processed_lines(proc))

    def test_drop_empty_lines(self, multiple_tweets):
        processor = StreamTextProcessor(multiple_tweets.split("\n") + [""])
        assert len(list(processor.get_lines())[0]) == 10
        assert processor.drop_empty_lines() is processor
        assert len(self.get_processed_lines(processor)) == 9

    def test_process_without_functions(self, processor):

        with pytest.raises(ValueError):
            list(processor.process())

    def test_stream(self, processor):
        processor.drop_lines_contain(arabic=True)
        assert len(list(processor.get_lines())[0]) == 9
        assert len(self.get_processed_lines(processor)) == 3

    def test_piping(self, processor):
        processor.filter_lines_contain(arabic=True).drop_lines_contain(
            english_letters=True, hashtags=True
        )
        assert len(self.get_processed_lines(processor)) == 3


class TestStreamFileProcessor(TestStreamTextProcessor):

    # Disable inhereted test
    test_drop_empty_lines = None

    @pytest.fixture()
    def processor(self, multiple_tweets_file):
        return StreamFileProcessor(multiple_tweets_file)

    def test_init_raises_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            StreamFileProcessor("invalid")

    def test_process_and_save(
        self,
        surah_al_ala_file: pathlib.Path,
        surah_al_ala_processed_file: pathlib.Path,
        tmp_path: pathlib.Path,
    ):
        processor = StreamFileProcessor(surah_al_ala_file)
        tmpfile = tmp_path / "tmp.txt"
        processor.normalize(all=True, yeh=False, waw=False).keep(
            arabic_letters=True
        ).drop_empty_lines()
        processor.process_and_save(tmpfile)

        assert tmpfile.read_text("utf8") == surah_al_ala_processed_file.read_text(
            "utf8"
        )

    def test_process_and_save_raises_file_exists_error(
        self, processor, surah_al_ala_processed_file
    ):
        with pytest.raises(FileExistsError):
            processor.process_and_save(surah_al_ala_processed_file)

    def test_process_and_save_override(self, processor, tmp_path):
        tmpfile = tmp_path / "tmp.txt"
        processor.keep(arabic=True)
        processor.process_and_save(str(tmpfile))
        processor.process_and_save(tmpfile, override=True)

    def test_processor_with_string_path(self, multiple_tweets_file):
        processor = StreamFileProcessor(str(multiple_tweets_file))
        assert len(list(processor.get_lines())[0]) == 9

    def test_processor_with_empty_returns(
        self, multiple_tweets_file, tmp_path: pathlib.Path
    ):
        tmpfile = tmp_path / "tmp.txt"
        processor = StreamFileProcessor(str(multiple_tweets_file))
        processor.keep(custom_strings="hello")
        processor.process_and_save(str(tmpfile))

        assert tmpfile.read_text() == EMPTY
