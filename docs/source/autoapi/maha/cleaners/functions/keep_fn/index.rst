:py:mod:`maha.cleaners.functions.keep_fn`
=========================================

.. py:module:: maha.cleaners.functions.keep_fn

.. autoapi-nested-parse::

   Functions that operate on a string and remove all but certain characters.



Module Contents
---------------


Functions
~~~~~~~~~

.. autosummary::

   keep
   keep_arabic_letters
   keep_arabic_characters
   keep_arabic_with_english_numbers
   keep_arabic_letters_with_harakat
   keep_strings



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


