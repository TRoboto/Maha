import pytest

from maha.datasets import get_available_datasets, load_dataset
from maha.datasets.templates import Dataset, IterableDataset, Name


def test_load_names():
    output = load_dataset("names")
    assert isinstance(output, Dataset)
    assert isinstance(output[0], Name)
    assert len(output) > 10000


def test_load_names_streaming():
    output = load_dataset("names", streaming=True)
    assert isinstance(output, IterableDataset)
    assert isinstance(next(iter(output)), Name)


def test_get_available_datasets():
    datasets = get_available_datasets()
    assert len(datasets) > 0
    assert isinstance(datasets, list)


def test_invalid_load():
    with pytest.raises(FileNotFoundError):
        load_dataset("invalid")  # type: ignore
