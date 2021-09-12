:py:mod:`maha.cleaners.functions`
=================================

.. py:module:: maha.cleaners.functions


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   contains_fn/index.rst
   keep_fn/index.rst
   normalize_fn/index.rst
   remove_fn/index.rst
   replace_fn/index.rst


Package Contents
----------------


Functions
~~~~~~~~~

.. autosummary::

   contains
   contains_expressions
   contain_strings
   contains_repeated_substring
   contains_single_letter_word
   keep
   keep_strings
   keep_arabic_letters
   keep_arabic_characters
   keep_arabic_with_english_numbers
   keep_arabic_letters_with_harakat
   normalize
   normalize_lam_alef
   normalize_small_alef
   remove
   remove_strings
   remove_extra_spaces
   remove_punctuations
   remove_english
   remove_all_harakat
   remove_harakat
   remove_numbers
   remove_tatweel
   remove_expressions
   remove_emails
   remove_hashtags
   remove_links
   remove_mentions
   reduce_repeated_substring
   remove_hash_keep_tag
   remove_arabic_letter_dots
   replace
   replace_except
   replace_pairs
   replace_expression
   arabic_numbers_to_english
   connect_single_letter_word



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


.. py:function:: keep(text, arabic = False, english = False, arabic_letters = False, english_letters = False, english_small_letters = False, english_capital_letters = False, numbers = False, harakat = False, all_harakat = False, punctuations = False, arabic_numbers = False, english_numbers = False, arabic_punctuations = False, english_punctuations = False, use_space = True, custom_strings = None)

   Keeps only certain characters in the given text and removes everything else.

   To add a new parameter, make sure that its name is the same as the corresponding
   constant.

   :param text: Text to be processed
   :type text: str
   :param arabic: Keep :data:`~.ARABIC` characters, by default False
   :type arabic: bool, optional
   :param english: Keep :data:`~.ENGLISH` characters, by default False
   :type english: bool, optional
   :param arabic_letters: Keep :data:`~.ARABIC_LETTERS` characters, by default False
   :type arabic_letters: bool, optional
   :param english_letters: Keep :data:`~.ENGLISH_LETTERS` characters, by default False
   :type english_letters: bool, optional
   :param english_small_letters: Keep :data:`~.ENGLISH_SMALL_LETTERS` characters, by default False
   :type english_small_letters: bool, optional
   :param english_capital_letters: Keep :data:`~.ENGLISH_CAPITAL_LETTERS` characters, by default False
   :type english_capital_letters: bool, optional
   :param numbers: Keep :data:`~.NUMBERS` characters, by default False
   :type numbers: bool, optional
   :param harakat: Keep :data:`~.HARAKAT` characters, by default False
   :type harakat: bool, optional
   :param all_harakat: Keep :data:`~.ALL_HARAKAT` characters, by default False
   :type all_harakat: bool, optional
   :param punctuations: Keep :data:`~.PUNCTUATIONS` characters, by default False
   :type punctuations: bool, optional
   :param arabic_numbers: Keep :data:`~.ARABIC_NUMBERS` characters, by default False
   :type arabic_numbers: bool, optional
   :param english_numbers: Keep :data:`~.ENGLISH_NUMBERS` characters, by default False
   :type english_numbers: bool, optional
   :param arabic_punctuations: Keep :data:`~.ARABIC_PUNCTUATIONS` characters, by default False
   :type arabic_punctuations: bool, optional
   :param english_punctuations: Keep :data:`~.ENGLISH_PUNCTUATIONS` characters, by default False
   :type english_punctuations: bool, optional
   :param use_space: False to not replace with space, check :func:`~.keep_strings`
                     for more information, by default True
   :type use_space: bool, optional
   :param custom_strings: Include any other string(s), by default None
   :type custom_strings: List[str], optional

   :returns: Processed text
   :rtype: str

   :raises ValueError: If no argument is set to True

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import keep
       >>> text = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
       >>> keep(text, arabic_letters=True)
       'بسم الله الرحمن الرحيم'


