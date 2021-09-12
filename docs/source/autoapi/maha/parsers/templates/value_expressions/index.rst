:py:mod:`maha.parsers.templates.value_expressions`
==================================================

.. py:module:: maha.parsers.templates.value_expressions


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   maha.parsers.templates.value_expressions.Value
   maha.parsers.templates.value_expressions.MatchedValue
   maha.parsers.templates.value_expressions.FunctionValue




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



