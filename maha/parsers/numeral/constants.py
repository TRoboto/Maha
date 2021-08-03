from maha.constants import ALEF_VARIATIONS, PATTERN_SPACE_OR_NONE

from ..helper import get_non_capturing_group

ALL_ALEF = "".join(ALEF_VARIATIONS)
TENS_SUFFIX = f"{PATTERN_SPACE_OR_NONE}ع?شر?[ةه]?"
NAME_OF_ZEROS = "صفر"
NAME_OF_ONE = "وا?حد[ةه]"
NAME_OF_TWO = "[إا][ثت]نت?[اي]ن"
NAME_OF_THREE = "[ثت]لا[ثت][ةه]?"
NAME_OF_FOUR = "[أا]ربع[ةه]?"
NAME_OF_FIVE = "خمس[ةه]?"
NAME_OF_SIX = "ست[ةه]?"
NAME_OF_SEVEN = "سبع[ةه]?"
NAME_OF_EIGHT = "[تث]ما?ني[ةه]?"
NAME_OF_NINE = "تسع[ةه]?"
NAME_OF_TEN = "عشر[ةه]?"
NAME_OF_ELEVEN = f"[{ALL_ALEF}]?حد[اى]?" + TENS_SUFFIX
NAME_OF_TWELVE = get_non_capturing_group(
    f"[{ALL_ALEF}][طت]نا?" + TENS_SUFFIX, f"[{ALL_ALEF}][ثت]نت?[اىي]ن?" + TENS_SUFFIX
)
NAME_OF_THIRTEEN = NAME_OF_THREE + TENS_SUFFIX
NAME_OF_FOURTEEN = NAME_OF_FOUR + TENS_SUFFIX
NAME_OF_FIFTEEN = NAME_OF_FIVE + TENS_SUFFIX
NAME_OF_SIXTEEN = NAME_OF_SIX + TENS_SUFFIX
NAME_OF_SEVENTEEN = NAME_OF_SEVEN + TENS_SUFFIX
NAME_OF_EIGHTEEN = NAME_OF_EIGHT + TENS_SUFFIX
NAME_OF_NINETEEN = NAME_OF_NINE + TENS_SUFFIX
