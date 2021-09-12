:py:mod:`maha.cleaners.functions.remove_fn`
===========================================

.. py:module:: maha.cleaners.functions.remove_fn

.. autoapi-nested-parse::

   Functions that operate on a string and remove certain characters.



Module Contents
---------------


Functions
~~~~~~~~~

.. autosummary::

   remove
   reduce_repeated_substring
   remove_hash_keep_tag
   remove_tatweel
   remove_emails
   remove_hashtags
   remove_links
   remove_mentions
   remove_punctuations
   remove_english
   remove_all_harakat
   remove_harakat
   remove_numbers
   remove_expressions
   remove_strings
   remove_extra_spaces
   remove_arabic_letter_dots



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


