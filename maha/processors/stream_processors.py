import pathlib
from functools import partial
from typing import Callable, Iterable, List, Union

from .base_processor import BaseProcessor


class StreamTextProcessor(BaseProcessor):
    """For processing a stream of text input.

    Parameters
    ----------
    lines : Iterable[str]
        A an iterable of strings to process
    """

    def __init__(self, lines: Iterable[str]) -> None:

        self.lines = lines
        self.functions = []

    def apply(self, fn: Callable[[str], str]):
        self.functions.append(partial(map, fn))

    def filter(self, fn: Callable[[str], bool]):
        self.functions.append(partial(filter, fn))

    def clean(self, n_lines: int = 100):
        """Applies all functions in sequence to the given iterable

        Parameters
        ----------
        n_lines : int, optional
            Number of lines to process at a time, by default 100

        Yields
        -------
        List[str]
            A list of processed text

        Raises
        ------
        ValueError
            If no functions were selected.
        """
        if len(self.functions) == 0:
            raise ValueError("No functions were selected")

        selected_lines = []
        for i, line in enumerate(self.lines):
            if i < n_lines:
                selected_lines.append(line)
            else:
                cleaned_text = self.apply_functions(selected_lines)
                yield cleaned_text
                selected_lines = [line]

        if selected_lines:
            cleaned_text = self.apply_functions(selected_lines)
            yield cleaned_text

    def apply_functions(self, text: List[str]):
        """Applies all functions in sequence to a given list of strings

        Parameters
        ----------
        text : List[str]
            List of strings to process
        """
        output = text
        for function in self.functions:
            output = list(function(text))
        return output


class StreamFileProcessor(StreamTextProcessor):
    """For processing file input.

    Parameters
    ----------
    file : Union[str, :obj:`pathlib.Path`]
        File to process.

    Raises
    ------
    FileNotFoundError
        If the file doesn't exist.
    """

    def __init__(self, file: Union[str, pathlib.Path]) -> None:

        if isinstance(file, str):
            file = pathlib.Path(file)

        if not file.is_file():
            raise FileNotFoundError(f"{str(file)} doesn't exist.")

        self.file = file.open("r", encoding="utf8")

        super().__init__(self.file)

    def clean(self, n_lines: int):
        yield super().clean(n_lines=n_lines)
        self.file.close()


class FolderProcessor:
    pass
