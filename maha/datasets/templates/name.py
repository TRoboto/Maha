__all__ = ["Name"]

from dataclasses import dataclass
from typing import List

from maha.cleaners.functions import keep, normalize


@dataclass
class Name:
    name: str
    """ The name """
    description: List[str]
    """ The meaning of the name """
    origin: str
    """ The origin of the name """

    def __init__(self, name: str, description: str, origin: str):
        self.name = name
        self.description = eval(description)
        self.origin = origin

    @property
    def cleaned_name(self):
        return keep(normalize(self.name, all=True), arabic_letters=True)
