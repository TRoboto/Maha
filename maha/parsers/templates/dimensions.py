from dataclasses import dataclass

from .enums import DimensionType, Unit


@dataclass
class Dimension:
    """Template for any parsed item"""

    start: int
    """Start index of the value in the text"""
    end: int
    """End index of the value in the text"""
    value: str
    """Extracted value"""
    dimension: DimensionType = DimensionType.GENERAL
    """Dimension type."""
    is_confident: bool = False
    """Whether the extracted value 100% belongs to the selected dimension. Some patterns
    may match for values that normally belong to the dimension but not always."""


@dataclass
class UnitDimension:
    """Dimension with unit"""

    unit: Unit
