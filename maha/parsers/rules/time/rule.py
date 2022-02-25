__all__ = [
    "RULE_TIME_YEARS",
    "RULE_TIME_MONTHS",
    "RULE_TIME_WEEKS",
    "RULE_TIME_DAYS",
    "RULE_TIME_HOURS",
    "RULE_TIME_MINUTES",
    "RULE_TIME_AM_PM",
    "RULE_TIME_NOW",
    "RULE_TIME",
    "parse_time",
]

from datetime import datetime

from maha.parsers.rules.time.template import TimeInterval

from ..common import FROM, TO, combine_patterns
from .values import *


def get_combined_value(groups, expression: ExpressionGroup):
    value = TimeValue()
    for group in groups:
        exp = expression.get_matched_expression(group)
        value += next(iter(exp(group))).value  # type: ignore
    return value


def process_time_interval(start_time: TimeValue, end_time: TimeValue):
    """Ensures that the end time is greater than the start time."""

    def set_start_if_none(value: str):
        if getattr(end_time, value) is not None and getattr(start_time, value) is None:
            setattr(start_time, value, getattr(end_time, value))

    def get_end_if_none(value: str, none_value=None):
        if (
            getattr(start_time, value) is not none_value
            and getattr(end_time, value) is none_value
        ):
            return TimeValue(**{value: getattr(start_time, value)})
        return TimeValue()

    now = datetime(2021, 9, 1)
    # always set am/pm to both if one is set
    set_start_if_none("am_pm")
    end_time += get_end_if_none("am_pm")

    for prop in [
        "microsecond",
        "second",
        "minute",
        "hour",
        "day",
        "weekday",
        "month",
        "year",
        "years",
        "months",
        "weeks",
        "days",
        "leapdays",
        "hours",
        "minutes",
        "seconds",
        "microseconds",
    ]:
        from_time = start_time + now
        to_time = end_time + now
        if from_time < to_time:
            break
        end_time += get_end_if_none(prop, 0 if prop[-1] == "s" else None)

    return TimeInterval(start_time, end_time)


def parse_time(match):
    groups = match.capturesdict()
    groups_keys = list(groups)
    text = match.group(0)

    def contains_to_time():
        return "to_time" in groups_keys

    # time interval
    if contains_to_time() and not TO.match(text) and groups["to_time"]:
        to_time_start = match.starts(groups_keys.index("to_time") + 1)[0]
        start_time = TimeValue()
        end_time = TimeValue()
        for group, exp_group in EXPERSSION_TIME_MAP.items():
            g_start = match.starts(groups_keys.index(group) + 1)
            if group not in groups_keys or not g_start:
                continue
            for m_start, m_group in zip(g_start, groups[group]):
                if m_start < to_time_start:
                    start_time += get_combined_value([m_group], exp_group)
                else:
                    end_time += get_combined_value([m_group], exp_group)
        return process_time_interval(start_time, end_time)

    value = TimeValue()
    for group, exp_group in EXPERSSION_TIME_MAP.items():
        if group in groups_keys and groups[group]:
            value += get_combined_value(groups[group], exp_group)

    # to time only
    if contains_to_time() and TO.match(text):
        return TimeInterval(end=value)

    # from time only
    elif FROM.match(text) and (
        not contains_to_time() or contains_to_time() and not groups["to_time"]
    ):
        return TimeInterval(start=value)

    # time only
    return value


years_expressions = ExpressionGroup(
    AFTER_N_YEARS,
    BEFORE_N_YEARS,
    LAST_TWO_YEARS,
    NEXT_TWO_YEARS,
    LAST_YEAR,
    NEXT_YEAR,
    NUMERAL_YEAR,
    ORDINAL_YEAR,
    THIS_YEAR,
)
weeks_expressions = ExpressionGroup(
    AFTER_N_WEEKS,
    BEFORE_N_WEEKS,
    LAST_TWO_WEEKS,
    NEXT_TWO_WEEKS,
    LAST_WEEK,
    NEXT_WEEK,
    THIS_WEEK,
)
days_expressions = ExpressionGroup(
    AFTER_N_DAYS,
    BEFORE_N_DAYS,
    AFTER_NEXT_WEEKDAY,
    PREVIOUS_WEEKDAY,
    NEXT_WEEKDAY,
    AFTER_TOMORROW,
    TOMORROW,
    LAST_SPECIFIC_DAY,
    BEFORE_PREVIOUS_WEEKDAY,
    BEFORE_YESTERDAY,
    YESTERDAY,
    LAST_DAY,
    THIS_DAY,
    WEEKDAY,
)
hours_expressions = ExpressionGroup(
    AFTER_N_HOURS,
    BEFORE_N_HOURS,
    LAST_TWO_HOURS,
    NEXT_TWO_HOURS,
    LAST_HOUR,
    NEXT_HOUR,
    NUMERAL_HOUR,
    ORDINAL_HOUR,
    THIS_HOUR,
)
minutes_expressions = ExpressionGroup(
    AFTER_N_MINUTES,
    BEFORE_N_MINUTES,
    LAST_TWO_MINUTES,
    NEXT_TWO_MINUTES,
    LAST_MINUTE,
    NEXT_MINUTE,
    NUMERAL_MINUTE,
    ORDINAL_MINUTE,
    THIS_MINUTE,
)
am_pm_expressions = ExpressionGroup(PM, AM)
now_expressions = ExpressionGroup(AT_THE_MOMENT)

