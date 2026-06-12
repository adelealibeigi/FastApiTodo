"""Exception handlers for converting exceptions to HTTP responses.

This module provides a scalable approach to exception handling.
Instead of creating individual handlers for each exception, we use
base exception handlers that automatically determine the HTTP status
code based on the error_code attribute.

To add a new exception:
1. Create the exception class (inheriting from ServiceError or DomainException)
2. Add its error_code to ERROR_CODE_TO_HTTP_STATUS in error_codes.py
3. That's it! No need to create or register a new handler.
"""

import logging

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.core.exceptions.service_exceptions import ServiceError
from src.service_api.exception.error_codes import get_http_status_for_error_code

logger = logging.getLogger(__name__)


def service_error_handler(request: Request, exc: ServiceError) -> JSONResponse:
    """
    This single handler handles all ServiceError subclasses.
    The HTTP status code is determined by the error_code attribute
    using the ERROR_CODE_TO_HTTP_STATUS mapping.

    No need to create individual handlers for each exception type!
    """
    http_status = get_http_status_for_error_code(exc.error_code)
    error_code = exc.error_code
    message = exc.message
    logger.warning(
        "Service error | code=%s | message=%s",
        error_code, message,
    )
    return JSONResponse(
        status_code=http_status,
        content={
            "detail": message,
            "error_code": error_code,
        },
    )


def validation_error_handler(
        request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handle Pydantic validation errors from request data.

    Transforms FastAPI's RequestValidationError into a structured,
    user-friendly format that matches our standard error response pattern.

    Returns a list of all validation errors with field locations and messages.
    """
    # Extract all validation errors from Pydantic
    errors = exc.errors()
    logger.info(
        "Validation error",
        extra={"errors": errors}
    )

    # Transform Pydantic errors into our standardized format
    validation_errors = []
    for error in errors:
        # Build field path (e.g., "body.email" or "query.page")
        field_location = ".".join(str(loc) for loc in error["loc"])

        validation_errors.append(
            {
                "field": field_location,
                "message": error["msg"],
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation failed",
            "error_code": "VALIDATION_ERROR",
            "errors": validation_errors,
        },
    )


def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle all other unhandled exceptions.

    This is the catch-all handler for any unexpected errors.
    """
    # Log the actual error for debugging
    # logger.error(f"Unhandled error: {exc}", exc_info=True)
    logger.exception(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal server error occurred",
            "error_code": "INTERNAL_SERVER_ERROR",
        },
    )
