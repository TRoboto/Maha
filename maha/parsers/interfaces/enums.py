from enum import Enum, auto


class DimensionType(Enum):
    """Type of the extracted value"""

    GENERAL = auto()
    AMOUNT_OF_MONEY = auto()
    DISTANCE = auto()
    DURATION = auto()
    ARABIC = auto()
    ENGLISH = auto()
    ARABIC_LETTERS = auto()
    ENGLISH_LETTERS = auto()
    ENGLISH_SMALL_LETTERS = auto()
    ENGLISH_CAPITAL_LETTERS = auto()
    NUMBERS = auto()
    HARAKAT = auto()
    ALL_HARAKAT = auto()
    TATWEEL = auto()
    PUNCTUATIONS = auto()
    ARABIC_NUMBERS = auto()
    ENGLISH_NUMBERS = auto()
    ARABIC_PUNCTUATIONS = auto()
    ENGLISH_PUNCTUATIONS = auto()
    ARABIC_LIGATURES = auto()
    ARABIC_HASHTAGS = auto()
    ARABIC_MENTIONS = auto()
    EMAILS = auto()
    ENGLISH_HASHTAGS = auto()
    ENGLISH_MENTIONS = auto()
    HASHTAGS = auto()
    LINKS = auto()
    MENTIONS = auto()
    EMOJIS = auto()


class NumeralType(Enum):
    DECIMALS = auto()
    INTEGERS = auto()
    ONES = auto()
    TENS = auto()
    HUNDREDS = auto()
    THOUSANDS = auto()
    MILLIONS = auto()
    BILLIONS = auto()
    TRILLIONS = auto()


class Unit(Enum):
    """Base class for all units"""

    pass


class MoneyUnit(Unit):
    EURO = auto()
    DOLLAR = auto()
    POUND = auto()


class DistanceUnit(Unit):
    METER = auto()
    MILE = auto()


class DurationUnit(Unit):
    SECONDS = auto()
    MINUTES = auto()
    HOURS = auto()
    DAYS = auto()
    WEEKS = auto()
    MONTHS = auto()
    YEARS = auto()
