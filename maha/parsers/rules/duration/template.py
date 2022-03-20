from __future__ import annotations

__all__ = ["DurationValue"]


from dataclasses import dataclass

from maha.parsers.templates import DurationUnit

from ..common import ValueUnit
from .utils import convert_between_durations


@dataclass(init=False)
class DurationValue:
    __slots__ = ("values", "normalized_unit")

    values: list[ValueUnit]
    normalized_unit: DurationUnit

    def __init__(self, values: list[ValueUnit], normalized_unit=DurationUnit.SECONDS):
        self.values = values
        self.normalized_unit = normalized_unit

    @property
    def normalized_value(self) -> ValueUnit:
        """Returns the value with unit normalized."""
        return convert_between_durations(*self.values, to_unit=self.normalized_unit)

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, item) -> ValueUnit:
        return self.values[item]
