"""
Expressions to extract amount of money.
"""

from ..templates import Expression, ExpressionGroup, MoneyUnit
from .helper import NUMBER_EXPRESSION, get_number_followed_by_string

EXPRESSION_AMOUNT_OF_MONEY_POUND = ExpressionGroup(
    Expression(f"£{NUMBER_EXPRESSION}", is_confident=True),
    Expression(get_number_followed_by_string("باوند")),
).set_unit(MoneyUnit.POUND)
