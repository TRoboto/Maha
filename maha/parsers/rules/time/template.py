__all__ = ["TimeExpression"]
from typing import Optional

from dateutil._common import weekday
from dateutil.relativedelta import relativedelta
from regex.regex import Match

from maha.parsers.rules.numeral.template import NumeralExpression
from maha.parsers.rules.time import rule
from maha.parsers.templates import Rule, TimeUnit
from maha.rexy import ExpressionResult


class TimeExpression(NumeralExpression):
    def parse(self, match: Match, text: str):
        start, end = match.span()

        groups = match.capturesdict()
        values = groups.get("value")
        units = groups.get("unit")
        multipliers = groups.get("multiplier")
        numerals = groups.get("numeral_value")
        bounds = groups.get("bound")

        time_value = relativedelta()
        for i in range(len(values)):
            value = values[i]
            unit = units[i]
            multiplier = multipliers[i]
            numeral = numerals[i]
            bound = bounds[i]

            extracted_unit = self.get_unit(unit)
            if extracted_unit is None:
                time_value += self.get_special_value(value)
                continue

            current_delta = relativedelta()
            bound_value = 0
            if bound:
                bound_value = self.get_bound_value(bound)
            if value:
                current_delta += self.get_value(value, bound_value, extracted_unit)
            elif numeral:
                current_delta = self.get_numeral_value(
                    numeral, multiplier, extracted_unit, bound_value
                )
            else:
                current_delta = relativedelta(
                    **{extracted_unit.name.lower(): bound_value}
                )

            time_value += current_delta

        return ExpressionResult(
            start=start,
            end=end,
            value=time_value,
            expression=self,
        )

    def get_numeral_value(
        self, value: str, multiplier: str, unit: TimeUnit, bound: int
    ) -> relativedelta:
        number = super().get_numeral_value(value, multiplier) * bound
        return relativedelta(**{unit.name.lower(): number})

    def get_bound_value(self, text: str) -> int:
        for r in rule.BOUND_RULES:
            if r.match(text):
                value = r.value  # type: ignore
                return value

        raise ValueError(f"Could not parse bound value: {text}")

    def apply_rules(self, text, *rule_names: str) -> bool:
        return bool(Rule.get_rules_with_names(*rule_names).apply(text))

    def get_unit(self, text: str) -> Optional[TimeUnit]:
        if self.apply_rules(text, "one_day", "several_days"):
            return TimeUnit.DAYS
        if self.apply_rules(text, "one_month", "several_months"):
            return TimeUnit.MONTHS

    def get_value(self, text: str, bound_value: int, unit: TimeUnit) -> relativedelta:
        for r in rule.ORDERED_TIMES:
            if r.match(text):
                value: int = r.value  # type: ignore
                if isinstance(value, weekday):
                    return relativedelta(weekday=value(bound_value))
                return relativedelta(**{unit.name.lower(): value})

        raise ValueError(f"Could not parse time value: {text}")

    def get_special_value(self, text: str) -> relativedelta:
        for r in rule.SPECIAL_TIMES:
            if r.match(text):
                value = r.value  # type: ignore
                return value

        raise ValueError(f"Could not parse special time value: {text}")
