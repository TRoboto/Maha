:py:mod:`maha.parsers.templates`
================================

.. py:module:: maha.parsers.templates


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   dimension/index.rst
   enums/index.rst
   text_expression/index.rst
   value_expressions/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   maha.parsers.templates.Dimension
   maha.parsers.templates.DimensionType
   maha.parsers.templates.NumeralType
   maha.parsers.templates.OrdinalType
   maha.parsers.templates.Day
   maha.parsers.templates.Month
   maha.parsers.templates.Unit
   maha.parsers.templates.TimeUnit
   maha.parsers.templates.MoneyUnit
   maha.parsers.templates.DistanceUnit
   maha.parsers.templates.DurationUnit
   maha.parsers.templates.TextExpression
   maha.parsers.templates.Value
   maha.parsers.templates.MatchedValue
   maha.parsers.templates.FunctionValue




.. py:class:: Dimension(expression, body, value, start, end, dimension_type)

   Template for the parsed item

   .. py:attribute:: expression
      :annotation: :maha.rexy.Expression

      The expression that was used to find the value

   .. py:attribute:: body
      :annotation: :str

      Text from the input that was matched by the expression.

   .. py:attribute:: value
      :annotation: :Any

      Extracted value

   .. py:attribute:: start
      :annotation: :int

      Start index of the value in the text

   .. py:attribute:: end
      :annotation: :int

      End index of the value in the text

   .. py:attribute:: dimension_type
      :annotation: :maha.parsers.templates.enums.DimensionType

      Dimension type.


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





.. py:class:: TextExpression(pattern, pickle = False)

   Bases: :py:obj:`maha.rexy.Expression`

   Expression that returns the matched text as value

   .. py:method:: parse(self, match, text)

      Extract the value from the input ``text`` and return it.

      .. note::
          This is a simple implementation that needs a group to match.

      .. warning::
          This method is called by :meth:`__call__` to extract the value from
          the input ``text``. You should not call this method directly.


      :param match: Matched object.
      :type match: :class:`regex.Match`
      :param text: Text in which the match was found.
      :type text: str

      :Yields: :class:`ExpressionResult` -- Extracted value.

      :raises ValueError: If no capture group was found.



.. py:class:: Value(value, pattern, pickle = False)

   Bases: :py:obj:`maha.rexy.Expression`

   Expression that returns a predefined value if the pattern matches.

   .. py:attribute:: value
      :annotation: :Any



   .. py:method:: parse(self, match, _)

      Extract the value from the input ``text`` and return it.

      .. note::
          This is a simple implementation that needs a group to match.

      .. warning::
          This method is called by :meth:`__call__` to extract the value from
          the input ``text``. You should not call this method directly.


      :param match: Matched object.
      :type match: :class:`regex.Match`
      :param text: Text in which the match was found.
      :type text: str

      :Yields: :class:`ExpressionResult` -- Extracted value.

      :raises ValueError: If no capture group was found.



.. py:class:: MatchedValue(expressions, pattern)

   Bases: :py:obj:`Value`

   Expression that returns a predefined value of a matched expression from the input
   expressions

   :param expressions: The expressions to match
   :type expressions: ExpressionGroup
   :param pattern: The pattern to match
   :type pattern: str

   :returns: The result of the expression
   :rtype: ExpressionResult

   .. py:method:: parse(self, match, _)

      Extract the value from the input ``text`` and return it.

      .. note::
          This is a simple implementation that needs a group to match.

      .. warning::
          This method is called by :meth:`__call__` to extract the value from
          the input ``text``. You should not call this method directly.


      :param match: Matched object.
      :type match: :class:`regex.Match`
      :param text: Text in which the match was found.
      :type text: str

      :Yields: :class:`ExpressionResult` -- Extracted value.

      :raises ValueError: If no capture group was found.



.. py:class:: FunctionValue(function, pattern, pickle = True)

   Bases: :py:obj:`Value`

   Expression that returns the output value of an input function when matched.

   :param function: The function to be called when the pattern matches.
   :type function: Callable
   :param pattern: The pattern to be matched.
   :type pattern: str

   :returns: The result of the expression.
   :rtype: ExpressionResult

   .. py:method:: parse(self, match, _)

      Extract the value from the input ``text`` and return it.

      .. note::
          This is a simple implementation that needs a group to match.

      .. warning::
          This method is called by :meth:`__call__` to extract the value from
          the input ``text``. You should not call this method directly.


      :param match: Matched object.
      :type match: :class:`regex.Match`
      :param text: Text in which the match was found.
      :type text: str

      :Yields: :class:`ExpressionResult` -- Extracted value.

      :raises ValueError: If no capture group was found.



