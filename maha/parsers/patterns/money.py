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

    expression = r"£([0-9]+)"
    unit = MoneyUnit.POUND
