import pathlib
from typing import Callable, List, Union

from .base_processor import BaseProcessor


class TextProcessor(BaseProcessor):
    """For processing text input.

    Parameters
    ----------
    text : Union[List[str], str]
        A text or list of strings to process
    """

    def apply(self, fn: Callable[[str], str]):
        self.lines = [fn(line) if line else line for line in self.lines]

    def filter(self, fn: Callable[[str], bool]):
        self.lines = list(filter(fn, self.lines))

    @classmethod
    def from_string(cls, text: str, sep: str = None):
        """Creates a new processor from the given text. Separate the text by the input
        ``sep`` argument if provided.

        Parameters
        ----------
        text : str
            Text to process
        sep : str, optional
            Separator used to split the given text, by default None

        Returns
        -------
        TextProcessor
            New text processor
        """
        out = text
        if sep:
            out = text.split(sep)
        return TextProcessor(out)

    @classmethod
    def from_list(cls, lines: List[str]):
        """Creates a new processor from the given list of strings.

        Parameters
        ----------
        lines : List[str]
            list of strings

        Returns
        -------
        TextProcessor
            New text processor
        """
        return TextProcessor(lines)


class FileProcessor(TextProcessor):
    """For processing file input.

    .. note::
        For large files (>100 MB), use :class:`~StreamFileProcessor`.

    Parameters
    ----------
    path : Union[str, :obj:`pathlib.Path`]
        Path of the file to process.

    Raises
    ------
    FileNotFoundError
        If the file doesn't exist.
    ValueError
        If the file is empty.
    """

    def __init__(self, path: Union[str, pathlib.Path]) -> None:

        if isinstance(path, str):
            path = pathlib.Path(path)

        if not path.is_file():
            raise FileNotFoundError(f"{str(path)} doesn't exist.")

        with path.open("r", encoding="utf8") as f:
            lines = f.readlines()

        if not lines:
            raise ValueError("File empty.")

        super().__init__(lines)


class FolderProcessor:
    pass
