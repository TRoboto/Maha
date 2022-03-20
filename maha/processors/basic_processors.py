""" All basic processors """

from __future__ import annotations

__all__ = [
    "TextProcessor",
    "FileProcessor",
]


import pathlib
from typing import Callable

from .base_processor import BaseProcessor


class TextProcessor(BaseProcessor):
    """For processing text input.

    Parameters
    ----------
    text : Union[List[str], str]
        A text or list of strings to process
    """

    def __init__(self, text: list[str] | str) -> None:
        self.set_lines(text)

    def apply(self, fn: Callable[[str], str]):
        self.lines: list[str] = list(map(fn, self.lines))

    def filter(self, fn: Callable[[str], bool]):
        self.lines = list(filter(fn, self.lines))

    def get_lines(self, n_lines: int = 100):
        for i in range(0, len(self.lines), n_lines):
            yield self.lines[i : i + n_lines]

    def set_lines(self, text: list[str] | str):
        """Overrides text

        Parameters
        ----------
        text : Union[List[str], str]
            New text or list of strings
        """
        self.lines = []
        if isinstance(text, str):
            self.lines = [text]
        else:
            self.lines.extend(text)

    @property
    def text(self) -> str:
        """Returns the processed text joined by the newline separator ``\\n``

        Returns
        -------
        str
            processed text
        """
        return "\n".join(self.lines)

    @classmethod
    def from_text(cls, text: str, sep: str | None = None):
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
        if sep:
            return TextProcessor(text.split(sep))

        return TextProcessor(text)

    @classmethod
    def from_list(cls, lines: list[str]):
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

    def drop_duplicates(self):
        """Drops duplicate lines from text"""
        self.lines = list(dict.fromkeys(self.lines))
        return self


class FileProcessor(TextProcessor):
    """For processing file input.

    .. note::
        For large files (>100 MB), use :class:`~.StreamFileProcessor`.

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

    def __init__(self, path: str | pathlib.Path) -> None:

        if isinstance(path, str):
            path = pathlib.Path(path)

        if not path.is_file():
            raise FileNotFoundError(f"{str(path)} doesn't exist.")

        with path.open("r", encoding="utf8") as f:
            text = f.read()

        if not text:
            raise ValueError("File empty.")

        super().__init__(text.split("\n"))


class DataFrameProcessor:
    def __init__(self):
        raise NotImplementedError()


class FolderProcessor:
    def __init__(self):
        raise NotImplementedError()