.. py:function:: keep_strings(text, strings, use_space = True)

   Keeps only the input strings ``strings`` in the given text ``text``

   By default, this works by replacing all strings except the input ``strings`` with
   a space, which means space is kept. This is to help separate texts when unwanted
   strings are present without spaces. For example, 'end.start' will be converted to
   'end start' if English letters :data:`~.ENGLISH_LETTERS` are passed to ``strings``.
   To disable this behavior, set ``use_space`` to False.

   .. note::
       Extra spaces (more than one space) are removed by default if ``use_space`` is
       set to True.

   :param text: Text to be processed
   :type text: str
   :param strings: list of strings to keep
   :type strings: Union[List[str], str]
   :param use_space: False to not replace with space, defaults to True

   :returns: Text that contains only the input strings.
   :rtype: str

   :raises ValueError: If no ``strings`` are provided

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import keep_strings
       >>> text = "لا حول ولا قوة إلا بالله"
       >>> keep_strings(text, "الله")
       'الله'


.. py:function:: keep_arabic_letters(text)

   Keeps only Arabic letters :data:`~.ARABIC_LETTERS` in the given text.

   :param text: Text to be processed
   :type text: str

   :returns: Text contains Arabic letters only.
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import keep_arabic_letters
       >>> text = " 1 يا أحلى mathematicians في العالم"
       >>> keep_arabic_letters(text)
       'يا أحلى في العالم'


.. py:function:: keep_arabic_characters(text)

   Keeps only common Arabic characters :data:`~.ARABIC` in the given text.

   :param text: Text to be processed
   :type text: str

   :returns: Text contains the common Arabic characters only.
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import keep_arabic_characters
       >>> text = "أَلمَانِيَا (بالألمانية: Deutschland) رسمِيّاً جُمهُورِيَّة أَلمَانِيَا الاِتِّحَاديَّة"
       >>> keep_arabic_characters(text)
       'أَلمَانِيَا بالألمانية رسمِيّاً جُمهُورِيَّة أَلمَانِيَا الاِتِّحَاديَّة'


.. py:function:: keep_arabic_with_english_numbers(text)

   Keeps only common Arabic characters :data:`~.ARABIC` and English numbers
   :data:`~.ENGLISH_NUMBERS` in the given text.

   :param text: Text to be processed
   :type text: str

   :returns: Text contains the common Arabic characters and English numbers only.
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import keep_arabic_with_english_numbers
       >>> text = "تتكون من 16 ولاية تُغطي مساحة 357,021 كيلومتر Deutschland"
       >>> keep_arabic_with_english_numbers(text)
       'تتكون من 16 ولاية تُغطي مساحة 357 021 كيلومتر'


.. py:function:: keep_arabic_letters_with_harakat(text)

   Keeps only Arabic letters :data:`~.ARABIC_LETTERS` and HARAKAT :data:`~.HARAKAT`
   in the given text.

   :param text: Text to be processed
   :type text: str

   :returns: Text contains Arabic letters with harakat only.
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import keep_arabic_letters_with_harakat
       >>> text = "إنّ في التّركِ قوة…"
       >>> keep_arabic_letters_with_harakat(text)
       'إنّ في التّركِ قوة'


