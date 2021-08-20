import itertools as it

from maha.expressions import EXPRESSION_DECIMAL, EXPRESSION_INTEGER, EXPRESSION_SPACE
from maha.expressions.general import EXPRESSION_SPACE_OR_NONE
from maha.parsers.expressions import (
    ALL_ALEF,
    EXPRESSION_END,
    EXPRESSION_START,
    HALF,
    QUARTER,
    SUM_SUFFIX,
    THIRD,
    THREE_QUARTERS,
    TWO_SUFFIX,
    WAW_CONNECTOR,
)
from maha.parsers.rules.templates import Rule
from maha.parsers.templates import ValueExpression
from maha.rexy import Expression, ExpressionGroup, named_group, non_capturing_group

from .template import NumeralExpression


def multiplier_group(value: str) -> str:
    return named_group("multiplier", value)


def numeral_value(value: str) -> str:
    return named_group("numeral_value", value)


def no_multiplier(expression: str):
    return numeral_value(expression) + multiplier_group("")


def get_fractions_pattern(multiplier: str) -> str:
    """
    Returns the fractions of a multiplier.


    Parameters
    ----------
    multiplier: str
        The multiplier text.

    Returns
    -------
    str
        Pattern for the fractions of the multiplier.
    """

    return non_capturing_group(
        *[
            "{multiplier}{space}{three_quarter}",
            "{half}{space}{multiplier}",
            "{third}{space}{multiplier}",
            "{quarter}{space}{multiplier}",
        ]
    ).format(
        half=numeral_value(str(HALF)),
        third=numeral_value(str(THIRD)),
        quarter=numeral_value(str(QUARTER)),
        three_quarter=numeral_value(str(THREE_QUARTERS)),
        space=EXPRESSION_SPACE,
        multiplier=multiplier_group(multiplier),
    )


def get_multiplier_pattern(singular: str, dual: str, plural: str) -> str:
    """
    Returns the regex pattern that matches a numeric followed a unit.

    Parameters
    ----------
    singular:
        The rule name of the singular form of the unit.
    dual:
        The rule name of the dual form of the unit.
    plural:
        The rule name of the plural form of the unit.
    """

    pattern_list = [
        "{decimal}{space}{multiplier_single_plural}",
        "{integer}{space}{multiplier_single_plural}",
        "{tens}{space}{multiplier_single_plural}",
        "{ones}{space}{multiplier_single_plural}",
        get_fractions_pattern(Rule.get(singular).pattern),
        get_fractions_pattern(Rule.get(dual).pattern),
        "{val}{multiplier_dual}",
        "{val}{multiplier_single}",
    ]

    pattern = non_capturing_group(*pattern_list).format(
        decimal=numeral_value(str(EXPRESSION_DECIMAL)),
        integer=numeral_value(str(EXPRESSION_INTEGER)),
        space=EXPRESSION_SPACE,
        multiplier_single_plural=multiplier_group(
            "|".join([Rule.get(singular).pattern, Rule.get(plural).pattern])
        ),
        multiplier_single=multiplier_group(Rule.get(singular).pattern),
        multiplier_dual=multiplier_group(Rule.get(dual).pattern),
        val=numeral_value(""),
        tens=numeral_value(_tens_only_pattern),
        ones=numeral_value(_ones_pattern),
    )
    return pattern


def wrap_pattern(pattern: str) -> str:
    """Adds start and end expression to the pattern."""
    return EXPRESSION_START + pattern + EXPRESSION_END


def get_combinations(*patterns: str):
    for (a, b) in it.combinations_with_replacement(patterns, 2):
        yield a + str(EXPRESSION_OF_FASILA) + b
        if a != b:
            yield b + str(EXPRESSION_OF_FASILA) + a


def _get_perfect_hundreds_pattern(prefix: str):
    return Rule.get(prefix) + EXPRESSION_SPACE_OR_NONE + Rule.get("one_hundred")


