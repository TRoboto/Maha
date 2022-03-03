from __future__ import annotations

__all__ = ["Expression"]


import hashlib
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

import regex as re
from regex import Match, Pattern

from maha import LIBRARY_PATH

from .expression_result import ExpressionResult

CACHE_PATH = Path(LIBRARY_PATH) / "rexy" / "cache"


@dataclass
class Expression:
    """Regex pattern holder.

    Parameters
    ----------
    pattern : str
        Regular expression pattern.
    pickle : bool
        If ``True``, the compiled pattern will be pickled. This is useful to save
        compilation time for large patterns.
    """

    __slots__ = ["pattern", "_compiled_pattern", "pickle"]

    pattern: str
    """Regular expersion(s) to match"""

    def __init__(
        self,
        pattern: str,
        pickle: bool = False,
    ):
        self.pattern = str(pattern)
        self.pickle = pickle
        self._compiled_pattern: Pattern[str] = None  # type: ignore

    def compile(self):
        """Compile the regular expersion."""
        if self._compiled_pattern is None:
            if self.pickle:
                self._load_compiled_pattern()
            else:
                self._compiled_pattern = re.compile(self.pattern, re.MULTILINE)

    def _load_compiled_pattern(self):
        # crp: compiled regex pattern
        path = CACHE_PATH / f"{hash(self)}.crp"
        if path.exists():
            with path.open("rb") as f:
                self._compiled_pattern = pickle.load(f)
        else:
            self._compiled_pattern = re.compile(self.pattern, re.MULTILINE)
            with path.open("wb") as f:
                pickle.dump(self._compiled_pattern, f)

    @classmethod
    def from_cache(cls, cache: str) -> Expression:
        """Load an expression from cache.

        Parameters
        ----------
        cache : str
            Name of the cache file.

        Returns
        -------
        :class:`~.Expression`
            Expression.
        """
        try:
            expression = cls("names")
            with open(CACHE_PATH / f"{cache}.crp", "rb") as f:
                expression._compiled_pattern = pickle.load(f)
            return expression
        except FileNotFoundError:
            raise ValueError(f"Cache file {cache} not found")

    def search(self, text: str):
        """Search for the pattern in the input ``text``.

        Parameters
        ----------
        text : str
            Text to search in.

        Returns
        -------
        :class:`regex.Match`
            Matched object.
        """
        self.compile()
        return self._compiled_pattern.search(text)

    def match(self, text: str) -> Match[str] | None:
        """Match the pattern in the input ``text``.

        Parameters
        ----------
        text : str
            Text to match in.

        Returns
        -------
        :class:`Match[str]`
            Matched object.
        """
        self.compile()
        return self._compiled_pattern.match(text)

    def fullmatch(self, text: str) -> Match[str] | None:
        """Match the pattern in the input ``text``.

        Parameters
        ----------
        text : str
            Text to match in.

        Returns
        -------
        :class:`Match[str]`
            Matched object.
        """
        self.compile()
        return self._compiled_pattern.fullmatch(text)

    def sub(self, repl: Callable[..., str] | str, text: str) -> str:
        """Replace all occurrences of the pattern in the input ``text``.

        Parameters
        ----------
        repl : str
            Replacement string.
        text : str
            Text to replace.

        Returns
        -------
        str
            Text with replaced occurrences.
        """
        self.compile()
        return self._compiled_pattern.sub(repl, text)

    def __call__(self, text: str) -> Iterable[ExpressionResult]:
        """
        Extract values from the input ``text``.

        Parameters
        ----------
        text : str
            Text to extract the value from.

        Yields
        -------
        :class:`~.ExpressionResult`
            Extracted value.
        """
        yield from self.parse(text)

    def parse(self, text: str) -> Iterable[ExpressionResult]:
        """
        Extract values from the input ``text``.

        Parameters
        ----------
        text : str
            Text to extract the value from.

        Yields
        -------
        :class:`~.ExpressionResult`
            Extracted value.
        """
        self.compile()

        for m in re.finditer(self._compiled_pattern, text):
            yield self._parse(m, text)

    def _parse(self, match: Match[str], _: str) -> ExpressionResult:
        """Extract the value from the input ``text`` and return it.

        .. note::
            This is a simple implementation that needs a group to match.

        .. warning::
            This method is called by :meth:`__call__` to extract the value from
            the input ``text``. You should not call this method directly.


        Parameters
        ----------
        match : :class:`regex.Match`
            Matched object.
        text : str
            Text in which the match was found.

        Yields
        -------
        :class:`~.ExpressionResult`
            Extracted value.

        Raises
        ------
        ValueError
            If no capture group was found.

        """
        start, end = match.span()

        captured_groups = match.groups()

        if captured_groups is None:
            raise ValueError("No captured groups")

        if len(captured_groups) == 1:
            captured_groups = captured_groups[0]
        value = captured_groups

        return ExpressionResult(start, end, value, self)

    def __str__(self) -> str:
        return self.pattern

    def __add__(self, other: str | Expression) -> str:
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)

    def __hash__(self):
        return int(hashlib.md5(self.pattern.encode()).hexdigest(), 16)
