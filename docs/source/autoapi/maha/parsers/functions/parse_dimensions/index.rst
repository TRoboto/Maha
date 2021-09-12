:py:mod:`maha.parsers.functions.parse_dimensions`
=================================================

.. py:module:: maha.parsers.functions.parse_dimensions


Module Contents
---------------


Functions
~~~~~~~~~

.. autosummary::

   parse_dimension



.. py:function:: parse_dimension(text, amount_of_money = None, duration = None, distance = None, numeral = None, ordinal = None, quantity = None, temperature = None, time = None, volume = None)

   Extract dimensions from a given text.

   :param text: Text to extract dimensions from
   :type text: str
   :param amount_of_money: Extract amount of money using the rule :data:`~.RULE_AMOUNT_OF_MONEY`,
                           by default None
   :type amount_of_money: bool, optional
   :param duration: Extract duration using the rule :data:`~.RULE_DURATION`,
                    by default None
   :type duration: bool, optional
   :param distance: Extract distance using the rule :data:`~.RULE_DISTANCE`,
                    by default None
   :type distance: bool, optional
   :param numeral: Extract numeral using the rule :data:`~.RULE_NUMERAL`,
                   by default None
   :type numeral: bool, optional
   :param ordinal: Extract ordinal using the rule :data:`~.RULE_ORDINAL`,
                   by default None
   :type ordinal: bool, optional
   :param quantity: Extract quantity using the rule :data:`~.RULE_QUANTITY`,
                    by default None
   :type quantity: bool, optional
   :param temperature: Extract temperature using the rule :data:`~.RULE_TEMPERATURE`,
                       by default None
   :type temperature: bool, optional
   :param time: Extract time using the rule :data:`~.RULE_TIME`,
                by default None
   :type time: bool, optional
   :param volume: Extract volume using the rule :data:`~.RULE_VOLUME`,
                  by default None
   :type volume: bool, optional

   :returns: List of :class:`~.Dimension` objects extracted from the text
   :rtype: List[:class:`~.Dimension`]

   :raises ValueError: If no argument is set to True


