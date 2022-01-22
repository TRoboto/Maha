from .common import *
from .duration import *
from .names import *
from .numeral import *
from .ordinal import *
from .time import *


def compile_rules():
    compile_numeral_rules()
    compile_ordinal_rules()
    compile_time_rules()
    compile_duration_rules()


def compile_numeral_rules():
    for rule in [
        RULE_NUMERAL_ONES,
        RULE_NUMERAL_TENS,
        RULE_NUMERAL_HUNDREDS,
        RULE_NUMERAL_THOUSANDS,
        RULE_NUMERAL_MILLIONS,
        RULE_NUMERAL_BILLIONS,
        RULE_NUMERAL_TRILLIONS,
        RULE_NUMERAL_INTEGERS,
        RULE_NUMERAL,
    ]:
        rule.compile()


def compile_ordinal_rules():
    for rule in [
        RULE_ORDINAL_ONES,
        RULE_ORDINAL_TENS,
        RULE_ORDINAL_HUNDREDS,
        RULE_ORDINAL_THOUSANDS,
        RULE_ORDINAL_MILLIONS,
        RULE_ORDINAL_BILLIONS,
        RULE_ORDINAL_TRILLIONS,
        RULE_ORDINAL,
    ]:
        rule.compile()


def compile_time_rules():
    for rule in [
        RULE_TIME_YEARS,
        RULE_TIME_MONTHS,
        RULE_TIME_WEEKS,
        RULE_TIME_DAYS,
        RULE_TIME_HOURS,
        RULE_TIME_MINUTES,
        RULE_TIME_AM_PM,
        RULE_TIME_NOW,
        RULE_TIME,
    ]:
        rule.compile()


def compile_duration_rules():
    for rule in [
        RULE_DURATION_SECONDS,
        RULE_DURATION_MINUTES,
        RULE_DURATION_HOURS,
        RULE_DURATION_DAYS,
        RULE_DURATION_WEEKS,
        RULE_DURATION_MONTHS,
        RULE_DURATION_YEARS,
        RULE_DURATION,
    ]:
        rule.compile()
