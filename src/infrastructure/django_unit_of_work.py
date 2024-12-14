from django.db import transaction

from apps.shared.unit_of_work import UnitOfWork


class DjangoUnitOfWork(UnitOfWork):
    """Context manager for Django transaction atomic"""

    def __enter__(self):
        self._transaction = transaction.atomic()
        self._transaction.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._transaction.__exit__(exc_type, exc_val, exc_tb)
