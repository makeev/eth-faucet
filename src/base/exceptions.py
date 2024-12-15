class BaseResponseError(Exception):
    """Raise 500 code by default"""

    code: int = 500


class BaseNotFoundError(BaseResponseError):
    """Raise 404 code by default"""

    code = 404


class BaseForbiddenError(BaseResponseError):
    """Raise 403 code by default"""

    code = 403


class BaseValidationError(BaseResponseError):
    """Raise 400 code by default"""

    code = 400

    def __init__(self, message: str = "Validation error", field: str | None = None):
        self.field = field
        super().__init__(message)
