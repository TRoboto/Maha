__all__ = ["get_available_datasets"]

from pathlib import Path

from .templates import *

DATASETS_MAP = {
    "names": Name,
}
"""List of available datasets with corresponding template."""


def get_dataset_path(filename: str):
    """Returns the path of a dataset.

    Parameters
    ----------
    filename : str
        The dataset filename.

    Returns
    -------
    str
        The path of the dataset.
    """
    return next((Path(__file__).parent / "data").glob(f"**/{filename}*"))


def get_available_datasets():
    """Returns a list of available datasets.

    Returns
    -------
    list
        A list of available datasets.
    """
    return list(DATASETS_MAP.keys())
