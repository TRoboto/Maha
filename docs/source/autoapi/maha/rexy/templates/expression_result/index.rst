:py:mod:`maha.rexy.templates.expression_result`
===============================================

.. py:module:: maha.rexy.templates.expression_result


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   maha.rexy.templates.expression_result.ExpressionResult




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


