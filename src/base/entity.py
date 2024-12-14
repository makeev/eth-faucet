from abc import ABC
from dataclasses import dataclass

from apps.shared.value_objects import Id


@dataclass
class BaseEntity(ABC):
    """
    BaseEntity is an abstract base class that provides common functionality for entities.

    Attributes:
        id (Id): The unique identifier for the entity.
    """
    id: Id

    def __eq__(self, other):
        """For easy comparison of entities"""
        return self.id == other.id

    def __hash__(self):
        """To use entity in sets and dicts"""
        return hash(self.id)

    def as_dict(self, exclude_id: bool = False) -> dict:
        """Useful for serialization"""
        d = self.__dict__.copy()

        if exclude_id:
            d.pop("id")

        # remove private attributes
        d = {k: v for k, v in d.items() if not k.startswith("_")}
        return d

    @property
    def kwargs(self) -> dict:
        """Useful for passing as kwargs to DAO methods"""
        return self.as_dict(exclude_id=True)
