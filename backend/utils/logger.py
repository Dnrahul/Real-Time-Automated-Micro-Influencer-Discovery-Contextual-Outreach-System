"""
========================================
📝 Logging Configuration Module
========================================

Provides structured logging for the entire application:
- Logs to both console and file
- Configurable log levels
- Production-ready format with timestamps
- Easy to integrate across all modules

Usage:
    from backend.utils.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Processing started")
    logger.error("An error occurred", exc_info=True)
"""

import logging
import os
from datetime import datetime
from pathlib import Path


# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)


def _get_log_format(level: str = "DETAILED") -> str:
    """Get appropriate log format based on level."""
    if level == "DETAILED":
        return (
            "[%(asctime)s] %(levelname)-8s [%(name)s] "
            "%(filename)s:%(lineno)d - %(message)s"
        )
    else:
        return "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def configure_logging(
    log_level: str = "INFO",
    log_file: str = None,
    format_type: str = "DETAILED"
) -> None:
    """
    Configure root logger with console and file handlers.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path (default: logs/app.log)
        format_type: Log format type (DETAILED or SIMPLE)
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Log format
    log_format = logging.Formatter(_get_log_format(format_type))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)

    # File handler
    if log_file is None:
        log_file = str(LOGS_DIR / "app.log")

    try:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(log_format)
        root_logger.addHandler(file_handler)
    except (IOError, OSError) as e:
        # If file handler fails, continue with console only
        logging.warning(f"Could not create file handler: {e}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.
    
    Args:
        name: Usually __name__ of the calling module
    
    Returns:
        Configured logger instance
    
    Example:
        from backend.utils.logger import get_logger
        logger = get_logger(__name__)
        logger.info("Module initialized")
    """
    return logging.getLogger(name)
