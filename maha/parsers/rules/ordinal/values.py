from maha.expressions import EXPRESSION_SPACE, EXPRESSION_SPACE_OR_NONE
from maha.parsers.expressions import ALL_ALEF, SUM_SUFFIX
from maha.parsers.templates import MatchedValue, Value
from maha.parsers.templates.rule import Rule
from maha.rexy import non_capturing_group

TEN_SUFFIX = f"{EXPRESSION_SPACE_OR_NONE}[تط]?[اع]?شر?[ةه]?"
TEN_SUFFIX_SIMPLE = f"{EXPRESSION_SPACE}عشر[ةه]?"
TEH_OPTIONAL_SUFFIX = "[ةه]?"
ALEF_LAM = non_capturing_group("ال")
ALEF_LAM_OPTIONAL = ALEF_LAM + "?"


one_prefix = "واحد"
two_prefix = non_capturing_group("[تث]ان[يى]", "[إا]?[ثت]نت؟[يى]")
three_prefix = "[تث]ال[ثت]"
four_prefix = "رابع"
five_prefix = "خامس"
six_prefix = "سادس"
seven_prefix = "سابع"
eight_prefix = "[تث]امن"
nine_prefix = "تاسع"
ten_prefix = "عاشر"

ONE = Value(1, ALEF_LAM_OPTIONAL + "[أا]ول[ىي]?")
TWO = Value(2, ALEF_LAM_OPTIONAL + "[تث]ان[يى]" + TEH_OPTIONAL_SUFFIX)
THREE = Value(3, ALEF_LAM_OPTIONAL + three_prefix + TEH_OPTIONAL_SUFFIX)
FOUR = Value(4, ALEF_LAM_OPTIONAL + four_prefix + TEH_OPTIONAL_SUFFIX)
FIVE = Value(5, ALEF_LAM_OPTIONAL + five_prefix + TEH_OPTIONAL_SUFFIX)
SIX = Value(6, ALEF_LAM_OPTIONAL + six_prefix + TEH_OPTIONAL_SUFFIX)
SEVEN = Value(7, ALEF_LAM_OPTIONAL + seven_prefix + TEH_OPTIONAL_SUFFIX)
EIGHT = Value(8, ALEF_LAM_OPTIONAL + eight_prefix + TEH_OPTIONAL_SUFFIX)
NINE = Value(9, ALEF_LAM_OPTIONAL + nine_prefix + TEH_OPTIONAL_SUFFIX)
TEN = Value(10, ALEF_LAM_OPTIONAL + ten_prefix + TEH_OPTIONAL_SUFFIX)

ONE_PREFIX = Value(1, ALEF_LAM + one_prefix + TEH_OPTIONAL_SUFFIX)
TWO_PREFIX = Value(2, ALEF_LAM + two_prefix + TEH_OPTIONAL_SUFFIX)
THREE_PREFIX = Value(3, ALEF_LAM + three_prefix + TEH_OPTIONAL_SUFFIX)
FOUR_PREFIX = Value(4, ALEF_LAM + four_prefix + TEH_OPTIONAL_SUFFIX)
FIVE_PREFIX = Value(5, ALEF_LAM + five_prefix + TEH_OPTIONAL_SUFFIX)
SIX_PREFIX = Value(6, ALEF_LAM + six_prefix + TEH_OPTIONAL_SUFFIX)
SEVEN_PREFIX = Value(7, ALEF_LAM + seven_prefix + TEH_OPTIONAL_SUFFIX)
EIGHT_PREFIX = Value(8, ALEF_LAM + eight_prefix + TEH_OPTIONAL_SUFFIX)
NINE_PREFIX = Value(9, ALEF_LAM + nine_prefix + TEH_OPTIONAL_SUFFIX)

