:py:mod:`maha.cleaners.functions.replace_fn`
============================================

.. py:module:: maha.cleaners.functions.replace_fn

.. autoapi-nested-parse::

   Functions that operate on a string and replace specific characters with others.



Module Contents
---------------


Functions
~~~~~~~~~

.. autosummary::

   connect_single_letter_word
   arabic_numbers_to_english
   replace_expression
   replace
   replace_except
   replace_pairs



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


