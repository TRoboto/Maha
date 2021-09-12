:py:mod:`maha.cleaners.functions.contains_fn`
=============================================

.. py:module:: maha.cleaners.functions.contains_fn

.. autoapi-nested-parse::

   Functions that operate on a string and check for values contained in it



Module Contents
---------------


Functions
~~~~~~~~~

.. autosummary::

   contains
   contains_repeated_substring
   contains_single_letter_word
   contains_expressions
   contain_strings



.. py:function:: contains(text, arabic = False, english = False, arabic_letters = False, english_letters = False, english_small_letters = False, english_capital_letters = False, numbers = False, harakat = False, all_harakat = False, tatweel = False, lam_alef_variations = False, lam_alef = False, punctuations = False, arabic_numbers = False, english_numbers = False, arabic_punctuations = False, english_punctuations = False, arabic_ligatures = False, persian = False, arabic_hashtags = False, arabic_mentions = False, emails = False, english_hashtags = False, english_mentions = False, hashtags = False, links = False, mentions = False, emojis = False, custom_strings = None, custom_expressions = None, operator = None)

   Check for certain characters, strings or patterns in the given text.

   To add a new parameter, make sure that its name is the same as the corresponding
   constant. For the patterns, only remove the prefix ``EXPRESSION_`` from the parameter name

   :param text: Text to check
   :type text: str
   :param arabic: Check for :data:`~.ARABIC` characters, by default False
   :type arabic: bool, optional
   :param english: Check for :data:`~.ENGLISH` characters, by default False
   :type english: bool, optional
   :param arabic_letters: Check for :data:`~.ARABIC_LETTERS` characters, by default False
   :type arabic_letters: bool, optional
   :param english_letters: Check for :data:`~.ENGLISH_LETTERS` characters, by default False
   :type english_letters: bool, optional
   :param english_small_letters: Check for :data:`~.ENGLISH_SMALL_LETTERS` characters, by default False
   :type english_small_letters: bool, optional
   :param english_capital_letters: Check for :data:`~.ENGLISH_CAPITAL_LETTERS` characters, by default False
   :type english_capital_letters: bool, optional
   :param numbers: Check for :data:`~.NUMBERS` characters, by default False
   :type numbers: bool, optional
   :param harakat: Check for :data:`~.HARAKAT` characters, by default False
   :type harakat: bool, optional
   :param all_harakat: Check for :data:`~.ALL_HARAKAT` characters, by default False
   :type all_harakat: bool, optional
   :param tatweel: Check for :data:`~.TATWEEL` character, by default False
   :type tatweel: bool, optional
   :param lam_alef_variations: Check for :data:`~.LAM_ALEF_VARIATIONS` characters, by default False
   :type lam_alef_variations: bool, optional
   :param lam_alef: Check for :data:`~.LAM_ALEF` character, by default False
   :type lam_alef: bool, optional
   :param punctuations: Check for :data:`~.PUNCTUATIONS` characters, by default False
   :type punctuations: bool, optional
   :param arabic_numbers: Check for :data:`~.ARABIC_NUMBERS` characters, by default False
   :type arabic_numbers: bool, optional
   :param english_numbers: Check for :data:`~.ENGLISH_NUMBERS` characters, by default False
   :type english_numbers: bool, optional
   :param arabic_punctuations: Check for :data:`~.ARABIC_PUNCTUATIONS` characters, by default False
   :type arabic_punctuations: bool, optional
   :param english_punctuations: Check for :data:`~.ENGLISH_PUNCTUATIONS` characters, by default False
   :type english_punctuations: bool, optional
   :param arabic_ligatures: Check for :data:`~.ARABIC_LIGATURES` words, by default False
   :type arabic_ligatures: bool, optional
   :param persian: Check for :data:`~.PERSIAN` characters, by default False
   :type persian: bool, optional
   :param arabic_hashtags: Check for Arabic hashtags using the expression :data:`~.EXPRESSION_ARABIC_HASHTAGS`,
                           by default False
   :type arabic_hashtags: bool, optional
   :param arabic_mentions: Check for Arabic mentions using the expression :data:`~.EXPRESSION_ARABIC_MENTIONS`,
                           by default False
   :type arabic_mentions: bool, optional
   :param emails: Check for Arabic hashtags using the expression :data:`~.EXPRESSION_EMAILS`,
                  by default False
   :type emails: bool, optional
   :param english_hashtags: Check for Arabic hashtags using the expression :data:`~.EXPRESSION_ENGLISH_HASHTAGS`,
                            by default False
   :type english_hashtags: bool, optional
   :param english_mentions: Check for Arabic hashtags using the expression :data:`~.EXPRESSION_ENGLISH_MENTIONS`,
                            by default False
   :type english_mentions: bool, optional
   :param hashtags: Check for Arabic hashtags using the expression :data:`~.EXPRESSION_HASHTAGS`,
                    by default False
   :type hashtags: bool, optional
   :param links: Check for Arabic hashtags using the expression :data:`~.EXPRESSION_LINKS`,
                 by default False
   :type links: bool, optional
   :param mentions: Check for Arabic hashtags using the expression :data:`~.EXPRESSION_MENTIONS`,
                    by default False
   :type mentions: bool, optional
   :param emojis: Check for emojis using the expression :data:`~.EXPRESSION_EMOJIS`,
                  by default False
   :type emojis: bool, optional
   :param custom_strings: Include any other string(s), by default None
   :type custom_strings: Union[List[str], str], optional
   :param custom_expressions: Include any other expressions, by default None
   :param operator: When multiple arguments are set to True, this operator is used  to combine
                    the output into a boolean. Takes 'and' or 'or', by default None
   :type operator: bool, optional

   :returns:

             * If one argument is set to True, a boolean value is returned. True if the text
             contains it, False otherwise.
             * If ``operator`` is set and more than one argument is set to True, a boolean
             value that combines the result with the "and/or" operator is returned.
             * If more than one argument is set to True, a dictionary is returned where
             keys are the True passed arguments and the corresponding values are
             booleans. True if the text contains the argument, False otherwise.
   :rtype: Union[Dict[str, bool], bool]

   :raises ValueError: If no argument is set to True

   .. rubric:: Examples

   .. code:: pycon

       >>> from maha.cleaners.functions import contains
       >>> text = "مقاييس أداء النماذج في التعلم الآلي Machine Learning ... 🌺"
       >>> contains(text, english=True, emails=True, emojis=True)
       {'english': True, 'emails': False, 'emojis': True}

   .. code:: pycon

       >>> from maha.cleaners.functions import contains
       >>> text = "قال رسول اللهﷺ إن خير أيامكم يوم الجمعة فأكثروا عليَّ من الصلاة فيه"
       >>> contains(text, english=True)
       False


