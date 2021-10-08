__all__ = ["load_dataset"]

from typing import Union, overload

from typing_extensions import Literal

from ..templates import Dataset, IterableDataset, Name
from ..utils import DATASETS_MAP, get_dataset_path


@overload
def load_dataset(
    name: Literal["names"], streaming: Literal[False] = False
) -> Dataset[Name]:
    ...


@overload
def load_dataset(
    name: Literal["names"], streaming: Literal[True]
) -> IterableDataset[Name]:
    ...


def load_dataset(name: str, streaming: bool = False) -> Union[Dataset, IterableDataset]:
    """Loads a dataset.

    Parameters
    ----------
    name
        Name of the dataset.
    streaming : bool, optional
        Whether to return a streaming dataset. If set to True, an IterableDataset is
        returned instead.

    Returns
    -------
    Union[:class:`~.Dataset`, :class:`~.IterableDataset`]
        The loaded dataset.

    Raises
    ------
    FileNotFoundError
        If the dataset does not exist.
    """
    if name not in DATASETS_MAP:
        raise FileNotFoundError(
            f"Dataset '{name}' not found. The available datasets are:\n"
            + "\n".join(DATASETS_MAP.keys())
        )

    path = get_dataset_path(name)
    template = DATASETS_MAP[name]
    if streaming:
        return IterableDataset(path, template)
    else:
        return Dataset(path, template)
