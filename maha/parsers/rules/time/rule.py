from dateutil.relativedelta import FR, MO, SA, SU, TH, TU, WE, relativedelta

from maha.constants import ARABIC_COMMA, COMMA
from maha.expressions import EXPRESSION_SPACE_OR_NONE
from maha.parsers.expressions import ALL_ALEF, EXPRESSION_SPACE
from maha.parsers.helper import get_unit_group, get_value_group, wrap_pattern
from maha.parsers.rules.numeral.rule import (
    TEH_OPTIONAL_SUFFIX,
    multiplier_group,
    numeral_value,
)
from maha.parsers.templates import Rule, RuleCollection, ValueExpression
from maha.rexy import Expression, ExpressionGroup, named_group, non_capturing_group

from .template import TimeExpression


def bound_group(value: str):
    """Returns the bound group for the given value and bound."""
    return named_group("bound", value)


def next_pattern(name: str):
    """Returns the next pattern for the given name."""
    return (
        spaced_patterns(get_unit_group(name), bound_group(str(NEXT)))
        + multiplier_group("")
        + numeral_value("")
        + get_value_group("")
    )


def value_group(name: str):
    """Returns the value group for the given name."""
    return (
        get_value_group(name)
        + multiplier_group("")
        + numeral_value("")
        + get_unit_group("")
        + bound_group("")
    )


def spaced_patterns(*patterns) -> str:
    """
    Returns a regex pattern that matches any of the given patterns,
    separated by spaces.

    Parameters
    ----------
    patterns
        The patterns to match.
    """
    return non_capturing_group(str(EXPRESSION_SPACE).join(str(p) for p in patterns))