.. py:function:: normalize(text, lam_alef = None, alef = None, waw = None, yeh = None, teh_marbuta = None, ligatures = None, spaces = None, all = False)

   Normalizes characters in the given text

   :param text: Text to process
   :type text: str
   :param lam_alef: Normalize :data:`~.LAM_ALEF_VARIATIONS` characters to :data:`~.LAM` and
                    :data:`~.ALEF`, by default None
   :type lam_alef: bool, optional
   :param alef: Normalize :data:`~.ALEF_VARIATIONS` characters to :data:`~.ALEF`,
                by default None
   :type alef: bool, optional
   :param waw: Normalize :data:`~.WAW_VARIATIONS` characters to :data:`~.WAW`,
               by default None
   :type waw: bool, optional
   :param yeh: Normalize :data:`~.YEH_VARIATIONS` characters to :data:`~.YEH` and
               :data:`~.ALEF`, by default None
   :type yeh: bool, optional
   :param teh_marbuta: Normalize :data:`~.TEH_MARBUTA` characters to :data:`~.HEH`, by default None
   :type teh_marbuta: bool, optional
   :param ligatures: Normalize :data:`~.ARABIC_LIGATURES` characters to the corresponding indices
                     in :data:`~.ARABIC_LIGATURES_NORMALIZED`, by default None
   :type ligatures: bool, optional
   :param spaces: Normalize space variations using the expression :data:`~.EXPRESSION_ALL_SPACES`,
                  by default None
   :type spaces: bool, optional
   :param all: Do all normalization except the ones that are set to False, by default False
   :type all: bool, optional

   :returns: Processed text
   :rtype: str

   :raises ValueError: If no argument is set to True

   .. rubric:: Examples

   .. code:: pycon

       >>> from maha.cleaners.functions import normalize
       >>> text = "عن أبي هريرة"
       >>> normalize(text, alef=True, teh_marbuta=True)
       'عن ابي هريره'

   .. code:: pycon

       >>> from maha.cleaners.functions import normalize
       >>> text = "قال رسول الله ﷺ"
       >>> normalize(text, ligatures=True)
       'قال رسول الله صلى الله عليه وسلم'

   .. code:: pycon

       >>> from maha.cleaners.functions import normalize
       >>> text = "قال مؤمن: ﷽ قل هو ﷲ أحد"
       ... # For space
       >>> normalize(text, all=True, waw=False)
       'قال مؤمن: بسم الله الرحمن الرحيم قل هو الله احد'


.. py:function:: normalize_lam_alef(text, keep_hamza = True)

   Normalize :data:`~.LAM_ALEF_VARIATIONS` to
   :data:`~.LAM_ALEF_VARIATIONS_NORMALIZED` If ``keep_hamza`` is True. Otherwise,
   normalize to :data:`~.LAM` and :data:`~.ALEF`

   :param text: Text to process
   :type text: str
   :param keep_hamza: True to preserve hamza and madda characters, by default True
   :type keep_hamza: bool, optional

   :returns: Normalized text
   :rtype: str

   .. rubric:: Examples

   .. code:: pycon

       >>> from maha.cleaners.functions import normalize_lam_alef
       >>> text = "السﻻم عليكم أحبتي، قالوا في صِفَةِ رَسُولِ الله يتَﻷلأ وَجْهُه"
       >>> normalize_lam_alef(text)
       'السلام عليكم أحبتي، قالوا في صِفَةِ رَسُولِ الله يتَلألأ وَجْهُه'

   .. code:: pycon

       >>> from maha.cleaners.functions import normalize_lam_alef
       >>> text = "اﻵن يا أصحابي"
       >>> normalize_lam_alef(text, keep_hamza=False)
       'الان يا أصحابي'


.. py:function:: normalize_small_alef(text, keep_madda = True, normalize_end = False)

   Normalize :data:`~.ALEF_SUPERSCRIPT` to :data:`~.ALEF`. If ``keep_madda`` is True
   and :data:`~.ALEF_SUPERSCRIPT` is followed by :data:`HAMZA_ABOVE`, then normalize
   to :data:`~.ALEF_MADDA_ABOVE`

   :param text: Text to process
   :type text: str
   :param keep_madda: True to preserve madda character, by default True
   :type keep_madda: bool, optional
   :param normalize_end: True to normalize :data:`~.ALEF_SUPERSCRIPT` that appear at the end of a word,
                         by default False
   :type normalize_end: bool, optional

   :returns: Normalized text
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import normalize_small_alef
       >>> text = "وَٱلصَّٰٓفَّٰتِ صَفّٗا"
       >>> normalize_small_alef(text)
       'وَٱلصَّآفَّاتِ صَفّٗا'


