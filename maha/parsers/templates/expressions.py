__all__ = ["Expression", "ExpressionGroup", "ExpressionResult"]

from dataclasses import dataclass
from typing import Callable, Iterable, List, Optional, Union

import regex as re

from .types import Unit


@dataclass
class Expression:
    __slots__ = ["pattern", "is_confident", "output", "unit"]

    pattern: str
    """Regular expersion(s) to match"""
    is_confident: bool
    """Whether the extracted value 100% belongs to the selected dimension. Some patterns
    may match for values that normally belong to the dimension but not always."""
    output: Optional[Callable[..., str]]
    """
    A function to operate on the extracted value.

    When ``output`` is set to ``None``, the extracted value is returned as-is.
    """
    unit: Optional[Unit]
    """Unit of the dimension"""

    def __init__(
        self,
        pattern: str,
        is_confident: bool = False,
        output: Callable[..., str] = None,
        unit: Optional[Unit] = None,
    ):
        self.pattern = pattern
        self.is_confident = is_confident
        self.unit = unit
        self.output = output

    def format(self, format_spec: str):
        self.pattern = self.pattern.format(format_spec)
        return self

    def set_unit(self, unit: Unit):
        self.unit = unit
        return self

    def __call__(self, text: str) -> Iterable["ExpressionResult"]:
        """
        Extract values from the input ``text``.

        Parameters
        ----------
        text : str
            Text to extract the value from.

        Yields
        -------
        :class:`~ExpressionResult`
            Extracted value.
        """
        for m in re.finditer(self.pattern, text):
            start, end = m.span()
            captured_groups = m.groups()
            if captured_groups:
                value = captured_groups
            else:
                value = text[start:end]

            if self.output is not None:
                value = self.output(value)
            yield ExpressionResult(start, end, value, self)

    def __repr__(self):
        out = f"Expression(pattern={self.pattern}, is_confident={self.is_confident})"
        return out


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
    value: str
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

    __slots__ = ["expressions", "confident_first", "smart", "_parsed_ranges"]

    def __init__(
        self,
        *expressions: Union[Expression, "ExpressionGroup"],
        confident_first: bool = False,
        smart: bool = False,
    ):

        self.confident_first = confident_first
        self.expressions = self.merge_expressions(expressions)
        if confident_first:
            self.expressions = sorted(
                self.expressions,
                key=lambda expression: expression.is_confident,
                reverse=True,
            )

        self._parsed_ranges = set()
        self.smart = smart

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

    def format(self, format_spec: str):
        for expression in self.expressions:
            expression.format(format_spec)
        return self

    def set_unit(self, unit: Unit):
        for expression in self.expressions:
            expression.set_unit(unit)
        return self

    def __repr__(self):
        out = f"ExpressionGroup({self.expressions})"
        return out

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
        :class:`~ExpressionResult`
            Extracted value.
        """
        if self.smart:
            yield from self.smart_parse(text)
        else:
            yield from self.normal_parse(text)

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

    def __add__(self, other: "ExpressionGroup") -> "ExpressionGroup":
        return ExpressionGroup(*self.expressions, *other.expressions)
