"""
========================================
🛠️ Utility Helper Functions
========================================

Common utilities used across modules:
- Data validation
- String processing
- List operations
- Date/time utilities

Centralized here to reduce code duplication
and improve maintainability.
"""

import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


# ── String/Text Utilities ─────────────────────────────────────

def clean_text(text: str, remove_urls: bool = True) -> str:
    """
    Clean text for processing.
    
    Args:
        text: Text to clean
        remove_urls: Remove URLs from text
    
    Returns:
        Cleaned text
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Remove URLs
    if remove_urls:
        text = re.sub(r"http\S+|www\.\S+", "", text)
    
    # Remove emojis
    text = re.sub(r"[^\w\s#@.,!?'-]", " ", text)
    
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    
    return text


def extract_hashtags(text: str) -> List[str]:
    """
    Extract all hashtags from text.
    
    Args:
        text: Text containing hashtags
    
    Returns:
        List of hashtags (without # prefix)
    """
    if not text:
        return []
    return re.findall(r"#(\w+)", text.lower())


def extract_mentions(text: str) -> List[str]:
    """
    Extract all @mentions from text.
    
    Args:
        text: Text containing mentions
    
    Returns:
        List of mentions (without @ prefix)
    """
    if not text:
        return []
    return re.findall(r"@(\w+)", text.lower())


def extract_emails(text: str) -> List[str]:
    """
    Extract email addresses from text.
    
    Args:
        text: Text containing emails
    
    Returns:
        List of email addresses
    """
    if not text:
        return []
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(pattern, text)


def estimate_email(name: str, username: str = "") -> str:
    """
    Try to estimate creator's email from name/username.
    
    Args:
        name: Creator's full name
        username: Creator's username
    
    Returns:
        Estimated email (not guaranteed to be correct)
    
    Note:
        This is a guess. Actual email should be obtained from
        creator's profile or verified by other means.
    """
    # If we have a username, try common patterns
    if username:
        # Remove @ prefix if present
        username = username.replace("@", "").lower()
        return f"{username}@gmail.com"
    
    # Try with name (first name + last name)
    if name:
        parts = name.lower().split()
        if len(parts) >= 2:
            # firstname.lastname@gmail.com
            return f"{parts[0]}.{parts[-1]}@gmail.com"
        elif len(parts) == 1:
            # firstname@gmail.com
            return f"{parts[0]}@gmail.com"
    
    return ""


# ── Date/Time Utilities ───────────────────────────────────────

def days_since(date_str: str, date_format: str = "%Y-%m-%d") -> Optional[int]:
    """
    Calculate days since a given date.
    
    Args:
        date_str: Date string
        date_format: Expected date format
    
    Returns:
        Number of days since date, or None if invalid
    """
    try:
        date = datetime.strptime(date_str, date_format)
        delta = datetime.now() - date
        return delta.days
    except (ValueError, TypeError):
        return None


def is_within_days(date_str: str, days: int, date_format: str = "%Y-%m-%d") -> bool:
    """
    Check if date is within N days from now.
    
    Args:
        date_str: Date string
        days: Number of days to check
        date_format: Expected date format
    
    Returns:
        True if date is within N days, False otherwise
    """
    days_ago = days_since(date_str, date_format)
    if days_ago is None:
        return False
    return 0 <= days_ago <= days


def format_date(date_obj: datetime, format_str: str = "%Y-%m-%d") -> str:
    """
    Format datetime object to string.
    
    Args:
        date_obj: Datetime object
        format_str: Desired format
    
    Returns:
        Formatted date string
    """
    try:
        return date_obj.strftime(format_str)
    except (AttributeError, ValueError):
        return ""


# ── List/Array Utilities ──────────────────────────────────────

def deduplicate(items: List[str]) -> List[str]:
    """
    Remove duplicates from list, maintaining order.
    
    Args:
        items: List of items
    
    Returns:
        List with duplicates removed
    """
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split list into chunks of specified size.
    
    Args:
        items: List to chunk
        chunk_size: Size of each chunk
    
    Returns:
        List of chunks
    
    Example:
        >>> chunk_list([1,2,3,4,5], 2)
        [[1,2], [3,4], [5]]
    """
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def flatten(nested_list: List[List[Any]]) -> List[Any]:
    """
    Flatten nested list.
    
    Args:
        nested_list: List of lists
    
    Returns:
        Flattened list
    """
    result = []
    for sublist in nested_list:
        if isinstance(sublist, list):
            result.extend(sublist)
        else:
            result.append(sublist)
    return result


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple dictionaries.
    
    Args:
        dicts: Variable number of dictionaries
    
    Returns:
        Merged dictionary (later dicts override earlier ones)
    """
    result = {}
    for d in dicts:
        if isinstance(d, dict):
            result.update(d)
    return result


# ── Number/Percentage Utilities ───────────────────────────────

def calculate_percentage(value: float, total: float) -> float:
    """
    Calculate percentage.
    
    Args:
        value: Part value
        total: Total value
    
    Returns:
        Percentage (0-100), or 0 if total is 0
    """
    if total == 0:
        return 0
    return round((value / total) * 100, 2)


def is_in_range(value: float, min_val: float, max_val: float) -> bool:
    """Check if value is within range (inclusive)."""
    return min_val <= value <= max_val


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value between min and max."""
    return max(min_val, min(value, max_val))


def normalize_score(
    value: float,
    min_val: float = 0,
    max_val: float = 100
) -> float:
    """
    Normalize value to 0-100 scale.
    
    Args:
        value: Value to normalize
        min_val: Minimum possible value
        max_val: Maximum possible value
    
    Returns:
        Normalized score (0-100)
    """
    if max_val == min_val:
        return 0
    normalized = ((value - min_val) / (max_val - min_val)) * 100
    return clamp(normalized, 0, 100)


# ── Validation Utilities ──────────────────────────────────────

def is_valid_email(email: str) -> bool:
    """
    Basic email validation.
    
    Args:
        email: Email address to validate
    
    Returns:
        True if email looks valid
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email)) if email else False


def is_valid_url(url: str) -> bool:
    """
    Basic URL validation.
    
    Args:
        url: URL to validate
    
    Returns:
        True if URL looks valid
    """
    pattern = r"^https?://[^\s/$.?#].[^\s]*$"
    return bool(re.match(pattern, url)) if url else False


def is_valid_username(username: str, min_length: int = 3) -> bool:
    """
    Validate username format.
    
    Args:
        username: Username to validate
        min_length: Minimum length required
    
    Returns:
        True if username is valid
    """
    if not username or len(username) < min_length:
        return False
    # Allow alphanumeric, dots, underscores, hyphens
    pattern = r"^[a-zA-Z0-9._-]+$"
    return bool(re.match(pattern, username))


# ── Data Type Utilities ───────────────────────────────────────

def safe_int(value: Any, default: int = 0) -> int:
    """
    Safely convert value to int with default fallback.
    
    Args:
        value: Value to convert
        default: Default if conversion fails
    
    Returns:
        Integer value or default
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert value to float with default fallback."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_bool(value: Any, default: bool = False) -> bool:
    """
    Safely convert value to bool with default fallback.
    
    Accepts: True, true, 1, "yes", "on" (case-insensitive)
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "yes", "1", "on")
    return bool(value) if value is not None else default
