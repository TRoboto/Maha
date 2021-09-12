:py:mod:`maha.parsers.templates.enums`
======================================

.. py:module:: maha.parsers.templates.enums


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   maha.parsers.templates.enums.DimensionType
   maha.parsers.templates.enums.NumeralType
   maha.parsers.templates.enums.OrdinalType
   maha.parsers.templates.enums.Day
   maha.parsers.templates.enums.Month
   maha.parsers.templates.enums.Unit
   maha.parsers.templates.enums.TimeUnit
   maha.parsers.templates.enums.MoneyUnit
   maha.parsers.templates.enums.DistanceUnit
   maha.parsers.templates.enums.DurationUnit




.. py:class:: DimensionType

   Bases: :py:obj:`enum.Enum`

   Type of the extracted value

   .. py:attribute:: GENERAL




   .. py:attribute:: AMOUNT_OF_MONEY




   .. py:attribute:: DISTANCE




   .. py:attribute:: DURATION




   .. py:attribute:: ORDINAL




   .. py:attribute:: NUMERAL




   .. py:attribute:: TIME




   .. py:attribute:: ARABIC




   .. py:attribute:: ENGLISH




   .. py:attribute:: ARABIC_LETTERS




   .. py:attribute:: ENGLISH_LETTERS




   .. py:attribute:: ENGLISH_SMALL_LETTERS




   .. py:attribute:: ENGLISH_CAPITAL_LETTERS




   .. py:attribute:: NUMBERS




   .. py:attribute:: HARAKAT




   .. py:attribute:: ALL_HARAKAT




   .. py:attribute:: TATWEEL




   .. py:attribute:: PUNCTUATIONS




   .. py:attribute:: ARABIC_NUMBERS




   .. py:attribute:: ENGLISH_NUMBERS




   .. py:attribute:: ARABIC_PUNCTUATIONS




   .. py:attribute:: ENGLISH_PUNCTUATIONS




   .. py:attribute:: ARABIC_LIGATURES




   .. py:attribute:: ARABIC_HASHTAGS




   .. py:attribute:: ARABIC_MENTIONS




   .. py:attribute:: EMAILS




   .. py:attribute:: ENGLISH_HASHTAGS




   .. py:attribute:: ENGLISH_MENTIONS




   .. py:attribute:: HASHTAGS




   .. py:attribute:: LINKS




   .. py:attribute:: MENTIONS




   .. py:attribute:: EMOJIS





.. py:class:: NumeralType

   Bases: :py:obj:`enum.Enum`

   Generic enumeration.

   Derive from this class to define new enumerations.


   .. py:attribute:: DECIMALS




   .. py:attribute:: INTEGERS




   .. py:attribute:: ONES




   .. py:attribute:: TENS




   .. py:attribute:: HUNDREDS




   .. py:attribute:: THOUSANDS




   .. py:attribute:: MILLIONS




   .. py:attribute:: BILLIONS




   .. py:attribute:: TRILLIONS





.. py:class:: OrdinalType

   Bases: :py:obj:`enum.Enum`

   Generic enumeration.

   Derive from this class to define new enumerations.


   .. py:attribute:: ONES




   .. py:attribute:: TENS




   .. py:attribute:: HUNDREDS




   .. py:attribute:: THOUSANDS




   .. py:attribute:: MILLIONS




   .. py:attribute:: BILLIONS




   .. py:attribute:: TRILLIONS





.. py:class:: Day

   Bases: :py:obj:`enum.Enum`

   Generic enumeration.

   Derive from this class to define new enumerations.


   .. py:attribute:: MONDAY
      :annotation: = 0



   .. py:attribute:: TUESDAY




   .. py:attribute:: WEDNESDAY




   .. py:attribute:: THURSDAY




   .. py:attribute:: FRIDAY




   .. py:attribute:: SATURDAY




   .. py:attribute:: SUNDAY





.. py:class:: Month

   Bases: :py:obj:`enum.Enum`

   Generic enumeration.

   Derive from this class to define new enumerations.


   .. py:attribute:: JANUARY




   .. py:attribute:: FEBRUARY




   .. py:attribute:: MARCH




   .. py:attribute:: APRIL




   .. py:attribute:: MAY




   .. py:attribute:: JUNE




   .. py:attribute:: JULY




   .. py:attribute:: AUGUST




   .. py:attribute:: SEPTEMBER




   .. py:attribute:: OCTOBER




   .. py:attribute:: NOVEMBER




   .. py:attribute:: DECEMBER





.. py:class:: Unit

   Bases: :py:obj:`enum.Enum`

   Base class for all units


.. py:class:: TimeUnit

   Bases: :py:obj:`Unit`

   Base class for all units

   .. py:attribute:: SECONDS




   .. py:attribute:: MINUTES




   .. py:attribute:: HOURS




   .. py:attribute:: DAYS




   .. py:attribute:: MONTHS




   .. py:attribute:: YEARS





.. py:class:: MoneyUnit

   Bases: :py:obj:`Unit`

   Base class for all units

   .. py:attribute:: EURO




   .. py:attribute:: DOLLAR




   .. py:attribute:: POUND





.. py:class:: DistanceUnit

   Bases: :py:obj:`Unit`

   Base class for all units

   .. py:attribute:: METER




   .. py:attribute:: MILE





.. py:class:: DurationUnit

   Bases: :py:obj:`Unit`

   Base class for all units

   .. py:attribute:: SECONDS




   .. py:attribute:: MINUTES




   .. py:attribute:: HOURS




   .. py:attribute:: DAYS




   .. py:attribute:: WEEKS




   .. py:attribute:: MONTHS




   .. py:attribute:: YEARS





