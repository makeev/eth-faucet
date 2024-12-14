from abc import abstractmethod
from enum import Enum
from typing import Any, Generic, Iterator, TypeVar

from django.db.models import Model, QuerySet

from apps.shared.value_objects import Id, RequiredId
from base.dao import BaseDAO
from base.entity import BaseEntity

ModelType = TypeVar("ModelType", bound=Model)
EntityType = TypeVar("EntityType", bound=BaseEntity)


class BaseDjangoDAO(BaseDAO, Generic[ModelType, EntityType]):
    """Base class for Django DAOs, common methods for CRUD operations with entities through Django models"""

    model: type[ModelType]

    def get_queryset(self) -> QuerySet[ModelType]:
        """Add some select_related or prefetch_related here"""
        return self.model.objects.all()  # type: ignore

    @abstractmethod
    def to_entity(self, model: ModelType) -> EntityType:
        """Convert Django model to domain entity"""
        raise NotImplementedError

    def get_by_id(self, id: Id) -> EntityType | None:
        if not isinstance(id, Id):
            id = Id(str(id))
        return self.get_by(id=id.value)

    def get_by(self, **kwargs) -> EntityType | None:
        try:
            obj = self.get_queryset().get(**kwargs)
            return self.to_entity(obj)
        except self.model.DoesNotExist:
            return None

    def _process_kwargs(self, **kwargs) -> dict:
        """Process keyword arguments before passing them to the model"""
        processed_kwargs: dict[str, Any] = {}
        for key, value in kwargs.items():
            if isinstance(value, BaseEntity):
                processed_kwargs[f"{key}_id"] = value.id
            elif isinstance(value, Enum):
                processed_kwargs[key] = value.value
            elif isinstance(value, Id):
                processed_kwargs[key] = value.value if value else None
            else:
                processed_kwargs[key] = value
        return processed_kwargs

    def create(self, **kwargs) -> RequiredId:
        """Create a new object in the database and return its ID"""
        obj = self.model.objects.create(**self._process_kwargs(**kwargs))
        return RequiredId(obj.pk)

    def update(self, id: Id, **kwargs) -> bool:
        """Update an existing object in the database"""
        obj = self.model.objects.get(pk=id.value)
        kwargs = self._process_kwargs(**kwargs)
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save(update_fields=kwargs.keys())
        return True

    def delete(self, id: Id) -> bool:
        """Delete an object from the database"""
        try:
            obj = self.model.objects.get(pk=id.value)
            obj.delete()
            return True
        except self.model.DoesNotExist:
            return False

    def filter_by(self, **kwargs) -> list[EntityType]:
        """Retrieve a list of entities matching the given criteria"""
        objs = self.get_queryset().filter(**kwargs)
        return [self.to_entity(obj) for obj in objs]

    def paginate(
        self, skip: int = 0, limit: int = 10, order_by: str | None = None, **kwargs: Any
    ) -> Iterator[EntityType]:
        """Retrieve entities with pagination and optional ordering."""
        queryset = self.get_queryset().filter(**kwargs)
        if order_by:
            queryset = queryset.order_by(order_by)
        objs = queryset[skip : skip + limit]
        return (self.to_entity(obj) for obj in objs)
