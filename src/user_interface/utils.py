from dataclasses import is_dataclass
from typing import Any

from drf_spectacular.utils import extend_schema as _extend_schema
from rest_framework.fields import empty
from rest_framework_dataclasses.serializers import DataclassSerializer


def extend_schema(request: Any = empty, responses: Any = empty, **kwargs):
    """
    Add support of DTO classes to the extend_schema decorator.
    You can use DTO or list of DTO to describe response data.
    """
    if is_dataclass(request):
        request = DataclassSerializer(dataclass=request)

    for status_code, response in responses.items():
        if is_dataclass(response):
            responses[status_code] = DataclassSerializer(dataclass=response)
        elif isinstance(response, list) and all(is_dataclass(item) for item in response):
            responses[status_code] = DataclassSerializer(dataclass=response[0], many=True)

    def decorator(func):
        return _extend_schema(request=request, responses=responses, **kwargs)(func)

    return decorator
