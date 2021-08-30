from ..common import combine_patterns
from .values import *


def get_combined_value(groups, expression):
    value = relativedelta()
    for group in groups:
        value += next(iter(expression.parse(group))).value
    return value


def parse_time(match):
    groups = match.capturesdict()

    _months = groups.get("months")
    _days = groups.get("days")

    value = relativedelta()

    if _days:
        value += get_combined_value(_days, days_expressions)
    if _months:
        value += get_combined_value(_months, months_expressions)
    return value


months_expressions = ExpressionGroup(
    AFTER_N_MONTHS,
    BEFORE_N_MONTHS,
    BEFORE_PREVIOUS_MONTH,
    AFTER_NEXT_MONTH,
    LAST_TWO_MONTHS,
    NEXT_TWO_MONTHS,
    LAST_MONTH,
    NEXT_MONTH,
    NEXT_SPECIFIC_MONTH,
    PREVIOUS_SPECIFIC_MONTH,
    THIS_MONTH,
)
days_expressions = ExpressionGroup(
    AFTER_N_DAYS,
    BEFORE_N_DAYS,
    BEFORE_PREVIOUS_WEEKDAY,
    AFTER_NEXT_WEEKDAY,
    PREVIOUS_WEEKDAY,
    NEXT_WEEKDAY,
    AFTER_TOMORROW,
    TOMORROW,
    BEFORE_YESTERDAY,
    YESTERDAY,
    THIS_DAY,
    WEEKDAY,
)

months_group = named_group("months", months_expressions.join())
days_group = named_group("days", days_expressions.join())

RULE_TIME_MONTHS = FunctionValue(parse_time, combine_patterns(months_group))
RULE_TIME_DAYS = FunctionValue(parse_time, combine_patterns(days_group))

RULE_TIME = FunctionValue(
    parse_time,
    combine_patterns(
        months_group, days_group, seperator=TIME_WORD_SEPARATOR, combine_all=True
    ),
)