.. py:function:: remove(text, arabic = False, english = False, arabic_letters = False, english_letters = False, english_small_letters = False, english_capital_letters = False, numbers = False, harakat = False, all_harakat = False, tatweel = False, punctuations = False, arabic_numbers = False, english_numbers = False, arabic_punctuations = False, english_punctuations = False, arabic_ligatures = False, arabic_hashtags = False, arabic_mentions = False, emails = False, english_hashtags = False, english_mentions = False, hashtags = False, links = False, mentions = False, emojis = False, use_space = True, custom_strings = None, custom_expressions = None)

   Removes certain characters from the given text.

   To add a new parameter, make sure that its name is the same as the corresponding
   constant. For the patterns, only remove the prefix ``EXPRESSION_`` from the parameter name

   :param text: Text to be processed
   :type text: str
   :param arabic: Remove :data:`~.ARABIC` characters, by default False
   :type arabic: bool, optional
   :param english: Remove :data:`~.ENGLISH` characters, by default False
   :type english: bool, optional
   :param arabic_letters: Remove :data:`~.ARABIC_LETTERS` characters, by default False
   :type arabic_letters: bool, optional
   :param english_letters: Remove :data:`~.ENGLISH_LETTERS` characters, by default False
   :type english_letters: bool, optional
   :param english_small_letters: Remove :data:`~.ENGLISH_SMALL_LETTERS` characters, by default False
   :type english_small_letters: bool, optional
   :param english_capital_letters: Remove :data:`~.ENGLISH_CAPITAL_LETTERS` characters, by default False
   :type english_capital_letters: bool, optional
   :param numbers: Remove :data:`~.NUMBERS` characters, by default False
   :type numbers: bool, optional
   :param harakat: Remove :data:`~.HARAKAT` characters, by default False
   :type harakat: bool, optional
   :param all_harakat: Remove :data:`~.ALL_HARAKAT` characters, by default False
   :type all_harakat: bool, optional
   :param tatweel: Remove :data:`~.TATWEEL` character, by default False
   :type tatweel: bool, optional
   :param punctuations: Remove :data:`~.PUNCTUATIONS` characters, by default False
   :type punctuations: bool, optional
   :param arabic_numbers: Remove :data:`~.ARABIC_NUMBERS` characters, by default False
   :type arabic_numbers: bool, optional
   :param english_numbers: Remove :data:`~.ENGLISH_NUMBERS` characters, by default False
   :type english_numbers: bool, optional
   :param arabic_punctuations: Remove :data:`~.ARABIC_PUNCTUATIONS` characters, by default False
   :type arabic_punctuations: bool, optional
   :param english_punctuations: Remove :data:`~.ENGLISH_PUNCTUATIONS` characters, by default False
   :type english_punctuations: bool, optional
   :param arabic_ligatures: Remove :data:`~.ARABIC_LIGATURES` words, by default False
   :type arabic_ligatures: bool, optional
   :param arabic_hashtags: Remove Arabic hashtags using the expression :data:`~.EXPRESSION_ARABIC_HASHTAGS`,
                           by default False
   :type arabic_hashtags: bool, optional
   :param arabic_mentions: Remove Arabic mentions using the expression :data:`~.EXPRESSION_ARABIC_MENTIONS`,
                           by default False
   :type arabic_mentions: bool, optional
   :param emails: Remove Arabic hashtags using the expression :data:`~.EXPRESSION_EMAILS`,
                  by default False
   :type emails: bool, optional
   :param english_hashtags: Remove Arabic hashtags using the expression :data:`~.EXPRESSION_ENGLISH_HASHTAGS`,
                            by default False
   :type english_hashtags: bool, optional
   :param english_mentions: Remove Arabic hashtags using the expression :data:`~.EXPRESSION_ENGLISH_MENTIONS`,
                            by default False
   :type english_mentions: bool, optional
   :param hashtags: Remove Arabic hashtags using the expression :data:`~.EXPRESSION_HASHTAGS`,
                    by default False
   :type hashtags: bool, optional
   :param links: Remove Arabic hashtags using the expression :data:`~.EXPRESSION_LINKS`,
                 by default False
   :type links: bool, optional
   :param mentions: Remove Arabic hashtags using the expression :data:`~.EXPRESSION_MENTIONS`,
                    by default False
   :type mentions: bool, optional
   :param emojis: Remove emojis using the expression :data:`~.EXPRESSION_EMOJIS`,
                  by default False
   :type emojis: bool, optional
   :param use_space: False to not replace with space, check :func:`~.remove_strings`
                     for more information, by default True
   :type use_space: bool, optional
   :param custom_strings: Include any other string(s), by default None
   :param custom_expressions: Include any other regular expression expressions, by default None
   :type custom_expressions: Union[:class:`~.ExpressionGroup`, :class:`~.Expression`, str]

   :returns: Processed text
   :rtype: str

   :raises ValueError: If no argument is set to True

   .. rubric:: Examples

   .. code:: pycon

       >>> from maha.cleaners.functions import remove
       >>> text = "ويندوز 11 سيدعم تطبيقات نظام أندرويد. #Windows11"
       >>> remove(text, hashtags=True)
       'ويندوز 11 سيدعم تطبيقات نظام أندرويد.'

   .. code:: pycon

       >>> from maha.cleaners.functions import remove
       >>> text = "قَالَ رَبِّ اشْرَحْ لِي صَدْرِي.."
       >>> remove(text, all_harakat=True, punctuations=True)
       'قال رب اشرح لي صدري'


