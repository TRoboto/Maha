from enum import Enum, auto


class DimensionType(Enum):
    AMOUNT_OF_MONEY = auto()
    DISTANCE = auto()
    DURATION = auto()


class Unit:
    pass


class MoneyUnit(Enum):
    EURO = auto()
    DOLLAR = auto()


class DistanceUnit(Enum):
    METER = auto()
    MILE = auto()


class DurationUnit(Enum):
    SECONDS = auto()
    MINUTES = auto()
