from ..common import combine_patterns
from .values import *


def get_combined_value(groups, expression: ExpressionGroup):
    value = TimeValue()
    for group in groups:
        value += next(iter(expression.parse(group))).value
    return value


def parse_time(match):
    groups = match.capturesdict()

    _year = groups.get("years")
    _months = groups.get("months")
    _weeks = groups.get("weeks")
    _days = groups.get("days")
    _hours = groups.get("hours")
    _minutes = groups.get("minutes")
    _am_pm = groups.get("am_pm")
    _now = groups.get("now")
    _month_day = groups.get("month_day")
    _year_month = groups.get("year_month")
    _hour_minute = groups.get("hour_minute")
    _hour_am_pm = groups.get("hour_am_pm")

    value = TimeValue()

    if _month_day:
        value += get_combined_value(_month_day, month_day_expressions)
    if _year_month:
        value += get_combined_value(_year_month, year_month_expressions)
    if _hour_minute:
        value += get_combined_value(_hour_minute, hour_minute_expressions)
    if _hour_am_pm:
        value += get_combined_value(_hour_am_pm, hour_am_pm_expressions)
    if _year:
        value += get_combined_value(_year, years_expressions)
    if _weeks:
        value += get_combined_value(_weeks, weeks_expressions)
    if _days:
        value += get_combined_value(_days, days_expressions)
    if _months:
        value += get_combined_value(_months, months_expressions)
    if _hours:
        value += get_combined_value(_hours, hours_expressions)
    if _minutes:
        value += get_combined_value(_minutes, minutes_expressions)
    if _am_pm:
        value += get_combined_value(_am_pm, am_pm_expressions)
    if _now:
        value += get_combined_value(_now, now_expressions)

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
months_expressions = ExpressionGroup(
    AFTER_N_MONTHS,
    BEFORE_N_MONTHS,
    AFTER_SPECIFIC_NEXT_MONTH,
    LAST_TWO_MONTHS,
    NEXT_TWO_MONTHS,
    LAST_MONTH,
    NEXT_MONTH,
    NEXT_SPECIFIC_MONTH,
    PREVIOUS_SPECIFIC_MONTH,
    BEFORE_SPECIFIC_PREVIOUS_MONTH,
    THIS_MONTH,
    SPECIFIC_MONTH,
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
    YESTERDAY,
    LAST_DAY,
    LAST_SPECIFIC_DAY,
    BEFORE_PREVIOUS_WEEKDAY,
    BEFORE_YESTERDAY,
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
    ORDINAL_SPECIFIC_DAY,
    LAST_SPECIFIC_DAY_OF_SPECIFIC_MONTH,
    ORDINAL_AND_SPECIFIC_MONTH,
    ORDINAL_AND_THIS_MONTH,
    NUMERAL_AND_SPECIFIC_MONTH,
    NUMERAL_AND_THIS_MONTH,
)
year_month_expressions = ExpressionGroup(YEAR_WITH_MONTH)
hour_minute_expressions = ExpressionGroup(
    NUMERAL_FRACTION_HOUR_MINUTE, ORDINAL_FRACTION_HOUR_MINUTE
)
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
hour_minute_group = named_group("hour_minute", hour_minute_expressions.join())
hour_am_pm_group = named_group("hour_am_pm", hour_am_pm_expressions.join())

RULE_TIME_YEARS = FunctionValue(parse_time, combine_patterns(years_group))
RULE_TIME_MONTHS = FunctionValue(parse_time, combine_patterns(months_group))
RULE_TIME_WEEKS = FunctionValue(parse_time, combine_patterns(weeks_group))
RULE_TIME_DAYS = FunctionValue(parse_time, combine_patterns(days_group))
RULE_TIME_HOURS = FunctionValue(parse_time, combine_patterns(hours_group))
RULE_TIME_MINUTES = FunctionValue(parse_time, combine_patterns(minutes_group))
RULE_TIME_MONTH_DAY = FunctionValue(parse_time, combine_patterns(month_day_group))
RULE_TIME_YEAR_MONTH = FunctionValue(parse_time, combine_patterns(year_month_group))
RULE_TIME_AM_PM = FunctionValue(parse_time, combine_patterns(am_pm_group))
RULE_TIME_NOW = FunctionValue(parse_time, combine_patterns(now_group))

RULE_TIME = FunctionValue(
    parse_time,
    combine_patterns(
        hour_am_pm_group,
        month_day_group,
        hour_minute_group,
        year_month_group,
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
    ),
)
