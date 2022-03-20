from __future__ import annotations

__all__ = [
    "StreamTextProcessor",
    "StreamFileProcessor",
]


import pathlib
from functools import partial
from typing import Callable, Iterable

from tqdm import tqdm

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
        self.functions: list[Callable] = []

    def apply(self, fn: Callable[[str], str]):
        self.functions.append(partial(map, fn))

    def filter(self, fn: Callable[[str], bool]):
        self.functions.append(partial(filter, fn))

    def get_lines(self, n_lines: int = 100):
        selected_lines = []

        for i, line in enumerate(self.lines, 1):
            selected_lines.append(line)
            if i % n_lines == 0:
                yield selected_lines
                selected_lines = []

        if selected_lines:
            yield selected_lines

    def process(self, n_lines: int = 100):
        """Applies all functions in sequence to the given iterable

        Parameters
        ----------
        n_lines : int, optional
            Number of lines to process at a time, by default 100

        Yields
        -------
        List[str]
            A list of processed text, it can be empty.

        Raises
        ------
        ValueError
            If no functions were selected.
        """
        if len(self.functions) == 0:
            raise ValueError("No functions were selected")

        for lines in self.get_lines(n_lines):
            yield self.apply_functions(lines)

    def apply_functions(self, text: list[str]):
        """Applies all functions in sequence to a given list of strings

        Parameters
        ----------
        text : List[str]
            List of strings to process
        """
        output = text
        for function in self.functions:
            output = list(function(output))
        return output


class StreamFileProcessor(StreamTextProcessor):
    """For processing file stream input.

    Parameters
    ----------
    path : Union[str, :obj:`pathlib.Path`]
        Path of the file to process.
    encoding : str
        File encoding.

    Raises
    ------
    FileNotFoundError
        If the file doesn't exist.
    """

    def __init__(self, path: str | pathlib.Path, encoding: str = "utf8") -> None:

        if isinstance(path, str):
            path = pathlib.Path(path)

        if not path.is_file():
            raise FileNotFoundError(f"{str(path)} doesn't exist.")

        self.encoding = encoding
        self.file = path
        self.openfile = path.open("r", encoding=encoding)
        super().__init__(self.openfile)

    def get_lines(self, n_lines: int = 100):
        # set pointer to top of the file
        self.openfile.seek(0)

        selected_lines = []

        with tqdm(
            total=self.file.stat().st_size,
            desc="Processing",
            unit="B",
            unit_scale=True,
            leave=True,
        ) as pbar:
            for i, line in enumerate(self.lines, 1):
                pbar.update(len(line.encode(self.encoding)))
                selected_lines.append(line.strip())
                if i % n_lines == 0:
                    yield selected_lines
                    selected_lines = []

        if selected_lines:
            yield selected_lines

    def process_and_save(
        self, path: str | pathlib.Path, n_lines: int = 100, override: bool = False
    ):
        """Process the input file and save the result in the given path

        Parameters
        ----------
        path : Union[str, :obj:`pathlib.Path`]
            Path to save the file
        n_lines : int, optional
            Number of lines to process at a time, by default 100
        override : bool, optional
            True to override the file if exists, by default False

        Raises
        ------
        FileExistsError
            If the file exists
        """
        if isinstance(path, str):
            path = pathlib.Path(path)

        if not override and path.is_file():
            raise FileExistsError(f"{str(path)} exists.")

        with path.open("w", encoding=self.encoding) as file:
            for lines in self.process(n_lines):
                text = "\n".join(lines).strip("\n")
                if not text:
                    continue
                file.write(text)
                file.write("\n")

    def __del__(self):
        if hasattr(self, "openfile"):
            self.openfile.close()


class StreamFolderProcessor:
    def __init__(self):
        raise NotImplementedError()
