from maha.parsers.expressions import ALL_ALEF, EXPRESSION_SPACE
from maha.parsers.helper import get_unit_group, get_value_group, wrap_pattern
from maha.parsers.rules.numeral.rule import (
    TEH_OPTIONAL_SUFFIX,
    multiplier_group,
    numeral_value,
)
from maha.parsers.templates import Rule, RuleCollection, ValueExpression
from maha.rexy import Expression, named_group, non_capturing_group

from .template import TimeExpression, TimeShift


def bound_group(value: str):
    """Returns the bound group for the given value and bound."""
    return named_group("bound", value)


def next_pattern(name: str):
    """Returns the next pattern for the given name."""
    return (
        get_unit_group(name)
        + EXPRESSION_SPACE
        + bound_group(str(NEXT))
        + multiplier_group("")
        + numeral_value("")
        + get_value_group("")
    )


def spaced_patterns(*patterns: str) -> str:
    """
    Returns a regex pattern that matches any of the given patterns,
    separated by spaces.

    Parameters
    ----------
    patterns : str
        The patterns to match.
    """
    return non_capturing_group(str(EXPRESSION_SPACE).join(patterns))


def previous_pattern(name: str):
    """Returns the previous pattern for the given name."""
    return (
        get_unit_group(name)
        + EXPRESSION_SPACE
        + bound_group(str(PREVIOUS))
        + multiplier_group("")
        + numeral_value("")
        + get_value_group("")
    )


def get_pattern(name: str, values: RuleCollection) -> str:
    """
    Returns the regex pattern that matches a numeric followed a unit.

    Parameters
    ----------
    name : str
        The name of the time in indefinite form (without 'ال').
    values : str
        The time values, e.g. 'آب', 'الخميس'.
    """
    singular = Rule.get("one_" + name)
    plural = Rule.get(f"several_{name}s")

    pattern_list = [
        # يوم الأحد القادم
        "{singular}{space}{value}{space}{next}{no_numeric}",
        # يوم الأحد بعد القادم
        "{singular}{space}{value}{space}{next_after}{no_numeric}",
        # اليوم القادم
        next_pattern(ALEF_LAM + singular),
        # اليوم السابق . الشهر الماضي
        previous_pattern(ALEF_LAM + singular),
        # يوم الأحد السابق
        "{singular}{space}{value}{space}{prev}{no_numeric}",
        # يوم الأحد قبل السابق
        "{singular}{space}{value}{space}{prev_before}{no_numeric}",
        # # بعد 3 أيام
        "{after}{space}{numeral}{space}{plural}",
        # # قبل 3 أيام
        "{before}{space}{numeral}{space}{plural}",
        # في هذا الشهر/اليوم
        "{in_from_this}{space}{alef_lam}{singular}{no_bound}{no_numeric}{no_value}",
        # يوم الأحد
        # شهر يناير
        "{singular}{space}{value}{no_bound}{no_numeric}",
        # اليوم، الشهر، السنة
        "{alef_lam}{singular}{no_bound}{no_numeric}{no_value}",
        # الخميس ، يناير
        "{alef_lam}{singular}{no_bound}{no_numeric}{no_value}",
    ]

    pattern = non_capturing_group(*pattern_list).format(
        singular=get_unit_group(singular.pattern),
        space=EXPRESSION_SPACE,
        value=get_value_group(values.join()),
        next=bound_group(str(NEXT)),
        prev=bound_group(str(PREVIOUS)),
        in_from_this=IN_FROM_THIS,
        plural=get_unit_group(plural.pattern),
        after=bound_group(str(AFTER)),
        before=bound_group(str(BEFORE)),
        numeral=Rule.get("tens").pattern,
        no_numeric=NO_NUMERAL,
        no_value=get_value_group(""),
        alef_lam=ALEF_LAM,
        no_bound=bound_group(""),
        next_after=bound_group(spaced_patterns(str(AFTER), str(NEXT))),
        prev_before=bound_group(spaced_patterns(str(BEFORE), str(PREVIOUS))),
    )
    return pattern


NO_NUMERAL = multiplier_group("") + numeral_value("")

