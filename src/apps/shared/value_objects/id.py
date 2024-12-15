from typing import Any
from uuid import UUID


class Id:
    """
    A class representing an identifier that can be a string, integer, UUID, or None.

    Attributes:
        value (str | None): The identifier value stored as a string or None.

    Methods:
        __init__(value: str | int | UUID | None = None):
            Initializes the Id with the given value. Raises TypeError if the value is not of type str, int, UUID, or None.
        __str__() -> str:
            Returns the string representation of the Id. Returns "-" if the value is None.
        __repr__() -> str:
            Returns the official string representation of the Id.
        __eq__(other) -> bool:
            Checks equality with another Id instance based on the value.
        __hash__() -> int:
            Returns the hash of the Id value.
        __bool__() -> bool:
            Returns True if the Id value is not None, otherwise False.
    """

    value: str | None

    def __init__(self, value: str | int | UUID | None = None):
        if value is not None and not isinstance(value, (str, int, UUID)):
            raise TypeError("Id must be str, int or None")

        # inside the class, we always store the value as a string for convienience
        self.value = str(value) if value is not None else None

    def __str__(self) -> str:
        return str(self.value) if self.value is not None else "-"

    def __repr__(self) -> str:
        return f"Id({self.value})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Id):
            return self.value == other.value
        return False

    def __hash__(self) -> int:
        return hash(self.value)

    def __bool__(self) -> bool:
        return self.value is not None


class RequiredId(Id):
    """
    A class representing a required identifier.

    Attributes:
        value (str): The value of the identifier.

    Methods:
        __init__(value: str | int | UUID | Id | Any):
            Initializes the RequiredId instance. Raises a ValueError if the provided value is None or if the value of an Id instance is None.
    """

    value: str

    def __init__(self, value: str | int | UUID | Id | Any):
        if isinstance(value, Id):
            if value.value is None:
                raise ValueError("Id must be provided")
            value = value.value
        elif value is None:
            raise ValueError("Id must be provided")

        super().__init__(value)
