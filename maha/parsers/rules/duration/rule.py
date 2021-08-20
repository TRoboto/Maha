"""Rules to extract duration."""


from maha.parsers.expressions import ALL_ALEF, TWO_SUFFIX
from maha.parsers.helper import wrap_pattern
from maha.parsers.rules.templates import Rule, get_unit_pattern
from maha.rexy import non_capturing_group

from .template import DurationExpression

Rule("one_second", non_capturing_group("ثاني[ةه]", "لح[زضظ][ةه]"))
Rule("one_minute", "دقيق[ةه]")
Rule("one_hour", "ساع[ةه]")
Rule("one_day", "يوما?")
Rule("one_week", f"{ALL_ALEF}سبوعا?")
Rule("one_month", "شهرا?")
Rule("one_year", non_capturing_group("سن[ةه]", "عاما?"))

Rule(
    "two_seconds",
    non_capturing_group("ثانيت" + TWO_SUFFIX, "لح[زضظ]ت" + TWO_SUFFIX),
),
Rule("two_minutes", "دقيقت" + TWO_SUFFIX),
Rule("two_hours", "ساعت" + TWO_SUFFIX),
Rule("two_days", "يوم" + TWO_SUFFIX),
Rule("two_weeks", f"{ALL_ALEF}سبوع" + TWO_SUFFIX),
Rule("two_months", "شهر" + TWO_SUFFIX),
Rule("two_years", non_capturing_group("سنت" + TWO_SUFFIX, "عام" + TWO_SUFFIX)),

Rule("several_seconds", non_capturing_group("ثواني", "لح[زضظ]ات"))
Rule("several_minutes", "دقا[يئ]ق"),
Rule("several_hours", "ساعات"),
Rule("several_days", f"{ALL_ALEF}يام"),
Rule("several_weeks", f"{ALL_ALEF}سابيعا?"),
Rule("several_months", non_capturing_group("شهور", "[أا]شهر")),
Rule("several_years", non_capturing_group("سنوات", "سنين", "[أا]عوام")),

_seconds_pattern = get_unit_pattern(
    Rule.get("one_second"), Rule.get("two_seconds"), Rule.get("several_seconds")
)
_minutes_pattern = get_unit_pattern(
    Rule.get("one_minute"), Rule.get("two_minutes"), Rule.get("several_minutes")
)
_hours_pattern = get_unit_pattern(
    Rule.get("one_hour"), Rule.get("two_hours"), Rule.get("several_hours")
)
_days_pattern = get_unit_pattern(
    Rule.get("one_day"), Rule.get("two_days"), Rule.get("several_days")
)
_weeks_pattern = get_unit_pattern(
    Rule.get("one_week"), Rule.get("two_weeks"), Rule.get("several_weeks")
)
_months_pattern = get_unit_pattern(
    Rule.get("one_month"), Rule.get("two_months"), Rule.get("several_months")
)
_years_pattern = get_unit_pattern(
    Rule.get("one_year"), Rule.get("two_years"), Rule.get("several_years")
)

Rule("seconds", DurationExpression(wrap_pattern(_seconds_pattern)))
Rule("minutes", DurationExpression(wrap_pattern(_minutes_pattern)))
Rule("hours", DurationExpression(wrap_pattern(_hours_pattern)))
Rule("days", DurationExpression(wrap_pattern(_days_pattern)))
Rule("weeks", DurationExpression(wrap_pattern(_weeks_pattern)))
Rule("months", DurationExpression(wrap_pattern(_months_pattern)))
Rule("years", DurationExpression(wrap_pattern(_years_pattern)))

Rule(
    "duration",
    DurationExpression(
        Rule.combine_patterns(
            _years_pattern,
            _months_pattern,
            _weeks_pattern,
            _days_pattern,
            _hours_pattern,
            _minutes_pattern,
            _seconds_pattern,
        )
    ),
)
