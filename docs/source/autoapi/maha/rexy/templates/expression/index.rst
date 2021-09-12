:py:mod:`maha.rexy.templates.expression`
========================================

.. py:module:: maha.rexy.templates.expression


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   maha.rexy.templates.expression.Expression




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



