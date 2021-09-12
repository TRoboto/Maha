:py:mod:`maha.processors.stream_processors`
===========================================

.. py:module:: maha.processors.stream_processors


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   maha.processors.stream_processors.StreamTextProcessor
   maha.processors.stream_processors.StreamFileProcessor




.. py:class:: StreamTextProcessor(lines)

   Bases: :py:obj:`maha.processors.base_processor.BaseProcessor`

   For processing a stream of text input.

   :param lines: A an iterable of strings to process
   :type lines: Iterable[str]

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


   .. py:method:: process(self, n_lines = 100)

      Applies all functions in sequence to the given iterable

      :param n_lines: Number of lines to process at a time, by default 100
      :type n_lines: int, optional

      :Yields: *List[str]* -- A list of processed text, it can be empty.

      :raises ValueError: If no functions were selected.


   .. py:method:: apply_functions(self, text)

      Applies all functions in sequence to a given list of strings

      :param text: List of strings to process
      :type text: List[str]



.. py:class:: StreamFileProcessor(path, encoding = 'utf8')

   Bases: :py:obj:`StreamTextProcessor`

   For processing file stream input.

   :param path: Path of the file to process.
   :type path: Union[str, :obj:`pathlib.Path`]
   :param encoding: File encoding.
   :type encoding: str

   :raises FileNotFoundError: If the file doesn't exist.

   .. py:method:: get_lines(self, n_lines = 100)

      Returns a generator of list of strings with length of ``n_lines``

      :param n_lines: Number of lines to yield, Defaults to 100
      :type n_lines: int

      :Yields: *List[str]* -- List of strings with length of ``n_lines``. The last list maybe of length
               less than ``n_lines``.


   .. py:method:: process_and_save(self, path, n_lines = 100, override = False)

      Process the input file and save the result in the given path

      :param path: Path to save the file
      :type path: Union[str, :obj:`pathlib.Path`]
      :param n_lines: Number of lines to process at a time, by default 100
      :type n_lines: int, optional
      :param override: True to override the file if exists, by default False
      :type override: bool, optional

      :raises FileExistsError: If the file exists



