__all__ = ["get_matched_numeral", "get_value"]


import maha.parsers.numeral.rule as rule
from maha.parsers.interfaces.expression_group import ExpressionGroup

from ..constants import WAW_CONNECTOR
from ..helper import convert_to_number_if_possible
from .expressions import *


def get_matched_numeral(numeral) -> int:
    return check_for_match(rule.ORDERED_NUMERALS, numeral)


def handle_fasila(text) -> float:
    fasila = rule.EXPRESSION_OF_FASILA.search(text)
    before, after = text.split(fasila.group(0))
    before = get_value(before)
    after = get_value(after)
    output = float(f"{before}.{after}")
    return output


def check_for_match(expression_group: ExpressionGroup, text: str) -> float:
    for exp in expression_group:
        if exp.match(text):
            return exp.value
    return None


def get_value(text: str) -> float:

    output = convert_to_number_if_possible(text)
    if not isinstance(output, str):
        return output

    if rule.EXPRESSION_OF_FASILA.search(text):
        return handle_fasila(text)

    waw = WAW_CONNECTOR.search(text)
    if waw:
        ones, tens = text.split(waw.group(0))
        output = get_matched_numeral(ones) + get_matched_numeral(tens)
        return output

    output = get_matched_numeral(text)
    return output
