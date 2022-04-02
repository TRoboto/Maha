"""
Logic for converting numbers to text
"""
__all__ = [
    "numbers_to_text",
]

import regex as re

import maha.cleaners.functions as functions
from maha.constants import TEH_MARBUTA
from maha.expressions import EXPRESSION_DECIMAL, EXPRESSION_INTEGER
from maha.parsers.utils import convert_to_number_if_possible
from maha.rexy import non_capturing_group

FASILA = "فاصلة"
TWO_SUFFIX_NOMINATIVE = "ان"
SUM_SUFFIX_NOMINATIVE = "ون"
TWO_SUM_SUFFIX_ACCUSATIVE = "ين"
CONNECTOR = "و"

ONE_HUNDRED = "مائة"
ONE_HUNDRED_PREFIX = "مئت"
ONE_THOUSAND = "ألف"
ONE_MILLION = "مليون"
ONE_BILLION = "مليار"
ONE_TRILLION = "تريليون"

BELOW_TEN_THOUSANDS = "آلاف"
BELOW_TEN_MILLIONS = "ملايين"
BELOW_TEN_BILLIONS = "مليارات"
BELOW_TEN_TRILLIONS = "تريليونات"


TEN_PREFIX = "عشر"
ELEVEN_PREFIX = "أحد"
EIGHT_PREFIX = "ثمان"

MULTIPLIER_MAP = {
    1: [ONE_THOUSAND, BELOW_TEN_THOUSANDS],
    2: [ONE_MILLION, BELOW_TEN_MILLIONS],
    3: [ONE_BILLION, BELOW_TEN_BILLIONS],
    4: [ONE_TRILLION, BELOW_TEN_TRILLIONS],
}

NUMBER_MAP = {
    "0": "صفر",
    "1": "واحد",
    "2": "إثن",
    "3": "ثلاث",
    "4": "أربع",
    "5": "خمس",
    "6": "ست",
    "7": "سبع",
    "8": "ثماني",
    "9": "تسع",
}


def numbers_to_text(text: str, accusative: bool = False):
    """Converts numbers in text to their equivalent text in Arabic.

    Parameters
    ----------
    text : str
        Text with numbers to be converted.
    accusative : bool, optional
        If True, the number will be converted to its accusative form.

    Returns
    -------
    str
        Text with numbers converted to their equivalent text in Arabic.

    """
    converted_text = functions.arabic_numbers_to_english(text)
    output = re.sub(
        non_capturing_group(EXPRESSION_DECIMAL, EXPRESSION_INTEGER),
        lambda x: number_to_text(x.group(), accusative),
        converted_text,
    )

    return output


def number_to_text(number: str, accusative: bool):
    number_corrected = convert_to_number_if_possible(number)
    if len(str(number_corrected)) > 15:
        print(f"Number {number} is too long to be converted to text")
        return number
    splits = str(number_corrected).split(".")
    if len(splits) == 2:
        integer, decimal = splits
        integer_part = _convert_number(integer, accusative)
        decimal_part = _handle_decimal_part(integer, decimal, accusative)

        if int(integer) and int(decimal):
            return integer_part + f" {FASILA} " + decimal_part
        elif int(integer):
            return integer_part
        elif int(decimal):
            return decimal_part

        return integer_part + decimal_part
    return _convert_number(splits[0], accusative)


def _handle_decimal_part(integer_part: str, decimal_part: str, accusative: bool) -> str:
    number = int(decimal_part)
    suffix = ""
    if number == 0:
        return ""
    if decimal_part[0] == "0" or int(integer_part) == 0:
        decimal_suffix = "1" + len(decimal_part.rstrip("0")) * "0"
        suffix = " من " + _convert_number(decimal_suffix, accusative)
    return _convert_number(decimal_part, accusative) + suffix


def _convert_number(number: str, accusative) -> str:
    if number == "0":
        return NUMBER_MAP[number]
    parts = [part[::-1] for part in re.split(r"(\d{1,3})", number[::-1]) if part]
    output = []
    for i, part in enumerate(parts):
        text = _get_text_for_hundreds(part, accusative)
        multiplier = _get_multiplier(part, i, accusative)
        if text and multiplier:
            if int(part) <= 2:
                output.append(multiplier)
            else:
                output.append(text + " " + multiplier)
        elif text:
            output.append(text)
    return f" {CONNECTOR}".join(output[::-1])


def _get_multiplier(part: str, i: int, accusative) -> str:
    if i == 0:
        return ""
    two_suffix = TWO_SUM_SUFFIX_ACCUSATIVE if accusative else TWO_SUFFIX_NOMINATIVE
    number = int(part)
    multiplier = MULTIPLIER_MAP[i]
    if number == 1:
        return multiplier[0]
    if number == 2:
        return multiplier[0] + two_suffix

    return multiplier[number <= 10]


def _get_text_for_hundreds(part: str, accusative: bool) -> str:
    number = int(part)
    part = str(number)  # removes leading zeros
    two_suffix = TWO_SUM_SUFFIX_ACCUSATIVE if accusative else TWO_SUFFIX_NOMINATIVE
    if number < 100:
        return _get_text_for_tens(part, accusative)

    if part[0] == "1":
        hundred_text = ONE_HUNDRED
    elif part[0] == "2":
        hundred_text = ONE_HUNDRED_PREFIX + two_suffix
    elif part[0] == "8":
        hundred_text = EIGHT_PREFIX + ONE_HUNDRED
    else:
        hundred_text = NUMBER_MAP[part[0]] + ONE_HUNDRED

    if part[1] == "0" and part[2] == "0":
        return hundred_text
    return (
        hundred_text
        + f" {CONNECTOR}"
        + _get_text_for_tens("".join(part[1:]), accusative)
    )


def _get_text_for_tens(part: str, accusative: bool) -> str:
    number = int(part)
    part = str(number)  # removes leading zeros
    sum_suffix = TWO_SUM_SUFFIX_ACCUSATIVE if accusative else SUM_SUFFIX_NOMINATIVE
    if number == 0:
        return ""
    if number < 10:
        return _from_one_to_nine(part, accusative)
    if number == 10:
        return TEN_PREFIX + TEH_MARBUTA
    if number == 11:
        return ELEVEN_PREFIX + " " + TEN_PREFIX
    if number == 12:
        return NUMBER_MAP["2"] + ("ي" if accusative else "ا") + " " + TEN_PREFIX
    if number < 20:
        return NUMBER_MAP[part[1]] + TEH_MARBUTA + " " + TEN_PREFIX
    if number == 20:
        return TEN_PREFIX + sum_suffix

    if part[1] == "0":
        return (
            NUMBER_MAP[part[0]] + sum_suffix
            if part[0] != "8"
            else EIGHT_PREFIX + sum_suffix
        )

    if part[0] == "8":
        ten = EIGHT_PREFIX + sum_suffix
    elif part[0] == "2":
        ten = TEN_PREFIX + sum_suffix
    else:
        ten = NUMBER_MAP[part[0]] + sum_suffix

    return _from_one_to_nine(part[1], accusative) + " " + CONNECTOR + ten


def _from_one_to_nine(part: str, accusative: bool) -> str:
    number = int(part)
    part = str(number)  # removes leading zeros
    two_suffix = TWO_SUM_SUFFIX_ACCUSATIVE if accusative else TWO_SUFFIX_NOMINATIVE
    if number == 1:
        return NUMBER_MAP[part]
    if number == 2:
        return NUMBER_MAP[part] + two_suffix
    return NUMBER_MAP[part] + TEH_MARBUTA