ALEF_LAM = Expression(non_capturing_group("ال"))
ALEF_LAM_OPTIONAL = Expression(ALEF_LAM + "?")
THIS = Expression(non_capturing_group("ها?ذ[ياه]", "ه[اذ]ي"))
AFTER = Expression("بعد")
BEFORE = Expression("[أاق]بل")
PREVIOUS = ValueExpression(
    -1, non_capturing_group("الماضي?", "السابق", "المنصرم", "الفا[يئ]ت")
)
NEXT = ValueExpression(
    1,
    non_capturing_group("الجاي", "القادم", "التالي?", "ال[اآ]تي?", "المقبل")
    + TEH_OPTIONAL_SUFFIX,
)
IN_FROM_THIS = Expression(
    non_capturing_group(non_capturing_group("في", "من", "خلال") + str(EXPRESSION_SPACE))
    + "?"
    + THIS
)

Rule("sunday", ValueExpression(TimeShift(days=-1), "ال[أا]حد"))
Rule("monday", "ال[إا][تث]نين")
Rule("tuesday", "ال[ثت]لا[ثت]اء")
Rule("wednesday", "ال[أا]ربعاء")
Rule("thursday", "الخميس")
Rule("friday", "الجمع[ةه]")
Rule("saturday", "السبت")
Rule("january", non_capturing_group("يناير", "كانون الثاني"))
Rule("february", non_capturing_group("فبراير", "شباط"))
Rule("march", non_capturing_group("مارس", "[اأآ]ذار"))
Rule("april", non_capturing_group("نيسان", f"{ALL_ALEF}بريل"))
Rule("may", non_capturing_group("مايو", "أيار"))
Rule("june", non_capturing_group("يونيو", "حزيران"))
Rule("july", non_capturing_group("يوليو", "تموز"))
Rule("august", non_capturing_group("[اأ]غسطس", "[أاآ]ب"))
Rule("september", non_capturing_group("سبتمبر", "[اأ]يلول"))
Rule("october", non_capturing_group("[اأ]كتوبر", "تشرين الأول"))
Rule("november", non_capturing_group("نوفمبر", "تشرين الثاني"))
Rule("december", non_capturing_group("ديسمبر", "كانون الأول"))


Rule(
    "time_now",
    ValueExpression(
        TimeShift.now(),
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
    ),
)
Rule(
    "yesterday",
    ValueExpression(
        TimeShift(days=-1),
        non_capturing_group(
            "[اإ]?مبارح", ALEF_LAM + "بارح[ةه]", ALEF_LAM_OPTIONAL + "[أا]مس"
        ),
    ),
)
Rule(
    "before_yesterday",
    ValueExpression(
        TimeShift(days=-1),
        spaced_patterns(
            non_capturing_group("[أا]ول", str(BEFORE)), Rule.get("yesterday").pattern
        ),
    ),
)
Rule(
    "tomorrow",
    ValueExpression(
        TimeShift(days=1),
        non_capturing_group(
            ALEF_LAM_OPTIONAL + "غدا?",
            "بكر[ةه]",
        ),
    ),
)
Rule(
    "after_tomorrow",
    ValueExpression(
        TimeShift(days=1),
        spaced_patterns(str(AFTER), Rule.get("tomorrow").pattern),
    ),
)
Rule(
    "time_day",
    TimeExpression(
        wrap_pattern(
            non_capturing_group(
                get_value_group(Rule.get("before_yesterday").pattern),
                get_value_group(Rule.get("yesterday").pattern),
                get_value_group(Rule.get("tomorrow").pattern),
                get_value_group(Rule.get("after_tomorrow").pattern),
                get_pattern("day", Rule.slice("sunday", "saturday")),
            ),
        )
    ),
)

Rule(
    "time_month",
    TimeExpression(
        wrap_pattern(get_pattern("month", Rule.slice("january", "december")))
    ),
)

Rule(
    "time",
    TimeExpression(
        wrap_pattern(
            non_capturing_group(
                Rule.get("time_now").pattern,
                Rule.get("time_day").pattern,
                Rule.get("time_month").pattern,
            ),
        )
    ),
)

ORDERED_TIMES = [
    Rule.get("time_now"),
    Rule.get("before_yesterday"),
    Rule.get("yesterday"),
    Rule.get("tomorrow"),
    Rule.get("after_tomorrow"),
]
