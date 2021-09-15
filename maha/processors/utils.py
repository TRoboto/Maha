from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable


@dataclass
class ObjectGet:
    """Used with get function in :class:`~.BaseProcessor`"""

    # function to use
    func: Callable
    # initial value
    prev: Any
    # name of the operation (argument name)
    name: str
    # Function to apply at end
    # Defaults for post_fn, return the input
    post_fn: Callable = lambda input: input
