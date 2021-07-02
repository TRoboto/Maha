""" The base for all processors """

__all__ = [
    "BaseProcessor",
]

from functools import partial
from typing import Callable, List, Union

from maha.cleaners.functions import (
    contains,
    keep,
    normalize,
    remove,
    replace,
    replace_pairs,
    replace_pattern,
)
from maha.utils import negate


class BaseProcessor:
    """Base class for all processors. It contains almost all functions needed for the
    processors.

    Parameters
    ----------
    text : Union[List[str], str]
        A text or list of strings to process
    """

    def __init__(self, text: Union[List[str], str]) -> None:
        self.set_text(text)

    def set_text(self, text: Union[List[str], str]):
        """Overrides the text of the class. Changes ``self.lines``

        Parameters
        ----------
        text : Union[List[str], str]
            A text or list of strings to process
        """
        self.lines = []
        if isinstance(text, str):
            self.lines = [text]
        else:
            self.lines.extend(text)

    @property
    def text(self) -> str:
        """Returns the processed text joined by the newline separator ``\n``

        Returns
        -------
        str
            processed text
        """
        return "\n".join(self.lines)

    def apply(self, fn: Callable[[str], str]):
        """Applies a function to every line

        .. note::
            To be implemented in sub classes.

        Parameters
        ----------
        fn :
            Function to apply
        """
        raise NotImplementedError()

    def filter(self, fn: Callable[[str], bool]):
        """Keeps lines for which input function is True

        .. note::
            To be implemented in sub classes.

        Parameters
        ----------
        fn :
            Function to check
        """
        raise NotImplementedError()

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
        custom_strings: Union[List[str], str] = None,
    ):
        """Applies :func:`~.keep` to every line"""
        self.apply(partial(keep, **self._arguments_except_self(locals())))
        return self

    def normalize(
        self,
        lam_alef: bool = False,
        alef: bool = False,
        waw: bool = False,
        yeh: bool = False,
        teh_marbuta: bool = False,
        ligatures: bool = False,
        spaces: bool = False,
    ):
        """Applies :func:`~.normalize` to every line"""
        self.apply(partial(normalize, **self._arguments_except_self(locals())))
        return self

    def replace(self, strings: Union[List[str], str], with_value: str):
        """Applies :func:`~.replace` to every line"""
        self.apply(partial(replace, **self._arguments_except_self(locals())))
        return self

    def replace_pattern(self, pattern: str, with_value: Union[Callable[..., str], str]):
        """Applies :func:`~.replace_pattern` to every line"""
        self.apply(partial(replace_pattern, **self._arguments_except_self(locals())))
        return self

    def replace_pairs(self, keys: List[str], values: List[str]):
        """Applies :func:`~.replace_pairs` to every line"""
        self.apply(partial(replace_pairs, **self._arguments_except_self(locals())))
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
        custom_strings: Union[List[str], str] = None,
        custom_patterns: Union[List[str], str] = None,
    ):
        """Applies :func:`~.remove` to every line"""
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
        custom_strings: Union[List[str], str] = None,
        custom_patterns: Union[List[str], str] = None,
        operator: str = "or",
    ):
        """Drop lines that contain any of the selected strings or patterns.

        .. note::
            Use ``operator='and'`` to drop lines that contain all selected strings
            or patterns.

        See :func:`~.contain` for arguments description"""

        if operator is None:
            raise ValueError("operator cannot be None")

        self.filter(negate(partial(contains, **self._arguments_except_self(locals()))))

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
        custom_strings: Union[List[str], str] = None,
        custom_patterns: Union[List[str], str] = None,
        operator: str = "or",
    ):
        """Keep lines that contain any of the selected strings or patterns.

        .. note::
            Use ``operator='and'`` to drop lines that contain all selected strings
            or patterns.

        See :func:`~.contain` for arguments description"""

        if operator is None:
            raise ValueError("operator cannot be None")

        self.filter(partial(contains, **self._arguments_except_self(locals())))

        return self

    def _arguments_except_self(self, arguments: dict):
        """Used in combination with local() to return all arguments withoutself"""
        return {k: v for k, v in arguments.items() if k != "self"}
