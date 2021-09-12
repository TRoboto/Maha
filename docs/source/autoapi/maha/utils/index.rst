:py:mod:`maha.utils`
====================

.. py:module:: maha.utils


Module Contents
---------------


Functions
~~~~~~~~~

.. autosummary::

   get_unicode
   check_positive_integer



.. py:function:: get_unicode(text)

   Returns the unicode for input text

   :param text: Text to encode
   :type text: str

   :returns: Text with characters encoded in raw unicode.
   :rtype: bytes


.. py:function:: check_positive_integer(value, var_name)

   Raises ValueError if the input value is not a positive integer.

   :param value: Input value
   :type value: float
   :param var_name: Variable name to include it in the error message
   :type var_name: str

   :raises ValueError: if the input value is not a positive integer.


