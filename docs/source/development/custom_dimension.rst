================
Custom Dimension
================

This document walks you through how to create a custom dimension,
which can be used later with :func:`~.parse_dimension`.

.. admonition:: Definition

    A dimension is simply a rule that combines a set of special expressions (e.g.
    :class:`~.Value`, :class:`~.MatchedValue`, and :class:`~.FunctionValue`).
    These expressions define a regular expression with a corresponding value.

A dimension consists of two main steps:

#. The :meth:`.Expression.parse` function of the rule is called on the input
   text. It returns a list of :class:`~.ExpressionResult` instances.

#. Each body of the :class:`~.ExpressionResult` is fully matched against all of the
   special expressions of that rule. Once a match is found, the corresponding
   value is evaluated and returned.

Simple rule
-----------

Let us start by creating a rule to extract number of books from text.

.. code-block:: pycon
    :emphasize-lines: 10

    >>> # Import the numeral rule.
    >>> from maha.parsers.rules import RULE_NUMERAL
    >>> # Import a helper function
    >>> from maha.parsers.rules import spaced_patterns
    >>> # Import the numeral parse function
    >>> from maha.parsers.rules.numeral.rule import parse_numeral
    >>> # Import the special expression, function value
    >>> from maha.parsers.templates import FunctionValue
    >>> # Define the rule, which is simply a number followed by a space and the word "كتاب".
    >>> RULE_BOOK_NUMBER = FunctionValue(
    ...     parse_numeral, spaced_patterns(RULE_NUMERAL, "كتاب"), pickle=False
    ... )
    >>> # Use the rule to parse the text.
    >>> sample_text = "في المكتبة مئة كتاب"
    >>> result = list(RULE_BOOK_NUMBER.parse(sample_text))[0]
    >>> result.value
    100
    >>> sample_text[result.start : result.end]
    'مئة كتاب'

The rule can be seen highlighted in the above code.
The rule is an instance of :class:`~.FunctionValue` that first finds any text that matches
a numeral followed by the word "كتاب", and then evaluates the numeral using the
:func:`~maha.parsers.rules.numeral.rule.parse_numeral` function and returns the result.

Multi-value rule
----------------

For more than one value, it is preferable to have all values defined in a file. To showcase
an example, here are the values used to define the :data:`RULE_DURATION`.

.. literalinclude:: ../../../maha/parsers/rules/duration/values.py

To define a rule for the values of seconds, you can do the following:

.. code-block:: pycon

    >>> # Import helper functions
    >>> from maha.rexy import non_capturing_group
    >>> from maha.parsers.rules import spaced_patterns
    >>> from maha.parsers.templates import FunctionValue

    >>> # Import the numeral parse function
    >>> from maha.parsers.rules.numeral.rule import parse_numeral

    >>> # Import the values for seconds
    >>> from maha.parsers.rules.duration.values import ONE_SECOND, TWO_SECONDS, SEVERAL_SECONDS

    >>> # Define a custom parse function for seconds which gets the matched object as input.
    >>> def parse_seconds(match):
    ...     # Get the matched text
    ...     matched_text = match.group(0)
    ...     # Check if the matched text is two seconds only.
    ...     if TWO_SECONDS.fullmatch(matched_text):
    ...         return 2
    ...     # Check if the matched text is one second only.
    ...     if ONE_SECOND.fullmatch(matched_text):
    ...         return 1
    ...     # If the code reaches this point, it means that the matched text is numeral
    ...     # followed by seconds
    ...     return parse_numeral(match)
    ...


    >>> # Define the rule
    >>> RULE_SECONDS = FunctionValue(
    ...     parse_seconds,
    ...     non_capturing_group(
    ...         # number + seconds (e.g. 100 ثانية or اربع ثواني)
    ...         spaced_patterns(RULE_NUMERAL, non_capturing_group(ONE_SECOND, SEVERAL_SECONDS)),
    ...         # ثانية or ثانيتين
    ...         TWO_SECONDS,
    ...         ONE_SECOND,
    ...     ),
    ...     pickle=False,
    ... )

    # Use the rule to parse the text.
    >>> sample_text = "تستغرق الف وعشرون ثانية للوصول"
    >>> sample_text2 = "تصل في ثانيتين"
    >>> sample_text3 = "تصل في ثانية"

    >>> list(RULE_SECONDS.parse(sample_text))[0].value
    1020
    >>> list(RULE_SECONDS.parse(sample_text2))[0].value
    2
    >>> list(RULE_SECONDS.parse(sample_text3))[0].value
    1

See :mod:`~maha.parsers.rules.duration` for the full implementation of durations rule.