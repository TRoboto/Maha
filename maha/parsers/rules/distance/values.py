from maha.expressions import EXPRESSION_SPACE_OR_NONE
from maha.parsers.templates import DistanceUnit, Value
from maha.rexy import non_capturing_group

from ..common import TWO_SUFFIX, ValueUnit

KILO = "كيلو"
CENTI = "سا?نتيم?"
MILLI = "مي?لي"
DECI = "ديسي"

ONE_METER = Value(ValueUnit(1, DistanceUnit.METERS), "مترا?")
ONE_KILOMETER = Value(
    ValueUnit(1, DistanceUnit.KILOMETERS),
    non_capturing_group(KILO + EXPRESSION_SPACE_OR_NONE + ONE_METER, "كم"),
)
ONE_CENTIMETER = Value(
    ValueUnit(1, DistanceUnit.CENTIMETERS),
    non_capturing_group(CENTI + EXPRESSION_SPACE_OR_NONE + ONE_METER, "سم"),
)
ONE_MILLIMETER = Value(
    ValueUnit(1, DistanceUnit.MILLIMETERS),
    non_capturing_group(MILLI + EXPRESSION_SPACE_OR_NONE + ONE_METER, "مم"),
)
ONE_DECIMETER = Value(
    ValueUnit(1, DistanceUnit.DECIMETERS),
    non_capturing_group(DECI + EXPRESSION_SPACE_OR_NONE + ONE_METER, "دسم"),
)
ONE_MILE = Value(ValueUnit(1, DistanceUnit.MILES), "ميلا?")
ONE_YARD = Value(ValueUnit(1, DistanceUnit.YARDS), "يارد[اةه]?")
ONE_FOOT = Value(ValueUnit(1, DistanceUnit.FEET), "قدما?")
ONE_INCH = Value(
    ValueUnit(1, DistanceUnit.INCHES), non_capturing_group("[إا]نشا?", "بوص[ةه]")
)

TWO_METERS = Value(ValueUnit(2, DistanceUnit.METERS), "متر" + TWO_SUFFIX)
TWO_MILES = Value(ValueUnit(2, DistanceUnit.MILES), "ميل" + TWO_SUFFIX)
TWO_FEET = Value(ValueUnit(2, DistanceUnit.FEET), "قدم" + TWO_SUFFIX)
TWO_INCHES = Value(
    ValueUnit(2, DistanceUnit.INCHES),
    non_capturing_group("[إا]نش" + TWO_SUFFIX, "بوصت" + TWO_SUFFIX),
)

SEVERAL_METERS = Value(
    ValueUnit(1, DistanceUnit.METERS), non_capturing_group("مترات", "[أا]متار")
)
SEVERAL_KILOMETERS = Value(
    ValueUnit(1, DistanceUnit.KILOMETERS),
    non_capturing_group(KILO + EXPRESSION_SPACE_OR_NONE + SEVERAL_METERS),
)
SEVERAL_CENTIMETERS = Value(
    ValueUnit(1, DistanceUnit.CENTIMETERS),
    non_capturing_group(CENTI + EXPRESSION_SPACE_OR_NONE + SEVERAL_METERS),
)
SEVERAL_MILLIMETERS = Value(
    ValueUnit(1, DistanceUnit.MILLIMETERS),
    non_capturing_group(MILLI + EXPRESSION_SPACE_OR_NONE + SEVERAL_METERS),
)
SEVERAL_DECIMETERS = Value(
    ValueUnit(1, DistanceUnit.DECIMETERS),
    non_capturing_group(DECI + EXPRESSION_SPACE_OR_NONE + SEVERAL_METERS),
)
SEVERAL_MILES = Value(
    ValueUnit(1, DistanceUnit.MILES), non_capturing_group("[اأ]ميال", "ميول")
)
SEVERAL_YARDS = Value(ValueUnit(1, DistanceUnit.YARDS), "ياردات")
SEVERAL_FEET = Value(ValueUnit(1, DistanceUnit.FEET), "[أا]قدام")
SEVERAL_INCHES = Value(
    ValueUnit(1, DistanceUnit.INCHES), non_capturing_group("[إا]نشات", "بوصات")
)
