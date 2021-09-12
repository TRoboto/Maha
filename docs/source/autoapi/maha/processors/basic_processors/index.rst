:py:mod:`maha.processors.basic_processors`
==========================================

.. py:module:: maha.processors.basic_processors

.. autoapi-nested-parse::

   All basic processors



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   maha.processors.basic_processors.TextProcessor
   maha.processors.basic_processors.FileProcessor




.. py:class:: TextProcessor(text)

   Bases: :py:obj:`maha.processors.base_processor.BaseProcessor`

   For processing text input.

   :param text: A text or list of strings to process
   :type text: Union[List[str], str]

   .. py:method:: apply(self, fn)

      Applies a function to each line

      :param fn: Function to apply


   .. py:method:: filter(self, fn)

      Keeps lines for which the input function is True

      :param fn: Function to check


   .. py:method:: get_lines(self, n_lines = 100)

      Returns a generator of list of strings with length of ``n_lines``

      :param n_lines: Number of lines to yield, Defaults to 100
      :type n_lines: int

      :Yields: *List[str]* -- List of strings with length of ``n_lines``. The last list maybe of length
               less than ``n_lines``.


   .. py:method:: set_lines(self, text)

      Overrides text

      :param text: New text or list of strings
      :type text: Union[List[str], str]


   .. py:method:: text(self)
      :property:

      Returns the processed text joined by the newline separator ``\n``

      :returns: processed text
      :rtype: str


   .. py:method:: from_string(cls, text, sep = None)
      :classmethod:

      Creates a new processor from the given text. Separate the text by the input
      ``sep`` argument if provided.

      :param text: Text to process
      :type text: str
      :param sep: Separator used to split the given text, by default None
      :type sep: str, optional

      :returns: New text processor
      :rtype: TextProcessor


   .. py:method:: from_list(cls, lines)
      :classmethod:

      Creates a new processor from the given list of strings.

      :param lines: list of strings
      :type lines: List[str]

      :returns: New text processor
      :rtype: TextProcessor


   .. py:method:: drop_duplicates(self)

      Drops duplicate lines from text



.. py:class:: FileProcessor(path)

   Bases: :py:obj:`TextProcessor`

   For processing file input.

   .. note::
       For large files (>100 MB), use :class:`~StreamFileProcessor`.

   :param path: Path of the file to process.
   :type path: Union[str, :obj:`pathlib.Path`]

   :raises FileNotFoundError: If the file doesn't exist.
   :raises ValueError: If the file is empty.


