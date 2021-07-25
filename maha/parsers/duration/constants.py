from maha.constants import ALEF_VARIATIONS, ARABIC_COMMA, COMMA, WAW

from ..utils.general import (
    SPACE_EXPRESSION,
    SPACE_OR_NONE_EXPRESSION,
    WAW_SEPARATOR,
    get_non_capturing_group,
)

TWO_SUFFIX = get_non_capturing_group("ين", "ان")
SUM_SUFFIX = get_non_capturing_group("ين", "ون")

NAME_OF_SECOND = get_non_capturing_group("ثاني[ةه]", "لح[زضظ]")
NAME_OF_TWO_SECONDS = get_non_capturing_group(
    "ثانيت" + TWO_SUFFIX, "لح[زضظ]ت" + TWO_SUFFIX
)
NAME_OF_SECONDS = get_non_capturing_group("ثواني", "لح[زضظ]ات")
NAME_OF_MINUTE = "دقيق[ةه]"
NAME_OF_TWO_MINUTES = "دقيقت" + TWO_SUFFIX
NAME_OF_MINUTES = "دقا[يئ]ق"
NAME_OF_HOUR = "ساع[ةه]"
NAME_OF_TWO_HOURS = "ساعت" + TWO_SUFFIX
NAME_OF_HOURS = "ساعات"
NAME_OF_DAY = "يوما?"
NAME_OF_TWO_DAYS = NAME_OF_DAY + TWO_SUFFIX
NAME_OF_DAYS = "[{}]يام".format("".join(ALEF_VARIATIONS))
NAME_OF_WEEK = "[{}]سبوعا?".format("".join(ALEF_VARIATIONS))
NAME_OF_TWO_WEEKS = NAME_OF_WEEK + TWO_SUFFIX
NAME_OF_WEEKS = "[{}]سابيعا?".format("".join(ALEF_VARIATIONS))
NAME_OF_MONTH = "شهرا?"
NAME_OF_TWO_MONTHS = NAME_OF_MONTH + TWO_SUFFIX
NAME_OF_MONTHS = get_non_capturing_group("شهور", "[أا]شهر")
NAME_OF_YEAR = get_non_capturing_group("سن[ةه]", "عاما?")
NAME_OF_TWO_YEARS = get_non_capturing_group("سنت" + TWO_SUFFIX, "عام" + TWO_SUFFIX)
NAME_OF_YEARS = get_non_capturing_group("سنوات", "سنين", "[أا]عوام")

SECONDS = get_non_capturing_group(NAME_OF_SECOND, NAME_OF_TWO_SECONDS, NAME_OF_SECONDS)
MINUTES = get_non_capturing_group(NAME_OF_MINUTE, NAME_OF_TWO_MINUTES, NAME_OF_MINUTES)
HOURS = get_non_capturing_group(NAME_OF_HOUR, NAME_OF_TWO_HOURS, NAME_OF_HOURS)
DAYS = get_non_capturing_group(NAME_OF_DAY, NAME_OF_TWO_DAYS, NAME_OF_DAYS)
WEEKS = get_non_capturing_group(NAME_OF_WEEK, NAME_OF_TWO_WEEKS, NAME_OF_WEEKS)
MONTHS = get_non_capturing_group(NAME_OF_MONTH, NAME_OF_TWO_MONTHS, NAME_OF_MONTHS)
YEARS = get_non_capturing_group(NAME_OF_YEAR, NAME_OF_TWO_YEARS, NAME_OF_YEARS)

SINGULAR_DURATIONS = get_non_capturing_group(
    NAME_OF_SECOND,
    NAME_OF_MINUTE,
    NAME_OF_HOUR,
    NAME_OF_DAY,
    NAME_OF_WEEK,
    NAME_OF_MONTH,
    NAME_OF_YEAR,
)
DUAL_DURATIONS = get_non_capturing_group(
    NAME_OF_TWO_SECONDS,
    NAME_OF_TWO_MINUTES,
    NAME_OF_TWO_HOURS,
    NAME_OF_TWO_DAYS,
    NAME_OF_TWO_WEEKS,
    NAME_OF_TWO_MONTHS,
    NAME_OF_TWO_YEARS,
)

WORD_SEPARATOR = (
    f"(?:{SPACE_EXPRESSION}|\\b)"
    f"(?:{COMMA}|{ARABIC_COMMA})?{SPACE_OR_NONE_EXPRESSION}{WAW}?"
    f"(?:{SPACE_OR_NONE_EXPRESSION}|\\b)"
)
