from dataclasses import dataclass

from maha.parsers.templates import DimensionType, MoneyUnit, UnitDimension


@dataclass
class MoneyDimension(UnitDimension):
    unit: MoneyUnit
    dimension_type: DimensionType = DimensionType.AMOUNT_OF_MONEY
    is_confident = True
    value = r"\1"


class PoundDimension(MoneyDimension):
    """Pound dimension"""

    expression = r"£([0-9]+)"
    unit = MoneyUnit.POUND
