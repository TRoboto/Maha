__all__ = ["UnitRule"]

from typing import Any

from maha.expressions import EXPRESSION_SPACE
from maha.parsers.helper import (
    get_fractions_of_unit_pattern,
    get_unit_group,
    get_value_group,
)
from maha.parsers.interfaces import Unit
from maha.parsers.rules.numeral.rule import RULE_NUMERAL
from maha.rexy import Expression
from maha.rexy.rexy import non_capturing_group

from .rule import Rule


class UnitRule(Rule):
    """Rule to extract a numeric followed a unit."""

    def get_single(self, type: Any) -> "Expression":
        """Returns the expression of a singular type."""
        raise NotImplementedError

    def get_dual(self, type: Any) -> "Expression":
        """Returns the expression of a dual type."""
        raise NotImplementedError

    def get_plural(self, type: Any) -> "Expression":
        """Returns the expression of a plural type."""
        raise NotImplementedError

    def get_pattern(self, unit: Unit) -> str:
        single = str(self.get_single(unit))
        dual = str(self.get_dual(unit))
        plural = str(self.get_plural(unit))

        pattern = non_capturing_group(
            *[
                "{numeral}{space}{unit_single_plural}",
                get_fractions_of_unit_pattern(single),
                get_fractions_of_unit_pattern(dual),
                "{val}{unit_dual}",
                "{val}{unit_single}",
            ]
        ).format(
            numeral=RULE_NUMERAL.expression,
            space=EXPRESSION_SPACE,
            unit_single_plural=get_unit_group("|".join([single, plural])),
            unit_single=get_unit_group(single),
            unit_dual=get_unit_group(dual),
            val=get_value_group(""),
        )
        return pattern
