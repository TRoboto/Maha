:py:mod:`maha.rexy.templates`
=============================

.. py:module:: maha.rexy.templates


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   expression/index.rst
   expression_group/index.rst
   expression_result/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   maha.rexy.templates.Expression
   maha.rexy.templates.ExpressionGroup
   maha.rexy.templates.ExpressionResult




.. py:class:: Expression(pattern, pickle = False)

   Regex pattern holder.

   :param pattern: Regular expression pattern.
   :type pattern: str
   :param pickle: If ``True``, the compiled pattern will be pickled. This is useful to save
                  compilation time for large patterns.
   :type pickle: bool

   .. py:attribute:: pattern
      :annotation: :str

      Regular expersion(s) to match

   .. py:method:: compile(self)

      Compile the regular expersion.


   .. py:method:: search(self, text)

      Search for the pattern in the input ``text``.

      :param text: Text to search in.
      :type text: str

      :returns: Matched object.
      :rtype: :class:`regex.Match`


   .. py:method:: match(self, text)

      Match the pattern in the input ``text``.

      :param text: Text to match in.
      :type text: str

      :returns: Matched object.
      :rtype: :class:`regex.Match`


   .. py:method:: fullmatch(self, text)

      Match the pattern in the input ``text``.

      :param text: Text to match in.
      :type text: str

      :returns: Matched object.
      :rtype: :class:`regex.Match`


   .. py:method:: sub(self, repl, text)

      Replace all occurrences of the pattern in the input ``text``.

      :param repl: Replacement string.
      :type repl: str
      :param text: Text to replace.
      :type text: str

      :returns: Text with replaced occurrences.
      :rtype: str


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



.. py:class:: ExpressionGroup(*expressions, smart = False)

   A group of expressions that match the same dimension. Expressions are evaluated
   in the order they were added.

   :param \*expressions: List of expressions to match. High-priority expressions should be passed first.
   :param smart: Whether to parse the text in a smart way. See :meth:`~.smart_parse`.
   :type smart: bool, optional

   .. py:method:: compile_expressions(self)


   .. py:method:: merge_expressions(self, expressions)


   .. py:method:: add(self, *expression)

      Add an expression to the group.


   .. py:method:: join(self)

      Returns non capturing group of the expressions.


   .. py:method:: get_matched_expression(self, text)

      Returns the expression that matches the text.


   .. py:method:: parse(self, text)

      Parses the text.

      :param text: Text to parse.
      :type text: str

      :Yields: :class:`rx.ExpressionResult` -- Extracted value.


   .. py:method:: normal_parse(self, text)

      Parse the input ``text`` and return the extracted values.


   .. py:method:: smart_parse(self, text)

      Parses the text. If a value matches two or more expressions, only the first
      expression parses the value, no value is matched more than once. This means
      high-priority expressions should be passed first.


   .. py:method:: clear_parsed(self)



.. py:class:: ExpressionResult

   A result of a single expression.

   .. py:attribute:: start
      :annotation: :int

      Start index of the matched text

   .. py:attribute:: end
      :annotation: :int

      End index of the matched text

   .. py:attribute:: value
      :annotation: :Any

      Extracted value

   .. py:attribute:: expression
      :annotation: :maha.rexy.Expression

      The expression that was used to find the value


