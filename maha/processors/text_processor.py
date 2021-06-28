from typing import Callable

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
