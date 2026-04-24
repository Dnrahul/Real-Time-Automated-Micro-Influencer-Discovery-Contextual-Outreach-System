"""
========================================
✉️ Outreach Generator
========================================
Generates personalized outreach messages:
1. Email (60–90 words)
2. Instagram DM (15–30 words)

References creator's actual content for personalization.
"""

import sys, os, random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from config.settings import settings

EMAIL_TEMPLATES = [
    {
        "subject": "Loved your {content_ref} - Let's Collaborate!",
        "body": (
            "Hi {name}! I came across your {content_type} on \"{content_ref}\" "
            "and was genuinely impressed. Your audience of {followers:,}+ clearly "
            "trusts your recommendations in {niche}.\n\n"
            "We're launching {brand_offering} and believe your expertise in "
            "{themes} makes you the perfect partner for a {collab_type} collaboration.\n\n"
            "Would you be open to a quick chat this week?\n\nBest,\n{sender_name}"
        )
    },
    {
        "subject": "Partnership Opportunity - Your {niche} Content is Great",
        "body": (
            "Hey {name}! Huge fan of your work, especially \"{content_ref}\". "
            "Your authentic approach to {themes} really stands out.\n\n"
            "I'm reaching out from {brand_name} — we're looking for voices in "
            "{niche} to try {brand_offering}. Given your {followers:,}+ engaged "
            "followers, we think this could be a great fit.\n\n"
            "Interested in a {collab_type} partnership?\n\n{sender_name}"
        )
    },
]

DM_TEMPLATES = [
    "Hey {name}! Loved your {themes} content! We're looking for {niche} creators for a {collab_type} collab. Interested?",
    "Hi {name}! Your \"{content_ref}\" was amazing! We'd love to send you {brand_offering} to review. DM us back?",
    "Hey {name}! Big fan of your {themes} content! We have a {collab_type} opportunity perfect for you. Can we chat?",
]

QUALITY_PHRASES = [
    "honest and detailed reviews", "authentic storytelling",
    "engaging and relatable style", "deep expertise",
    "creative presentation", "informative approach",
]

BRAND_OFFERINGS = {
    "Beauty & Skincare": "a new line of natural skincare products",
    "Education & EdTech": "an innovative learning platform",
    "Fitness & Health": "premium fitness supplements",
    "Technology & Gadgets": "our latest tech products",
    "Finance & Fintech": "a user-friendly investment app",
    "Food & Cooking": "artisanal cooking ingredients",
    "Travel & Lifestyle": "curated travel experiences",
    "Parenting & Family": "child-friendly wellness products",
    "General/Lifestyle": "our exciting new product line",
}


def _get_content_reference(creator: dict) -> str:
    titles = creator.get("recent_video_titles", [])
    if titles:
        return titles[0]
    captions = creator.get("recent_captions", [])
    if captions:
        c = captions[0]
        return c[:50] + "..." if len(c) > 50 else c
    themes = creator.get("themes", ["content"])
    return f"{themes[0]} content"


def generate_outreach(creator: dict, brand_name: str = "Our Brand") -> dict:
    """Generate personalized email + DM for a single creator."""
    name = creator.get("name", "Creator")
    followers = creator.get("subscribers", creator.get("followers", 0))
    niche = creator.get("niche", "General/Lifestyle")
    themes = creator.get("themes", ["content creation"])
    segment = creator.get("segment", {})
    collab_types = segment.get("collaboration_types", ["Sponsored Post"])

    tv = {
        "name": name.split()[0],
        "platform": creator.get("platform", "social media").capitalize(),
        "followers": followers,
        "niche": niche,
        "themes": ", ".join(themes[:3]),
        "content_ref": _get_content_reference(creator),
        "content_type": "video" if creator.get("platform") == "youtube" else "post",
        "quality": random.choice(QUALITY_PHRASES),
        "collab_type": collab_types[0] if collab_types else "Sponsored Post",
        "brand_name": brand_name,
        "brand_offering": BRAND_OFFERINGS.get(niche, "our exciting products"),
        "sender_name": settings.SMTP_FROM_NAME,
    }

    et = random.choice(EMAIL_TEMPLATES)
    try:
        email_subject = et["subject"].format(**tv)
        email_body = et["body"].format(**tv)
    except (KeyError, IndexError):
        email_subject = f"Collaboration Opportunity for {name}"
        email_body = f"Hi {name}, we'd love to collaborate with you!"

    dt = random.choice(DM_TEMPLATES)
    try:
        dm_message = dt.format(**tv)
    except (KeyError, IndexError):
        dm_message = f"Hey {name}! Love your content. Want to collab?"

    return {
        "email_subject": email_subject,
        "email_body": email_body,
        "dm_message": dm_message,
        "outreach_status": "GENERATED"
    }


def generate_bulk_outreach(creators: list, brand_name: str = "Our Brand") -> list:
    """Generate outreach for multiple creators."""
    for creator in creators:
        creator["outreach"] = generate_outreach(creator, brand_name)
    print(f"[Outreach Generator] Generated outreach for {len(creators)} creators")
    return creators