def previous_pattern(name: str):
    """Returns the previous pattern for the given name."""
    return (
        spaced_patterns(get_unit_group(name), bound_group(str(PREVIOUS)))
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
    dual = Rule.get(f"two_{name}s")
    plural = Rule.get(f"several_{name}s")

    pattern_list = [
        # يوم الأحد القادم
        "{singular}{space}{value}{space}{next}{no_numeric}",
        # يوم الأحد بعد القادم
        "{singular}{space}{value}{space}{next_after}{no_numeric}",
        # يوم الأحد السابق
        "{singular}{space}{value}{space}{prev}{no_numeric}",
        # يوم الأحد قبل السابق
        "{singular}{space}{value}{space}{prev_before}{no_numeric}",
        # بعد 3 أيام
        "{after}{space}{numeral}{space}{plural}{no_value}",
        # # قبل 3 أيام
        "{before}{space}{numeral}{space}{plural}{no_value}",
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
        numeral=non_capturing_group(
            Rule.get("integers").pattern, Rule.get("tens").pattern
        ),
        no_numeric=NO_NUMERAL,
        no_value=get_value_group(""),
        alef_lam=ALEF_LAM,
        no_bound=bound_group(""),
        next_after=bound_group(str(AFTER_NEXT)),
        prev_before=bound_group(str(BEFORE_PREVIOUS)),
        dual_singular=get_unit_group(
            non_capturing_group(dual.pattern, singular.pattern)
        ),
    )
    return pattern


NO_NUMERAL = multiplier_group("") + numeral_value("")
TIME_WORD_SEPARATOR = Expression(
    non_capturing_group(
        f"{EXPRESSION_SPACE_OR_NONE}{non_capturing_group(COMMA, ARABIC_COMMA)}",
        str(EXPRESSION_SPACE),
    )
    + non_capturing_group(r"\b", str(EXPRESSION_SPACE_OR_NONE))
)

ALEF_LAM = Expression(non_capturing_group("ال"))
ALEF_LAM_OPTIONAL = Expression(ALEF_LAM + "?")
THIS = Expression(non_capturing_group("ها?ذ[ياه]", "ه[اذ]ي"))
AFTER = ValueExpression(
    +1, non_capturing_group("[إا]لل?ي" + EXPRESSION_SPACE) + f"?" + "بعد"
)
BEFORE = ValueExpression(
    -1, non_capturing_group("[إا]لل?ي" + EXPRESSION_SPACE) + "?" + "[أاق]بل"
)
PREVIOUS = ValueExpression(
    -1, non_capturing_group("الماضي?", "السابق", "المنصرم", "الفا[يئ]ت")
)
NEXT = ValueExpression(
    1,
    non_capturing_group("الجاي", "القادم", "التالي?", "ال[اآ]تي?", "المقبل")
    + TEH_OPTIONAL_SUFFIX,
)
AFTER_NEXT = ValueExpression(2, spaced_patterns(AFTER, NEXT))
BEFORE_PREVIOUS = ValueExpression(-2, spaced_patterns(BEFORE, PREVIOUS))
IN_FROM_THIS = Expression(
    non_capturing_group(non_capturing_group("في", "من", "خلال") + str(EXPRESSION_SPACE))
    + "?"
    + THIS
)
AT_THE_MOMENT = ValueExpression(
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
YESTERDAY = ValueExpression(
    relativedelta(days=-1),
    non_capturing_group(
        "[اإ]?مبارح",
        ALEF_LAM + "بارح[ةه]",
        ALEF_LAM_OPTIONAL + "[أا]مس",
        spaced_patterns(BEFORE, Rule.get("one_day")),
        spaced_patterns(ALEF_LAM + Rule.get("one_day"), PREVIOUS),
    ),
)
BEFORE_YESTERDAY = ValueExpression(
    relativedelta(days=-2),
    non_capturing_group(
        spaced_patterns(non_capturing_group("[أا]ول", str(BEFORE)), YESTERDAY),
        spaced_patterns(ALEF_LAM + Rule.get("one_day"), BEFORE_PREVIOUS),
        spaced_patterns(BEFORE, Rule.get("two_days")),
    ),
)
TOMORROW = ValueExpression(
    relativedelta(days=1),
    non_capturing_group(
        ALEF_LAM_OPTIONAL + "غدا?",
        "بكر[ةه]",
        spaced_patterns(ALEF_LAM + Rule.get("one_day"), NEXT),
        spaced_patterns(AFTER, Rule.get("one_day")),
    ),
)
AFTER_TOMORROW = ValueExpression(
    relativedelta(days=2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + Rule.get("one_day"), AFTER_NEXT),
        spaced_patterns(AFTER, TOMORROW),
        spaced_patterns(AFTER, Rule.get("two_days")),
    ),
)
LAST_MONTH = ValueExpression(
    relativedelta(months=-1),
    non_capturing_group(
        spaced_patterns(BEFORE, Rule.get("one_month")),
        spaced_patterns(ALEF_LAM + Rule.get("one_month"), PREVIOUS),
    ),
)
LAST_TWO_MONTHS = ValueExpression(
    relativedelta(months=-2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + Rule.get("one_month"), BEFORE_PREVIOUS),
        spaced_patterns(BEFORE, Rule.get("two_months")),
    ),
)
NEXT_MONTH = ValueExpression(
    relativedelta(months=1),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + Rule.get("one_month"), NEXT),
        spaced_patterns(AFTER, Rule.get("one_month")),
    ),
)
NEXT_TWO_MONTHS = ValueExpression(
    relativedelta(months=2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + Rule.get("one_month"), AFTER_NEXT),
        spaced_patterns(AFTER, Rule.get("two_months")),
    ),
)
Rule("sunday", ValueExpression(SU, "ال[أا]حد"))
Rule("monday", ValueExpression(MO, "ال[إا][تث]نين"))
Rule("tuesday", ValueExpression(TU, "ال[ثت]لا[ثت]اء"))
Rule("wednesday", ValueExpression(WE, "ال[أا]ربعاء"))
Rule("thursday", ValueExpression(TH, "الخميس"))
Rule("friday", ValueExpression(FR, "الجمع[ةه]"))
Rule("saturday", ValueExpression(SA, "السبت"))
Rule(
    "january",
    ValueExpression(
        relativedelta(month=1), non_capturing_group("يناير", "كانون الثاني")
    ),
)
Rule(
    "february",
    ValueExpression(relativedelta(month=2), non_capturing_group("فبراير", "شباط")),
)
Rule(
    "march",
    ValueExpression(relativedelta(month=3), non_capturing_group("مارس", "[اأآ]ذار")),
)
Rule(
    "april",
    ValueExpression(
        relativedelta(month=4), non_capturing_group("نيسان", f"{ALL_ALEF}بريل")
    ),
)
Rule(
    "may", ValueExpression(relativedelta(month=5), non_capturing_group("مايو", "أيار"))
)
Rule(
    "june",
    ValueExpression(relativedelta(month=6), non_capturing_group("يونيو", "حزيران")),
)
Rule(
    "july",
    ValueExpression(relativedelta(month=7), non_capturing_group("يوليو", "تموز")),
)
Rule(
    "august",
    ValueExpression(relativedelta(month=8), non_capturing_group("[اأ]غسطس", "[أاآ]ب")),
)
Rule(
    "september",
    ValueExpression(relativedelta(month=9), non_capturing_group("سبتمبر", "[اأ]يلول")),
)
Rule(
    "october",
    ValueExpression(
        relativedelta(month=10), non_capturing_group("[اأ]كتوبر", "تشرين الأول")
    ),
)
Rule(
    "november",
    ValueExpression(
        relativedelta(month=11), non_capturing_group("نوفمبر", "تشرين الثاني")
    ),
)
Rule(
    "december",
    ValueExpression(
        relativedelta(month=12), non_capturing_group("ديسمبر", "كانون الأول")
    ),
)