TEN_SUFFIX = Expression(f"{EXPRESSION_SPACE_OR_NONE}[تط]?[اع]?شر?[ةه]?")
TEH_OPTIONAL_SUFFIX = Expression("[ةه]?")
EXPRESSION_OF_FASILA = Expression(
    EXPRESSION_SPACE + "فاصل" + TEH_OPTIONAL_SUFFIX + EXPRESSION_SPACE
)

Rule("three_prefix", "[ثت]لا[ثت]"),
Rule("four_prefix", "[أا]ربع"),
Rule("five_prefix", "خمس"),
Rule("six_prefix", "ست"),
Rule("seven_prefix", "سبع"),
Rule("eight_prefix", "[تث]ما?ني?"),
Rule("nine_prefix", "تسع"),
Rule("ten_prefix", "عشر"),

Rule("zero", ValueExpression(0, "صفر")),
Rule("one", ValueExpression(1, "وا?حد" + TEH_OPTIONAL_SUFFIX)),
Rule("two", ValueExpression(2, "[إا][ثت]نت?[اي]ن")),
Rule("three", ValueExpression(3, Rule.get("three_prefix") + TEH_OPTIONAL_SUFFIX)),
Rule("four", ValueExpression(4, Rule.get("four_prefix") + TEH_OPTIONAL_SUFFIX)),
Rule("five", ValueExpression(5, Rule.get("five_prefix") + TEH_OPTIONAL_SUFFIX)),
Rule("six", ValueExpression(6, Rule.get("six_prefix") + TEH_OPTIONAL_SUFFIX)),
Rule("seven", ValueExpression(7, Rule.get("seven_prefix") + TEH_OPTIONAL_SUFFIX)),
Rule("eight", ValueExpression(8, Rule.get("eight_prefix") + TEH_OPTIONAL_SUFFIX)),
Rule("nine", ValueExpression(9, Rule.get("nine_prefix") + TEH_OPTIONAL_SUFFIX)),
Rule("ten", ValueExpression(10, Rule.get("ten_prefix") + TEH_OPTIONAL_SUFFIX))
Rule("eleven", ValueExpression(11, f"{ALL_ALEF}?حد[اى]?" + TEN_SUFFIX)),
Rule(
    "twelve",
    ValueExpression(
        12,
        non_capturing_group(
            f"{ALL_ALEF}[طت]نا?" + TEN_SUFFIX,
            f"{ALL_ALEF}[ثت]نت?[اىي]ن?" + TEN_SUFFIX,
        ),
    ),
)
Rule("thirteen", ValueExpression(13, "[ثت]لا?[ثت]" + TEH_OPTIONAL_SUFFIX + TEN_SUFFIX)),
Rule("fourteen", ValueExpression(14, Rule.get("four") + TEN_SUFFIX))
Rule("fifteen", ValueExpression(15, Rule.get("five") + TEN_SUFFIX))
Rule("sixteen", ValueExpression(16, Rule.get("six") + TEN_SUFFIX))
Rule("seventeen", ValueExpression(17, Rule.get("seven") + TEN_SUFFIX))
Rule("eighteen", ValueExpression(18, "[تث]ما?ني?" + TEH_OPTIONAL_SUFFIX + TEN_SUFFIX))
Rule("nineteen", ValueExpression(19, Rule.get("nine") + TEN_SUFFIX))

Rule("twenty", ValueExpression(20, Rule.get("ten_prefix") + SUM_SUFFIX)),
Rule("thirty", ValueExpression(30, Rule.get("three_prefix") + SUM_SUFFIX)),
Rule("forty", ValueExpression(40, Rule.get("four_prefix") + SUM_SUFFIX)),
Rule("fifty", ValueExpression(50, Rule.get("five_prefix") + SUM_SUFFIX)),
Rule("sixty", ValueExpression(60, Rule.get("six_prefix") + SUM_SUFFIX)),
Rule("seventy", ValueExpression(70, Rule.get("seven_prefix") + SUM_SUFFIX)),
Rule("eighty", ValueExpression(80, Rule.get("eight_prefix") + SUM_SUFFIX)),
Rule("ninety", ValueExpression(90, Rule.get("nine_prefix") + SUM_SUFFIX)),

