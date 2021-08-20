from maha.expressions import EXPRESSION_SPACE, EXPRESSION_SPACE_OR_NONE
from maha.parsers.expressions import ALL_ALEF, SUM_SUFFIX, TWO_SUFFIX, WAW_CONNECTOR
from maha.parsers.helper import wrap_pattern
from maha.parsers.templates import Rule, ValueExpression
from maha.rexy import Expression, ExpressionGroup, named_group, non_capturing_group

from .template import OrdinalExpression


def multiplier_group(value: str) -> str:
    return named_group("multiplier", value)


def numeral_value(value: str) -> str:
    return named_group("numeral_value", value)


def get_multiplier_pattern(singular: str, dual: str) -> str:
    # order matters
    _pattern = [
        "{tens}{space}{multiplier_single}",
        "{ones}{space}{multiplier_single}",
        "{val}{multiplier_dual}",
        "{val}{multiplier_single}",
    ]
    pattern = non_capturing_group(*_pattern).format(
        space=EXPRESSION_SPACE,
        multiplier_single=multiplier_group(Rule.get(singular).pattern),
        multiplier_dual=multiplier_group(Rule.get(dual).pattern),
        val=numeral_value(""),
        tens=numeral_value(_ones_pattern),
        ones=numeral_value(_tens_only_pattern),
    )
    return pattern


def no_multiplier(expression: str):
    return numeral_value(expression) + multiplier_group("")


def add_prefix(pattern: Rule):
    return ALEF_LAM + pattern


def ones_wrap(rule_name: str):
    return add_prefix(Rule.get(rule_name)) + TEH_OPTIONAL_SUFFIX


def ones_owrap(rule_name: str):
    return ALEF_LAM_OPTIONAL + Rule.get(rule_name) + TEH_OPTIONAL_SUFFIX


def perfect_tens_wrap(rule_name: str):
    return add_prefix(Rule.get(rule_name)) + SUM_SUFFIX


def perfect_hundreds_wrap(rule_name: str):
    return (
        ALEF_LAM
        + Rule.get(rule_name)
        + EXPRESSION_SPACE_OR_NONE
        + Rule.get("one_hundred")
    )


TEN_SUFFIX = Expression(f"{EXPRESSION_SPACE_OR_NONE}[تط]?[اع]?شر?[ةه]?")
TEN_SUFFIX_SIMPLE = Expression(f"{EXPRESSION_SPACE}عشر[ةه]?")
TEH_OPTIONAL_SUFFIX = Expression("[ةه]?")
ALEF_LAM = Expression(non_capturing_group("ال"))
ALEF_LAM_OPTIONAL = Expression(ALEF_LAM + "?")

Rule("ordinal_one_prefix", "واحد")
Rule("ordinal_two_prefix", non_capturing_group("[تث]ان[يى]", "[إا]?[ثت]نت؟[يى]"))
Rule("ordinal_three_prefix", "[تث]ال[ثت]")
Rule("ordinal_four_prefix", "رابع")
Rule("ordinal_five_prefix", "خامس")
Rule("ordinal_six_prefix", "سادس")
Rule("ordinal_seven_prefix", "سابع")
Rule("ordinal_eight_prefix", "[تث]امن")
Rule("ordinal_nine_prefix", "تاسع")
Rule("ordinal_ten_prefix", "عاشر")

Rule("ordinal_one_alone", ValueExpression(1, ALEF_LAM_OPTIONAL + "[أا]ول[ىي]?"))
Rule(
    "ordinal_two_alone",
    ValueExpression(2, ALEF_LAM_OPTIONAL + "[تث]ان[يى]" + TEH_OPTIONAL_SUFFIX),
)
Rule("ordinal_three_alone", ValueExpression(3, ones_owrap("ordinal_three_prefix")))
Rule("ordinal_four_alone", ValueExpression(4, ones_owrap("ordinal_four_prefix")))
Rule("ordinal_five_alone", ValueExpression(5, ones_owrap("ordinal_five_prefix")))
Rule("ordinal_six_alone", ValueExpression(6, ones_owrap("ordinal_six_prefix")))
Rule("ordinal_seven_alone", ValueExpression(7, ones_owrap("ordinal_seven_prefix")))
Rule("ordinal_eight_alone", ValueExpression(8, ones_owrap("ordinal_eight_prefix")))
Rule("ordinal_nine_alone", ValueExpression(9, ones_owrap("ordinal_nine_prefix")))

