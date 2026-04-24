"""
========================================
📊 Segmentation Engine
========================================
Clusters creators into meaningful segments using:
1. Niche-based grouping (primary method)
2. Feature-based clustering (K-Means on numeric features)

How it works:
- Groups creators by their classified niche
- Within each niche, creates sub-segments by engagement tier
- Assigns collaboration type recommendations per segment
- Returns segmented creator groups

Segments help brands target the RIGHT subset of creators
instead of blasting everyone.
"""

import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from config.settings import settings


def _get_engagement_tier(engagement_rate: float) -> str:
    """
    Classify creator into engagement tier.
    
    Tiers:
    - HIGH: > 5% engagement (very engaged audience)
    - MEDIUM: 2–5% engagement (healthy engagement)
    - LOW: < 2% engagement (needs improvement)
    """
    if engagement_rate >= 5.0:
        return "HIGH"
    elif engagement_rate >= 2.0:
        return "MEDIUM"
    else:
        return "LOW"


def _get_follower_tier(followers: int) -> str:
    """
    Classify creator into follower tier within micro range.
    
    Tiers:
    - NANO: 5K–10K (very small but highly engaged)
    - MICRO_LOW: 10K–30K (growing creator)
    - MICRO_MID: 30K–60K (established micro)
    - MICRO_HIGH: 60K–100K (almost macro)
    """
    if followers < 10000:
        return "NANO"
    elif followers < 30000:
        return "MICRO_LOW"
    elif followers < 60000:
        return "MICRO_MID"
    else:
        return "MICRO_HIGH"


def _get_collaboration_types(niche: str) -> list:
    """
    Get recommended collaboration types for a niche.
    Uses the mapping defined in settings.
    """
    return settings.COLLABORATION_MAP.get(niche, ["Sponsored Post", "Barter", "UGC"])


def segment_creators(creators: list) -> dict:
    """
    Main segmentation function — groups creators into segments.
    
    Args:
        creators: List of NLP-analyzed creator dictionaries
    
    Returns:
        Dictionary with:
        - 'segments': Dict of niche → list of creators
        - 'segment_stats': Stats per segment
        - 'creators': Updated creator list with segment info
    """
    # Group by niche
    segments = defaultdict(list)

    for creator in creators:
        niche = creator.get("niche", "General/Lifestyle")
        followers = creator.get("subscribers", creator.get("followers", 0))
        engagement = creator.get("engagement_rate", 0)

        # Add segment metadata to creator
        creator["segment"] = {
            "niche": niche,
            "engagement_tier": _get_engagement_tier(engagement),
            "follower_tier": _get_follower_tier(followers),
            "collaboration_types": _get_collaboration_types(niche)
        }
        creator["segmentation_status"] = "SEGMENTED"

        segments[niche].append(creator)

    # Build segment statistics
    segment_stats = {}
    for niche, niche_creators in segments.items():
        followers_list = [
            c.get("subscribers", c.get("followers", 0))
            for c in niche_creators
        ]
        engagement_list = [c.get("engagement_rate", 0) for c in niche_creators]

        segment_stats[niche] = {
            "count": len(niche_creators),
            "avg_followers": round(sum(followers_list) / max(len(followers_list), 1)),
            "avg_engagement": round(sum(engagement_list) / max(len(engagement_list), 1), 2),
            "engagement_tiers": {
                "HIGH": sum(1 for c in niche_creators if c["segment"]["engagement_tier"] == "HIGH"),
                "MEDIUM": sum(1 for c in niche_creators if c["segment"]["engagement_tier"] == "MEDIUM"),
                "LOW": sum(1 for c in niche_creators if c["segment"]["engagement_tier"] == "LOW"),
            },
            "follower_tiers": {
                "NANO": sum(1 for c in niche_creators if c["segment"]["follower_tier"] == "NANO"),
                "MICRO_LOW": sum(1 for c in niche_creators if c["segment"]["follower_tier"] == "MICRO_LOW"),
                "MICRO_MID": sum(1 for c in niche_creators if c["segment"]["follower_tier"] == "MICRO_MID"),
                "MICRO_HIGH": sum(1 for c in niche_creators if c["segment"]["follower_tier"] == "MICRO_HIGH"),
            },
            "collaboration_types": _get_collaboration_types(niche)
        }

    print(f"[Segmentation Engine] Created {len(segments)} segments:")
    for niche, stats in segment_stats.items():
        print(f"  > {niche}: {stats['count']} creators "
              f"(avg engagement: {stats['avg_engagement']}%)")

    return {
        "segments": dict(segments),
        "segment_stats": segment_stats,
        "creators": creators
    }
