__all__ = ["Name"]

from dataclasses import dataclass
from typing import List

from maha.cleaners.functions import keep, normalize


@dataclass
class Name:
    """Template for the names dataset.

    Parameters
    ----------
    name : str
        Name of person.
    description : str
        Description or meaning of the name. Can contain multiple descriptions separated
        by "||".
    origin : str
        Origin of the name.
    """

    name: str
    description: List[str]
    origin: str

    def __init__(self, name: str, description: str, origin: str):
        self.name = name
        self.description = description.split("||")
        self.origin = origin

        self._cleaned_name = None

    @property
    def cleaned_name(self):
        """Cleaned and normalized name."""
        if not self._cleaned_name:
            self._cleaned_name = keep(
                normalize(self.name, all=True), arabic_letters=True
            )
        return self._cleaned_name
