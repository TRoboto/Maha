""" The base for all processors """
from __future__ import annotations

__all__ = [
    "BaseProcessor",
]


from abc import ABC, abstractmethod
from functools import partial
from typing import Callable

from maha.cleaners.functions import (
    connect_single_letter_word,
    contains,
    contains_repeated_substring,
    contains_single_letter_word,
    keep,
    normalize,
    reduce_repeated_substring,
    remove,
    replace,
    replace_expression,
    replace_pairs,
)
from maha.rexy import Expression, ExpressionGroup

from .utils import ObjectGet


class BaseProcessor(ABC):
    """Base class for all processors. It contains almost all functions needed for the
    processors.

    Parameters
    ----------
    text : Union[List[str], str]
        A text or list of strings to process
    """

    @abstractmethod
    def get_lines(self, n_lines: int = 100):
        """Returns a generator of list of strings with length of ``n_lines``

        Parameters
        ----------
        n_lines : int
            Number of lines to yield, Defaults to 100

        Yields
        -------
        List[str]
            List of strings with length of ``n_lines``. The last list maybe of length
            less than ``n_lines``.
        """
        raise NotImplementedError()

    @abstractmethod
    def apply(self, fn: Callable[[str], str]):
        """Applies a function to each line

        Parameters
        ----------
        fn :
            Function to apply
        """
        raise NotImplementedError()

    @abstractmethod
    def filter(self, fn: Callable[[str], bool]):
        """Keeps lines for which the input function is True

        Parameters
        ----------
        fn :
            Function to check
        """
        raise NotImplementedError()

    def get(
        self,
        unique_characters: bool = False,
        character_length: bool = False,
        word_length: bool = False,
    ):
        """Returns statistics about the provided text

        Parameters
        ----------
        unique_characters : bool, optional
            Return all unique characters, by default False
        character_length : bool, optional
            Return the character length of each string, by default False
        word_length : bool, optional
            Return the word length of each string (split by space), by default False

        Returns
        -------
        Union[Dict[str, Any], Any]
            * If one argument is set to True, its value is return
            * If more than one argument is set to True, a dictionary is returned where
                keys are the True passed arguments with the corresponding values

        """

        objects = []
        if unique_characters:
            objects.append(
                ObjectGet(
                    func=lambda prev, current: prev | set(current),
                    prev=set(),
                    name="unique_characters",
                    post_fn=list,
                )
            )

        if character_length:
            objects.append(
                ObjectGet(
                    func=lambda prev, current: prev + [len(current)],
                    prev=[],
                    name="character_length",
                )
            )

        if word_length:
            objects.append(
                ObjectGet(
                    func=lambda prev, current: prev + [len(current.split())],
                    prev=[],
                    name="word_length",
                )
            )
        for line in self.get_lines(1):
            line = line[0]
            for obj in objects:
                obj.prev = obj.func(obj.prev, line)

        output = {}
        if len(objects) == 1:
            output = objects[0].post_fn(objects[0].prev)
        else:
            for obj in objects:
                output[obj.name] = obj.post_fn(obj.prev)

        return output

    def print_unique_characters(self):
        """Prints all unique characters in the text"""
        unique = self.get(unique_characters=True)
        print(f"{len(unique)} unique characters were found, they are:")
        print(unique)
        return self

    def keep(
        self,
        arabic: bool = False,
        english: bool = False,
        arabic_letters: bool = False,
        english_letters: bool = False,
        english_small_letters: bool = False,
        english_capital_letters: bool = False,
        numbers: bool = False,
        harakat: bool = False,
        all_harakat: bool = False,
        punctuations: bool = False,
        arabic_numbers: bool = False,
        english_numbers: bool = False,
        arabic_punctuations: bool = False,
        english_punctuations: bool = False,
        use_space: bool = True,
        custom_strings: list[str] | str | None = None,
    ):
        """Applies :func:`~.keep` to each line"""
        self.apply(partial(keep, **self._arguments_except_self(locals())))
        return self

    def normalize(
        self,
        lam_alef: bool | None = None,
        alef: bool | None = None,
        waw: bool | None = None,
        yeh: bool | None = None,
        teh_marbuta: bool | None = None,
        ligatures: bool | None = None,
        spaces: bool | None = None,
        all: bool | None = None,
    ):
        """Applies :func:`~.normalize` to each line"""
        self.apply(partial(normalize, **self._arguments_except_self(locals())))
        return self

    def connect_single_letter_word(
        self,
        waw: bool | None = None,
        feh: bool | None = None,
        beh: bool | None = None,
        lam: bool | None = None,
        kaf: bool | None = None,
        teh: bool | None = None,
        all: bool | None = None,
        custom_strings: list[str] | str | None = None,
    ):
        """Applies :func:`~.connect_single_letter_word` to each line"""
        self.apply(
            partial(connect_single_letter_word, **self._arguments_except_self(locals()))
        )
        return self

    def replace(self, strings: list[str] | str, with_value: str):
        """Applies :func:`~.replace` to each line"""
        self.apply(partial(replace, **self._arguments_except_self(locals())))
        return self

    def replace_expression(
        self,
        expression: Expression | ExpressionGroup | str,
        with_value: Callable[..., str] | str,
    ):
        """Applies :func:`~.replace_expression` to each line"""
        self.apply(partial(replace_expression, **self._arguments_except_self(locals())))
        return self

    def replace_pairs(self, keys: list[str], values: list[str]):
        """Applies :func:`~.replace_pairs` to each line"""
        self.apply(partial(replace_pairs, **self._arguments_except_self(locals())))
        return self

    def reduce_repeated_substring(self, min_repeated: int = 3, reduce_to: int = 2):
        """Applies :func:`~.reduce_repeated_substring` to each line"""
        self.apply(
            partial(reduce_repeated_substring, **self._arguments_except_self(locals()))
        )
        return self

    def remove(
        self,
        arabic: bool = False,
        english: bool = False,
        arabic_letters: bool = False,
        english_letters: bool = False,
        english_small_letters: bool = False,
        english_capital_letters: bool = False,
        numbers: bool = False,
        harakat: bool = False,
        all_harakat: bool = False,
        tatweel: bool = False,
        punctuations: bool = False,
        arabic_numbers: bool = False,
        english_numbers: bool = False,
        arabic_punctuations: bool = False,
        english_punctuations: bool = False,
        arabic_ligatures: bool = False,
        arabic_hashtags: bool = False,
        arabic_mentions: bool = False,
        emails: bool = False,
        english_hashtags: bool = False,
        english_mentions: bool = False,
        hashtags: bool = False,
        links: bool = False,
        mentions: bool = False,
        emojis: bool = False,
        use_space: bool = True,
        custom_strings: list[str] | str | None = None,
        custom_expressions: list[str] | str | None = None,
    ):
        """Applies :func:`~.remove` to each line"""
        self.apply(partial(remove, **self._arguments_except_self(locals())))
        return self

    def drop_lines_contain(
        self,
        arabic: bool = False,
        english: bool = False,
        arabic_letters: bool = False,
        english_letters: bool = False,
        english_small_letters: bool = False,
        english_capital_letters: bool = False,
        numbers: bool = False,
        harakat: bool = False,
        all_harakat: bool = False,
        tatweel: bool = False,
        lam_alef_variations: bool = False,
        lam_alef: bool = False,
        punctuations: bool = False,
        arabic_numbers: bool = False,
        english_numbers: bool = False,
        arabic_punctuations: bool = False,
        english_punctuations: bool = False,
        arabic_ligatures: bool = False,
        persian: bool = False,
        arabic_hashtags: bool = False,
        arabic_mentions: bool = False,
        emails: bool = False,
        english_hashtags: bool = False,
        english_mentions: bool = False,
        hashtags: bool = False,
        links: bool = False,
        mentions: bool = False,
        emojis: bool = False,
        custom_strings: list[str] | str | None = None,
        custom_expressions: list[str] | str | None = None,
        operator: str = "or",
    ):
        """Drop lines that contain any of the selected strings or patterns.

        .. note::
            Use ``operator='and'`` to drop lines that contain all selected strings
            or patterns.

        See :func:`~.contains` for arguments description"""

        if operator is None:
            raise ValueError("operator cannot be None")

        arguments = locals()
        self.filter(
            lambda text: not contains(text, **self._arguments_except_self(arguments))
        )

        return self

    def drop_empty_lines(self):
        """Drop empty lines."""
        return self.drop_lines_below_len(1)

    def drop_lines_below_len(self, length: int, word_level=False):
        """Drop lines with a number of characters/words less than the input ``length``

        Parameters
        ----------
        length : int
            Number of characters/words
        word_level : bool, optional
            True to switch to word level, which splits the text by space,
            by default False
        """
        self.filter(
            lambda line: (len(line.split()) if word_level else len(line)) >= length
        )
        return self

    def drop_lines_above_len(self, length: int, word_level=False):
        """Drop lines with a number of characters/words more than the input ``length``

        Parameters
        ----------
        length : int
            Number of characters/words
        word_level : bool, optional
            True to switch to word level, which splits the text by space,
            by default False
        """
        filter_fn = (
            lambda line: (len(line.split()) if word_level else len(line)) <= length
        )
        self.filter(filter_fn)
        return self

    def drop_lines_contain_repeated_substring(self, repeated=3):
        """Drop lines containing a number of consecutive repeated substrings

        Parameters
        ----------
        repeated : int, optional
            Minimum number of repetitions, by default 3

        """
        self.filter(lambda line: not contains_repeated_substring(line, repeated))
        return self

    def drop_lines_contain_single_letter_word(
        self,
        arabic_letters: bool = False,
        english_letters: bool = False,
    ):
        """Drop lines containing a single-letter word (e.g."محمد و احمد" or
        "how r u"). In Arabic, single-letter words are rare.

        .. warning::
            In English, all lines containing the letter "I" will be dropped since it is
            considered a single-letter word

        See :func:`~.contains_single_letter_word`.
        See also :func:`~.connect_single_letter_word`.
        """

        arguments = locals()
        self.filter(
            lambda text: not contains_single_letter_word(
                text, **self._arguments_except_self(arguments)
            )
        )
        return self

    def filter_lines_contain(
        self,
        arabic: bool = False,
        english: bool = False,
        arabic_letters: bool = False,
        english_letters: bool = False,
        english_small_letters: bool = False,
        english_capital_letters: bool = False,
        numbers: bool = False,
        harakat: bool = False,
        all_harakat: bool = False,
        tatweel: bool = False,
        lam_alef_variations: bool = False,
        lam_alef: bool = False,
        punctuations: bool = False,
        arabic_numbers: bool = False,
        english_numbers: bool = False,
        arabic_punctuations: bool = False,
        english_punctuations: bool = False,
        arabic_ligatures: bool = False,
        persian: bool = False,
        arabic_hashtags: bool = False,
        arabic_mentions: bool = False,
        emails: bool = False,
        english_hashtags: bool = False,
        english_mentions: bool = False,
        hashtags: bool = False,
        links: bool = False,
        mentions: bool = False,
        emojis: bool = False,
        custom_strings: list[str] | str | None = None,
        custom_expressions: list[str] | str | None = None,
        operator: str = "or",
    ):
        """Keep lines that contain any of the selected strings or patterns.

        .. note::
            Use ``operator='and'`` to drop lines that contain all selected strings
            or patterns.

        See :func:`~.contains` for arguments description"""

        if operator is None:
            raise ValueError("operator cannot be None")

        arguments = locals()
        self.filter(
            lambda text: bool(contains(text, **self._arguments_except_self(arguments)))
        )
        return self

    def _arguments_except_self(self, arguments: dict):
        """Used in combination with local() to return all arguments withoutself"""
        return {k: v for k, v in arguments.items() if k not in ["self", "arguments"]}
