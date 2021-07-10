from dataclasses import dataclass

from .enums import DimensionType, Unit


@dataclass
class Dimension:
    start: int
    end: int
    value: str
    dimension: DimensionType
    is_confident: bool


@dataclass
class UnitDimension:
    unit: Unit
