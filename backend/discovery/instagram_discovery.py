"""
========================================
📸 Instagram Discovery Module
========================================
Discovers micro-influencers on Instagram using
keyword-based search.

NOTE: Instagram does not have a free public API for
search. This module provides:
1. MOCK data (realistic Indian influencer profiles)
2. Placeholder for real integration via Apify / Instagrapi

How it works:
1. Takes a keyword (e.g., "skincare")
2. Generates/fetches Instagram creator profiles
3. Returns raw creator data for the filtering pipeline
"""

import sys
import os
import random
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from config.settings import settings


# ── Instagram-specific Indian creator data ────────────────────
INSTAGRAM_CREATORS = [
    {
        "name": "Nidhi Katiyar", "handle": "nidhikatiyar01",
        "bio": "Beauty & Makeup 💄 | Mumbai | Cruelty-free products only 🐰",
        "niche_hint": "beauty"
    },
    {
        "name": "Ranveer Allahbadia", "handle": "beerbiceps",
        "bio": "Fitness 💪 | Mindset 🧠 | Entrepreneurship | Mumbai",
        "niche_hint": "fitness"
    },
    {
        "name": "Ankur Warikoo", "handle": "ankurwarikoo",
        "bio": "Making money simple 💰 | Content Creator | Author | Delhi",
        "niche_hint": "finance"
    },
    {
        "name": "Saloni Srivastava", "handle": "salonisrivastava_",
        "bio": "Study tips + College life 📚 | UPSC aspirant | Lucknow",
        "niche_hint": "education"
    },
    {
        "name": "Aashna Shroff", "handle": "aabornebyaashna",
        "bio": "Fashion | Beauty | Lifestyle ✨ | Mumbai",
        "niche_hint": "beauty"
    },
    {
        "name": "Gaurav Taneja", "handle": "gauravtaneja_",
        "bio": "Pilot ✈️ | Fitness Freak 🏋️ | YouTuber | Delhi",
        "niche_hint": "fitness"
    },
    {
        "name": "Kunal Shah", "handle": "kunalb11",
        "bio": "Startups | Fintech | Building CRED | Bangalore",
        "niche_hint": "finance"
    },
    {
        "name": "Sejal Kumar", "handle": "sejalkumar1195",
        "bio": "Fashion + Travel + Music 🎵 | Delhi | Creating since 2015",
        "niche_hint": "lifestyle"
    },
    {
        "name": "Kabita Singh", "handle": "kaaborsingh",
        "bio": "Home Chef 👩‍🍳 | Indian Recipes | Odisha ❤️",
        "niche_hint": "food"
    },
    {
        "name": "Techy Hitesh", "handle": "techyhitesh",
        "bio": "Tech Reviews 📱 | Gadget Unboxing | Jaipur | 🇮🇳",
        "niche_hint": "tech"
    },
    {
        "name": "Dolly Singh", "handle": "dollysingh",
        "bio": "Comedy | Lifestyle | Fashion | Mumbai girl 💅",
        "niche_hint": "lifestyle"
    },
    {
        "name": "Raj Shamani", "handle": "rajshamani",
        "bio": "Business | Motivation | Podcast Host | India 🇮🇳",
        "niche_hint": "finance"
    },
    {
        "name": "Shivesh Bhatia", "handle": "shiveshbhatia",
        "bio": "Baker 🧁 | Food Blogger | Author | Delhi",
        "niche_hint": "food"
    },
    {
        "name": "Mithila Palkar", "handle": "mikipalkar",
        "bio": "Actor 🎬 | Singer 🎤 | Coffee addict ☕ | Mumbai",
        "niche_hint": "lifestyle"
    },
    {
        "name": "Prajakta Koli", "handle": "mostlysane",
        "bio": "Comedy Creator 😂 | Mental Health Advocate | Mumbai",
        "niche_hint": "lifestyle"
    },
]

# Hashtag pools per niche
HASHTAG_POOLS = {
    "beauty": ["#skincare", "#makeup", "#beautytips", "#glowingskin", "#indianbeauty",
                "#affordablebeauty", "#skincareinindia", "#beautyreview", "#naturalbeauty"],
    "fitness": ["#fitness", "#gymlife", "#workout", "#indianfitness", "#yoga",
                "#healthylifestyle", "#fitnessmotivation", "#homeworkout", "#gains"],
    "finance": ["#finance", "#investing", "#stockmarket", "#mutualfunds", "#money",
                "#financialfreedom", "#indianstocks", "#nifty", "#personalfinance"],
    "education": ["#study", "#upsc", "#education", "#neet", "#jee", "#studygram",
                  "#studytips", "#examprep", "#iit", "#college"],
    "tech": ["#tech", "#gadgets", "#smartphone", "#review", "#unboxing",
             "#techreview", "#android", "#apple", "#bestphone"],
    "food": ["#food", "#recipe", "#indianfood", "#cooking", "#homemade",
             "#streetfood", "#biryani", "#foodie", "#indianrecipe"],
    "lifestyle": ["#lifestyle", "#fashion", "#ootd", "#travel", "#vlog",
                  "#indianblogger", "#style", "#trendy", "#creator"],
}

