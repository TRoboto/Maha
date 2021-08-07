__all__ = ["get_matched_numeral", "get_value"]

import re

import maha.parsers.numeral.rule as rule

from ..constants import HALF, QUARTER, THIRD, THREE_QUARTERS, WAW_CONNECTOR
from ..helper import convert_to_number_if_possible
from .constants import *

NUMBER_MAP = {
    NAME_OF_TWO_HUNDREDS: 200,
    NAME_OF_TWO_THOUSANDS: 2000,
    NAME_OF_TWO_MILLIONS: 2000000,
    NAME_OF_TWO_BILLIONS: 2000000000,
    NAME_OF_TWO_TRILLIONS: 2000000000000,
    NAME_OF_HUNDREDS: 100,
    NAME_OF_HUNDRED: 100,
    NAME_OF_THOUSANDS: 1000,
    NAME_OF_THOUSAND: 1000,
    NAME_OF_MILLIONS: 1000000,
    NAME_OF_MILLION: 1000000,
    NAME_OF_BILLIONS: 1000000000,
    NAME_OF_BILLION: 1000000000,
    NAME_OF_TRILLIONS: 1000000000000,
    NAME_OF_TRILLION: 1000000000000,
    NAME_OF_ELEVEN: 11,
    NAME_OF_TWELVE: 12,
    NAME_OF_THIRTEEN: 13,
    NAME_OF_FOURTEEN: 14,
    NAME_OF_FIFTEEN: 15,
    NAME_OF_SIXTEEN: 16,
    NAME_OF_SEVENTEEN: 17,
    NAME_OF_EIGHTEEN: 18,
    NAME_OF_NINETEEN: 19,
    NAME_OF_ZERO: 0,
    NAME_OF_ONE: 1,
    NAME_OF_TWO: 2,
    # This is a special case of the pattern twenty and eighty.
    # TODO: Improve this.
    NAME_OF_TWENTY: 2,
    NAME_OF_THREE: 3,
    NAME_OF_FOUR: 4,
    NAME_OF_FIVE: 5,
    NAME_OF_SIX: 6,
    NAME_OF_SEVEN: 7,
    NAME_OF_EIGHT: 8,
    NAME_OF_NINE: 9,
    NAME_OF_TEN: 10,
    HALF: 0.5,
    QUARTER: 0.25,
    THIRD: 1 / 3,
    THREE_QUARTERS: 0.75,
}


def get_matched_numeral(numeral) -> int:
    for key, value in NUMBER_MAP.items():
        if re.match(key, numeral):
            return value


def get_value(text: str) -> float:
    fasila = re.search(rule.FASILA, text)
    if fasila:
        before, after = text.split(fasila.group(0))
        before = convert_to_number_if_possible(before)
        after = convert_to_number_if_possible(after)
        if isinstance(before, str):
            before = get_matched_numeral(before)
        if isinstance(after, str):
            after = get_matched_numeral(after)
        output = float(f"{before}.{after}")
        return output

    waw = re.search(WAW_CONNECTOR, text)
    if waw:
        ones, tens = text.split(waw.group(0))
        output = get_matched_numeral(ones) + 10 * get_matched_numeral(tens)
        return output

    if re.match(rule._PATTERN_NUMERAL_PERFECT_TENS, text):
        return 10 * get_matched_numeral(text)

    if re.match(rule._PATTERN_NUMERAL_PERFECT_HUNDREDS, text):
        return 100 * get_matched_numeral(text)

    output = get_matched_numeral(text)
    return output
