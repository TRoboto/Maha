:py:mod:`maha.processors.base_processor`
========================================

.. py:module:: maha.processors.base_processor

.. autoapi-nested-parse::

   The base for all processors



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   maha.processors.base_processor.BaseProcessor




.. py:class:: BaseProcessor

   Bases: :py:obj:`abc.ABC`

   Base class for all processors. It contains almost all functions needed for the
   processors.

   :param text: A text or list of strings to process
   :type text: Union[List[str], str]

   .. py:method:: get_lines(self, n_lines = 100)
      :abstractmethod:

      Returns a generator of list of strings with length of ``n_lines``

      :param n_lines: Number of lines to yield, Defaults to 100
      :type n_lines: int

      :Yields: *List[str]* -- List of strings with length of ``n_lines``. The last list maybe of length
               less than ``n_lines``.


   .. py:method:: apply(self, fn)
      :abstractmethod:

      Applies a function to each line

      :param fn: Function to apply


   .. py:method:: filter(self, fn)
      :abstractmethod:

      Keeps lines for which the input function is True

      :param fn: Function to check


   .. py:method:: get(self, unique_characters = False, character_length = False, word_length = False)

      Returns statistics about the provided text

      :param unique_characters: Return all unique characters, by default False
      :type unique_characters: bool, optional
      :param character_length: Return the character length of each string, by default False
      :type character_length: bool, optional
      :param word_length: Return the word length of each string (split by space), by default False
      :type word_length: bool, optional

      :returns:

                * If one argument is set to True, its value is return
                * If more than one argument is set to True, a dictionary is returned where
                    keys are the True passed arguments with the corresponding values
      :rtype: Union[Dict[str, Any], Any]


   .. py:method:: print_unique_characters(self)

      Prints all unique characters in the text


   .. py:method:: keep(self, arabic = False, english = False, arabic_letters = False, english_letters = False, english_small_letters = False, english_capital_letters = False, numbers = False, harakat = False, all_harakat = False, punctuations = False, arabic_numbers = False, english_numbers = False, arabic_punctuations = False, english_punctuations = False, use_space = True, custom_strings = None)

      Applies :func:`~.keep` to each line


   .. py:method:: normalize(self, lam_alef = None, alef = None, waw = None, yeh = None, teh_marbuta = None, ligatures = None, spaces = None, all = None)

      Applies :func:`~.normalize` to each line


   .. py:method:: connect_single_letter_word(self, waw = None, feh = None, beh = None, lam = None, kaf = None, teh = None, all = None, custom_strings = None)

      Applies :func:`~.connect_single_letter_word` to each line


   .. py:method:: replace(self, strings, with_value)

      Applies :func:`~.replace` to each line


   .. py:method:: replace_expression(self, expression, with_value)

      Applies :func:`~.replace_expression` to each line


   .. py:method:: replace_pairs(self, keys, values)

      Applies :func:`~.replace_pairs` to each line


   .. py:method:: reduce_repeated_substring(self, min_repeated = 3, reduce_to = 2)

      Applies :func:`~.reduce_repeated_substring` to each line


   .. py:method:: remove(self, arabic = False, english = False, arabic_letters = False, english_letters = False, english_small_letters = False, english_capital_letters = False, numbers = False, harakat = False, all_harakat = False, tatweel = False, punctuations = False, arabic_numbers = False, english_numbers = False, arabic_punctuations = False, english_punctuations = False, arabic_ligatures = False, arabic_hashtags = False, arabic_mentions = False, emails = False, english_hashtags = False, english_mentions = False, hashtags = False, links = False, mentions = False, emojis = False, use_space = True, custom_strings = None, custom_expressions = None)

      Applies :func:`~.remove` to each line


   .. py:method:: drop_lines_contain(self, arabic = False, english = False, arabic_letters = False, english_letters = False, english_small_letters = False, english_capital_letters = False, numbers = False, harakat = False, all_harakat = False, tatweel = False, lam_alef_variations = False, lam_alef = False, punctuations = False, arabic_numbers = False, english_numbers = False, arabic_punctuations = False, english_punctuations = False, arabic_ligatures = False, persian = False, arabic_hashtags = False, arabic_mentions = False, emails = False, english_hashtags = False, english_mentions = False, hashtags = False, links = False, mentions = False, emojis = False, custom_strings = None, custom_expressions = None, operator = 'or')

      Drop lines that contain any of the selected strings or patterns.

      .. note::
          Use ``operator='and'`` to drop lines that contain all selected strings
          or patterns.

      See :func:`~.contains` for arguments description


   .. py:method:: drop_empty_lines(self)

      Drop empty lines.


   .. py:method:: drop_lines_below_len(self, length, word_level=False)

      Drop lines with a number of characters/words less than the input ``length``

      :param length: Number of characters/words
      :type length: int
      :param word_level: True to switch to word level, which splits the text by space,
                         by default False
      :type word_level: bool, optional


   .. py:method:: drop_lines_above_len(self, length, word_level=False)

      Drop lines with a number of characters/words more than the input ``length``

      :param length: Number of characters/words
      :type length: int
      :param word_level: True to switch to word level, which splits the text by space,
                         by default False
      :type word_level: bool, optional


   .. py:method:: drop_lines_contain_repeated_substring(self, repeated=3)

      Drop lines containing a number of consecutive repeated substrings

      :param repeated: Minimum number of repetitions, by default 3
      :type repeated: int, optional


   .. py:method:: drop_lines_contain_single_letter_word(self, arabic_letters = False, english_letters = False)

      Drop lines containing a single-letter word (e.g."محمد و احمد" or
      "how r u"). In Arabic, single-letter words are rare.

      .. warning::
          In English, all lines containing the letter "I" will be dropped since it is
          considered a single-letter word

      See :func:`~.contains_single_letter_word`.
      See also :func:`~.connect_single_letter_word`.


   .. py:method:: filter_lines_contain(self, arabic = False, english = False, arabic_letters = False, english_letters = False, english_small_letters = False, english_capital_letters = False, numbers = False, harakat = False, all_harakat = False, tatweel = False, lam_alef_variations = False, lam_alef = False, punctuations = False, arabic_numbers = False, english_numbers = False, arabic_punctuations = False, english_punctuations = False, arabic_ligatures = False, persian = False, arabic_hashtags = False, arabic_mentions = False, emails = False, english_hashtags = False, english_mentions = False, hashtags = False, links = False, mentions = False, emojis = False, custom_strings = None, custom_expressions = None, operator = 'or')

      Keep lines that contain any of the selected strings or patterns.

      .. note::
          Use ``operator='and'`` to drop lines that contain all selected strings
          or patterns.

      See :func:`~.contains` for arguments description