month_day_expressions = ExpressionGroup(
    DAY_MONTH_FORM,
    ORDINAL_SPECIFIC_DAY,
    LAST_SPECIFIC_DAY_OF_SPECIFIC_MONTH,
    ORDINAL_AND_MONTH,
    NUMERAL_AND_MONTH,
)
year_month_day_expressions = ExpressionGroup(
    DAY_MONTH_YEAR_FORM,
)
year_month_expressions = ExpressionGroup(MONTH_YEAR_FORM, YEAR_WITH_MONTH)
hour_minute_expressions = ExpressionGroup(
    NUMERAL_FRACTION_HOUR_MINUTE, ORDINAL_FRACTION_HOUR_MINUTE, HOUR_MINUTE_FORM
)
hour_minute_second_expressions = ExpressionGroup(HOUR_MINUTE_SECOND_FORM)
hour_am_pm_expressions = ExpressionGroup(
    NUMERAL_FRACTION_HOUR_AM,
    ORDINAL_FRACTION_HOUR_AM,
    NUMERAL_FRACTION_HOUR_PM,
    ORDINAL_FRACTION_HOUR_PM,
    NUMERAL_HOUR_AM,
    NUMERAL_HOUR_PM,
    ORDINAL_HOUR_AM,
    ORDINAL_HOUR_PM,
)


now_group = named_group("now", now_expressions.join())
years_group = named_group("years", years_expressions.join())
months_group = named_group("months", months_expressions.join())
weeks_group = named_group("weeks", weeks_expressions.join())
days_group = named_group("days", days_expressions.join())
hours_group = named_group("hours", hours_expressions.join())
minutes_group = named_group("minutes", minutes_expressions.join())
am_pm_group = named_group("am_pm", am_pm_expressions.join())
month_day_group = named_group("month_day", month_day_expressions.join())
year_month_group = named_group("year_month", year_month_expressions.join())
year_month_day_group = named_group("year_month_day", year_month_day_expressions.join())
hour_minute_group = named_group("hour_minute", hour_minute_expressions.join())
hour_minute_second_group = named_group("h_m_s", hour_minute_second_expressions.join())
hour_am_pm_group = named_group("hour_am_pm", hour_am_pm_expressions.join())

RULE_TIME_YEARS = FunctionValue(parse_time, combine_patterns(years_group))
RULE_TIME_MONTHS = FunctionValue(parse_time, combine_patterns(months_group))
RULE_TIME_WEEKS = FunctionValue(parse_time, combine_patterns(weeks_group))
RULE_TIME_DAYS = FunctionValue(parse_time, combine_patterns(days_group))
RULE_TIME_HOURS = FunctionValue(parse_time, combine_patterns(hours_group))
RULE_TIME_MINUTES = FunctionValue(parse_time, combine_patterns(minutes_group))
RULE_TIME_AM_PM = FunctionValue(parse_time, combine_patterns(am_pm_group))
RULE_TIME_NOW = FunctionValue(parse_time, combine_patterns(now_group))


_all_time_expressions_pattern = combine_patterns(
    year_month_day_group,
    year_month_group,
    month_day_group,
    hour_minute_second_group,
    hour_minute_group,
    hour_am_pm_group,
    now_group,
    years_group,
    months_group,
    weeks_group,
    days_group,
    hours_group,
    minutes_group,
    am_pm_group,
    seperator=TIME_WORD_SEPARATOR,
    combine_all=True,
)
from_time_group = named_group(
    "from_time", spaced_patterns(FROM, _all_time_expressions_pattern)
)
to_time_group = named_group(
    "to_time", TO + EXPRESSION_SPACE_OR_NONE + _all_time_expressions_pattern
)
from_time_to_time_group = named_group(
    "from_time_to_time", spaced_patterns(from_time_group, to_time_group)
)

RULE_TIME_FROM = FunctionValue(parse_time, from_time_group)
RULE_TIME_TO = FunctionValue(parse_time, to_time_group)
RULE_TIME_FROM_TO = FunctionValue(parse_time, from_time_to_time_group)

RULE_TIME = FunctionValue(
    parse_time,
    optional_non_capturing_group(FROM + EXPRESSION_SPACE, TO + EXPRESSION_SPACE_OR_NONE)
    + _all_time_expressions_pattern
    + optional_non_capturing_group(EXPRESSION_SPACE + to_time_group),
)


EXPERSSION_TIME_MAP = {
    "month_day": month_day_expressions,
    "year_month": year_month_expressions,
    "year_month_day": year_month_day_expressions,
    "hour_minute": hour_minute_expressions,
    "hour_am_pm": hour_am_pm_expressions,
    "h_m_s": hour_minute_second_expressions,
    "years": years_expressions,
    "months": months_expressions,
    "weeks": weeks_expressions,
    "days": days_expressions,
    "hours": hours_expressions,
    "minutes": minutes_expressions,
    "am_pm": am_pm_expressions,
    "now": now_expressions,
}
