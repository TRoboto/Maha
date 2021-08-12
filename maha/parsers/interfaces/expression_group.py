__all__ = ["ExpressionGroup"]

from typing import Iterable, List, Union

import maha.parsers.interfaces as interfaces
from maha.rexy import non_capturing_group


class ExpressionGroup:
    """A group of expressions that match the same dimension. Expressions are evaluated
    in the order they were added. If ``confident_first`` is ``True``, confident
    expressions are evaluated first in the order they were added and the rest are
    evaluated also in the order they were added.

    Parameters
    ----------
    *expressions : interfaces.Expression
        List of expressions to match. High-priority expressions should be passed first.
    confident_first : bool, optional
        Whether confident expressions should be evaluated first.
    smart : bool, optional
        Whether to parse the text in a smart way. See :meth:`~.smart_parse`.
    """

    __slots__ = ["expressions", "smart", "_parsed_ranges"]

    def __init__(
        self,
        *expressions: Union[interfaces.Expression, "ExpressionGroup"],
        smart: bool = False,
    ):

        self.expressions = self.merge_expressions(expressions)
        self._parsed_ranges = set()
        self.smart = smart

    def compile_expressions(self):
        for expression in self.expressions:
            expression.compile()

    def merge_expressions(
        self, expressions: Iterable[Union[interfaces.Expression, "ExpressionGroup"]]
    ) -> List[interfaces.Expression]:
        result = []
        for expression in expressions:
            if isinstance(expression, ExpressionGroup):
                result.extend(expression.expressions)
            else:
                result.append(expression)
        return result

    def add(self, *expression: interfaces.Expression) -> None:
        """
        Add an expression to the group.
        """
        self.expressions.extend(expression)

    def join(self) -> str:
        """
        Returns non capturing group of the expressions.
        """
        return non_capturing_group(*list(map(str, self.expressions)))

    def parse(self, text: str) -> Iterable["interfaces.ExpressionResult"]:
        """
        Parses the text.

        Parameters
        ----------
        text : str
            Text to parse.

        Yields
        -------
        :class:`interfaces.ExpressionResult`
            Extracted value.
        """
        # TODO: Maybe provide a way to clean the text before parsing?
        # (e.g. remove harakat)
        if self.smart:
            yield from self.smart_parse(text)
        else:
            yield from self.normal_parse(text)

        self.clear_parsed()

    def normal_parse(self, text: str) -> Iterable["interfaces.ExpressionResult"]:
        """
        Parse the input ``text`` and return the extracted values.
        """
        for expression in self.expressions:
            yield from expression(text)

    def smart_parse(self, text: str) -> Iterable["interfaces.ExpressionResult"]:
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

    def _is_parsed(self, result: "interfaces.ExpressionResult"):
        for start, end in self._parsed_ranges:
            if start <= result.start <= end and start <= result.end <= end:
                return True

        return False

    def clear_parsed(self):
        self._parsed_ranges = set()

    def __add__(self, other: "ExpressionGroup") -> "ExpressionGroup":
        self.expressions.extend(other.expressions)
        return self

    def __getitem__(self, index: int) -> interfaces.Expression:
        return self.expressions[index]

    def __len__(self) -> int:
        return len(self.expressions)