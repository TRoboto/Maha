from dataclasses import dataclass

from maha.parsers.templates.enums import DimensionType


@dataclass
class EntityPattern:
    expression: str
    """Regular expersion to match"""
    output: str
    r"""Whether a simple string or captured groups (\1\2...)"""
    dimension_type: DimensionType
    """Dimension type."""
    is_confident: bool = False
    """Whether the extracted value 100% belongs to the selected dimension. Some patterns
    may match for values that normally belong to the dimension but not always."""