.. py:function:: contains_repeated_substring(text, min_repeated = 3)

   Check for consecutive substrings that are repeated at least ``min_repeated``
   times. For example with the default arguments, the text 'hhhhhh' should return True

   :param text: Text to check
   :type text: str
   :param min_repeated: Minimum number of consecutive repeated substring to consider, by default 3
   :type min_repeated: int, optional

   :returns: True if the input text contains consecutive substrings, otherwise False
   :rtype: bool

   :raises ValueError: If non positive integer is passed

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import contains_repeated_substring
       >>> text = "كانت اللعبة حللللللللوة جداً"
       >>> contains_repeated_substring(text)
       True


.. py:function:: contains_single_letter_word(text, arabic_letters = False, english_letters = False)

   Check for a single-letter word. For example, "how r u" should return True if
   ``english_letters`` is set to True because it contains two single-letter word,
   "r" and "u".

   :param text: Text to check
   :type text: str
   :param arabic_letters: Check for all :data:`~.ARABIC_LETTERS`, by default False
   :type arabic_letters: bool, optional
   :param english_letters: Check for all :data:`~.ENGLISH_LETTERS`, by default False
   :type english_letters: bool, optional

   :returns: True if the input text contains single-letter word, False otherwise
   :rtype: bool

   :raises ValueError: If no argument is set to True

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import contains_single_letter_word
       >>> text = "cu later my friend, ك"
       >>> contains_single_letter_word(text, arabic_letters=True, english_letters=True)
       True


.. py:function:: contains_expressions(text, expressions)

   Check for matched strings in the given ``text`` using the input ``expressions``

   .. note::
       Use lookahead/lookbehind when substrings should not be captured or removed.

   :param text: Text to check
   :type text: str
   :param expressions: Expression(s) to use
   :type expressions: Union[:class:`ExpressionGroup`, :class:`Expression`, str]

   :returns: True if the pattern is found in the given text, False otherwise.
   :rtype: bool

   :raises ValueError: If ``expressions`` are not of type :class:`Expression`, :class:`ExpressionGroup`
       or str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import contains_expressions
       >>> text = "علم الهندسة (Engineering)"
       >>> contains_expressions(text, r"\([A-Za-z]+\)")
       True


.. py:function:: contain_strings(text, strings)

   Check for the input ``strings`` in the given ``text``

   :param text: Text to check
   :type text: str
   :param strings: String or list of strings to check for
   :type strings: Union[List[str], str]

   :returns: True if the input string(s) are found in the text, False otherwise
   :rtype: bool

   :raises ValueError: If no ``strings`` are provided

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import contain_strings
       >>> text = "الله أكبر، الحمد لله رب العالمين"
       >>> contain_strings(text, "الله")
       True


