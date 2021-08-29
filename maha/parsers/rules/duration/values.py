from maha.parsers.templates import DurationUnit, Value
from maha.rexy import non_capturing_group

from ..common import ALL_ALEF, TWO_SUFFIX, ValueUnit

ONE_SECOND = Value(
    ValueUnit(1, DurationUnit.SECONDS), non_capturing_group("ثاني[ةه]", "لح[زضظ][ةه]")
)
ONE_MINUTE = Value(ValueUnit(1, DurationUnit.MINUTES), "دقيق[ةه]")
ONE_HOUR = Value(ValueUnit(1, DurationUnit.HOURS), "ساع[ةه]")
ONE_DAY = Value(ValueUnit(1, DurationUnit.DAYS), "يوما?")
ONE_WEEK = Value(ValueUnit(1, DurationUnit.WEEKS), f"{ALL_ALEF}سبوعا?")
ONE_MONTH = Value(ValueUnit(1, DurationUnit.MONTHS), "شهرا?")
ONE_YEAR = Value(
    ValueUnit(1, DurationUnit.YEARS), non_capturing_group("سن[ةه]", "عاما?")
)

TWO_SECONDS = Value(
    ValueUnit(2, DurationUnit.SECONDS),
    non_capturing_group("ثانيت" + TWO_SUFFIX, "لح[زضظ]ت" + TWO_SUFFIX),
)
TWO_MINUTES = Value(ValueUnit(2, DurationUnit.MINUTES), "دقيقت" + TWO_SUFFIX)
TWO_HOURS = Value(ValueUnit(2, DurationUnit.HOURS), "ساعت" + TWO_SUFFIX)
TWO_DAYS = Value(ValueUnit(2, DurationUnit.DAYS), "يوم" + TWO_SUFFIX)
TWO_WEEKS = Value(ValueUnit(2, DurationUnit.WEEKS), f"{ALL_ALEF}سبوع" + TWO_SUFFIX)
TWO_MONTHS = Value(ValueUnit(2, DurationUnit.MONTHS), "شهر" + TWO_SUFFIX)
TWO_YEARS = Value(
    ValueUnit(2, DurationUnit.YEARS),
    non_capturing_group("سنت" + TWO_SUFFIX, "عام" + TWO_SUFFIX),
)

SEVERAL_SECONDS = Value(
    ValueUnit(1, DurationUnit.SECONDS), non_capturing_group("ثواني", "لح[زضظ]ات")
)
SEVERAL_MINUTES = Value(ValueUnit(1, DurationUnit.MINUTES), "دقا[يئ]ق")
SEVERAL_HOURS = Value(ValueUnit(1, DurationUnit.HOURS), "ساعات")
SEVERAL_DAYS = Value(ValueUnit(1, DurationUnit.DAYS), f"{ALL_ALEF}يام")
SEVERAL_WEEKS = Value(ValueUnit(1, DurationUnit.WEEKS), f"{ALL_ALEF}سابيعا?")
SEVERAL_MONTHS = Value(
    ValueUnit(1, DurationUnit.MONTHS), non_capturing_group("شهور", "[أا]شهر")
)
SEVERAL_YEARS = Value(
    ValueUnit(1, DurationUnit.YEARS), non_capturing_group("سنوات", "سنين", "[أا]عوام")
)
