"""
========================================
🔎 Filtering Engine
========================================
Filters discovered creators based on:
1. Follower count (5K–100K micro-influencer range)
2. Location (India-based)
3. Engagement rate (minimum threshold)
4. Activity recency (active in last N days)

How it works:
- Takes raw creator list from discovery modules
- Applies each filter sequentially
- Returns only creators who pass ALL criteria
- Logs why creators were rejected (for debugging)
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from config.settings import settings


def _check_follower_range(creator: dict) -> bool:
    """
    Check if creator's followers are in micro-influencer range.
    Range: strictly 5,000 to 100,000.
    """
    followers = creator.get("subscribers", creator.get("followers", 0))
    return 5000 <= followers <= 100000


def _check_location(creator: dict) -> bool:
    """
    Check if creator is based in the target country (India).
    Looks at 'country' and 'location' fields.
    """
    country = creator.get("country", "").upper()
    location = creator.get("location", "").lower()

    # Check country code
    if country == settings.TARGET_COUNTRY:
        return True

    # Check if "india" is mentioned in location
    if "india" in location:
        return True

    return False


def _check_engagement(creator: dict) -> bool:
    """
    Check if creator meets minimum engagement rate.
    Engagement must be >= 2.0%
    """
    engagement = creator.get("engagement_rate", 0)
    return engagement >= 2.0


def _check_activity(creator: dict) -> bool:
    """
    Check if creator has been active within the configured timeframe.
    Default: active within last 30 days.
    """
    last_active_str = creator.get("last_active", "")
    if not last_active_str:
        return False  # No activity data → reject

    try:
        last_active = datetime.strptime(last_active_str, "%Y-%m-%d")
        cutoff = datetime.now() - timedelta(days=settings.DAYS_SINCE_LAST_ACTIVE)
        return last_active >= cutoff
    except (ValueError, TypeError):
        return False


def filter_creators(creators: list) -> dict:
    """
    Main filtering function — applies all filters to a list of creators.
    
    Args:
        creators: List of raw creator dictionaries from discovery
    
    Returns:
        Dictionary with:
        - 'passed': List of creators who passed all filters
        - 'rejected': List of dicts with creator name + rejection reason
        - 'stats': Summary statistics
    """
    passed = []
    rejected = []

    for creator in creators:
        name = creator.get("name", "Unknown")
        rejection_reasons = []

        # Apply each filter
        if not _check_follower_range(creator):
            followers = creator.get("subscribers", creator.get("followers", 0))
            rejection_reasons.append(
                f"Followers ({followers:,}) outside range "
                f"({settings.MIN_FOLLOWERS:,}–{settings.MAX_FOLLOWERS:,})"
            )

        if not _check_location(creator):
            rejection_reasons.append(
                f"Location ({creator.get('location', 'unknown')}) "
                f"not in target country ({settings.TARGET_COUNTRY})"
            )

        if not _check_engagement(creator):
            rejection_reasons.append(
                f"Engagement rate ({creator.get('engagement_rate', 0)}%) "
                f"below minimum ({settings.MIN_ENGAGEMENT_RATE}%)"
            )

        if not _check_activity(creator):
            rejection_reasons.append(
                f"Last active ({creator.get('last_active', 'unknown')}) "
                f"outside {settings.DAYS_SINCE_LAST_ACTIVE}-day window"
            )

        # Verdict
        if rejection_reasons:
            rejected.append({
                "name": name,
                "reasons": rejection_reasons
            })
        else:
            # Mark as filtered
            creator["filter_status"] = "PASSED"
            passed.append(creator)

    # Summary stats
    stats = {
        "total_input": len(creators),
        "total_passed": len(passed),
        "total_rejected": len(rejected),
        "pass_rate": round(len(passed) / max(len(creators), 1) * 100, 1)
    }

    print(f"[Filter Engine] {stats['total_passed']}/{stats['total_input']} "
          f"creators passed ({stats['pass_rate']}% pass rate)")

    return {
        "passed": passed,
        "rejected": rejected,
        "stats": stats
    }
