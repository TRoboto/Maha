"""
Functions that return shared expressions.
"""

NUMBER_EXPRESSION: str = "([0-9]+)"


def get_number_followed_by_string(expression: str) -> str:
    return r"\b{}\s*{}\b".format(NUMBER_EXPRESSION, expression)
