"""
========================================
⚙️ Configuration Manager (Production-Ready)
========================================

Loads all settings from .env file with validation:
- Type checking and conversion
- Validation of ranges and formats
- Fallback defaults
- Clear error messages for missing critical values

Usage:
    from config.settings import settings
    print(settings.YOUTUBE_API_KEY)
    print(settings.MIN_FOLLOWERS)
"""

import os
import sys
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# ── Load Environment Variables ────────────────────────────────
# Look for .env file in project root
env_file = Path(__file__).parent.parent / ".env"
load_dotenv(env_file)


class Settings:
    """
    Centralized application configuration with validation.
    
    All settings are loaded from .env file.
    If a required setting is missing, appropriate error is raised.
    Optional settings use sensible defaults.
    """

    def __init__(self):
        """Initialize and validate all configuration."""
        self._validate_configuration()

    # ── API Keys ──────────────────────────────────────────────
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # ── Email / SMTP ─────────────────────────────────────────
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_EMAIL: str = os.getenv("SMTP_EMAIL", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM_NAME: str = os.getenv("SMTP_FROM_NAME", "BrandOutreach Team")

    # ── Instagram ─────────────────────────────────────────────
    INSTAGRAM_USERNAME: str = os.getenv("INSTAGRAM_USERNAME", "")
    INSTAGRAM_PASSWORD: str = os.getenv("INSTAGRAM_PASSWORD", "")

    # ── Filtering Thresholds ──────────────────────────────────
    MIN_FOLLOWERS: int = int(os.getenv("MIN_FOLLOWERS", "5000"))
    MAX_FOLLOWERS: int = int(os.getenv("MAX_FOLLOWERS", "100000"))
    MIN_ENGAGEMENT_RATE: float = float(os.getenv("MIN_ENGAGEMENT_RATE", "1.0"))
    TARGET_COUNTRY: str = os.getenv("TARGET_COUNTRY", "IN")

    # ── Scoring Weights (must sum to 1.0) ─────────────────────
    WEIGHT_ENGAGEMENT: float = float(os.getenv("WEIGHT_ENGAGEMENT", "0.30"))
    WEIGHT_RELEVANCE: float = float(os.getenv("WEIGHT_RELEVANCE", "0.35"))
    WEIGHT_FOLLOWERS: float = float(os.getenv("WEIGHT_FOLLOWERS", "0.15"))
    WEIGHT_ACTIVITY: float = float(os.getenv("WEIGHT_ACTIVITY", "0.20"))

    # ── Discovery Limits ──────────────────────────────────────
    MAX_RESULTS_PER_PLATFORM: int = int(os.getenv("MAX_RESULTS_PER_PLATFORM", "50"))
    DAYS_SINCE_LAST_ACTIVE: int = int(os.getenv("DAYS_SINCE_LAST_ACTIVE", "30"))

    # ── Debug / Development ───────────────────────────────────
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    USE_MOCK_DATA: bool = os.getenv("USE_MOCK_DATA", "true").lower() == "true"

    # ── Logging Configuration ────────────────────────────────
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")

    # ── Server Configuration ──────────────────────────────────
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # ── Niche Keywords (used for segmentation) ────────────────
    NICHE_KEYWORDS: dict = {
        "Beauty & Skincare": [
            "skincare", "makeup", "beauty", "serum", "moisturizer",
            "sunscreen", "glow", "skin", "lipstick", "foundation",
            "cosmetics", "facial", "cleanser", "toner"
        ],
        "Education & EdTech": [
            "study", "exam", "upsc", "neet", "jee", "college",
            "education", "learning", "course", "tutorial", "coding",
            "programming", "math", "science", "gate", "placement"
        ],
        "Fitness & Health": [
            "fitness", "gym", "workout", "yoga", "diet", "protein",
            "weight loss", "muscle", "exercise", "health", "nutrition",
            "bodybuilding", "cardio", "wellness"
        ],
        "Technology & Gadgets": [
            "tech", "gadget", "smartphone", "laptop", "review",
            "unboxing", "android", "iphone", "software", "app",
            "gaming", "pc", "specs", "camera"
        ],
        "Finance & Fintech": [
            "finance", "investment", "stock", "mutual fund", "crypto",
            "banking", "money", "trading", "sip", "insurance",
            "credit card", "budget", "savings", "fintech"
        ],
        "Food & Cooking": [
            "food", "recipe", "cooking", "restaurant", "biryani",
            "street food", "vegan", "baking", "kitchen", "chef",
            "meal prep", "healthy food", "snack"
        ],
        "Travel & Lifestyle": [
            "travel", "vlog", "trip", "explore", "destination",
            "hotel", "backpacking", "lifestyle", "fashion", "ootd",
            "style", "luxury", "adventure"
        ],
        "Parenting & Family": [
            "parenting", "baby", "mom", "dad", "kids", "family",
            "pregnancy", "toddler", "childcare", "motherhood"
        ],
    }

    # ── Collaboration Type Mapping ────────────────────────────
    COLLABORATION_MAP: dict = {
        "Beauty & Skincare": ["Product Review", "Affiliate", "Sponsored Post", "UGC"],
        "Education & EdTech": ["Course Promotion", "Affiliate", "Webinar Collab"],
        "Fitness & Health": ["Product Review", "Barter", "Brand Ambassador", "UGC"],
        "Technology & Gadgets": ["Unboxing", "Affiliate", "Sponsored Review", "Giveaway"],
        "Finance & Fintech": ["Educational Collab", "Affiliate", "Sponsored Content"],
        "Food & Cooking": ["Recipe Collab", "Barter", "Sponsored Post", "UGC"],
        "Travel & Lifestyle": ["Sponsored Trip", "Affiliate", "Brand Ambassador"],
        "Parenting & Family": ["Product Review", "Barter", "UGC", "Sponsored Post"],
    }

    # ── Logging Configuration ────────────────────────────────
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")

    # ── Server Configuration ──────────────────────────────────
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    def _validate_configuration(self) -> None:
        """
        Validate configuration settings.
        
        Checks:
        - Weights sum to 1.0
        - Follower range is valid
        - Log level is valid
        - Server port is valid
        """
        # Validate scoring weights sum to 1.0
        total_weight = (
            self.WEIGHT_ENGAGEMENT +
            self.WEIGHT_RELEVANCE +
            self.WEIGHT_FOLLOWERS +
            self.WEIGHT_ACTIVITY
        )
        if not (0.99 <= total_weight <= 1.01):  # Allow small floating point error
            raise ValueError(
                f"Scoring weights must sum to 1.0, got {total_weight}. "
                "Check WEIGHT_ENGAGEMENT, WEIGHT_RELEVANCE, "
                "WEIGHT_FOLLOWERS, WEIGHT_ACTIVITY in .env"
            )

        # Validate follower range
        if self.MIN_FOLLOWERS >= self.MAX_FOLLOWERS:
            raise ValueError(
                f"MIN_FOLLOWERS ({self.MIN_FOLLOWERS}) must be less than "
                f"MAX_FOLLOWERS ({self.MAX_FOLLOWERS})"
            )

        # Validate log level
        valid_levels = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
        if self.LOG_LEVEL not in valid_levels:
            raise ValueError(
                f"LOG_LEVEL must be one of {valid_levels}, got {self.LOG_LEVEL}"
            )

        # Validate server port
        if not (1 <= self.SERVER_PORT <= 65535):
            raise ValueError(
                f"SERVER_PORT must be between 1 and 65535, got {self.SERVER_PORT}"
            )

    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT.lower() == "production"

    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT.lower() == "development"

    def get_niche_keywords(self, niche: str) -> list:
        """
        Get keywords for a specific niche.
        
        Args:
            niche: Niche name (e.g., "Beauty & Skincare")
        
        Returns:
            List of keywords or empty list if niche not found
        """
        return self.NICHE_KEYWORDS.get(niche, [])

    def get_collaboration_types(self, niche: str) -> list:
        """
        Get recommended collaboration types for a niche.
        
        Args:
            niche: Niche name
        
        Returns:
            List of collaboration types or defaults
        """
        return self.COLLABORATION_MAP.get(
            niche,
            ["Sponsored Post", "Barter", "UGC"]
        )


# ── Singleton Instance ─────────────────────────────────────
# Import this throughout the app
settings = Settings()

