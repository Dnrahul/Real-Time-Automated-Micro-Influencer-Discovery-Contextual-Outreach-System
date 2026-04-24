"""
========================================
🔍 YouTube Discovery Module
========================================
Discovers micro-influencers on YouTube using the
YouTube Data API v3 based on keyword search.

Strictly uses the YouTube Data API v3. No mock data.
"""

import sys
import os
from datetime import datetime

# Add project root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from config.settings import settings
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def discover_youtube_creators(keyword: str, max_results: int = 10) -> list:
    """
    Main discovery function — searches YouTube for creators
    matching the given keyword.
    
    Args:
        keyword: Search term (e.g., "skincare")
        max_results: Maximum number of results to return (default: 10)
    
    Returns:
        List of raw creator dictionaries
    """
    api_key = settings.YOUTUBE_API_KEY
    
    # Bonus: Debug print
    print(f"Using API KEY: {bool(api_key and api_key != 'your_youtube_api_key_here')}")

    # Validation: Missing API Key
    if not api_key or api_key == "your_youtube_api_key_here":
        raise ValueError("CRITICAL ERROR: YOUTUBE_API_KEY is missing or invalid in your .env file.")

    try:
        youtube = build("youtube", "v3", developerKey=api_key)

        # Step 1: Search for channels dynamically matching the keyword
        search_query = f"{keyword} influencer India"
        search_response = youtube.search().list(
            q=search_query,
            type="channel",
            part="snippet",
            maxResults=max_results,
            regionCode="IN",
            relevanceLanguage="en",
            order="relevance"
        ).execute()

        channel_ids = list(set(
            item["snippet"]["channelId"]
            for item in search_response.get("items", [])
        ))

        if not channel_ids:
            print(f"[YouTube Discovery] No channels found via API for keyword: {keyword}")
            return []  # Safe fallback: empty list

        # Step 2: Get channel details (subscribers, etc.)
        channels_response = youtube.channels().list(
            id=",".join(channel_ids),
            part="snippet,statistics"
        ).execute()

        creators = []
        for channel in channels_response.get("items", []):
            stats = channel.get("statistics", {})
            snippet = channel.get("snippet", {})

            # 1. Extract needed fields
            channel_id = channel.get("id")
            channel_name = snippet.get("title", "Unknown")
            description = snippet.get("description", "")
            subscribers = int(stats.get("subscriberCount", 0))
            
            if not channel_id:
                continue

            # 2. Build Profile URL
            handle = snippet.get("customUrl", "")
            if handle:
                handle_formatted = handle if handle.startswith("@") else f"@{handle}"
                profile_url = f"https://www.youtube.com/{handle_formatted}"
            else:
                profile_url = f"https://www.youtube.com/channel/{channel_id}"

            # Calculate basic engagement heuristics
            total_videos = int(stats.get("videoCount", 0))
            view_count = int(stats.get("viewCount", 0))
            avg_views = view_count // max(total_videos, 1)
            engagement_rate = min(round((avg_views / max(subscribers, 1)) * 100, 2), 15.0)

            creator = {
                "id": channel_id,
                "name": channel_name,
                "platform": "YouTube",
                "profile_url": profile_url,
                "subscribers": subscribers,
                "followers": subscribers,
                "channel_description": description,
                "engagement_rate": engagement_rate,
                "location": snippet.get("country", "IN"),
                "country": snippet.get("country", "IN"),
                "discovered_via_keyword": keyword,
                "discovery_timestamp": datetime.now().isoformat()
            }
            creators.append(creator)

        print(f"[YouTube Discovery] Found {len(creators)} creators via API")
        return creators

    except HttpError as e:
        # Validation: API Fails
        print(f"[YouTube Discovery] API ERROR: {e.reason}")
        return []  # Safe fallback: empty list
    except Exception as e:
        print(f"[YouTube Discovery] UNEXPECTED ERROR: {e}")
        return []  # Safe fallback: empty list
