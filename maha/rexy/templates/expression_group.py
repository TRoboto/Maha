from __future__ import annotations

__all__ = ["ExpressionGroup"]


from typing import Iterable, overload

import maha.rexy as rx


class ExpressionGroup:
    """A group of expressions that match the same dimension. Expressions are evaluated
    in the order they were added.

    Parameters
    ----------
    *expressions :
        List of expressions to match. High-priority expressions should be passed first.
    smart : bool, optional
        Whether to parse the text in a smart way. See :meth:`~.smart_parse`.
    """

    __slots__ = ["expressions", "smart", "_parsed_ranges"]

    def __init__(
        self,
        *expressions: rx.Expression | ExpressionGroup,
        smart: bool = False,
    ):

        self.expressions = self._merge_expressions(expressions)
        self._parsed_ranges: set[tuple[int, int]] = set()
        self.smart = smart

    def compile_expressions(self):
        for expression in self.expressions:
            expression.compile()

    def _merge_expressions(
        self, expressions: Iterable[rx.Expression | ExpressionGroup]
    ) -> list[rx.Expression]:
        result = []
        for expression in expressions:
            if isinstance(expression, ExpressionGroup):
                result.extend(expression.expressions)
            else:
                result.append(expression)
        return result

    def add(self, *expression: rx.Expression) -> None:
        """Add an expression to the group.

        Parameters
        ----------
        *expression :
            Expressions to add.
        """
        self.expressions.extend(expression)

    def join(self) -> str:
        """Returns non capturing group of the expressions.

        Returns
        -------
        str
            Non capturing group of the patterns.
        """
        return rx.non_capturing_group(*list(map(str, self.expressions)))

    def get_matched_expression(self, text: str) -> rx.Expression | None:
        """Returns the expression that fully matches the text.

        Parameters
        ----------
        text : str
            Text to match.

        Returns
        -------
        :class:`~.Expression`
            Expression that fully matches the text.
        """
        for expression in self.expressions:
            if expression.fullmatch(text):
                return expression
        return None

    def parse(self, text: str) -> Iterable[rx.ExpressionResult]:
        """
        Parses the text.

        Parameters
        ----------
        text : str
            Text to parse.

        Yields
        -------
        :class:`~.ExpressionResult`
            Extracted value.
        """
        # TODO: Maybe provide a way to clean the text before parsing?
        # (e.g. remove harakat)
        if self.smart:
            yield from self.smart_parse(text)
        else:
            yield from self.normal_parse(text)

        self._clear_parsed()

    def normal_parse(self, text: str) -> Iterable[rx.ExpressionResult]:
        """Parse the input ``text`` and return the extracted values.

        Parameters
        ----------
        text : str
            Text to parse.

        Yields
        -------
        :class:`~.ExpressionResult`
            Extracted value.
        """
        for expression in self.expressions:
            yield from expression.parse(text)

    def smart_parse(self, text: str) -> Iterable[rx.ExpressionResult]:
        """
        Parses the text. If a value matches two or more expressions, only the first
        expression parses the value, no value is matched more than once. This means
        high-priority expressions should be added to the group first.

        Parameters
        ----------
        text : str
            Text to parse.

        Yields
        -------
        :class:`~.ExpressionResult`
            Extracted value.
        """

        for result in self.normal_parse(text):
            if self._is_parsed(result):
                continue
            self._parsed_ranges.add((result.start, result.end))
            yield result

    def _is_parsed(self, result: rx.ExpressionResult):
        for start, end in self._parsed_ranges:
            if start <= result.start <= end and start <= result.end <= end:
                return True

        return False

    def _clear_parsed(self):
        self._parsed_ranges = set()

    def __add__(self, other: ExpressionGroup) -> ExpressionGroup:
        self.expressions.extend(other.expressions)
        return self

    def __iter__(self):
        return iter(self.expressions)

    @overload
    def __getitem__(self, index: int) -> rx.Expression:
        ...

    @overload
    def __getitem__(self, index: slice) -> ExpressionGroup:
        ...

    def __getitem__(self, index: int | slice) -> rx.Expression | ExpressionGroup:
        if isinstance(index, slice):
            return ExpressionGroup(*self.expressions[index])

        return self.expressions[index]

    def __len__(self) -> int:
        return len(self.expressions)
