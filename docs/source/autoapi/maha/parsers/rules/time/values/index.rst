:py:mod:`maha.parsers.rules.time.values`
========================================

.. py:module:: maha.parsers.rules.time.values


Module Contents
---------------


Functions
~~~~~~~~~

.. autosummary::

   value_group
   parse_value
   specific_month
   parse_time_fraction



Attributes
~~~~~~~~~~

.. autoapisummary::

   maha.parsers.rules.time.values.THIS
   maha.parsers.rules.time.values.AFTER
   maha.parsers.rules.time.values.BEFORE
   maha.parsers.rules.time.values.PREVIOUS
   maha.parsers.rules.time.values.NEXT
   maha.parsers.rules.time.values.AFTER_NEXT
   maha.parsers.rules.time.values.BEFORE_PREVIOUS
   maha.parsers.rules.time.values.IN_FROM_AT
   maha.parsers.rules.time.values.THIS
   maha.parsers.rules.time.values.LAST
   maha.parsers.rules.time.values.TIME_WORD_SEPARATOR
   maha.parsers.rules.time.values.ordinal_ones_tens
   maha.parsers.rules.time.values.numeral_ones_tens
   maha.parsers.rules.time.values.AT_THE_MOMENT
   maha.parsers.rules.time.values.numeral_thousands
   maha.parsers.rules.time.values.ordinal_thousands
   maha.parsers.rules.time.values.NUMERAL_YEAR
   maha.parsers.rules.time.values.ORDINAL_YEAR
   maha.parsers.rules.time.values.THIS_YEAR
   maha.parsers.rules.time.values.LAST_YEAR
   maha.parsers.rules.time.values.LAST_TWO_YEARS
   maha.parsers.rules.time.values.NEXT_YEAR
   maha.parsers.rules.time.values.NEXT_TWO_YEARS
   maha.parsers.rules.time.values.AFTER_N_YEARS
   maha.parsers.rules.time.values.BEFORE_N_YEARS
   maha.parsers.rules.time.values.JANUARY
   maha.parsers.rules.time.values.FEBRUARY
   maha.parsers.rules.time.values.MARCH
   maha.parsers.rules.time.values.APRIL
   maha.parsers.rules.time.values.MAY
   maha.parsers.rules.time.values.JUNE
   maha.parsers.rules.time.values.JULY
   maha.parsers.rules.time.values.AUGUST
   maha.parsers.rules.time.values.SEPTEMBER
   maha.parsers.rules.time.values.OCTOBER
   maha.parsers.rules.time.values.NOVEMBER
   maha.parsers.rules.time.values.DECEMBER
   maha.parsers.rules.time.values.THIS_MONTH
   maha.parsers.rules.time.values.LAST_MONTH
   maha.parsers.rules.time.values.LAST_TWO_MONTHS
   maha.parsers.rules.time.values.NEXT_MONTH
   maha.parsers.rules.time.values.NEXT_TWO_MONTHS
   maha.parsers.rules.time.values.AFTER_N_MONTHS
   maha.parsers.rules.time.values.BEFORE_N_MONTHS
   maha.parsers.rules.time.values.SPECIFIC_MONTH
   maha.parsers.rules.time.values.NEXT_SPECIFIC_MONTH
   maha.parsers.rules.time.values.PREVIOUS_SPECIFIC_MONTH
   maha.parsers.rules.time.values.AFTER_SPECIFIC_NEXT_MONTH
   maha.parsers.rules.time.values.BEFORE_SPECIFIC_PREVIOUS_MONTH
   maha.parsers.rules.time.values.THIS_WEEK
   maha.parsers.rules.time.values.LAST_WEEK
   maha.parsers.rules.time.values.LAST_TWO_WEEKS
   maha.parsers.rules.time.values.NEXT_WEEK
   maha.parsers.rules.time.values.NEXT_TWO_WEEKS
   maha.parsers.rules.time.values.AFTER_N_WEEKS
   maha.parsers.rules.time.values.BEFORE_N_WEEKS
   maha.parsers.rules.time.values.SUNDAY
   maha.parsers.rules.time.values.MONDAY
   maha.parsers.rules.time.values.TUESDAY
   maha.parsers.rules.time.values.WEDNESDAY
   maha.parsers.rules.time.values.THURSDAY
   maha.parsers.rules.time.values.FRIDAY
   maha.parsers.rules.time.values.SATURDAY
   maha.parsers.rules.time.values.WEEKDAY
   maha.parsers.rules.time.values.THIS_DAY
   maha.parsers.rules.time.values.YESTERDAY
   maha.parsers.rules.time.values.BEFORE_YESTERDAY
   maha.parsers.rules.time.values.TOMORROW
   maha.parsers.rules.time.values.AFTER_TOMORROW
   maha.parsers.rules.time.values.AFTER_N_DAYS
   maha.parsers.rules.time.values.BEFORE_N_DAYS
   maha.parsers.rules.time.values.NEXT_WEEKDAY
   maha.parsers.rules.time.values.PREVIOUS_WEEKDAY
   maha.parsers.rules.time.values.AFTER_NEXT_WEEKDAY
   maha.parsers.rules.time.values.BEFORE_PREVIOUS_WEEKDAY
   maha.parsers.rules.time.values.LAST_DAY
   maha.parsers.rules.time.values.LAST_SPECIFIC_DAY
   maha.parsers.rules.time.values.ORDINAL_SPECIFIC_DAY
   maha.parsers.rules.time.values.LAST_SPECIFIC_DAY_OF_SPECIFIC_MONTH
   maha.parsers.rules.time.values.NUMERAL_HOUR
   maha.parsers.rules.time.values.ORDINAL_HOUR
   maha.parsers.rules.time.values.THIS_HOUR
   maha.parsers.rules.time.values.LAST_HOUR
   maha.parsers.rules.time.values.LAST_TWO_HOURS
   maha.parsers.rules.time.values.NEXT_HOUR
   maha.parsers.rules.time.values.NEXT_TWO_HOURS
   maha.parsers.rules.time.values.AFTER_N_HOURS
   maha.parsers.rules.time.values.BEFORE_N_HOURS
   maha.parsers.rules.time.values.NUMERAL_MINUTE
   maha.parsers.rules.time.values.ORDINAL_MINUTE
   maha.parsers.rules.time.values.THIS_MINUTE
   maha.parsers.rules.time.values.LAST_MINUTE
   maha.parsers.rules.time.values.LAST_TWO_MINUTES
   maha.parsers.rules.time.values.NEXT_MINUTE
   maha.parsers.rules.time.values.NEXT_TWO_MINUTES
   maha.parsers.rules.time.values.AFTER_N_MINUTES
   maha.parsers.rules.time.values.BEFORE_N_MINUTES
   maha.parsers.rules.time.values.PM
   maha.parsers.rules.time.values.AM
   maha.parsers.rules.time.values.YEAR_WITH_MONTH
   maha.parsers.rules.time.values.MONTH_YEAR_FORM
   maha.parsers.rules.time.values.ORDINAL_AND_SPECIFIC_MONTH
   maha.parsers.rules.time.values.ORDINAL_AND_THIS_MONTH
   maha.parsers.rules.time.values.NUMERAL_AND_SPECIFIC_MONTH
   maha.parsers.rules.time.values.NUMERAL_AND_THIS_MONTH
   maha.parsers.rules.time.values.DAY_MONTH_FORM
   maha.parsers.rules.time.values.DAY_MONTH_YEAR_FORM
   maha.parsers.rules.time.values.NUMERAL_FRACTION_HOUR_MINUTE
   maha.parsers.rules.time.values.ORDINAL_FRACTION_HOUR_MINUTE
   maha.parsers.rules.time.values.HOUR_MINUTE_FORM
   maha.parsers.rules.time.values.HOUR_MINUTE_SECOND_FORM
   maha.parsers.rules.time.values.NUMERAL_HOUR_PM
   maha.parsers.rules.time.values.NUMERAL_HOUR_AM
   maha.parsers.rules.time.values.NUMERAL_FRACTION_HOUR_AM
   maha.parsers.rules.time.values.NUMERAL_FRACTION_HOUR_PM
   maha.parsers.rules.time.values.ORDINAL_HOUR_PM
   maha.parsers.rules.time.values.ORDINAL_HOUR_AM
   maha.parsers.rules.time.values.ORDINAL_FRACTION_HOUR_AM
   maha.parsers.rules.time.values.ORDINAL_FRACTION_HOUR_PM


