import pathlib
from typing import Union

from .text_processor import TextProcessor


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
