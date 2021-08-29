from dateutil.relativedelta import FR, MO, SA, SU, TH, TU, WE, relativedelta

from maha.constants import ARABIC_COMMA, COMMA
from maha.expressions import EXPRESSION_SPACE, EXPRESSION_SPACE_OR_NONE
from maha.parsers.expressions import ALL_ALEF
from maha.parsers.rules.duration.values import (
    ONE_DAY,
    ONE_MONTH,
    SEVERAL_DAYS,
    SEVERAL_MONTHS,
    TWO_DAYS,
    TWO_MONTHS,
)
from maha.parsers.rules.numeral.rule import RULE_NUMERAL
from maha.parsers.rules.numeral.values import TEH_OPTIONAL_SUFFIX
from maha.parsers.rules.ordinal.values import ALEF_LAM, ALEF_LAM_OPTIONAL
from maha.parsers.templates import FunctionValue, Value
from maha.rexy import Expression, ExpressionGroup, named_group, non_capturing_group

from ..common import spaced_patterns

value_group = lambda v: named_group("value", v)

TIME_WORD_SEPARATOR = Expression(
    non_capturing_group(
        f"{EXPRESSION_SPACE_OR_NONE}{non_capturing_group(COMMA, ARABIC_COMMA)}",
        str(EXPRESSION_SPACE),
    )
    + non_capturing_group(r"\b", str(EXPRESSION_SPACE_OR_NONE))
)

THIS = Expression(non_capturing_group("ها?ذ[ياه]", "ه[اذ]ي"))
AFTER = Value(+1, non_capturing_group("[إا]لل?ي" + EXPRESSION_SPACE) + f"?" + "بعد")
BEFORE = Value(-1, non_capturing_group("[إا]لل?ي" + EXPRESSION_SPACE) + "?" + "[أاق]بل")
PREVIOUS = Value(-1, non_capturing_group("الماضي?", "السابق", "المنصرم", "الفا[يئ]ت"))
NEXT = Value(
    1,
    non_capturing_group("الجاي", "القادم", "التالي?", "ال[اآ]تي?", "المقبل")
    + TEH_OPTIONAL_SUFFIX,
)
AFTER_NEXT = Value(2, spaced_patterns(AFTER, NEXT))
BEFORE_PREVIOUS = Value(-2, spaced_patterns(BEFORE, PREVIOUS))
IN_FROM_AT = Expression(non_capturing_group("في", "من", "خلال", "الموافق"))
IN_FROM_AT_THIS = Expression(spaced_patterns(IN_FROM_AT + "?", THIS))
AT_THE_MOMENT = Value(
    relativedelta(seconds=0),
    non_capturing_group(
        "ال[أآا]ن",
        THIS
        + non_capturing_group(
            "الوقت",
            "اللح[زضظ][ةه]",
        ),
        "هس[ةه]",
        "في الحال",
    ),
)
LAST_MONTH = Value(
    relativedelta(months=-1),
    non_capturing_group(
        spaced_patterns(BEFORE, ONE_MONTH),
        spaced_patterns(ALEF_LAM + ONE_MONTH, PREVIOUS),
    ),
)
LAST_TWO_MONTHS = Value(
    relativedelta(months=-2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + ONE_MONTH, BEFORE_PREVIOUS),
        spaced_patterns(BEFORE, TWO_MONTHS),
    ),
)
NEXT_MONTH = Value(
    relativedelta(months=1),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + ONE_MONTH, NEXT),
        spaced_patterns(AFTER, ONE_MONTH),
    ),
)
NEXT_TWO_MONTHS = Value(
    relativedelta(months=2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + ONE_MONTH, AFTER_NEXT),
        spaced_patterns(AFTER, TWO_MONTHS),
    ),
)


JANUARY = Value(relativedelta(month=1), non_capturing_group("يناير", "كانون الثاني"))
FEBRUARY = Value(relativedelta(month=2), non_capturing_group("فبراير", "شباط"))
MARCH = Value(relativedelta(month=3), non_capturing_group("مارس", "[اأآ]ذار"))
APRIL = Value(relativedelta(month=4), non_capturing_group("نيسان", f"{ALL_ALEF}بريل"))
MAY = Value(relativedelta(month=5), non_capturing_group("مايو", "أيار"))
JUNE = Value(relativedelta(month=6), non_capturing_group("يونيو", "حزيران"))
JULY = Value(relativedelta(month=7), non_capturing_group("يوليو", "تموز"))
AUGUST = Value(relativedelta(month=8), non_capturing_group("[اأآ]غسطس", "[أاآ]ب"))
SEPTEMBER = Value(relativedelta(month=9), non_capturing_group("سبتمبر", "[اأ]يلول"))
OCTOBER = Value(
    relativedelta(month=10), non_capturing_group("[اأ]كتوبر", "تشرين الأول")
)
NOVEMBER = Value(relativedelta(month=11), non_capturing_group("نوفمبر", "تشرين الثاني"))
DECEMBER = Value(relativedelta(month=12), non_capturing_group("ديسمبر", "كانون الأول"))

