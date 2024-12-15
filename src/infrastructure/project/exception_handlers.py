from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from base.exceptions import BaseForbiddenError, BaseNotFoundError, BaseResponseError, BaseValidationError


def custom_exception_handler(exc, context):
    # default DRF exception handler
    response = exception_handler(exc, context)

    # if response is not None, it means that the exception has been handled by DRF
    if response is not None:
        return response

    # custom exceptions
    if isinstance(exc, BaseNotFoundError):
        return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)
    elif isinstance(exc, BaseForbiddenError):
        return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)
    elif isinstance(exc, BaseValidationError):
        if exc.field:
            return Response({exc.field: [str(exc)]}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    elif isinstance(exc, BaseResponseError):
        return Response({"detail": str(exc)}, status=exc.code)

    return None