ELEVEN = Value(
    11,
    non_capturing_group(
        ALEF_LAM + f"{ALL_ALEF}?حد[اى]?" + TEN_SUFFIX,
        ALEF_LAM_OPTIONAL + "حاد[يى]" + TEN_SUFFIX_SIMPLE,
    ),
)
TWELVE = Value(
    12,
    non_capturing_group(
        ALEF_LAM
        + non_capturing_group(
            f"{ALL_ALEF}[طت]نا?" + TEN_SUFFIX,
            f"{ALL_ALEF}[ثت]نت?[اىي]ن?" + TEN_SUFFIX,
        ),
        ALEF_LAM_OPTIONAL + two_prefix + TEN_SUFFIX_SIMPLE,
    ),
)
THIRTEEN = Value(13, THREE + TEN_SUFFIX_SIMPLE)
FOURTEEN = Value(14, FOUR + TEN_SUFFIX_SIMPLE)
FIFTEEN = Value(15, FIVE + TEN_SUFFIX_SIMPLE)
SIXTEEN = Value(16, SIX + TEN_SUFFIX_SIMPLE)
SEVENTEEN = Value(17, SEVEN + TEN_SUFFIX_SIMPLE)
EIGHTEEN = Value(18, EIGHT + TEN_SUFFIX_SIMPLE)
NINETEEN = Value(19, NINE + TEN_SUFFIX_SIMPLE)

TWENTY = Value(20, ALEF_LAM + "عشر" + SUM_SUFFIX)
THIRTY = Value(30, ALEF_LAM + Rule.get("three_prefix") + SUM_SUFFIX)
FORTY = Value(40, ALEF_LAM + Rule.get("four_prefix") + SUM_SUFFIX)
FIFTY = Value(50, ALEF_LAM + Rule.get("five_prefix") + SUM_SUFFIX)
SIXTY = Value(60, ALEF_LAM + Rule.get("six_prefix") + SUM_SUFFIX)
SEVENTY = Value(70, ALEF_LAM + Rule.get("seven_prefix") + SUM_SUFFIX)
EIGHTY = Value(80, ALEF_LAM + Rule.get("eight_prefix") + SUM_SUFFIX)
NINETY = Value(90, ALEF_LAM + Rule.get("nine_prefix") + SUM_SUFFIX)

ONE_HUNDRED = Value(100, ALEF_LAM + Rule.get("one_hundred"))
TWO_HUNDREDS = Value(200, ALEF_LAM + Rule.get("two_hundreds"))
THREE_HUNDREDS = Value(
    300,
    ALEF_LAM + Rule.get("three") + EXPRESSION_SPACE_OR_NONE + Rule.get("one_hundred"),
)
FOUR_HUNDREDS = Value(
    400,
    ALEF_LAM + Rule.get("four") + EXPRESSION_SPACE_OR_NONE + Rule.get("one_hundred"),
)
FIVE_HUNDREDS = Value(
    500,
    ALEF_LAM + Rule.get("five") + EXPRESSION_SPACE_OR_NONE + Rule.get("one_hundred"),
)
SIX_HUNDREDS = Value(
    600, ALEF_LAM + Rule.get("six") + EXPRESSION_SPACE_OR_NONE + Rule.get("one_hundred")
)
SEVEN_HUNDREDS = Value(
    700,
    ALEF_LAM + Rule.get("seven") + EXPRESSION_SPACE_OR_NONE + Rule.get("one_hundred"),
)
EIGHT_HUNDREDS = Value(
    800,
    ALEF_LAM + Rule.get("eight") + EXPRESSION_SPACE_OR_NONE + Rule.get("one_hundred"),
)
NINE_HUNDREDS = Value(
    900,
    ALEF_LAM + Rule.get("nine") + EXPRESSION_SPACE_OR_NONE + Rule.get("one_hundred"),
)
ONE_THOUSAND = Value(1000, ALEF_LAM + Rule.get("one_thousand"))
TWO_THOUSANDS = Value(2000, ALEF_LAM + Rule.get("two_thousands"))
ONE_MILLION = Value(1000000, ALEF_LAM + Rule.get("one_million"))
TWO_MILLIONS = Value(2000000, ALEF_LAM + Rule.get("two_millions"))
ONE_BILLION = Value(1000000000, ALEF_LAM + Rule.get("one_billion"))
TWO_BILLIONS = Value(2000000000, ALEF_LAM + Rule.get("two_billions"))
ONE_TRILLION = Value(1000000000000, ALEF_LAM + Rule.get("one_trillion"))
TWO_TRILLIONS = Value(2000000000000, ALEF_LAM + Rule.get("two_trillions"))
