"""
========================================
🧪 Test Examples - Scoring Engine
========================================

Example unit tests for the scoring engine.
Run with: pytest tests/test_scoring.py -v

These tests show best practices for:
- Testing individual functions
- Mocking external dependencies
- Testing edge cases
- Using fixtures
"""

import pytest
from datetime import datetime, timedelta
from backend.scoring.scoring_engine import (
    score_engagement,
    score_followers,
    score_activity,
    score_relevance,
    score_creators,
)


class TestEngagementScoring:
    """Test suite for engagement score calculation."""

    def test_zero_engagement(self):
        """Test that zero engagement gets zero score."""
        assert score_engagement(0) == 0

    def test_low_engagement(self):
        """Test scoring for low engagement."""
        assert 10 < score_engagement(0.5) < 20

    def test_minimum_acceptable(self):
        """Test scoring at minimum acceptable engagement."""
        assert 15 < score_engagement(1.0) < 25

    def test_good_engagement(self):
        """Test scoring for good engagement."""
        score = score_engagement(3.0)
        assert 55 < score < 65

    def test_great_engagement(self):
        """Test scoring for great engagement."""
        score = score_engagement(5.0)
        assert 75 < score < 85

    def test_exceptional_engagement(self):
        """Test scoring for exceptional engagement."""
        assert score_engagement(10.0) == 100

    def test_engagement_is_monotonic(self):
        """Test that engagement score increases with engagement rate."""
        scores = [score_engagement(x) for x in [0.5, 1.0, 2.0, 3.0, 5.0, 8.0]]
        assert scores == sorted(scores), "Scores should increase monotonically"


class TestFollowerScoring:
    """Test suite for follower count scoring."""

    def test_too_low_followers(self):
        """Test that very low followers get penalized."""
        assert score_followers(2000) == 0

    def test_minimum_micro(self):
        """Test scoring at minimum micro-influencer range."""
        score = score_followers(5000)
        assert 35 < score < 45

    def test_sweet_spot_lower(self):
        """Test scoring at sweet spot (20K)."""
        score = score_followers(20000)
        assert 75 < score < 85

    def test_sweet_spot_ideal(self):
        """Test scoring at ideal follower count (40K)."""
        assert score_followers(40000) == 100

    def test_sweet_spot_upper(self):
        """Test scoring at upper sweet spot (60K)."""
        score = score_followers(60000)
        assert 85 < score < 95

    def test_macro_influencer(self):
        """Test that macro-influencers (>100K) get low score."""
        assert score_followers(100000) > 60

    def test_too_high_followers(self):
        """Test that very high followers get penalized."""
        assert score_followers(500000) < 50


class TestActivityScoring:
    """Test suite for activity recency scoring."""

    def test_active_today(self):
        """Test that today's activity gets high score."""
        today = datetime.now().strftime("%Y-%m-%d")
        assert score_activity(today) == 100

    def test_active_recently(self):
        """Test that recent activity (1-3 days) gets high score."""
        date_2_days_ago = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
        assert score_activity(date_2_days_ago) > 85

    def test_active_week_ago(self):
        """Test that activity from a week ago gets moderate score."""
        date_1_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        score = score_activity(date_1_week_ago)
        assert 70 < score < 80

    def test_active_2_weeks_ago(self):
        """Test that activity from 2 weeks ago gets lower score."""
        date_2_weeks_ago = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
        score = score_activity(date_2_weeks_ago)
        assert 45 < score < 55

    def test_inactive_month_ago(self):
        """Test that activity from a month ago gets low score."""
        date_1_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        score = score_activity(date_1_month_ago)
        assert 20 < score < 30

    def test_inactive_too_long(self):
        """Test that activity older than 30 days gets zero score."""
        date_2_months_ago = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
        assert score_activity(date_2_months_ago) == 0

    def test_invalid_date(self):
        """Test that invalid date gets zero score."""
        assert score_activity("invalid-date") == 0

    def test_empty_date(self):
        """Test that empty date string gets zero score."""
        assert score_activity("") == 0


class TestRelevanceScoring:
    """Test suite for relevance score calculation."""

    def test_perfect_match(self):
        """Test creator with perfect keyword match."""
        creator = {
            "themes": ["skincare", "beauty", "product review"],
            "keywords": [("skincare", 15), ("makeup", 12)],
            "niche": "Beauty & Skincare",
            "content_corpus": "skincare tips for indian skin"
        }
        score = score_relevance(creator, "skincare")
        assert score == 100

    def test_no_match(self):
        """Test creator with no keyword match."""
        creator = {
            "themes": ["fitness", "gym"],
            "keywords": [("workout", 10)],
            "niche": "Fitness & Health",
            "content_corpus": "gym workout routine"
        }
        score = score_relevance(creator, "skincare")
        assert score < 30

    def test_partial_match(self):
        """Test creator with partial match."""
        creator = {
            "themes": ["skincare"],
            "keywords": [("skincare", 8)],
            "niche": "General/Lifestyle",
            "content_corpus": "some skincare content"
        }
        score = score_relevance(creator, "skincare")
        assert 40 < score < 70


class TestScoringIntegration:
    """Integration tests for complete scoring."""

    @pytest.fixture
    def sample_creator(self):
        """Fixture providing a sample creator for testing."""
        return {
            "name": "Test Creator",
            "engagement_rate": 3.5,
            "subscribers": 45000,
            "last_active": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "themes": ["skincare", "beauty"],
            "keywords": [("skincare", 15), ("beauty", 12)],
            "niche": "Beauty & Skincare",
            "content_corpus": "skincare routine beauty tips"
        }

    def test_score_creators_returns_valid_score(self, sample_creator):
        """Test that score_creators returns a valid score."""
        creators = [sample_creator]
        results = score_creators(creators, "skincare")

        assert len(results) == 1
        assert "fit_score" in results[0]
        assert 0 <= results[0]["fit_score"] <= 100

    def test_score_breakdown_available(self, sample_creator):
        """Test that score breakdown is available."""
        creators = [sample_creator]
        results = score_creators(creators, "skincare")

        breakdown = results[0].get("score_breakdown", {})
        assert "engagement" in breakdown
        assert "relevance" in breakdown
        assert "followers" in breakdown
        assert "activity" in breakdown

    def test_scores_are_sorted(self, sample_creator):
        """Test that results are sorted by score (highest first)."""
        creators = [
            {**sample_creator, "name": "Low Score", "engagement_rate": 0.5},
            {**sample_creator, "name": "High Score", "engagement_rate": 6.0},
            {**sample_creator, "name": "Mid Score", "engagement_rate": 3.5},
        ]
        results = score_creators(creators, "test")

        scores = [r["fit_score"] for r in results]
        assert scores == sorted(scores, reverse=True)


# ========================================
# Running Tests
# ========================================
"""
Run all tests:
    pytest tests/ -v

Run specific test file:
    pytest tests/test_scoring.py -v

Run specific test class:
    pytest tests/test_scoring.py::TestEngagementScoring -v

Run specific test:
    pytest tests/test_scoring.py::TestEngagementScoring::test_zero_engagement -v

Run with coverage:
    pytest tests/ --cov=backend

Run with markers:
    pytest tests/ -m "not slow"

Run in parallel:
    pytest tests/ -n auto
"""