Rule("one_hundred", ValueExpression(100, "ما?[يئ][ةه]"))
Rule("two_hundreds", ValueExpression(200, "م[يئ]ت" + TWO_SUFFIX))
Rule("three_hundreds", ValueExpression(300, _get_perfect_hundreds_pattern("three")))
Rule("four_hundreds", ValueExpression(400, _get_perfect_hundreds_pattern("four")))
Rule("five_hundreds", ValueExpression(500, _get_perfect_hundreds_pattern("five")))
Rule("six_hundreds", ValueExpression(600, _get_perfect_hundreds_pattern("six")))
Rule("seven_hundreds", ValueExpression(700, _get_perfect_hundreds_pattern("seven")))
Rule("eight_hundreds", ValueExpression(800, _get_perfect_hundreds_pattern("eight")))
Rule("nine_hundreds", ValueExpression(900, _get_perfect_hundreds_pattern("nine")))
Rule("several_hundreds", ValueExpression(100, "م[يئ]ات"))

Rule("one_thousand", ValueExpression(1000, "[أا]لف"))
Rule("two_thousands", ValueExpression(2000, Rule.get("one_thousand") + TWO_SUFFIX))
Rule(
    "several_thousands",
    ValueExpression(1000, non_capturing_group(f"{ALL_ALEF}ل[او]ف", f"{ALL_ALEF}لفات")),
)
Rule("one_million", ValueExpression(1000000, "مليون")),
Rule("two_millions", ValueExpression(2000000, Rule.get("one_million") + TWO_SUFFIX))
Rule("several_millions", ValueExpression(1000000, "ملايين"))
Rule(
    "one_billion", ValueExpression(1000000000, non_capturing_group("بلايين", "مليارات"))
)
Rule("two_billions", ValueExpression(2000000000, Rule.get("one_billion") + TWO_SUFFIX))
Rule(
    "several_billions",
    ValueExpression(3000000000, non_capturing_group("بلايين", "مليارات")),
)
Rule("one_trillion", ValueExpression(1000000000000, "تري?ليون"))
Rule(
    "two_trillions",
    ValueExpression(2000000000000, Rule.get("one_trillion") + TWO_SUFFIX),
)
Rule(
    "several_trillions", ValueExpression(3000000000000, Rule.get("one_trillion") + "ات")
)
# 0 1 2 3 4 5 6 7 8 9
_ones_pattern = Rule.slice("zero", "nine").join()
_ones = no_multiplier(_ones_pattern)
Rule("ones", NumeralExpression(wrap_pattern(_ones)))

# 10 20 30 40 50 60 70 80 90
_perfect_tens = Rule.slice("twenty", "ninety").add_rule(Rule.get("ten"))
Rule(
    "perfect_tens", NumeralExpression(no_multiplier(wrap_pattern(_perfect_tens.join())))
)

# 21 22 23 24 ... 96 97 98 99
_combined_tens = (
    Rule.slice("one", "nine").join()
    + WAW_CONNECTOR
    + Rule.slice("twenty", "ninety").join()
)
Rule("combined_tens", NumeralExpression(wrap_pattern(no_multiplier(_combined_tens))))

# 10 11 12 13 14 ... 95 96 97 98 99
_tens_only_pattern = non_capturing_group(
    *_perfect_tens.patterns,
    _combined_tens,
    *Rule.slice("eleven", "nineteen").patterns,
    Rule.get("ten").pattern,
)
_tens_only = no_multiplier(_tens_only_pattern)
Rule("tens_only", NumeralExpression(wrap_pattern(_tens_only)))

# 300 400 500 600 700 800 900
_perfect_hundreds = no_multiplier(Rule.slice("three_hundreds", "nine_hundreds").join())
Rule("perfect_hundreds", NumeralExpression(wrap_pattern(_perfect_hundreds)))

Rule("integers", NumeralExpression(no_multiplier(str(EXPRESSION_INTEGER))))
Rule(
    "decimals",
    no_multiplier(
        non_capturing_group(
            str(EXPRESSION_DECIMAL),
            *list(
                get_combinations(
                    str(EXPRESSION_INTEGER), _tens_only_pattern, _ones_pattern
                )
            ),
        )
    ),
)