Rule("time_now", TimeExpression(wrap_pattern(value_group(str(AT_THE_MOMENT)))))

Rule("yesterday", TimeExpression(wrap_pattern(value_group(str(YESTERDAY)))))
Rule(
    "before_yesterday", TimeExpression(wrap_pattern(value_group(str(BEFORE_YESTERDAY))))
)
Rule("tomorrow", TimeExpression(wrap_pattern(value_group(str(TOMORROW)))))
Rule("after_tomorrow", TimeExpression(wrap_pattern(value_group(str(AFTER_TOMORROW)))))

Rule("last_month", TimeExpression(wrap_pattern(value_group(str(LAST_MONTH)))))
Rule("last_two_months", TimeExpression(wrap_pattern(value_group(str(LAST_TWO_MONTHS)))))
Rule("next_month", TimeExpression(wrap_pattern(value_group(str(NEXT_MONTH)))))
Rule("next_two_months", TimeExpression(wrap_pattern(value_group(str(NEXT_TWO_MONTHS)))))
Rule(
    "time_day",
    TimeExpression(
        wrap_pattern(
            non_capturing_group(
                value_group(str(AFTER_TOMORROW)),
                value_group(str(BEFORE_YESTERDAY)),
                value_group(str(YESTERDAY)),
                value_group(str(TOMORROW)),
                get_pattern("day", Rule.slice("sunday", "saturday")),
            ),
        )
    ),
)

Rule(
    "time_month",
    TimeExpression(
        wrap_pattern(
            non_capturing_group(
                value_group(str(NEXT_TWO_MONTHS)),
                value_group(str(NEXT_MONTH)),
                value_group(str(LAST_TWO_MONTHS)),
                value_group(str(LAST_MONTH)),
                get_pattern("month", Rule.slice("january", "december")),
            )
        ),
    ),
)

Rule(
    "time",
    TimeExpression(
        wrap_pattern(
            Rule.combine_patterns(
                Rule.get("time_now").pattern,
                Rule.get("time_day").pattern,
                Rule.get("time_month").pattern,
                seperator=TIME_WORD_SEPARATOR,
            ),
        )
    ),
)

ORDERED_TIMES = ExpressionGroup(
    Rule.slice("january", "december").expression_group,
    Rule.slice("sunday", "saturday").expression_group,
)

SPECIAL_TIMES = ExpressionGroup(
    BEFORE_YESTERDAY,
    AFTER_TOMORROW,
    YESTERDAY,
    TOMORROW,
    LAST_TWO_MONTHS,
    NEXT_TWO_MONTHS,
    LAST_MONTH,
    NEXT_MONTH,
)

BOUND_RULES = ExpressionGroup(
    BEFORE_PREVIOUS,
    AFTER_NEXT,
    BEFORE,
    AFTER,
    PREVIOUS,
    NEXT,
)
