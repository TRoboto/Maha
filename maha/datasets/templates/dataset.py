__all__ = ["Dataset", "IterableDataset"]

from pathlib import Path
from typing import Generic, Type, TypeVar, Union

from .dataset_templates import *

T = TypeVar("T", Name, Name)


class Dataset(Generic[T]):
    """Base class for all datasets.

    Parameters
    ----------
    path : Union[str, Path]
        Path to the dataset.
    template : Type
        Template class for the dataset.
    sep : str, optional
        Separator for the dataset. The default is "\t".
    """

    def __init__(self, path: Union[str, Path], template: Type[T], sep: str = "\t"):
        if isinstance(path, str):
            path = Path(path)
        self.path = path
        self._data_str = path.open("r", encoding="utf-8").read().splitlines()[1:]
        self.sep = sep
        self.template = template
        self._map_template()

    def _map_template(self):
        self._data = [self.template(*line.split(self.sep)) for line in self._data_str]

    @property
    def data(self):
        return self._data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]


class IterableDataset(Generic[T]):
    """Base class for all datasets that need to be streamed.

    Parameters
    ----------
    path : Union[str, Path]
        Path to the dataset.
    template : Type
        Template class for the dataset.
    sep : str, optional
        Separator for the dataset. The default is "\t".
    """

    def __init__(self, path: Union[str, Path], template: Type[T], sep: str = "\t"):
        if isinstance(path, str):
            path = Path(path)
        self.path = path
        self._data = path.open("r", encoding="utf-8")
        self.template = template
        self.sep = sep

    def __iter__(self):
        # skip header
        next(self._data)
        for item in self._data:
            yield self.template(*item.strip().split(self.sep))
