:py:mod:`maha.parsers.functions.parse_fn`
=========================================

.. py:module:: maha.parsers.functions.parse_fn

.. autoapi-nested-parse::

   Functions that extracts values from text



Module Contents
---------------


Functions
~~~~~~~~~

.. autosummary::

   parse
   parse_expression



.. py:function:: parse(text, arabic = False, english = False, arabic_letters = False, english_letters = False, english_small_letters = False, english_capital_letters = False, numbers = False, harakat = False, all_harakat = False, tatweel = False, punctuations = False, arabic_numbers = False, english_numbers = False, arabic_punctuations = False, english_punctuations = False, arabic_ligatures = False, arabic_hashtags = False, arabic_mentions = False, emails = False, english_hashtags = False, english_mentions = False, hashtags = False, links = False, mentions = False, emojis = False, custom_expressions = None, include_space=False)

   Extracts certain characters/patterns from the given text.

   To add a new parameter, make sure that its name is the same as the corresponding
   constant. For the patterns, only remove the prefix ``EXPRESSION_`` from the parameter name

   .. todo::
       Add the ability to combine all expressions before parsing.

   :param text: Text to be processed
   :type text: str
   :param arabic: Extract :data:`~.ARABIC` characters, by default False
   :type arabic: bool, optional
   :param english: Extract :data:`~.ENGLISH` characters, by default False
   :type english: bool, optional
   :param arabic_letters: Extract :data:`~.ARABIC_LETTERS` characters, by default False
   :type arabic_letters: bool, optional
   :param english_letters: Extract :data:`~.ENGLISH_LETTERS` characters, by default False
   :type english_letters: bool, optional
   :param english_small_letters: Extract :data:`~.ENGLISH_SMALL_LETTERS` characters, by default False
   :type english_small_letters: bool, optional
   :param english_capital_letters: Extract :data:`~.ENGLISH_CAPITAL_LETTERS` characters, by default False
   :type english_capital_letters: bool, optional
   :param numbers: Extract :data:`~.NUMBERS` characters, by default False
   :type numbers: bool, optional
   :param harakat: Extract :data:`~.HARAKAT` characters, by default False
   :type harakat: bool, optional
   :param all_harakat: Extract :data:`~.ALL_HARAKAT` characters, by default False
   :type all_harakat: bool, optional
   :param tatweel: Extract :data:`~.TATWEEL` character, by default False
   :type tatweel: bool, optional
   :param punctuations: Extract :data:`~.PUNCTUATIONS` characters, by default False
   :type punctuations: bool, optional
   :param arabic_numbers: Extract :data:`~.ARABIC_NUMBERS` characters, by default False
   :type arabic_numbers: bool, optional
   :param english_numbers: Extract :data:`~.ENGLISH_NUMBERS` characters, by default False
   :type english_numbers: bool, optional
   :param arabic_punctuations: Extract :data:`~.ARABIC_PUNCTUATIONS` characters, by default False
   :type arabic_punctuations: bool, optional
   :param english_punctuations: Extract :data:`~.ENGLISH_PUNCTUATIONS` characters, by default False
   :type english_punctuations: bool, optional
   :param arabic_ligatures: Extract :data:`~.ARABIC_LIGATURES` words, by default False
   :type arabic_ligatures: bool, optional
   :param arabic_hashtags: Extract Arabic hashtags using the expression :data:`~.EXPRESSION_ARABIC_HASHTAGS`,
                           by default False
   :type arabic_hashtags: bool, optional
   :param arabic_mentions: Extract Arabic mentions using the expression :data:`~.EXPRESSION_ARABIC_MENTIONS`,
                           by default False
   :type arabic_mentions: bool, optional
   :param emails: Extract Arabic hashtags using the expression :data:`~.EXPRESSION_EMAILS`,
                  by default False
   :type emails: bool, optional
   :param english_hashtags: Extract Arabic hashtags using the expression :data:`~.EXPRESSION_ENGLISH_HASHTAGS`,
                            by default False
   :type english_hashtags: bool, optional
   :param english_mentions: Extract Arabic hashtags using the expression :data:`~.EXPRESSION_ENGLISH_MENTIONS`,
                            by default False
   :type english_mentions: bool, optional
   :param hashtags: Extract Arabic hashtags using the expression :data:`~.EXPRESSION_HASHTAGS`,
                    by default False
   :type hashtags: bool, optional
   :param links: Extract Arabic hashtags using the expression :data:`~.EXPRESSION_LINKS`,
                 by default False
   :type links: bool, optional
   :param mentions: Extract Arabic hashtags using the expression :data:`~.EXPRESSION_MENTIONS`,
                    by default False
   :type mentions: bool, optional
   :param emojis: Extract emojis using the expression :data:`~.EXPRESSION_EMOJIS`,
                  by default False
   :type emojis: bool, optional
   :param custom_expressions: optional. Include any other string(s), by default None
   :type custom_expressions: Union[:class:`~.ExpressionGroup`, :class:`~.Expression`],
   :param include_space: Include the space expression :data:`~.EXPRESSION_SPACE` with all characters,
                         by default False
   :type include_space: bool, optional

   :returns: List of dimensions extracted from the text
   :rtype: List[:class:`~.Dimension`]

   :raises ValueError: If no argument is set to True


.. py:function:: parse_expression(text, expressions, dimension_type = DimensionType.GENERAL)

   Extract matched strings in the given ``text`` using the input ``patterns``

   :param text: Text to check
   :type text: str
   :param expressions: Expression(s) to use
   :type expressions: Union[:class:`~.ExpressionGroup`, :class:`~.Expression`]
   :param dimension_type: Dimension type of the input ``expressions``,
                          by default :attr:`.DimensionType.GENERAL`
   :type dimension_type: DimensionType

   :returns: List of extracted dimensions
   :rtype: List[:class:`~.Dimension`]

   :raises ValueError: If ``expressions`` are invalid


