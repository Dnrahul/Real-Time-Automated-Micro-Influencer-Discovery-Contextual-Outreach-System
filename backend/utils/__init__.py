"""
========================================
Backend Utils Package
========================================

Utility modules for logging, error handling,
and common helper functions.

Import from here:
    from backend.utils import get_logger
    from backend.utils.exceptions import ValidationError
    from backend.utils.helpers import clean_text, is_valid_email
"""

from .logger import get_logger, configure_logging
from .exceptions import (
    ApplicationError,
    ConfigurationError,
    ValidationError,
    DiscoveryError,
    FilteringError,
    EnrichmentError,
    NLPError,
    ScoringError,
    OutreachError,
    AutomationError,
    ExternalServiceError,
)

__all__ = [
    "get_logger",
    "configure_logging",
    "ApplicationError",
    "ConfigurationError",
    "ValidationError",
    "DiscoveryError",
    "FilteringError",
    "EnrichmentError",
    "NLPError",
    "ScoringError",
    "OutreachError",
    "AutomationError",
    "ExternalServiceError",
]
