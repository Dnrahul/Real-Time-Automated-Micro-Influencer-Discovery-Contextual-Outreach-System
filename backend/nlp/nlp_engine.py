"""
========================================
🧠 NLP Engine
========================================
Performs Natural Language Processing on creator content:
1. Keyword extraction (TF-IDF based)
2. Theme detection (matching against niche keywords)
3. Niche classification (assigns primary niche)
4. Content sentiment (basic positive/negative)

How it works:
- Takes enriched creator profiles with 'content_corpus'
- Uses TF-IDF to find important keywords in each corpus
- Matches keywords against predefined niche categories
- Assigns the best-matching niche to each creator
- Extracts top themes (what the creator talks about most)

This is a keyword-based approach (no LLM needed),
making it fast and free.
"""

import sys
import os
import re
from collections import Counter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from config.settings import settings

# ── Stopwords (common words to ignore) ────────────────────────
STOPWORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "you", "your",
    "he", "she", "it", "they", "them", "this", "that", "is", "am",
    "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "will", "would", "shall", "should", "may",
    "might", "must", "can", "could", "a", "an", "the", "and", "but",
    "or", "nor", "not", "so", "yet", "for", "at", "by", "to", "from",
    "in", "on", "of", "with", "about", "into", "through", "during",
    "before", "after", "above", "below", "between", "out", "off",
    "over", "under", "again", "further", "then", "once", "here",
    "there", "when", "where", "why", "how", "all", "each", "every",
    "both", "few", "more", "most", "other", "some", "such", "no",
    "only", "own", "same", "than", "too", "very", "just", "because",
    "as", "until", "while", "if", "up", "down", "also", "new", "now",
    "hey", "hi", "hello", "get", "got", "like", "make", "know",
    "join", "community", "subscribers", "create", "content", "more",
    "full", "watch", "video", "check", "link", "bio", "follow",
    "india", "indian", "really", "actually", "best", "top"
}

# ── Positive / Negative word lists (basic sentiment) ──────────
POSITIVE_WORDS = {
    "love", "amazing", "great", "excellent", "awesome", "fantastic",
    "wonderful", "brilliant", "superb", "perfect", "beautiful",
    "happy", "recommend", "best", "favorite", "incredible", "useful",
    "helpful", "effective", "affordable", "honest", "genuine"
}

NEGATIVE_WORDS = {
    "bad", "worst", "terrible", "awful", "horrible", "disappointing",
    "waste", "scam", "fake", "poor", "useless", "overpriced",
    "avoid", "annoying", "boring", "never"
}


def _tokenize(text: str) -> list:
    """
    Simple tokenizer: lowercase, split on non-alphanumeric,
    remove stopwords and short words.
    """
    if not text:
        return []
    # Lowercase and split
    words = re.findall(r"[a-z]+", text.lower())
    # Remove stopwords and short words
    return [w for w in words if w not in STOPWORDS and len(w) > 2]


def _extract_keywords(text: str, top_n: int = 15) -> list:
    """
    Extract top keywords using word frequency (simplified TF).
    
    Args:
        text: Content corpus text
        top_n: Number of top keywords to return
    
    Returns:
        List of (keyword, count) tuples
    """
    tokens = _tokenize(text)
    counter = Counter(tokens)
    return counter.most_common(top_n)


def _detect_themes(keywords: list) -> list:
    """
    Detect content themes by matching keywords against
    the niche keyword database.
    
    Returns list of theme strings (e.g., ["skincare", "product reviews"])
    """
    themes = []
    keyword_words = [kw[0] for kw in keywords]  # Just the words

    # Check each niche's keywords
    for niche, niche_kws in settings.NICHE_KEYWORDS.items():
        for niche_kw in niche_kws:
            # Check if niche keyword appears in extracted keywords
            niche_kw_parts = niche_kw.lower().split()
            if any(part in keyword_words for part in niche_kw_parts):
                if niche_kw not in themes:
                    themes.append(niche_kw)

    # Also add raw top keywords as themes (if not already present)
    for kw, count in keywords[:5]:
        if kw not in themes and count >= 2:
            themes.append(kw)

    return themes[:10]  # Cap at 10 themes


def _classify_niche(keywords: list, themes: list) -> str:
    """
    Classify the creator into a primary niche category.
    Uses scoring: each niche keyword match = 1 point.
    Highest scoring niche wins.
    """
    keyword_words = set(kw[0] for kw in keywords)
    theme_words = set(themes)
    all_words = keyword_words | theme_words

    niche_scores = {}

    for niche, niche_kws in settings.NICHE_KEYWORDS.items():
        score = 0
        for niche_kw in niche_kws:
            parts = niche_kw.lower().split()
            if any(part in all_words for part in parts):
                score += 1
        if score > 0:
            niche_scores[niche] = score

    if niche_scores:
        return max(niche_scores, key=niche_scores.get)
    return "General/Lifestyle"


def _analyze_sentiment(text: str) -> dict:
    """
    Basic sentiment analysis using word matching.
    Returns sentiment label and score.
    """
    tokens = set(re.findall(r"[a-z]+", text.lower()))
    pos_count = len(tokens & POSITIVE_WORDS)
    neg_count = len(tokens & NEGATIVE_WORDS)
    total = pos_count + neg_count

    if total == 0:
        return {"label": "neutral", "score": 0.5}

    pos_ratio = pos_count / total

    if pos_ratio >= 0.6:
        return {"label": "positive", "score": round(pos_ratio, 2)}
    elif pos_ratio <= 0.3:
        return {"label": "negative", "score": round(pos_ratio, 2)}
    else:
        return {"label": "mixed", "score": round(pos_ratio, 2)}


def analyze_creators(creators: list) -> list:
    """
    Main NLP function — analyzes each creator's content.
    
    Args:
        creators: List of enriched creator dictionaries
    
    Returns:
        List of creators with new NLP fields:
        - keywords: Top extracted keywords
        - themes: Detected content themes
        - niche: Classified niche category
        - sentiment: Content sentiment analysis
        - nlp_status: "ANALYZED"
    """
    analyzed = []

    for creator in creators:
        corpus = creator.get("content_corpus", "")

        # Extract keywords
        keywords = _extract_keywords(corpus)
        creator["keywords"] = [{"word": kw, "count": cnt} for kw, cnt in keywords]

        # Detect themes
        themes = _detect_themes(keywords)
        creator["themes"] = themes if themes else ["general content"]

        # Classify niche
        creator["niche"] = _classify_niche(keywords, themes)

        # Sentiment analysis
        creator["sentiment"] = _analyze_sentiment(corpus)

        # Mark as analyzed
        creator["nlp_status"] = "ANALYZED"

        analyzed.append(creator)

    print(f"[NLP Engine] Analyzed {len(analyzed)} creator profiles")

    # Print niche distribution
    niche_counts = Counter(c["niche"] for c in analyzed)
    for niche, count in niche_counts.most_common():
        print(f"  > {niche}: {count} creators")

    return analyzed
