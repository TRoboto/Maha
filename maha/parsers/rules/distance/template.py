from __future__ import annotations

__all__ = ["DistanceValue"]


from dataclasses import dataclass

from maha.parsers.templates import DistanceUnit

from ..common import ValueUnit
from .utils import convert_between_distances


@dataclass(init=False)
class DistanceValue:
    __slots__ = ("values", "normalized_unit")

    values: list[ValueUnit]
    normalized_unit: DistanceUnit

    def __init__(self, values: list[ValueUnit], normalized_unit=DistanceUnit.METERS):
        self.values = values
        self.normalized_unit = normalized_unit

    @property
    def normalized_value(self) -> ValueUnit:
        """Returns the value with unit normalized."""
        return convert_between_distances(*self.values, to_unit=self.normalized_unit)

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, item) -> ValueUnit:
        return self.values[item]
