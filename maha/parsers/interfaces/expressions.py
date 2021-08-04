__all__ = ["Expression", "ExpressionGroup", "ExpressionResult"]
import inspect
from dataclasses import dataclass
from typing import Any, Iterable, List, Optional, Union

import regex as re
from regex.regex import Match

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

    def __call__(self, text: str) -> Iterable["ExpressionResult"]:
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

    def parse(self, match: Match, text: Optional[str]) -> "ExpressionResult":
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

        return ExpressionResult(start, end, value, self)


@dataclass
class ExpressionResult:
    """
    A result of a single expression.
    """

    __slots__ = ["start", "end", "value", "expression"]

    start: int
    """Start index of the matched text"""
    end: int
    """End index of the matched text"""
    value: Any
    """Extracted value"""
    expression: Expression
    """The expression that was used to find the value"""


class ExpressionGroup:
    """A group of expressions that match the same dimension. Expressions are evaluated
    in the order they were added. If ``confident_first`` is ``True``, confident
    expressions are evaluated first in the order they were added and the rest are
    evaluated also in the order they were added.

    Parameters
    ----------
    *expressions : Expression
        List of expressions to match. High-priority expressions should be passed first.
    confident_first : bool, optional
        Whether confident expressions should be evaluated first.
    smart : bool, optional
        Whether to parse the text in a smart way. See :meth:`~.smart_parse`.
    """

    __slots__ = ["expressions", "smart", "_parsed_ranges"]

    def __init__(
        self,
        *expressions: Union[Expression, "ExpressionGroup"],
        smart: bool = False,
    ):

        self.expressions = self.merge_expressions(expressions)
        self._parsed_ranges = set()
        self.smart = smart

    def compile_expressions(self):
        for expression in self.expressions:
            expression.compile()

    def merge_expressions(
        self, expressions: Iterable[Union[Expression, "ExpressionGroup"]]
    ) -> List[Expression]:
        result = []
        for expression in expressions:
            if isinstance(expression, ExpressionGroup):
                result.extend(expression.expressions)
            else:
                result.append(expression)
        return result

    def __getitem__(self, index: int) -> Expression:
        return self.expressions[index]

    def parse(self, text: str) -> Iterable[ExpressionResult]:
        """
        Parses the text.

        Parameters
        ----------
        text : str
            Text to parse.

        Yields
        -------
        :class:`ExpressionResult`
            Extracted value.
        """
        # TODO: Maybe provide a way to clean the text before parsing?
        # (e.g. remove harakat)
        if self.smart:
            yield from self.smart_parse(text)
        else:
            yield from self.normal_parse(text)

        self.clear_parsed()

    def normal_parse(self, text: str) -> Iterable[ExpressionResult]:
        """
        Parse the input ``text`` and return the extracted values.
        """
        for expression in self.expressions:
            yield from expression(text)

    def smart_parse(self, text: str) -> Iterable[ExpressionResult]:
        """
        Parses the text. If a value matches two or more expressions, only the first
        expression parses the value, no value is matched more than once. This means
        high-priority expressions should be passed first.
        """

        for result in self.normal_parse(text):
            if self._is_parsed(result):
                continue
            self._parsed_ranges.add((result.start, result.end))
            yield result

    def _is_parsed(self, result: ExpressionResult):
        for start, end in self._parsed_ranges:
            if start <= result.start <= end and start <= result.end <= end:
                return True

        return False

    def clear_parsed(self):
        self._parsed_ranges = set()

    def __add__(self, other: "ExpressionGroup") -> "ExpressionGroup":
        self.expressions.extend(other.expressions)
        return self