.. py:function:: remove_strings(text, strings, use_space = True)

   Removes the input strings ``strings`` in the given text ``text``

   This works by replacing all input strings ``strings`` with a space,
   which means space cannot be removed. This is to help separate texts when unwanted
   strings are present without spaces. For example, 'end.start' will be converted
   to 'end start' if dot :data:`~.DOT` is passed to ``strings``.
   To disable this behavior, set ``use_space`` to False.

   .. note::
       Extra spaces (more than one space) are removed by default if ``use_space`` is
       set to True.

   :param text: Text to be processed
   :type text: str
   :param strings: list of strings to remove
   :type strings: Union[List[str], str]
   :param use_space: False to not replace with space, defaults to True

   :returns: Text with input strings removed.
   :rtype: str

   :raises ValueError: If no ``strings`` are provided

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import remove_strings
       >>> text = "ومن الكلمات المحظورة السلاح"
       >>> remove_strings(text, "السلاح")
       'ومن الكلمات المحظورة'


.. py:function:: remove_extra_spaces(text, max_spaces = 1)

   Keeps a maximum of ``max_spaces`` number of spaces when extra spaces are present
   (more than one space)

   :param text: Text to be processed
   :type text: str
   :param max_spaces: Maximum number of spaces to keep, by default 1
   :type max_spaces: int, optional

   :returns: Text with extra spaces removed
   :rtype: str

   :raises ValueError: When a negative or float value is assigned to ``max_spaces``

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import remove_extra_spaces
       >>> text = "وكان صديقنا    العزيز   محمد من أفضل   الأشخاص الذين قابلتهم"
       >>> remove_extra_spaces(text)
       'وكان صديقنا العزيز محمد من أفضل الأشخاص الذين قابلتهم'


.. py:function:: remove_punctuations(text)

   Removes all punctuations :data:`~.PUNCTUATIONS` from the given text.

   :param text: Text to be processed
   :type text: str

   :returns: Text with punctuations removed.
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import remove_punctuations
       >>> text = "مثال على الرموز الخاصة كالتالي $ ^ & * ( ) ! @"
       >>> remove_punctuations(text)
       'مثال على الرموز الخاصة كالتالي'


.. py:function:: remove_english(text)

   Removes all english characters :data:`~.ENGLISH` from the given text.

   :param text: Text to be processed
   :type text: str

   :returns: Text with english removed.
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import remove_english
       >>> text = "ومن أفضل الجامعات هي جامعة إكسفورد (Oxford University)"
       >>> remove_english(text)
       'ومن أفضل الجامعات هي جامعة إكسفورد'


