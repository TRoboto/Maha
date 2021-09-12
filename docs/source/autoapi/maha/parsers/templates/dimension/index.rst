:py:mod:`maha.parsers.templates.dimension`
==========================================

.. py:module:: maha.parsers.templates.dimension


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   maha.parsers.templates.dimension.Dimension




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


