import pathlib
from typing import Callable, Union

from .base_processor import BaseProcessor


class TextProcessor(BaseProcessor):
    """For processing text input.

    Parameters
    ----------
    text : Union[List[str], str]
        A text or list of strings to process
    """

    def apply(self, fn: Callable[[str], str]):
        self.lines = list(map(fn, self.lines))

    def filter(self, fn: Callable[[str], bool]):
        self.lines = list(filter(fn, self.lines))


class FileProcessor(TextProcessor):
    """For processing file input.

    Parameters
    ----------
    file : Union[str, :obj:`pathlib.Path`]
        File to process.

    Raises
    ------
    FileNotFoundError
        If the file doesn't exist.
    ValueError
        If the file is empty.
    """

    def __init__(self, file: Union[str, pathlib.Path]) -> None:

        if isinstance(file, str):
            file = pathlib.Path(file)

        if not file.is_file():
            raise FileNotFoundError(f"{str(file)} doesn't exist.")

        with file.open("r", encoding="utf8") as f:
            lines = f.readlines()

        if not lines:
            raise ValueError("File empty.")

        super().__init__(lines)


class FolderProcessor:
    pass
