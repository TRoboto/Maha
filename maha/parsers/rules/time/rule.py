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
from maha.parsers.rules.utils import spaced_patterns
from maha.parsers.templates import Rule, RuleCollection, Value
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
    ]

    pattern = non_capturing_group(*pattern_list).format(
        singular=get_unit_group(singular.pattern),
        space=EXPRESSION_SPACE,
        value=get_value_group(values.join()),
        next=bound_group(str(NEXT)),
        prev=bound_group(str(PREVIOUS)),
        in_from_this=IN_FROM_AT_THIS,
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
YESTERDAY = Value(
    relativedelta(days=-1),
    non_capturing_group(
        "[اإ]?مبارح",
        ALEF_LAM + "بارح[ةه]",
        ALEF_LAM_OPTIONAL + "[أا]مس",
        spaced_patterns(BEFORE, Rule.get("one_day")),
        spaced_patterns(ALEF_LAM + Rule.get("one_day"), PREVIOUS),
    ),
)
BEFORE_YESTERDAY = Value(
    relativedelta(days=-2),
    non_capturing_group(
        spaced_patterns(non_capturing_group("[أا]ول", str(BEFORE)), YESTERDAY),
        spaced_patterns(ALEF_LAM + Rule.get("one_day"), BEFORE_PREVIOUS),
        spaced_patterns(BEFORE, Rule.get("two_days")),
    ),
)
TOMORROW = Value(
    relativedelta(days=1),
    non_capturing_group(
        ALEF_LAM_OPTIONAL + "غدا?",
        "بكر[ةه]",
        spaced_patterns(ALEF_LAM + Rule.get("one_day"), NEXT),
        spaced_patterns(AFTER, Rule.get("one_day")),
    ),
)
AFTER_TOMORROW = Value(
    relativedelta(days=2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + Rule.get("one_day"), AFTER_NEXT),
        spaced_patterns(AFTER, TOMORROW),
        spaced_patterns(AFTER, Rule.get("two_days")),
    ),
)
LAST_MONTH = Value(
    relativedelta(months=-1),
    non_capturing_group(
        spaced_patterns(BEFORE, Rule.get("one_month")),
        spaced_patterns(ALEF_LAM + Rule.get("one_month"), PREVIOUS),
    ),
)
LAST_TWO_MONTHS = Value(
    relativedelta(months=-2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + Rule.get("one_month"), BEFORE_PREVIOUS),
        spaced_patterns(BEFORE, Rule.get("two_months")),
    ),
)
NEXT_MONTH = Value(
    relativedelta(months=1),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + Rule.get("one_month"), NEXT),
        spaced_patterns(AFTER, Rule.get("one_month")),
    ),
)
NEXT_TWO_MONTHS = Value(
    relativedelta(months=2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + Rule.get("one_month"), AFTER_NEXT),
        spaced_patterns(AFTER, Rule.get("two_months")),
    ),
)
Rule("sunday", Value(SU, "ال[أا]حد"))
Rule("monday", Value(MO, "ال[إا][تث]نين"))
Rule("tuesday", Value(TU, "ال[ثت]لا[ثت]اء"))
Rule("wednesday", Value(WE, "ال[أا]ربعاء"))
Rule("thursday", Value(TH, "الخميس"))
Rule("friday", Value(FR, "الجمع[ةه]"))
Rule("saturday", Value(SA, "السبت"))
Rule(
    "january",
    Value(relativedelta(month=1), non_capturing_group("يناير", "كانون الثاني")),
)
Rule(
    "february",
    Value(relativedelta(month=2), non_capturing_group("فبراير", "شباط")),
)
Rule(
    "march",
    Value(relativedelta(month=3), non_capturing_group("مارس", "[اأآ]ذار")),
)
Rule(
    "april",
    Value(relativedelta(month=4), non_capturing_group("نيسان", f"{ALL_ALEF}بريل")),
)
Rule("may", Value(relativedelta(month=5), non_capturing_group("مايو", "أيار")))
Rule(
    "june",
    Value(relativedelta(month=6), non_capturing_group("يونيو", "حزيران")),
)
Rule(
    "july",
    Value(relativedelta(month=7), non_capturing_group("يوليو", "تموز")),
)
Rule(
    "august",
    Value(relativedelta(month=8), non_capturing_group("[اأ]غسطس", "[أاآ]ب")),
)
Rule(
    "september",
    Value(relativedelta(month=9), non_capturing_group("سبتمبر", "[اأ]يلول")),
)
Rule(
    "october",
    Value(relativedelta(month=10), non_capturing_group("[اأ]كتوبر", "تشرين الأول")),
)
Rule(
    "november",
    Value(relativedelta(month=11), non_capturing_group("نوفمبر", "تشرين الثاني")),
)
Rule(
    "december",
    Value(relativedelta(month=12), non_capturing_group("ديسمبر", "كانون الأول")),
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
                value_group(Rule.slice("sunday", "saturday").join()),
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
                value_group(Rule.slice("january", "december").join()),
                get_pattern("month", Rule.slice("january", "december")),
            )
        ),
    ),
)

Rule(
    "time",
    TimeExpression(
        Rule.combine_patterns(
            # spaced_patterns(
            #     get_unit_group(Rule.get("one_day") + "?"),
            #     get_value_group(Rule.slice("sunday", "saturday").join()),
            #     IN_FROM_AT + '?',
            #     Rule.get('integer').pattern,
            #     value_group(Rule.slice("january", "december").join())
            # ),
            Rule.get("time_now").pattern,
            Rule.get("time_day").pattern,
            Rule.get("time_month").pattern,
            seperator=TIME_WORD_SEPARATOR,
        ),
    ),
)

ORDERED_TIMES = ExpressionGroup()

SPECIAL_TIMES = ExpressionGroup(
    Rule.slice("january", "december").expression_group,
    Rule.slice("sunday", "saturday").expression_group,
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
