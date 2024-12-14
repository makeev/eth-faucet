class BaseNotFoundError(Exception):
    """Raise 404 code by default"""
    pass


class BaseForbiddenError(Exception):
    """Raise 403 code by default"""
    pass


class BaseValidationError(Exception):
    """Raise 400 code by default"""
    def __init__(self, message: str = "Validation error", field: str | None = None):
        self.field = field
        super().__init__(message)