Rule("ordinal_one", ValueExpression(1, ones_wrap("ordinal_one_prefix")))
Rule("ordinal_two", ValueExpression(2, ones_wrap("ordinal_two_prefix")))
Rule("ordinal_three", ValueExpression(3, ones_wrap("ordinal_three_prefix")))
Rule("ordinal_four", ValueExpression(4, ones_wrap("ordinal_four_prefix")))
Rule("ordinal_five", ValueExpression(5, ones_wrap("ordinal_five_prefix")))
Rule("ordinal_six", ValueExpression(6, ones_wrap("ordinal_six_prefix")))
Rule("ordinal_seven", ValueExpression(7, ones_wrap("ordinal_seven_prefix")))
Rule("ordinal_eight", ValueExpression(8, ones_wrap("ordinal_eight_prefix")))
Rule("ordinal_nine", ValueExpression(9, ones_wrap("ordinal_nine_prefix")))
Rule("ordinal_ten", ValueExpression(10, ones_owrap("ordinal_ten_prefix")))

Rule(
    "ordinal_eleven",
    ValueExpression(
        11,
        non_capturing_group(
            ALEF_LAM + f"{ALL_ALEF}?حد[اى]?" + TEN_SUFFIX,
            ALEF_LAM_OPTIONAL + "حاد[يى]" + TEN_SUFFIX_SIMPLE,
        ),
    ),
)
Rule(
    "ordinal_twelve",
    ValueExpression(
        12,
        non_capturing_group(
            ALEF_LAM
            + non_capturing_group(
                f"{ALL_ALEF}[طت]نا?" + TEN_SUFFIX,
                f"{ALL_ALEF}[ثت]نت?[اىي]ن?" + TEN_SUFFIX,
            ),
            ALEF_LAM_OPTIONAL + Rule.get("ordinal_two_prefix") + TEN_SUFFIX_SIMPLE,
        ),
    ),
)
Rule(
    "ordinal_thirteen",
    ValueExpression(13, Rule.get("ordinal_three_alone") + TEN_SUFFIX_SIMPLE),
)
Rule(
    "ordinal_fourteen",
    ValueExpression(14, Rule.get("ordinal_four_alone") + TEN_SUFFIX_SIMPLE),
)
Rule(
    "ordinal_fifteen",
    ValueExpression(15, Rule.get("ordinal_five_alone") + TEN_SUFFIX_SIMPLE),
)
Rule(
    "ordinal_sixteen",
    ValueExpression(16, Rule.get("ordinal_six_alone") + TEN_SUFFIX_SIMPLE),
)
Rule(
    "ordinal_seventeen",
    ValueExpression(17, Rule.get("ordinal_seven_alone") + TEN_SUFFIX_SIMPLE),
)
Rule(
    "ordinal_eighteen",
    ValueExpression(18, Rule.get("ordinal_eight_alone") + TEN_SUFFIX_SIMPLE),
)
Rule(
    "ordinal_nineteen",
    ValueExpression(19, Rule.get("ordinal_nine_alone") + TEN_SUFFIX_SIMPLE),
)
Rule(
    "ordinal_twenty",
    ValueExpression(20, ALEF_LAM + "عشر" + SUM_SUFFIX),
)
Rule("ordinal_thirty", ValueExpression(30, perfect_tens_wrap("three_prefix")))
Rule("ordinal_forty", ValueExpression(40, perfect_tens_wrap("four_prefix")))
Rule("ordinal_fifty", ValueExpression(50, perfect_tens_wrap("five_prefix")))
Rule("ordinal_sixty", ValueExpression(60, perfect_tens_wrap("six_prefix")))
Rule("ordinal_seventy", ValueExpression(70, perfect_tens_wrap("seven_prefix")))
Rule("ordinal_eighty", ValueExpression(80, perfect_tens_wrap("eight_prefix")))
Rule("ordinal_ninety", ValueExpression(90, perfect_tens_wrap("nine_prefix")))
Rule("ordinal_one_hundred", ValueExpression(100, ALEF_LAM + Rule.get("one_hundred")))
Rule("ordinal_two_hundreds", ValueExpression(200, ALEF_LAM + Rule.get("two_hundreds")))
Rule("ordinal_three_hundreds", ValueExpression(300, perfect_hundreds_wrap("three")))
Rule("ordinal_four_hundreds", ValueExpression(400, perfect_hundreds_wrap("four")))
Rule("ordinal_five_hundreds", ValueExpression(500, perfect_hundreds_wrap("five")))
Rule("ordinal_six_hundreds", ValueExpression(600, perfect_hundreds_wrap("six")))
Rule("ordinal_seven_hundreds", ValueExpression(700, perfect_hundreds_wrap("seven")))
Rule("ordinal_eight_hundreds", ValueExpression(800, perfect_hundreds_wrap("eight")))
Rule("ordinal_nine_hundreds", ValueExpression(900, perfect_hundreds_wrap("nine")))