.. py:function:: remove_all_harakat(text)

   Removes all harakat :data:`~.ALL_HARAKAT` from the given text.

   :param text: Text to be processed
   :type text: str

   :returns: Text with all harakat removed.
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import remove_all_harakat
       >>> text = "وَٱلصَّٰٓفَّٰتِ صَفّٗا (1) فَٱلزَّٰجِرَٰتِ زَجۡرٗا"
       >>> remove_all_harakat(text)
       'وٱلصفت صفا (1) فٱلزجرت زجرا'


.. py:function:: remove_harakat(text)

   Removes common harakat :data:`~.HARAKAT` from the given text.

   :param text: Text to be processed
   :type text: str

   :returns: Text with common harakat removed.
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import remove_harakat
       >>> text = "ألا تَرَى: كلَّ مَنْ تَرجو وتَأمَلُهُ مِنَ البَرِيَّةِ (مسكينُ بْنُ مسكينِ)"
       >>> remove_harakat(text)
       'ألا ترى: كل من ترجو وتأمله من البرية (مسكين بن مسكين)'


.. py:function:: remove_numbers(text)

   Removes all numbers :data:`~.NUMBERS` from the given text.

   :param text: Text to be processed
   :type text: str

   :returns: Text with numbers removed.
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import remove_numbers
       >>> text = "ورقم أبو تريكة في نادي الأهلي هو إثنين وعشرين (22)"
       >>> remove_numbers(text)
       'ورقم أبو تريكة في نادي الأهلي هو إثنين وعشرين ( )'


.. py:function:: remove_tatweel(text)

   Removes tatweel symbol :data:`~.TATWEEL` from the given text.

   :param text: Text to process
   :type text: str

   :returns: Text with tatweel symbol removed.
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import remove_tatweel
       >>> text = "الحمــــــــد لله رب العــــــــــــالمـــــــيـــــن"
       >>> remove_tatweel(text)
       'الحمد لله رب العالمين'


.. py:function:: remove_expressions(text, patterns, remove_spaces = True)

   Removes matched characters from the given text ``text`` using input
   patterns ``patterns``

   .. note::
       Use lookahead/lookbehind when substrings should not be captured or removed.

   :param text: Text to process
   :type text: str
   :param patterns: Expression(s) to use
   :param remove_spaces: False to keep extra spaces, defaults to True
   :type remove_spaces: bool, optional

   :returns: Text with matched characters removed.
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import remove_expressions
       >>> text = "الأميرُ الغازي أرطُغرُل، أو اختصارًا أرطغرل (بالتركية: Ertuğrul)"
       >>> remove_expressions(text, r"\(.*\)")
       'الأميرُ الغازي أرطُغرُل، أو اختصارًا أرطغرل'


.. py:function:: remove_emails(text)

   Removes emails using pattern :data:`~.EXPRESSION_EMAILS` from the given text.

   :param text: Text to be processed
   :type text: str

   :returns: Text with emails removed.
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import remove_emails
       >>> text = "يمكن استخدام الإيميل الشخصي، كمثال user1998@gmail.com"
       >>> remove_emails(text)
       'يمكن استخدام الإيميل الشخصي، كمثال'


