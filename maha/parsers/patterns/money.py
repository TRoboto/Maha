from dataclasses import dataclass

from maha.parsers.templates import DimensionType, MoneyUnit, UnitDimensionPattern


@dataclass(init=False)
class MoneyDimension(UnitDimensionPattern):
    unit: MoneyUnit
    dimension: DimensionType = DimensionType.AMOUNT_OF_MONEY
    is_confident = True
    output = None


class PoundDimension(MoneyDimension):
    """Pound dimension"""

    expression = ["£([0-9]+)", r"([0-9]+)\s*با?وند\b"]
    unit = MoneyUnit.POUND