# ----------------------------------------------------
# DAYS
# ----------------------------------------------------
SUNDAY = Value(SU, "ال[أا]حد")
MONDAY = Value(MO, "ال[إا][تث]نين")
TUESDAY = Value(TU, "ال[ثت]لا[ثت]اء")
WEDNESDAY = Value(WE, "ال[أا]ربعاء")
THURSDAY = Value(TH, "الخميس")
FRIDAY = Value(FR, "الجمع[ةه]")
SATURDAY = Value(SA, "السبت")
_days = ExpressionGroup(SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY)

WEEKDAY = FunctionValue(
    lambda match: relativedelta(
        weekday=_days.get_matched_expression(match.group("value")).value  # type: ignore
    ),
    non_capturing_group("يوم") + "?" + named_group("value", _days.join()),
)
THIS_DAY = Value(
    relativedelta(days=0), non_capturing_group("اليوم", IN_FROM_AT_THIS + "اليوم")
)
YESTERDAY = Value(
    relativedelta(days=-1),
    non_capturing_group(
        "[اإ]?مبارح",
        ALEF_LAM + "بارح[ةه]",
        ALEF_LAM_OPTIONAL + "[أا]مس",
        spaced_patterns(BEFORE, ONE_DAY),
        spaced_patterns(ALEF_LAM + ONE_DAY, PREVIOUS),
    ),
)
BEFORE_YESTERDAY = Value(
    relativedelta(days=-2),
    non_capturing_group(
        spaced_patterns(non_capturing_group("[أا]ول", str(BEFORE)), YESTERDAY),
        spaced_patterns(ALEF_LAM + ONE_DAY, BEFORE_PREVIOUS),
        spaced_patterns(BEFORE, TWO_DAYS),
    ),
)
TOMORROW = Value(
    relativedelta(days=1),
    non_capturing_group(
        ALEF_LAM_OPTIONAL + "غدا?",
        "بكر[ةه]",
        spaced_patterns(ALEF_LAM + ONE_DAY, NEXT),
        spaced_patterns(AFTER, ONE_DAY),
    ),
)
AFTER_TOMORROW = Value(
    relativedelta(days=2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + ONE_DAY, AFTER_NEXT),
        spaced_patterns(AFTER, TOMORROW),
        spaced_patterns(AFTER, TWO_DAYS),
    ),
)


def parse_value(value: dict) -> relativedelta:
    return relativedelta(**value)


AFTER_N_DAYS = FunctionValue(
    lambda match: parse_value({"days": list(RULE_NUMERAL(match.group("value")))[0]}),
    spaced_patterns(AFTER, value_group(RULE_NUMERAL), SEVERAL_DAYS),
)
BEFORE_N_DAYS = FunctionValue(
    lambda match: parse_value({"days": list(RULE_NUMERAL(match.group("value")))[0]}),
    spaced_patterns(BEFORE, value_group(RULE_NUMERAL), SEVERAL_DAYS),
)
NEXT_WEEKDAY = FunctionValue(
    lambda match: parse_value(
        {"weekday": _days.get_matched_expression(match.group("value")).value(1)}  # type: ignore
    ),
    spaced_patterns("يوم", value_group(_days.join()), NEXT),
)
PREVIOUS_WEEKDAY = FunctionValue(
    lambda match: parse_value(
        {"weekday": _days.get_matched_expression(match.group("value")).value(-1)}  # type: ignore
    ),
    spaced_patterns("يوم", value_group(_days.join()), PREVIOUS),
)
AFTER_NEXT_WEEKDAY = FunctionValue(
    lambda match: parse_value(
        {"weekday": _days.get_matched_expression(match.group("value")).value(2)}  # type: ignore
    ),
    spaced_patterns("يوم", value_group(_days.join()), AFTER_NEXT),
)
BEFORE_PREVIOUS_WEEKDAY = FunctionValue(
    lambda match: parse_value(
        {"weekday": _days.get_matched_expression(match.group("value")).value(-2)}  # type: ignore
    ),
    spaced_patterns("يوم", value_group(_days.join()), BEFORE_PREVIOUS),
)
