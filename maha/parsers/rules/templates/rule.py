__all__ = ["Rule"]

from dataclasses import dataclass
from typing import Any, List

from maha.parsers.expressions import EXPRESSION_END, EXPRESSION_START, WORD_SEPARATOR
from maha.parsers.templates import Dimension, DimensionType
from maha.rexy import Expression, non_capturing_group


@dataclass
class Rule:
    """
    Template representing a rule.
    """

    __slots__ = ["expression", "rule_type"]

    rule_type: DimensionType
    expression: Expression

    def __init__(self, expression: Expression, rule_type) -> None:
        """Returns a combined expression for the given types."""
        self.expression = expression
        self.rule_type = rule_type

    def __call__(self, text: str) -> List[Dimension]:
        return self.apply(text)

    def apply(self, text: str) -> List[Dimension]:
        """Applies the rule to the given text."""
        output = []
        for result in self.expression(text):
            start = result.start
            end = result.end
            value = result.value
            body = text[start:end]
            output.append(
                Dimension(result.expression, body, value, start, end, self.rule_type)
            )
        return output

    def compile(self):
        """Compiles the rule."""
        self.expression.compile()

    def combine_patterns(self, *types: Any) -> str:
        """
        Intelligently combine the patterns of the input in the types.

        Parameters
        ----------
        types : Any
            The types/enums to combine.

        Returns
        -------
        str
            The combined pattern.
        """
        all_expressions = non_capturing_group(
            *[self.get_pattern(type) for type in types]
        )
        patterns = [EXPRESSION_START + all_expressions + EXPRESSION_END]

        for u in types[1:]:
            pattern = (
                non_capturing_group(
                    WORD_SEPARATOR + self.get_pattern(u) + EXPRESSION_END
                )
                + "?"
            )
            patterns.append(pattern)
        return "".join(patterns)

    def get_pattern(self, type: Any) -> str:
        """Returns the pattern for the given type."""
        raise NotImplementedError

    def __str__(self) -> str:
        return str(self.expression)