.. py:function:: value_group(value)


.. py:function:: parse_value(value)


.. py:data:: THIS




.. py:data:: AFTER




.. py:data:: BEFORE




.. py:data:: PREVIOUS




.. py:data:: NEXT




.. py:data:: AFTER_NEXT




.. py:data:: BEFORE_PREVIOUS




.. py:data:: IN_FROM_AT




.. py:data:: THIS




.. py:data:: LAST




.. py:data:: TIME_WORD_SEPARATOR




.. py:data:: ordinal_ones_tens




.. py:data:: numeral_ones_tens




.. py:data:: AT_THE_MOMENT




.. py:data:: numeral_thousands




.. py:data:: ordinal_thousands




.. py:data:: NUMERAL_YEAR




.. py:data:: ORDINAL_YEAR




.. py:data:: THIS_YEAR




.. py:data:: LAST_YEAR




.. py:data:: LAST_TWO_YEARS




.. py:data:: NEXT_YEAR




.. py:data:: NEXT_TWO_YEARS




.. py:data:: AFTER_N_YEARS




.. py:data:: BEFORE_N_YEARS




.. py:data:: JANUARY




.. py:data:: FEBRUARY




.. py:data:: MARCH




.. py:data:: APRIL




.. py:data:: MAY




.. py:data:: JUNE




