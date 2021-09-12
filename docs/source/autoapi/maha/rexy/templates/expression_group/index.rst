:py:mod:`maha.rexy.templates.expression_group`
==============================================

.. py:module:: maha.rexy.templates.expression_group


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   maha.rexy.templates.expression_group.ExpressionGroup




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



