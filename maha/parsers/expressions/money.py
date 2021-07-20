"""
Expressions to extract amount of money.
"""

from ..templates import Expression, MoneyUnit

_NUMBER_EXPRESSION = "([0-9]+)"

EXPRESSION_AMOUNT_OF_MONEY_POUND = [
    e.format(_NUMBER_EXPRESSION).set_unit(MoneyUnit.POUND)
    for e in [
        Expression("£{}", is_confident=True),
        Expression(r"{}\s*باوند\b"),
    ]
]