Rule("tens", NumeralExpression(Rule.combine_patterns(_tens_only, _ones)))
Rule(
    "hundreds",
    NumeralExpression(
        Rule.combine_patterns(
            _perfect_hundreds,
            get_multiplier_pattern("one_hundred", "two_hundreds", "several_hundreds"),
            _tens_only,
            _ones,
        )
    ),
)

Rule(
    "thousands",
    NumeralExpression(
        Rule.combine_patterns(
            get_multiplier_pattern(
                "one_thousand", "two_thousands", "several_thousands"
            ),
            _perfect_hundreds,
            get_multiplier_pattern("one_hundred", "two_hundreds", "several_hundreds"),
            _tens_only,
            _ones,
        )
    ),
)

Rule(
    "millions",
    NumeralExpression(
        Rule.combine_patterns(
            get_multiplier_pattern("one_million", "two_millions", "several_millions"),
            get_multiplier_pattern(
                "one_thousand", "two_thousands", "several_thousands"
            ),
            _perfect_hundreds,
            get_multiplier_pattern("one_hundred", "two_hundreds", "several_hundreds"),
            _tens_only,
            _ones,
        )
    ),
)
Rule(
    "billions",
    NumeralExpression(
        Rule.combine_patterns(
            get_multiplier_pattern("one_billion", "two_billions", "several_billions"),
            get_multiplier_pattern("one_million", "two_millions", "several_millions"),
            get_multiplier_pattern(
                "one_thousand", "two_thousands", "several_thousands"
            ),
            _perfect_hundreds,
            get_multiplier_pattern("one_hundred", "two_hundreds", "several_hundreds"),
            _tens_only,
            _ones,
        )
    ),
)
Rule(
    "trillions",
    NumeralExpression(
        Rule.combine_patterns(
            get_multiplier_pattern(
                "one_trillion", "two_trillions", "several_trillions"
            ),
            get_multiplier_pattern("one_billion", "two_billions", "several_billions"),
            get_multiplier_pattern("one_million", "two_millions", "several_millions"),
            get_multiplier_pattern(
                "one_thousand", "two_thousands", "several_thousands"
            ),
            _perfect_hundreds,
            get_multiplier_pattern("one_hundred", "two_hundreds", "several_hundreds"),
            _tens_only,
            _ones,
        )
    ),
)

# generalize the above rules with fasila
# non_capturing_group(
#     Rule.get("trillions").pattern
#     + EXPRESSION_OF_FASILA
#     + Rule.get("trillions").pattern,
#     Rule.get("trillions").pattern,
#     Rule.get("integers").pattern,
# )
Rule(
    "numeral",
    NumeralExpression(
        Rule.combine_patterns(
            get_multiplier_pattern(
                "one_trillion", "two_trillions", "several_trillions"
            ),
            get_multiplier_pattern("one_billion", "two_billions", "several_billions"),
            get_multiplier_pattern("one_million", "two_millions", "several_millions"),
            get_multiplier_pattern(
                "one_thousand", "two_thousands", "several_thousands"
            ),
            _perfect_hundreds,
            get_multiplier_pattern("one_hundred", "two_hundreds", "several_hundreds"),
            Rule.get("decimals").pattern,
            _tens_only,
            _ones,
            Rule.get("integers").pattern,
        )
    ),
)

ORDERED_NUMERALS = ExpressionGroup(
    Rule.get_rules_with_name_startswith("two_").expression_group,
    Rule.get_rules_with_name_startswith("one_").expression_group,
    Rule.get_rules_with_name_startswith("several").expression_group,
    Rule.slice("three_hundreds", "nine_hundreds").expression_group,
    Rule.slice("twenty", "ninety").expression_group,
    Rule.slice("eleven", "ninety").expression_group,
    Rule.slice("zero", "ten").expression_group,
    THREE_QUARTERS,
    HALF,
    QUARTER,
    THIRD,
)
""" The order of which the expressions are evaluated. """
