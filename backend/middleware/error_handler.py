"""
========================================
🛡️ Error Handling Middleware
========================================

FastAPI middleware for:
- Catching unhandled exceptions
- Converting them to proper HTTP responses
- Logging errors with context
- Providing consistent error format

Usage in main.py:
    from backend.middleware.error_handler import setup_error_handlers
    setup_error_handlers(app)
"""

import traceback
from typing import Callable
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from backend.utils import get_logger
from backend.utils.exceptions import ApplicationError

logger = get_logger(__name__)


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unhandled exceptions and convert to proper HTTP responses.
    
    All exceptions are logged with full traceback for debugging.
    """
    logger.error(
        f"Unhandled exception: {type(exc).__name__}",
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred. Please try again later.",
            "status_code": 500,
        }
    )


async def application_exception_handler(
    request: Request,
    exc: ApplicationError
) -> JSONResponse:
    """
    Handle custom ApplicationError exceptions with proper status codes.
    """
    logger.warning(
        f"Application error: {exc.error_code} - {exc.message}",
        extra={"error_code": exc.error_code}
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """
    Handle Pydantic validation errors with detail about invalid fields.
    """
    logger.warning(f"Validation error: {exc.error_count()} field(s)")
    
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"][1:]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Invalid request data",
            "status_code": 422,
            "errors": errors
        }
    )


def setup_error_handlers(app: FastAPI) -> None:
    """
    Register all exception handlers to the FastAPI app.
    
    Call this in main.py:
        setup_error_handlers(app)
    """
    app.add_exception_handler(ApplicationError, application_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    logger.info("Error handlers registered successfully")
