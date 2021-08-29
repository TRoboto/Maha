from .values import *


def get_combined_value(groups, expression):
    value = relativedelta()
    for group in groups:
        value += next(iter(expression.parse(group))).value
    return value


def parse_time(match):
    groups = match.capturesdict()

    _days = groups.get("days")

    value = relativedelta()

    if _days:
        value += get_combined_value(_days, days_expressions)
    return value


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

days_group = named_group("days", days_expressions.join())

RULE_TIME_DAYS = FunctionValue(parse_time, days_group)
