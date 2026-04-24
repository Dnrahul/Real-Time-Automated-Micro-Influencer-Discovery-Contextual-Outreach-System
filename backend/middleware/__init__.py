"""
========================================
Middleware Package
========================================

Middleware for FastAPI application:
- Error handling and exception conversion
- Request/response logging
- Validation

Import from here:
    from backend.middleware.error_handler import setup_error_handlers
"""

from .error_handler import setup_error_handlers

__all__ = ["setup_error_handlers"]
