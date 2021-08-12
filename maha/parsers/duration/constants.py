from maha.rexy import Expression, non_capturing_group

from ..constants import ALL_ALEF, TWO_SUFFIX

EXPRESSION_OF_SECOND = Expression(non_capturing_group("ثاني[ةه]", "لح[زضظ]"))
EXPRESSION_OF_TWO_SECONDS = Expression(
    non_capturing_group("ثانيت" + TWO_SUFFIX, "لح[زضظ]ت" + TWO_SUFFIX)
)
EXPRESSION_OF_SECONDS = Expression(non_capturing_group("ثواني", "لح[زضظ]ات"))
EXPRESSION_OF_MINUTE = Expression("دقيق[ةه]")
EXPRESSION_OF_TWO_MINUTES = Expression("دقيقت" + TWO_SUFFIX)
EXPRESSION_OF_MINUTES = Expression("دقا[يئ]ق")
EXPRESSION_OF_HOUR = Expression("ساع[ةه]")
EXPRESSION_OF_TWO_HOURS = Expression("ساعت" + TWO_SUFFIX)
EXPRESSION_OF_HOURS = Expression("ساعات")
EXPRESSION_OF_DAY = Expression("يوما?")
EXPRESSION_OF_TWO_DAYS = Expression(EXPRESSION_OF_DAY + TWO_SUFFIX)
EXPRESSION_OF_DAYS = Expression("{}يام".format(ALL_ALEF))
EXPRESSION_OF_WEEK = Expression("{}سبوعا?".format(ALL_ALEF))
EXPRESSION_OF_TWO_WEEKS = Expression(EXPRESSION_OF_WEEK + TWO_SUFFIX)
EXPRESSION_OF_WEEKS = Expression("{}سابيعا?".format(ALL_ALEF))
EXPRESSION_OF_MONTH = Expression("شهرا?")
EXPRESSION_OF_TWO_MONTHS = Expression(EXPRESSION_OF_MONTH + TWO_SUFFIX)
EXPRESSION_OF_MONTHS = Expression(non_capturing_group("شهور", "[أا]شهر"))
EXPRESSION_OF_YEAR = Expression(non_capturing_group("سن[ةه]", "عاما?"))
EXPRESSION_OF_TWO_YEARS = Expression(
    non_capturing_group("سنت" + TWO_SUFFIX, "عام" + TWO_SUFFIX)
)
EXPRESSION_OF_YEARS = Expression(non_capturing_group("سنوات", "سنين", "[أا]عوام"))

SECONDS = Expression(
    non_capturing_group(
        EXPRESSION_OF_SECOND, EXPRESSION_OF_TWO_SECONDS, EXPRESSION_OF_SECONDS
    )
)
MINUTES = Expression(
    non_capturing_group(
        EXPRESSION_OF_MINUTE, EXPRESSION_OF_TWO_MINUTES, EXPRESSION_OF_MINUTES
    )
)
HOURS = Expression(
    non_capturing_group(
        EXPRESSION_OF_HOUR, EXPRESSION_OF_TWO_HOURS, EXPRESSION_OF_HOURS
    )
)
DAYS = Expression(
    non_capturing_group(EXPRESSION_OF_DAY, EXPRESSION_OF_TWO_DAYS, EXPRESSION_OF_DAYS)
)
WEEKS = Expression(
    non_capturing_group(
        EXPRESSION_OF_WEEK, EXPRESSION_OF_TWO_WEEKS, EXPRESSION_OF_WEEKS
    )
)
MONTHS = Expression(
    non_capturing_group(
        EXPRESSION_OF_MONTH, EXPRESSION_OF_TWO_MONTHS, EXPRESSION_OF_MONTHS
    )
)
YEARS = Expression(
    non_capturing_group(
        EXPRESSION_OF_YEAR, EXPRESSION_OF_TWO_YEARS, EXPRESSION_OF_YEARS
    )
)

SINGULAR_DURATIONS = Expression(
    non_capturing_group(
        EXPRESSION_OF_SECOND,
        EXPRESSION_OF_MINUTE,
        EXPRESSION_OF_HOUR,
        EXPRESSION_OF_DAY,
        EXPRESSION_OF_WEEK,
        EXPRESSION_OF_MONTH,
        EXPRESSION_OF_YEAR,
    )
)
DUAL_DURATIONS = Expression(
    non_capturing_group(
        EXPRESSION_OF_TWO_SECONDS,
        EXPRESSION_OF_TWO_MINUTES,
        EXPRESSION_OF_TWO_HOURS,
        EXPRESSION_OF_TWO_DAYS,
        EXPRESSION_OF_TWO_WEEKS,
        EXPRESSION_OF_TWO_MONTHS,
        EXPRESSION_OF_TWO_YEARS,
    )
)
