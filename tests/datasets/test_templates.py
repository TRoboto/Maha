from pathlib import Path

import maha
from maha.datasets import load_dataset
from maha.datasets.templates import Dataset, IterableDataset, Name
from maha.datasets.utils import get_dataset_path


def test_cleaned_name():
    name = Name("أحمدُ", "Description", "Origin")
    assert name.cleaned_name == "احمد"


def test_load_names_streaming():
    output = load_dataset("names", streaming=True)
    assert isinstance(output, IterableDataset)
    assert isinstance(next(iter(output)), Name)


def test_init_dataset_with_str():
    dataset = Dataset(str(get_dataset_path("names")), Name)
    assert isinstance(dataset.path, Path)


def test_init_iterable_dataset_with_str():
    dataset = IterableDataset(str(get_dataset_path("names")), Name)
    assert isinstance(dataset.path, Path)
