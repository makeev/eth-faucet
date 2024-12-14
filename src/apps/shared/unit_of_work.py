from abc import ABC, abstractmethod


class UnitOfWork(ABC):
    """
    Abstract base class for a Unit of Work pattern.

    The Unit of Work pattern is used to group a set of operations into a single transaction.
    This class defines the interface for entering and exiting the unit of work context.

    Methods:
        __enter__: Enter the runtime context related to this object.
        __exit__: Exit the runtime context related to this object.
    """
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
