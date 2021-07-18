__all__ = ["Expression"]

from dataclasses import dataclass
from typing import Callable, Optional

from .types import Unit


@dataclass
class Expression:
    __slots__ = ["pattern", "is_confident", "output", "unit"]

    pattern: str
    """Regular expersion(s) to match"""
    is_confident: bool
    """Whether the extracted value 100% belongs to the selected dimension. Some patterns
    may match for values that normally belong to the dimension but not always."""
    output: Callable[..., str]
    """
    A function to operate on the extracted value.

    When ``output`` is set to ``None``, the extracted value is returned as-is.
    """
    unit: Optional[Unit]
    """Unit of the dimension"""

    def __init__(
        self,
        pattern: str,
        is_confident: bool = False,
        output: Callable[..., str] = None,
        unit: Optional[Unit] = None,
    ):
        self.pattern = pattern
        self.is_confident = is_confident
        self.unit = unit
        if output is None:
            self.output = lambda *args: "".join(args) if len(args) > 1 else args[0]
        else:
            self.output = output

    def __repr__(self):
        out = f"Expression(pattern={self.pattern}, is_confident={self.is_confident})"
        return out

    def format(self, format_spec: str):
        self.pattern = self.pattern.format(format_spec)
        return self

    def set_unit(self, unit: Unit):
        self.unit = unit
        return self
