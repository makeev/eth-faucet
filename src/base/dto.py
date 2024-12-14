from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from dataclasses_json import DataClassJsonMixin

from base.entity import BaseEntity

E = TypeVar("E", bound=BaseEntity)


@dataclass(frozen=True)
class BaseDTO(DataClassJsonMixin, ABC):
    pass


@dataclass(frozen=True)
class BaseEntityDTO(BaseDTO, Generic[E]):
    @classmethod
    @abstractmethod
    def from_entity(cls, entity: E) -> "BaseEntityDTO":
        raise NotImplementedError


DTOType = TypeVar("DTOType", bound=BaseEntityDTO)


@dataclass(frozen=True)
class PaginatedDTO(BaseDTO, Generic[DTOType]):
    page: int
    page_size: int
    total: int
    objects_list: list[DTOType]

    def num_pages(self) -> int:
        return self.total // self.page_size + 1

    def to_dict(self, encode_json=False) -> dict:
        return {
            "page": self.page,
            "page_size": self.page_size,
            "total": self.total,
            "num_pages": self.num_pages(),
            "objects_list": self.objects_list,
        }