.. py:data:: JULY




.. py:data:: AUGUST




.. py:data:: SEPTEMBER




.. py:data:: OCTOBER




.. py:data:: NOVEMBER




.. py:data:: DECEMBER




.. py:data:: THIS_MONTH




.. py:data:: LAST_MONTH




.. py:data:: LAST_TWO_MONTHS




.. py:data:: NEXT_MONTH




.. py:data:: NEXT_TWO_MONTHS




.. py:data:: AFTER_N_MONTHS




.. py:data:: BEFORE_N_MONTHS




.. py:function:: specific_month(match, next_month=False, years=0)


.. py:data:: SPECIFIC_MONTH




.. py:data:: NEXT_SPECIFIC_MONTH




.. py:data:: PREVIOUS_SPECIFIC_MONTH




.. py:data:: AFTER_SPECIFIC_NEXT_MONTH




.. py:data:: BEFORE_SPECIFIC_PREVIOUS_MONTH




.. py:data:: THIS_WEEK




.. py:data:: LAST_WEEK




.. py:data:: LAST_TWO_WEEKS




.. py:data:: NEXT_WEEK




.. py:data:: NEXT_TWO_WEEKS




.. py:data:: AFTER_N_WEEKS




.. py:data:: BEFORE_N_WEEKS




.. py:data:: SUNDAY




.. py:data:: MONDAY




.. py:data:: TUESDAY




.. py:data:: WEDNESDAY




.. py:data:: THURSDAY




.. py:data:: FRIDAY




.. py:data:: SATURDAY




.. py:data:: WEEKDAY




.. py:data:: THIS_DAY




.. py:data:: YESTERDAY




.. py:data:: BEFORE_YESTERDAY




.. py:data:: TOMORROW




.. py:data:: AFTER_TOMORROW




.. py:data:: AFTER_N_DAYS




.. py:data:: BEFORE_N_DAYS




.. py:data:: NEXT_WEEKDAY




.. py:data:: PREVIOUS_WEEKDAY




.. py:data:: AFTER_NEXT_WEEKDAY




.. py:data:: BEFORE_PREVIOUS_WEEKDAY




.. py:data:: LAST_DAY




.. py:data:: LAST_SPECIFIC_DAY




.. py:data:: ORDINAL_SPECIFIC_DAY




.. py:data:: LAST_SPECIFIC_DAY_OF_SPECIFIC_MONTH




.. py:data:: NUMERAL_HOUR




.. py:data:: ORDINAL_HOUR




.. py:data:: THIS_HOUR




.. py:data:: LAST_HOUR




.. py:data:: LAST_TWO_HOURS




.. py:data:: NEXT_HOUR




.. py:data:: NEXT_TWO_HOURS




.. py:data:: AFTER_N_HOURS




.. py:data:: BEFORE_N_HOURS




.. py:data:: NUMERAL_MINUTE




.. py:data:: ORDINAL_MINUTE




.. py:data:: THIS_MINUTE




.. py:data:: LAST_MINUTE




.. py:data:: LAST_TWO_MINUTES




.. py:data:: NEXT_MINUTE




.. py:data:: NEXT_TWO_MINUTES




.. py:data:: AFTER_N_MINUTES




.. py:data:: BEFORE_N_MINUTES




.. py:data:: PM




.. py:data:: AM




.. py:data:: YEAR_WITH_MONTH




.. py:data:: MONTH_YEAR_FORM




.. py:data:: ORDINAL_AND_SPECIFIC_MONTH




.. py:data:: ORDINAL_AND_THIS_MONTH




.. py:data:: NUMERAL_AND_SPECIFIC_MONTH




.. py:data:: NUMERAL_AND_THIS_MONTH




.. py:data:: DAY_MONTH_FORM




.. py:data:: DAY_MONTH_YEAR_FORM




.. py:function:: parse_time_fraction(match, expression, am_pm=None)


.. py:data:: NUMERAL_FRACTION_HOUR_MINUTE




.. py:data:: ORDINAL_FRACTION_HOUR_MINUTE




.. py:data:: HOUR_MINUTE_FORM




.. py:data:: HOUR_MINUTE_SECOND_FORM




.. py:data:: NUMERAL_HOUR_PM




.. py:data:: NUMERAL_HOUR_AM




.. py:data:: NUMERAL_FRACTION_HOUR_AM




.. py:data:: NUMERAL_FRACTION_HOUR_PM




.. py:data:: ORDINAL_HOUR_PM




.. py:data:: ORDINAL_HOUR_AM




.. py:data:: ORDINAL_FRACTION_HOUR_AM




.. py:data:: ORDINAL_FRACTION_HOUR_PM




