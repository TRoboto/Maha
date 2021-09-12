:py:mod:`maha.parsers.templates.text_expression`
================================================

.. py:module:: maha.parsers.templates.text_expression


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   maha.parsers.templates.text_expression.TextExpression




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



