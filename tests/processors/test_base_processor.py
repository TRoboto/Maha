from typing import Generator, Type

import pytest

from maha.constants import (
    ALEF_VARIATIONS,
    ARABIC_LETTERS,
    ARABIC_LIGATURES,
    ENGLISH_LETTERS,
    PATTERN_HASHTAGS,
    TEH_MARBUTA,
)
from maha.processors import BaseProcessor
from tests.utils import list_not_in_string, list_only_in_string


def test_base_processor_initialization():
    with pytest.raises(TypeError):
        BaseProcessor()


class TestBaseProcessor:
    __test__ = False

    def get_processed_lines(self, proc):
        raise NotImplementedError()

    def get_processed_text(self, proc):
        raise NotImplementedError

    def test_lines_correct(self, processor: BaseProcessor):
        assert len(list(processor.get_lines(1))) == 9

    def test_get_lines(self, processor: BaseProcessor):
        lines = processor.get_lines(1)
        assert isinstance(lines, Generator)
        line = next(lines)
        assert len(line) == 1
        assert len(list(lines)) == 8

    def test_get_lines_more_than_one(self, processor: BaseProcessor):
        lines = processor.get_lines(6)
        assert len(next(lines)) == 6
        assert len(next(lines)) == 3

    def test_apply(self, processor: BaseProcessor):
        processor.apply(lambda l: l.replace("#Windows11", "Windows11"))
        assert "#Windows11" not in self.get_processed_text(processor)
        assert "Windows11" in self.get_processed_text(processor)

    def test_filter(self, processor: BaseProcessor):
        processor.filter(lambda l: "الصلاة" in l)
        assert len(self.get_processed_lines(processor)) == 1

    def test_get_with_unique_characters(self, processor: BaseProcessor):
        unique_chars = processor.get(unique_characters=True)
        assert isinstance(unique_chars, list)
        assert len(unique_chars) == 91

    def test_get_with_word_length(self, processor: BaseProcessor):
        word_length = processor.get(word_length=True)
        assert isinstance(word_length, list)
        assert len(word_length) == 9
        assert word_length == [17, 37, 19, 8, 7, 8, 12, 3, 11]

    def test_get_with_character_length(self, processor: BaseProcessor):
        char_length = processor.get(character_length=True)
        assert isinstance(char_length, list)
        assert len(char_length) == 9
        assert char_length == [85, 212, 98, 50, 33, 46, 69, 29, 73]

    def test_get_with_more_than_one_input(self, processor: BaseProcessor):
        outputs = processor.get(character_length=True, word_length=True)
        assert isinstance(outputs, dict)
        assert len(outputs) == 2
        assert "character_length" in outputs
        assert "word_length" in outputs

    def test_print_unique_characters(self, processor: BaseProcessor):
        assert processor.print_unique_characters() is processor

    def test_keep(self, processor: BaseProcessor):
        assert processor.keep(arabic_letters=True) is processor
        assert len(self.get_processed_lines(processor)) == 9
        assert len([l for l in self.get_processed_lines(processor) if l]) == 6
        assert all(
            [
                list_only_in_string(ARABIC_LETTERS, line)
                for line in self.get_processed_lines(processor)
            ]
        )

    def test_normalize(self, processor: BaseProcessor):
        assert processor.normalize(alef=True, teh_marbuta=True) is processor
        assert len(self.get_processed_lines(processor)) == 9
        assert list_not_in_string(
            ALEF_VARIATIONS[1:] + [TEH_MARBUTA], self.get_processed_text(processor)
        )

    def test_normalize_all(self, processor: BaseProcessor):
        processor.normalize(all=True, teh_marbuta=False)
        assert len(self.get_processed_lines(processor)) == 9
        assert TEH_MARBUTA in self.get_processed_text(processor)
        assert list_not_in_string(
            ALEF_VARIATIONS[1:] + ARABIC_LIGATURES, self.get_processed_text(processor)
        )

    def test_connect_single_letter_word(self, processor: BaseProcessor):
        assert processor.connect_single_letter_word(all=True) is processor
        assert len(self.get_processed_lines(processor)) == 9
        processor.drop_lines_contain_single_letter_word()
        assert len(self.get_processed_lines(processor)) == 6

    def test_replace(self, processor: BaseProcessor):
        assert processor.replace(["#Windows11", "12:00"], "TEST") is processor
        assert len(self.get_processed_lines(processor)) == 9
        assert self.get_processed_text(processor).count("TEST") == 2
        assert list_not_in_string(
            ["#Windows11", "12:00"], self.get_processed_text(processor)
        )

    def test_replace_pattern(self, processor: BaseProcessor):
        assert processor.replace_pattern(PATTERN_HASHTAGS, "HASHTAG") is processor
        assert len(self.get_processed_lines(processor)) == 9
        assert self.get_processed_text(processor).count("HASHTAG") == 6
        assert "#Windows11" not in self.get_processed_text(processor)

    def test_replace_pairs(self, processor: BaseProcessor):
        assert (
            processor.replace_pairs(["#Windows11", "12:00"], ["Windows11", "12"])
            is processor
        )
        assert len(self.get_processed_lines(processor)) == 9
        assert "Windows11" in self.get_processed_text(processor)
        assert "12" in self.get_processed_text(processor)
        assert "#Windows11" not in self.get_processed_text(processor)
        assert "12:00" not in self.get_processed_text(processor)

    def test_reduce_repeated_substring(self, processor: BaseProcessor):
        assert processor.reduce_repeated_substring() is processor
        assert len(self.get_processed_lines(processor)) == 9
        assert "هه" in self.get_processed_text(processor)
        assert "ههه" not in self.get_processed_text(processor)

    def test_remove(self, processor: BaseProcessor):
        assert processor.remove(hashtags=True) is processor
        assert len(self.get_processed_lines(processor)) == 9
        assert "#" not in self.get_processed_text(processor)

    def test_drop_lines_contain(self, processor: BaseProcessor):
        assert (
            processor.drop_lines_contain(arabic_ligatures=True, english_letters=True)
            is processor
        )
        assert len(self.get_processed_lines(processor)) == 3
        assert list_not_in_string(
            ARABIC_LIGATURES + ENGLISH_LETTERS, self.get_processed_text(processor)
        )

    def test_drop_lines_contain_with_and(self, processor: BaseProcessor):
        assert (
            processor.drop_lines_contain(
                arabic_ligatures=True, english_letters=True, operator="and"
            )
            is processor
        )
        assert len(self.get_processed_lines(processor)) == 9
        processor.drop_lines_contain(arabic_ligatures=True, emojis=True, operator="and")
        assert len(self.get_processed_lines(processor)) == 8

    def test_drop_lines_contain_raises_valueerror(self, processor: BaseProcessor):
        with pytest.raises(ValueError):
            processor.drop_lines_contain(arabic_ligatures=True, operator=None)

    def test_drop_empty_lines_no_empty(self, processor: BaseProcessor):
        assert processor.drop_empty_lines() is processor
        assert len(self.get_processed_lines(processor)) == 9

    def test_drop_lines_below_len(self, processor: BaseProcessor):
        assert processor.drop_lines_below_len(69) is processor
        assert len(self.get_processed_lines(processor)) == 5

    def test_drop_lines_below_len_word_level(self, processor: BaseProcessor):
        assert processor.drop_lines_below_len(7, word_level=True) is processor
        assert len(self.get_processed_lines(processor)) == 8
        processor.drop_lines_below_len(8, word_level=True)
        assert len(self.get_processed_lines(processor)) == 7

    def test_drop_lines_above_len(self, processor: BaseProcessor):
        assert processor.drop_lines_above_len(85) is processor
        assert len(self.get_processed_lines(processor)) == 7

    def test_drop_lines_above_len_word_level(self, processor: BaseProcessor):
        assert processor.drop_lines_above_len(17, word_level=True) is processor
        assert len(self.get_processed_lines(processor)) == 7
        processor.drop_lines_above_len(16, word_level=True)
        assert len(self.get_processed_lines(processor)) == 6

    def test_drop_lines_with_repeated_substring(self, processor: BaseProcessor):
        assert processor.drop_lines_contain_repeated_substring(3) is processor
        assert len(self.get_processed_lines(processor)) == 8

    def test_drop_lines_contain_single_letter_word(self, processor: BaseProcessor):
        assert processor.drop_lines_contain_single_letter_word() is processor
        assert len(self.get_processed_lines(processor)) == 4

    def test_filter_lines_contain(self, processor: BaseProcessor):
        assert (
            processor.filter_lines_contain(arabic_ligatures=True, english_letters=True)
            is processor
        )
        assert len(self.get_processed_lines(processor)) == 6

    def test_filter_lines_contain_with_and(self, processor: BaseProcessor):
        assert (
            processor.filter_lines_contain(
                arabic_ligatures=True, emojis=True, operator="and"
            )
            is processor
        )
        assert len(self.get_processed_lines(processor)) == 1
        processor.filter_lines_contain(
            arabic_ligatures=True, english_letters=True, operator="and"
        )
        assert len(self.get_processed_lines(processor)) == 0

    def test_filter_lines_contain_raises_value_error(self, processor: BaseProcessor):
        with pytest.raises(ValueError):
            processor.filter_lines_contain(arabic_ligatures=True, operator=None)
