__all__ = ["Dataset", "IterableDataset"]
from pathlib import Path
from typing import Type, Union


class Dataset:
    def __init__(self, path: Union[str, Path], template: Type, sep: str = "\t"):
        if isinstance(path, str):
            path = Path(path)
        self.path = path
        self._data = path.open("r", encoding="utf-8").read().splitlines()[1:]
        self.template = template
        self.sep = sep
        self.map_template()

    def map_template(self):
        self._data = [self.template(*line.split(self.sep)) for line in self._data]

    @property
    def data(self):
        return self._data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]


class IterableDataset:
    def __init__(self, path: Union[str, Path], template: Type, sep: str = "\t"):
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
