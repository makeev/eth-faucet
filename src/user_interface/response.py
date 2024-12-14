from typing import Generic, TypeVar

from rest_framework.response import Response

from base.dto import BaseDTO

T = TypeVar("T", bound=BaseDTO)


class TypedResponse(Response, Generic[T]):
    """Typed version of DRF Response, bounded to BaseDTO"""

    def __init__(self, data: T, *args, **kwargs):
        # check if data is instance of BaseDTO(T var)
        super().__init__(data, *args, **kwargs)
        self.data: T = data
