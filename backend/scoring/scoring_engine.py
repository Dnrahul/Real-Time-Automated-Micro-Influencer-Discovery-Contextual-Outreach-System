"""
========================================
⭐ Scoring Engine
========================================
Calculates a Brand-Fit Score (0–100) for each creator using NLP.
Combines relevance, engagement, and activity.
"""

import sys
import os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from config.settings import settings


def calculate_nlp_relevance(keyword: str, text_corpus: str) -> float:
    """
    Calculates a relevance score (0-100) using TF-IDF and Cosine Similarity.
    """
    if not text_corpus or not keyword:
        return 0.0
    
    vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
    
    try:
        tfidf_matrix = vectorizer.fit_transform([keyword, text_corpus])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return round(similarity[0][0] * 100, 2)
    except ValueError:
        return 0.0


def _score_relevance(creator: dict, keyword: str) -> float:
    """
    Builds a text corpus for the creator and calculates the NLP relevance score.
    """
    title = creator.get("name", "")
    description = creator.get("channel_description", "")
    themes = " ".join(creator.get("themes", []))
    video_titles = " ".join(creator.get("recent_video_titles", []))
    
    corpus = f"{title} {description} {themes} {video_titles}"
    
    relevance_score = calculate_nlp_relevance(keyword, corpus)
    creator["relevance_score"] = relevance_score
    
    return relevance_score


def score_creators(creators: list, keyword: str) -> list:
    """
    Calculates final brand fit score, formats dict, and sorts descending.
    """
    final_results = []
    
    for creator in creators:
        # 1. Calculate NLP Relevance Score
        relevance = _score_relevance(creator, keyword)
        
        # FILTER OUT UNRELATED:
        # If the relevance score is exactly 0, it means the keyword 
        # is nowhere to be found in their corpus. We must skip them entirely!
        if relevance < 1.0:
            continue
            
        # 2. Normalize Engagement (10% engagement = 100 score)
        engagement_score = min(creator.get("engagement_rate", 0) * 10, 100)
        
        # 3. Default Activity Score (Assume 100 for now if API fetched recently)
        activity_score = 100 
        
        # 4. Final Weighted Score: 50% Relevance, 30% Engagement, 20% Activity
        fit_score = (relevance * 0.50) + (engagement_score * 0.30) + (activity_score * 0.20)
        
        # Standardize fields to match output requirements
        final_format = {
            "name": creator.get("name", "Unknown"),
            "platform": creator.get("platform", "YouTube"),
            "followers": creator.get("followers", creator.get("subscribers", 0)),
            "engagement_rate": creator.get("engagement_rate", 0.0),
            "niche": creator.get("niche", keyword.title()),
            "fit_score": round(fit_score, 2),
            "profile_url": creator.get("profile_url", ""),
            "relevance_score": creator.get("relevance_score", 0.0),
            # Preserve these fields for other pipeline steps
            "id": creator.get("id"),
            "themes": creator.get("themes", []),
            "score_breakdown": {
                "engagement": round(engagement_score, 1),
                "relevance": round(relevance, 1),
                "activity": round(activity_score, 1)
            },
            "scoring_status": "SCORED"
        }
        
        # Merge any other original fields like location, email if needed
        for k, v in creator.items():
            if k not in final_format:
                final_format[k] = v

        final_results.append(final_format)
        
    # Sort descending by fit_score for high-quality ranking
    final_results.sort(key=lambda x: x["fit_score"], reverse=True)
    
    print(f"[Scoring Engine] Scored {len(final_results)} creators using TF-IDF")
    return final_results
