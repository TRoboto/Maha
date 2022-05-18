from __future__ import annotations

__all__ = ["DistanceValue"]


from dataclasses import dataclass, field

from maha.parsers.templates import DistanceUnit

from ..common import ValueUnit
from .utils import convert_between_distances


@dataclass
class DistanceValue:

    valueunit: ValueUnit
    normalized_unit: DistanceUnit = field(default=DistanceUnit.METERS, repr=False)

    @property
    def value(self):
        return self.valueunit.value

    @property
    def unit(self):
        return self.valueunit.unit

    @property
    def normalized_value(self) -> ValueUnit:
        """Returns the value with unit normalized."""
        return convert_between_distances(self.valueunit, to_unit=self.normalized_unit)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value}, unit={self.unit})"
