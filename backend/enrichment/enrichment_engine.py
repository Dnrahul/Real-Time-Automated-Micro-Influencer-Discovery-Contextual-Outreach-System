"""
========================================
📝 Content Enrichment Engine
========================================
Enriches creator profiles with additional content data:
1. Extracts and normalizes captions/descriptions
2. Collects hashtags
3. Builds a content corpus for NLP analysis
4. Estimates email from available data

How it works:
- Takes filtered creator list
- For YouTube: uses video titles + channel description
- For Instagram: uses captions + hashtags + bio
- Combines into a unified 'content_corpus' field
- This corpus is fed into the NLP engine next
"""

import sys
import os
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def _extract_hashtags(text: str) -> list:
    """Extract all hashtags from a text string."""
    if not text:
        return []
    return re.findall(r"#(\w+)", text)


def _extract_mentions(text: str) -> list:
    """Extract all @mentions from a text string."""
    if not text:
        return []
    return re.findall(r"@(\w+)", text)


def _clean_text(text: str) -> str:
    """
    Clean text for NLP processing:
    - Remove URLs
    - Remove special characters (keep spaces, letters, numbers)
    - Normalize whitespace
    """
    if not text:
        return ""
    # Remove URLs
    text = re.sub(r"http\S+|www\.\S+", "", text)
    # Remove emojis (basic)
    text = re.sub(r"[^\w\s#@.,!?'-]", " ", text)
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _build_content_corpus(creator: dict) -> str:
    """
    Build a unified text corpus from all available content.
    This corpus will be used by the NLP engine.
    """
    parts = []

    # YouTube-specific fields
    if creator.get("platform") == "youtube":
        # Channel description
        desc = creator.get("channel_description", "")
        if desc:
            parts.append(_clean_text(desc))

        # Recent video titles
        titles = creator.get("recent_video_titles", [])
        for title in titles:
            parts.append(_clean_text(title))

    # Instagram-specific fields
    elif creator.get("platform") == "instagram":
        # Bio
        bio = creator.get("bio", "")
        if bio:
            parts.append(_clean_text(bio))

        # Recent captions
        captions = creator.get("recent_captions", [])
        for caption in captions:
            parts.append(_clean_text(caption))

        # Hashtags as text
        hashtags = creator.get("recent_hashtags", [])
        for tag in hashtags:
            # Remove # prefix if present, convert to word
            clean_tag = tag.replace("#", "")
            parts.append(clean_tag)

    # Combine everything
    corpus = " ".join(parts)
    return corpus


def _estimate_email(creator: dict) -> str:
    """
    Try to extract/estimate email from available data.
    Checks bio, description, and existing email field.
    """
    # If email already exists
    existing = creator.get("email", "")
    if existing and "@" in existing:
        return existing

    # Try to extract from description/bio
    text = creator.get("channel_description", "") + " " + creator.get("bio", "")
    emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    if emails:
        return emails[0]

    # Generate estimated email from handle/name
    handle = creator.get("channel_handle", creator.get("username", ""))
    if handle:
        clean_handle = handle.replace("@", "")
        return f"{clean_handle}@gmail.com"

    return ""


def enrich_creators(creators: list) -> list:
    """
    Main enrichment function — adds content context to each creator.
    
    Args:
        creators: List of filtered creator dictionaries
    
    Returns:
        List of enriched creator dictionaries with new fields:
        - content_corpus: Combined text for NLP
        - all_hashtags: Collected hashtags
        - all_mentions: Collected mentions
        - estimated_email: Best guess email
        - enrichment_status: "ENRICHED"
    """
    enriched = []

    for creator in creators:
        # Build content corpus for NLP
        creator["content_corpus"] = _build_content_corpus(creator)

        # Collect all hashtags
        all_text = " ".join([
            creator.get("channel_description", ""),
            creator.get("bio", ""),
            " ".join(creator.get("recent_captions", [])),
            " ".join(creator.get("recent_video_titles", []))
        ])
        creator["all_hashtags"] = _extract_hashtags(all_text)
        creator["all_mentions"] = _extract_mentions(all_text)

        # Estimate email
        creator["estimated_email"] = _estimate_email(creator)

        # Mark as enriched
        creator["enrichment_status"] = "ENRICHED"

        enriched.append(creator)

    print(f"[Enrichment Engine] Enriched {len(enriched)} creator profiles")
    return enriched