.. py:function:: remove_hashtags(text)

   Removes hashtags (strings that start with # symbol) using pattern
   :data:`~.EXPRESSION_HASHTAGS` from the given text.

   :param text: Text to be processed
   :type text: str

   :returns: Text with hashtags removed.
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import remove_hashtags
       >>> text = "ويمكن القول أن مكة المكرمة من أجمل المناطق على وجه الأرض #السعودية"
       >>> remove_hashtags(text)
       'ويمكن القول أن مكة المكرمة من أجمل المناطق على وجه الأرض'


.. py:function:: remove_links(text)

   Removes links using pattern :data:`~.EXPRESSION_LINKS` from the given text.

   :param text: Text to be processed
   :type text: str

   :returns: Text with links removed.
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import remove_links
       >>> text = "لمشاهدة آخر التطورات يرجى زيارة الموقع التالي: https://github.com/TRoboto/Maha"
       >>> remove_links(text)
       'لمشاهدة آخر التطورات يرجى زيارة الموقع التالي:'


.. py:function:: remove_mentions(text)

   Removes mentions (strings that start with @ symbol) using pattern
   :data:`~.EXPRESSION_MENTIONS` from the given text.

   :param text: Text to be processed
   :type text: str

   :returns: Text with mentions removed.
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import remove_mentions
       >>> text = "@test لو سمحت صديقنا تزورنا على المعرض لاستلام الجائزة"
       >>> remove_mentions(text)
       'لو سمحت صديقنا تزورنا على المعرض لاستلام الجائزة'


.. py:function:: reduce_repeated_substring(text, min_repeated = 3, reduce_to = 2)

   Reduces consecutive substrings that are repeated at least ``min_repeated`` times
   to ``reduce_to`` times. For example with the default arguments, 'hhhhhh' is
   reduced to 'hh'

   TODO: Maybe change the implemention for 50x speed
   https://stackoverflow.com/questions/29481088/how-can-i-tell-if-a-string-repeats-itself-in-python/29489919#29489919

   :param text: Text to process
   :type text: str
   :param min_repeated: Minimum number of consecutive repeated substring to consider, by default 3
   :type min_repeated: int, optional
   :param reduce_to: Number of substring to keep, by default 2
   :type reduce_to: int, optional

   :returns: Processed text
   :rtype: str

   :raises ValueError: If non positive integer is passed or ``reduce_to`` is greater than
       ``min_repeated``

   .. rubric:: Examples

   ..code:: pycon

       >>> from maha.cleaners.functions import reduce_repeated_substring
       >>> text = "ههههههههههههههه"
       >>> reduce_repeated_substring(text)
       'هه'

   ..code:: pycon

       >>> from maha.cleaners.functions import reduce_repeated_substring
       >>> text = "ويييييييييين راححححححححححححوا"
       >>> reduce_repeated_substring(text, reduce_to=1)
       'وين راحوا'


.. py:function:: remove_hash_keep_tag(text)

   Removes the hash symbol :data:`~.HASHTAG` from all hashtags in the given text.

   :param text: Text to process
   :type text: str

   :returns: Text without hashtags.
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import remove_hash_keep_tag
       >>> text = "We love #Jordan very much"
       >>> remove_hash_keep_tag(text)
       'We love Jordan very much'


.. py:function:: remove_arabic_letter_dots(text)

   Remove dots from :data:`~.ARABIC_LETTERS` in the given ``text`` using the
   :data:`~.ARABIC_DOTLESS_MAP`

   :param text: Text to be processed
   :type text: str

   :returns: Text with dotless Arabic letters
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import remove_arabic_letter_dots
       >>> text = "الحَمدُ للهِ الَّذي بنِعمتِه تَتمُّ الصَّالحاتُ"
       >>> remove_arabic_letter_dots(text)
       'الحَمدُ للهِ الَّدى ٮٮِعمٮِه ٮَٮمُّ الصَّالحاٮُ'


.. py:function:: replace(text, strings, with_value)

   Replaces the input ``strings`` in the given text with the given value

   :param text: Text to process
   :type text: str
   :param strings: Strings to replace
   :param with_value: Value to replace the input strings with

   :returns: Processed text
   :rtype: str

   .. rubric:: Examples

   .. code:: pycon

       >>> from maha.cleaners.functions import replace
       >>> text = "حصل الولد على معدل 50%"
       >>> replace(text, "%", " بالمئة")
       'حصل الولد على معدل 50 بالمئة'

   .. code:: pycon

       >>> from maha.cleaners.functions import replace
       >>> text = "ولقد كلف هذا المنتج 100 $"
       >>> replace(text, "$", "دولار")
       'ولقد كلف هذا المنتج 100 دولار'


.. py:function:: replace_except(text, strings, with_value)

   Replaces everything except the input ``strings`` in the given text
   with the given value

   :param text: Text to process
   :type text: str
   :param strings: Strings to preserve (not replace)
   :param with_value: Value to replace all other strings with.

   :returns: Processed text
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import replace_except
       >>> from maha.constants import ARABIC_LETTERS, SPACE, EMPTY
       >>> text = "لَيتَ الذينَ تُحبُّ العيّنَ رؤيَتهم"
       >>> replace_except(text, ARABIC_LETTERS + [SPACE], EMPTY)
       'ليت الذين تحب العين رؤيتهم'


.. py:function:: replace_pairs(text, keys, values)

   Replaces each key with its corresponding value in the given text

   :param text: Text to process
   :type text: str
   :param keys: Strings to be replaced
   :param values: Strings to be replaced with

   :returns: Processed text
   :rtype: str

   :raises ValueError: If keys and values are of different lengths

   .. rubric:: Example

   ..  code:: pycon

       >>> from maha.cleaners.functions import replace_pairs
       >>> text = 'شلونك يا محمد؟'
       >>> replace_pairs(text, ['شلونك'] , ['كيف حالك'])
       'كيف حالك يا محمد؟'


.. py:function:: replace_expression(text, expression, with_value)

   Matches characters from the input text using the given ``expression``
   and replaces all matched characters with the given value.

   :param text: Text to process
   :type text: str
   :param expression: Pattern/Expression used to match characters from the text
   :param with_value: Value to replace the matched characters with

   :returns: Processed text
   :rtype: str

   .. rubric:: Examples

   .. code:: pycon

       >>> from maha.cleaners.functions import replace_expression
       >>> text = "ولقد حصلت على ١٠ من ١٠ "
       >>> replace_expression(text, "١٠", "عشرة")
       'ولقد حصلت على عشرة من عشرة '

   .. code:: pycon

       >>> from maha.cleaners.functions import replace_expression
       >>> text = "ذهبت الفتاه إلى المدرسه"
       >>> replace_expression(text, "ه( |$)", "ة ").strip()
       'ذهبت الفتاة إلى المدرسة'


.. py:function:: arabic_numbers_to_english(text)

   Converts Arabic numbers :data:`~.ARABIC_NUMBERS` to the corresponding English
   numbers :data:`~.ENGLISH_NUMBERS`

   :param text: Text to process
   :type text: str

   :returns: Processed text with all occurrences of Arabic numbers converted
             to English numbers
   :rtype: str

   .. rubric:: Examples

   .. code:: pycon

       >>> from maha.cleaners.functions import arabic_numbers_to_english
       >>> text = "٣"
       >>> arabic_numbers_to_english(text)
       '3'

   .. code:: pycon

       >>> from maha.cleaners.functions import arabic_numbers_to_english
       >>> text = "١٠"
       >>> arabic_numbers_to_english(text)
       '10'


.. py:function:: connect_single_letter_word(text, waw = None, feh = None, beh = None, lam = None, kaf = None, teh = None, all = None, custom_strings = None)

   Connects single-letter word with the letter following it.

   :param text: Text to process
   :type text: str
   :param waw: Connect :data:`.WAW` letter, by default None
   :type waw: bool, optional
   :param feh: Connect :data:`.FEH` letter, by default None
   :type feh: bool, optional
   :param beh: Connect :data:`.BEH` letter, by default None
   :type beh: bool, optional
   :param lam: Connect :data:`.LAM` letter, by default None
   :type lam: bool, optional
   :param kaf: Connect :data:`.KAF` letter, by default None
   :type kaf: bool, optional
   :param teh: Connect :data:`.TEH` letter, by default None
   :type teh: bool, optional
   :param all: Connect all letter except the ones set to False, by default None
   :type all: bool, optional
   :param custom_strings: Include any other string(s) to connect, by default None
   :type custom_strings: Union[List[str], str], optional


