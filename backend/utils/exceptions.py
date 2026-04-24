"""
========================================
⚠️ Custom Exception Classes
========================================

Defines application-specific exceptions for:
- API errors (discovery, external services)
- Validation errors (invalid input, filters)
- Processing errors (enrichment, NLP, scoring)
- Configuration errors (missing env vars)

All custom exceptions inherit from a base class
for consistent error handling.

Usage:
    from backend.utils.exceptions import (
        DiscoveryError, ValidationError, ConfigError
    )
    
    try:
        result = discover_creators(keyword)
    except DiscoveryError as e:
        logger.error(f"Discovery failed: {e}")
        raise
"""


class ApplicationError(Exception):
    """
    Base exception for all application errors.
    
    Attributes:
        message: Human-readable error message
        error_code: Machine-readable error code
        status_code: HTTP status code (for API responses)
    """
    
    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: dict = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> dict:
        """Convert exception to response-friendly dictionary."""
        return {
            "error": self.error_code,
            "message": self.message,
            "status_code": self.status_code,
            "details": self.details
        }


class ConfigurationError(ApplicationError):
    """
    Raised when configuration is missing or invalid.
    
    Example:
        if not YOUTUBE_API_KEY:
            raise ConfigurationError(
                "YOUTUBE_API_KEY is not set",
                error_code="MISSING_ENV_VAR",
                status_code=500
            )
    """
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            message=message,
            error_code="CONFIG_ERROR",
            status_code=500,
            details=details
        )


class ValidationError(ApplicationError):
    """
    Raised when input validation fails.
    
    Example:
        if len(keyword) < 2:
            raise ValidationError(
                "Keyword too short",
                error_code="INVALID_KEYWORD_LENGTH",
                status_code=400,
                details={"field": "keyword", "min_length": 2}
            )
    """
    
    def __init__(
        self,
        message: str,
        error_code: str = "VALIDATION_ERROR",
        details: dict = None
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=400,
            details=details
        )


class DiscoveryError(ApplicationError):
    """
    Raised when creator discovery fails.
    
    Reasons:
    - API rate limit exceeded
    - Invalid API key
    - Network error
    - No results found
    
    Example:
        if not response:
            raise DiscoveryError(
                "YouTube API returned no results",
                error_code="NO_RESULTS",
                status_code=404
            )
    """
    
    def __init__(self, message: str, error_code: str = "DISCOVERY_ERROR"):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=503
        )


class FilteringError(ApplicationError):
    """Raised when filtering process fails."""
    
    def __init__(self, message: str, error_code: str = "FILTERING_ERROR"):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=422
        )


class EnrichmentError(ApplicationError):
    """Raised when content enrichment fails."""
    
    def __init__(self, message: str, error_code: str = "ENRICHMENT_ERROR"):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=500
        )


class NLPError(ApplicationError):
    """Raised when NLP analysis fails."""
    
    def __init__(self, message: str, error_code: str = "NLP_ERROR"):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=500
        )


class ScoringError(ApplicationError):
    """Raised when scoring engine fails."""
    
    def __init__(self, message: str, error_code: str = "SCORING_ERROR"):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=500
        )


class OutreachError(ApplicationError):
    """Raised when outreach generation fails."""
    
    def __init__(self, message: str, error_code: str = "OUTREACH_ERROR"):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=500
        )


class AutomationError(ApplicationError):
    """
    Raised when automated sending fails.
    
    Reasons:
    - SMTP connection error
    - Invalid email address
    - DM sending failed
    """
    
    def __init__(self, message: str, error_code: str = "AUTOMATION_ERROR"):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=500
        )


class ExternalServiceError(ApplicationError):
    """
    Raised when external service is unavailable.
    
    Reasons:
    - API rate limit
    - Service down
    - Network timeout
    """
    
    def __init__(
        self,
        service_name: str,
        message: str,
        error_code: str = "SERVICE_UNAVAILABLE"
    ):
        details = {"service": service_name}
        super().__init__(
            message=f"{service_name}: {message}",
            error_code=error_code,
            status_code=503,
            details=details
        )
