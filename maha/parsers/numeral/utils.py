import re

from ..constants import WAW_CONNECTOR
from .constants import *

NUMBER_MAP = {
    NAME_OF_ELEVEN: 11,
    NAME_OF_TWELVE: 12,
    NAME_OF_THIRTEEN: 13,
    NAME_OF_FOURTEEN: 14,
    NAME_OF_FIFTEEN: 15,
    NAME_OF_SIXTEEN: 16,
    NAME_OF_SEVENTEEN: 17,
    NAME_OF_EIGHTEEN: 18,
    NAME_OF_NINETEEN: 19,
    NAME_OF_ONE: 1,
    NAME_OF_TWO: 2,
    NAME_OF_THREE: 3,
    NAME_OF_FOUR: 4,
    NAME_OF_FIVE: 5,
    NAME_OF_SIX: 6,
    NAME_OF_SEVEN: 7,
    NAME_OF_EIGHT: 8,
    NAME_OF_NINE: 9,
    NAME_OF_TEN: 10,
}


def get_matched_numeral(numeral):
    for key, value in NUMBER_MAP.items():
        if re.match(key, numeral):
            return value


def get_value(text):
    waw = re.search(WAW_CONNECTOR, text)
    if waw:
        ones, tens = text.split(waw.group(0))
        output = get_matched_numeral(ones) + 10 * get_matched_numeral(tens)
    else:
        output = get_matched_numeral(text)
    return output
