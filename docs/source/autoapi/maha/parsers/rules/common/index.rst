:py:mod:`maha.parsers.rules.common`
===================================

.. py:module:: maha.parsers.rules.common


Module Contents
---------------


Functions
~~~~~~~~~

.. autosummary::

   get_fractions_of_unit_pattern
   get_fractions_of_pattern
   wrap_pattern
   spaced_patterns



Attributes
~~~~~~~~~~

.. autoapisummary::

   maha.parsers.rules.common.THIRD
   maha.parsers.rules.common.QUARTER
   maha.parsers.rules.common.HALF
   maha.parsers.rules.common.THREE_QUARTERS
   maha.parsers.rules.common.WAW_CONNECTOR
   maha.parsers.rules.common.WORD_SEPARATOR
   maha.parsers.rules.common.ALL_ALEF
   maha.parsers.rules.common.TWO_SUFFIX
   maha.parsers.rules.common.SUM_SUFFIX
   maha.parsers.rules.common.EXPRESSION_START
   maha.parsers.rules.common.EXPRESSION_END


.. py:data:: THIRD


   Pattern that matches the pronunciation of third in Arabic

.. py:data:: QUARTER


   Pattern that matches the pronunciation of quarter in Arabic

.. py:data:: HALF


   Pattern that matches the pronunciation of half in Arabic

.. py:data:: THREE_QUARTERS


   Pattern that matches the pronunciation of three quarters in Arabic

.. py:data:: WAW_CONNECTOR


   Pattern that matches WAW as a connector between two words

.. py:data:: WORD_SEPARATOR


   Pattern that matches the word separator between numerals in Arabic

.. py:data:: ALL_ALEF


   Pattern that matches all possible forms of the ALEF in Arabic

.. py:data:: TWO_SUFFIX


   Pattern that matches the two-suffix of words in Arabic

.. py:data:: SUM_SUFFIX


   Pattern that matches the sum-suffix of words in Arabic

.. py:data:: EXPRESSION_START


   Pattern that matches the start of a rule expression in Arabic

.. py:data:: EXPRESSION_END


   Pattern that matches the end of a rule expression in Arabic

.. py:function:: get_fractions_of_unit_pattern(unit)

   Returns the fractions of a unit pattern.

   :param unit: The unit pattern.
   :type unit: str

   :returns: Pattern for the fractions of the unit.
   :rtype: str


.. py:function:: get_fractions_of_pattern(pattern)

   Returns the fractions of a pattern.

   :param pattern: The pattern.
   :type pattern: str

   :returns: Pattern for the fractions of the input pattern.
   :rtype: str


.. py:function:: wrap_pattern(pattern)

   Adds start and end expression to the pattern.


.. py:function:: spaced_patterns(*patterns)

   Returns a regex pattern that matches any of the given patterns,
   separated by spaces.

   :param patterns: The patterns to match.


