:py:mod:`maha.parsers.rules.duration.utils`
===========================================

.. py:module:: maha.parsers.rules.duration.utils


Module Contents
---------------


Functions
~~~~~~~~~

.. autosummary::

   convert_between_durations



.. py:function:: convert_between_durations(*durations, to_unit)

   Converts a list of durations to another unit using the mapping
   :data:`~.DURATION_CONVERSION_MAP`.

   :param \*durations: List of durations to convert.
   :param to_unit: The unit to convert to.

   :returns: The converted value.
   :rtype: float