INDIAN_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
    "Pune", "Kolkata", "Jaipur", "Ahmedabad", "Lucknow"
]


def _match_niche_to_keyword(keyword: str) -> str:
    """Determine which niche matches the keyword best."""
    keyword_lower = keyword.lower()
    niche_scores = {}
    for niche, keywords_list in settings.NICHE_KEYWORDS.items():
        score = sum(1 for kw in keywords_list if kw in keyword_lower)
        if score > 0:
            niche_scores[niche] = score
    if niche_scores:
        return max(niche_scores, key=niche_scores.get)
    return "lifestyle"


def _generate_mock_instagram_creators(keyword: str, count: int = 10) -> list:
    """
    Generate realistic mock Instagram creator data.
    
    Args:
        keyword: Search keyword for context
        count: Number of mock creators to generate
    
    Returns:
        List of creator dictionaries
    """
    creators = []
    niche_key = _match_niche_to_keyword(keyword)

    # Pick relevant creators based on keyword
    relevant_creators = [c for c in INSTAGRAM_CREATORS if niche_key[:4].lower() in c.get("niche_hint", "").lower()]
    if len(relevant_creators) < count:
        # Add some random creators to fill
        others = [c for c in INSTAGRAM_CREATORS if c not in relevant_creators]
        relevant_creators.extend(random.sample(others, min(count - len(relevant_creators), len(others))))

    hashtags = HASHTAG_POOLS.get(
        next((k for k in HASHTAG_POOLS if k in niche_key.lower()), "lifestyle"),
        HASHTAG_POOLS["lifestyle"]
    )

    for i, base in enumerate(relevant_creators[:count]):
        followers = random.randint(5000, 90000)
        following = random.randint(200, 2000)
        total_posts = random.randint(50, 800)
        avg_likes = int(followers * random.uniform(0.03, 0.15))
        avg_comments = int(avg_likes * random.uniform(0.05, 0.15))
        engagement_rate = round(((avg_likes + avg_comments) / max(followers, 1)) * 100, 2)

        days_ago = random.randint(0, 20)
        last_active = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        city = random.choice(INDIAN_CITIES)

        # Generate recent captions
        recent_captions = [
            f"Loving this new {keyword} journey! {random.choice(hashtags)} {random.choice(hashtags)}",
            f"Sharing my top picks for {keyword} 🔥 {random.choice(hashtags)}",
            f"This changed my life! Full review on stories ✨ {random.choice(hashtags)}"
        ]

        creator = {
            "id": f"IG_{random.randint(100000, 999999)}_{i}",
            "name": base["name"],
            "platform": "instagram",
            "username": base["handle"],
            "profile_url": f"https://instagram.com/{base['handle']}",
            "bio": base["bio"],
            "followers": followers,
            "following": following,
            "total_posts": total_posts,
            "avg_likes": avg_likes,
            "avg_comments": avg_comments,
            "engagement_rate": engagement_rate,
            "location": f"{city}, India",
            "country": "IN",
            "last_active": last_active,
            "recent_captions": recent_captions,
            "recent_hashtags": random.sample(hashtags, min(5, len(hashtags))),
            "email": f"{base['handle']}@gmail.com",
            "discovered_via_keyword": keyword,
            "discovery_timestamp": datetime.now().isoformat()
        }
        creators.append(creator)

    return creators


def discover_instagram_creators(keyword: str, max_results: int = None) -> list:
    """
    Main discovery function — searches Instagram for creators
    matching the given keyword.
    
    Args:
        keyword: Search term (e.g., "skincare")
        max_results: Maximum number of results to return
    
    Returns:
        List of raw creator dictionaries
        
    NOTE: This uses mock data by default. For real Instagram
    data, integrate with:
    - Apify Instagram Scraper (free tier available)
    - Instagrapi library (unofficial Instagram API)
    """
    if max_results is None:
        max_results = settings.MAX_RESULTS_PER_PLATFORM

    # Always use mock for Instagram (no free official API)
    print(f"[Instagram Discovery] Using mock data for keyword: '{keyword}'")
    return _generate_mock_instagram_creators(keyword, count=max_results)
