from maha.expressions import EXPRESSION_SPACE_OR_NONE
from maha.parsers.templates import Value
from maha.rexy import Expression, non_capturing_group

from ..common import ALL_ALEF, SUM_SUFFIX, TEH_OPTIONAL_SUFFIX, TWO_SUFFIX

TEN_SUFFIX = f"{EXPRESSION_SPACE_OR_NONE}[تط]?[اع]?شر?[ةه]?"
EXPRESSION_OF_FASILA = Expression("فاصل" + TEH_OPTIONAL_SUFFIX)


three_prefix = "[ثت]لا[ثت]"
four_prefix = "[أا]ربع"
five_prefix = "خمس"
six_prefix = "ست"
seven_prefix = "سبع"
eight_prefix = "[تث]ما?ني?"
nine_prefix = "تسع"
ten_prefix = "عشر"

ZERO = Value(0, "صفر")
ONE = Value(1, "وا?حد" + TEH_OPTIONAL_SUFFIX)
TWO = Value(2, "[إا]?[ثت]نت?[اي]ن")
THREE = Value(3, three_prefix + TEH_OPTIONAL_SUFFIX)
FOUR = Value(4, four_prefix + TEH_OPTIONAL_SUFFIX)
FIVE = Value(5, five_prefix + TEH_OPTIONAL_SUFFIX)
SIX = Value(6, six_prefix + TEH_OPTIONAL_SUFFIX)
SEVEN = Value(7, seven_prefix + TEH_OPTIONAL_SUFFIX)
EIGHT = Value(8, eight_prefix + TEH_OPTIONAL_SUFFIX)
NINE = Value(9, nine_prefix + TEH_OPTIONAL_SUFFIX)
TEN = Value(10, ten_prefix + TEH_OPTIONAL_SUFFIX)

ELEVEN = Value(11, f"{ALL_ALEF}?حد[اى]?" + TEN_SUFFIX)
TWELVE = Value(
    12,
    non_capturing_group(
        f"{ALL_ALEF}[طت]نا?" + TEN_SUFFIX,
        f"{ALL_ALEF}[ثت]نت?[اىي]ن?" + TEN_SUFFIX,
    ),
)
THIRTEEN = Value(13, "[ثت]لا?[ثت]" + TEH_OPTIONAL_SUFFIX + TEN_SUFFIX)
FOURTEEN = Value(14, FOUR + TEN_SUFFIX)
FIFTEEN = Value(15, FIVE + TEN_SUFFIX)
SIXTEEN = Value(16, SIX + TEN_SUFFIX)
SEVENTEEN = Value(17, SEVEN + TEN_SUFFIX)
EIGHTEEN = Value(18, "[تث]ما?ني?" + TEH_OPTIONAL_SUFFIX + TEN_SUFFIX)
NINETEEN = Value(19, NINE + TEN_SUFFIX)

TWENTY = Value(20, ten_prefix + SUM_SUFFIX)
THIRTY = Value(30, three_prefix + SUM_SUFFIX)
FORTY = Value(40, four_prefix + SUM_SUFFIX)
FIFTY = Value(50, five_prefix + SUM_SUFFIX)
SIXTY = Value(60, six_prefix + SUM_SUFFIX)
SEVENTY = Value(70, seven_prefix + SUM_SUFFIX)
EIGHTY = Value(80, eight_prefix + SUM_SUFFIX)
NINETY = Value(90, nine_prefix + SUM_SUFFIX)

ONE_HUNDRED = Value(100, "ما?[يئ][ةه]")
TWO_HUNDREDS = Value(200, "م[يئ]ت" + TWO_SUFFIX)
THREE_HUNDREDS = Value(300, THREE + EXPRESSION_SPACE_OR_NONE + ONE_HUNDRED)
FOUR_HUNDREDS = Value(400, FOUR + EXPRESSION_SPACE_OR_NONE + ONE_HUNDRED)
FIVE_HUNDREDS = Value(500, FIVE + EXPRESSION_SPACE_OR_NONE + ONE_HUNDRED)
SIX_HUNDREDS = Value(600, SIX + EXPRESSION_SPACE_OR_NONE + ONE_HUNDRED)
SEVEN_HUNDREDS = Value(700, SEVEN + EXPRESSION_SPACE_OR_NONE + ONE_HUNDRED)
EIGHT_HUNDREDS = Value(800, EIGHT + EXPRESSION_SPACE_OR_NONE + ONE_HUNDRED)
NINE_HUNDREDS = Value(900, NINE + EXPRESSION_SPACE_OR_NONE + ONE_HUNDRED)
SEVERAL_HUNDREDS = Value(100, "م[يئ]ات")

ONE_THOUSAND = Value(1000, "[أا]لف")
TWO_THOUSANDS = Value(2000, ONE_THOUSAND + TWO_SUFFIX)
SEVERAL_THOUSANDS = Value(
    1000, non_capturing_group(f"{ALL_ALEF}ل[او]ف", f"{ALL_ALEF}لفات")
)
ONE_MILLION = Value(1000000, "مليون")
TWO_MILLIONS = Value(2000000, ONE_MILLION + TWO_SUFFIX)
SEVERAL_MILLIONS = Value(1000000, "ملايين")
ONE_BILLION = Value(1000000000, non_capturing_group("بليون", "مليار"))
TWO_BILLIONS = Value(2000000000, ONE_BILLION + TWO_SUFFIX)
SEVERAL_BILLIONS = Value(1000000000, non_capturing_group("بلايين", "مليارات"))
ONE_TRILLION = Value(1000000000000, "تري?ليون")
TWO_TRILLIONS = Value(2000000000000, ONE_TRILLION + TWO_SUFFIX)
SEVERAL_TRILLIONS = Value(1000000000000, ONE_TRILLION + "ات")