Rule(
    "ordinal_one_thousand", ValueExpression(1000, add_prefix(Rule.get("one_thousand")))
)
Rule(
    "ordinal_two_thousands",
    ValueExpression(2000, add_prefix(Rule.get("two_thousands"))),
)
Rule(
    "ordinal_one_million",
    ValueExpression(1000000, add_prefix(Rule.get("one_million"))),
)
Rule(
    "ordinal_two_millions",
    ValueExpression(2000000, add_prefix(Rule.get("two_millions"))),
)
Rule(
    "ordinal_one_billion",
    ValueExpression(1000000000, add_prefix(Rule.get("one_billion"))),
)
Rule(
    "ordinal_two_billions",
    ValueExpression(2000000000, add_prefix(Rule.get("two_billions"))),
)
Rule(
    "ordinal_one_trillion",
    ValueExpression(1000000000000, add_prefix(Rule.get("one_trillion"))),
)
Rule(
    "ordinal_two_trillions",
    ValueExpression(2000000000000, add_prefix(Rule.get("two_trillions"))),
)

# 1 2 3 4 5 6 7 8 9
_ones_pattern = Rule.slice("ordinal_one_alone", "ordinal_nine_alone").join()
_ones = no_multiplier(_ones_pattern)
Rule("ordinal_ones", OrdinalExpression(wrap_pattern(_ones)))

_ones_prefix = no_multiplier(Rule.slice("ordinal_one", "ordinal_nine").join())
Rule("ordinal_ones_prefix", OrdinalExpression(wrap_pattern(_ones_prefix)))

# 10 20 30 40 50 60 70 80 90
_perfect_tens = Rule.slice("ordinal_ten", "ordinal_ninety")
Rule(
    "ordinal_perfect_tens",
    OrdinalExpression(no_multiplier(wrap_pattern(_perfect_tens.join()))),
)
# 21 22 23 24 ... 96 97 98 99
_combined_tens = (
    Rule.slice("ordinal_one", "ordinal_nine").join()
    + WAW_CONNECTOR
    + Rule.slice("ordinal_twenty", "ordinal_ninety").join()
)
# 10 11 12 13 14 ... 95 96 97 98 99
_tens_only_pattern = non_capturing_group(
    *_perfect_tens.patterns,
    _combined_tens,
    *Rule.slice("ordinal_eleven", "ordinal_nineteen").patterns,
)
_tens_only = no_multiplier(_tens_only_pattern)
Rule("ordinal_tens_only", OrdinalExpression(wrap_pattern(_tens_only)))

