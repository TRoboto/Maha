__all__ = ["Expression"]

from dataclasses import dataclass
from typing import Iterable, Optional

import regex as re
from regex.regex import Match

import maha.parsers.interfaces as interfaces

from ..helper import convert_to_number_if_possible


@dataclass
class Expression:
    __slots__ = ["pattern", "_compiled_pattern"]

    pattern: str
    """Regular expersion(s) to match"""

    def __init__(
        self,
        pattern: str,
    ):
        self.pattern = pattern
        self._compiled_pattern = None

    def compile(self):
        if self._compiled_pattern is None:
            self._compiled_pattern = re.compile(self.pattern, re.MULTILINE)

    def __call__(self, text: str) -> Iterable["interfaces.ExpressionResult"]:
        """
        Extract values from the input ``text``.

        Parameters
        ----------
        text : str
            Text to extract the value from.

        Yields
        -------
        :class:`ExpressionResult`
            Extracted value.

        Raises
        ------
        ValueError
            If the output value is not a float or a string.
        """
        self.compile()

        for m in re.finditer(self._compiled_pattern, text):
            yield self.parse(m, text)

    def parse(self, match: Match, text: Optional[str]) -> "interfaces.ExpressionResult":
        """Extract the value from the input ``text`` and return it.

        .. note::
            This is a simple implementation that needs a group to be found.

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
        :class:`ExpressionResult`
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

        captured_groups = list(map(convert_to_number_if_possible, captured_groups))
        if len(captured_groups) == 1:
            captured_groups = captured_groups[0]
        value = captured_groups

        return interfaces.ExpressionResult(start, end, value, self)