# 300 400 500 600 700 800 900
_perfect_hundreds = no_multiplier(
    Rule.slice("ordinal_three_hundreds", "ordinal_nine_hundreds").join()
)
Rule("ordinal_perfect_hundreds", OrdinalExpression(wrap_pattern(_perfect_hundreds)))


Rule("ordinal_tens", OrdinalExpression(Rule.combine_patterns(_tens_only, _ones)))
Rule(
    "ordinal_hundreds",
    OrdinalExpression(
        Rule.combine_patterns(
            _perfect_hundreds,
            get_multiplier_pattern("ordinal_one_hundred", "ordinal_two_hundreds"),
            _tens_only,
            _ones,
        )
    ),
)
Rule(
    "ordinal_thousands",
    OrdinalExpression(
        Rule.combine_patterns(
            get_multiplier_pattern("ordinal_one_thousand", "ordinal_two_thousands"),
            _perfect_hundreds,
            get_multiplier_pattern("ordinal_one_hundred", "ordinal_two_hundreds"),
            _tens_only,
            _ones,
        )
    ),
)
Rule(
    "ordinal_millions",
    OrdinalExpression(
        Rule.combine_patterns(
            get_multiplier_pattern("ordinal_one_million", "ordinal_two_millions"),
            get_multiplier_pattern("ordinal_one_thousand", "ordinal_two_thousands"),
            _perfect_hundreds,
            get_multiplier_pattern("ordinal_one_hundred", "ordinal_two_hundreds"),
            _tens_only,
            _ones,
        )
    ),
)
Rule(
    "ordinal_billions",
    OrdinalExpression(
        Rule.combine_patterns(
            get_multiplier_pattern("ordinal_one_billion", "ordinal_two_billions"),
            get_multiplier_pattern("ordinal_one_million", "ordinal_two_millions"),
            get_multiplier_pattern("ordinal_one_thousand", "ordinal_two_thousands"),
            _perfect_hundreds,
            get_multiplier_pattern("ordinal_one_hundred", "ordinal_two_hundreds"),
            _tens_only,
            _ones,
        )
    ),
)

Rule(
    "ordinal_trillions",
    OrdinalExpression(
        Rule.combine_patterns(
            get_multiplier_pattern("ordinal_one_trillion", "ordinal_two_trillions"),
            get_multiplier_pattern("ordinal_one_billion", "ordinal_two_billions"),
            get_multiplier_pattern("ordinal_one_million", "ordinal_two_millions"),
            get_multiplier_pattern("ordinal_one_thousand", "ordinal_two_thousands"),
            _perfect_hundreds,
            get_multiplier_pattern("ordinal_one_hundred", "ordinal_two_hundreds"),
            _tens_only,
            _ones,
        )
    ),
)
Rule("ordinal", Rule.get("ordinal_trillions").expression)

ORDERED_ORDINALS = ExpressionGroup(
    Rule.get_rules_with_names(
        "ordinal_two_trillions",
        "ordinal_two_billions",
        "ordinal_two_millions",
        "ordinal_two_thousands",
        "ordinal_two_hundreds",
    ).expression_group,
    Rule.get_rules_with_names(
        "ordinal_one_trillion",
        "ordinal_one_billion",
        "ordinal_one_million",
        "ordinal_one_thousand",
        "ordinal_one_hundred",
    ).expression_group,
    Rule.slice("ordinal_three_hundreds", "ordinal_nine_hundreds").expression_group,
    Rule.slice("ordinal_twenty", "ordinal_ninety").expression_group,
    Rule.slice("ordinal_eleven", "ordinal_nineteen").expression_group,
    Rule.slice("ordinal_one_alone", "ordinal_nine_alone").expression_group,
    Rule.slice("ordinal_one", "ordinal_ten").expression_group,
)
""" The order of which the expressions are evaluated. """
