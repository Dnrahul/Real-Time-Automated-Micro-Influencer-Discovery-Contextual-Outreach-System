# 🏗️ Architecture Documentation

## System Architecture & Design Patterns

Comprehensive technical documentation of the Micro-Influencer Discovery System architecture.

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Layers](#architecture-layers)
3. [Data Flow](#data-flow)
4. [Design Patterns](#design-patterns)
5. [Module Specifications](#module-specifications)
6. [Database Design](#database-design)
7. [API Design](#api-design)
8. [Error Handling](#error-handling)
9. [Scalability Considerations](#scalability-considerations)
10. [Future Enhancements](#future-enhancements)

---

## System Overview

### High-Level Architecture

```
┌────────────────────────────────────────────────────┐
│                  USER INTERFACES                   │
│  ┌──────────────────┐        ┌──────────────────┐ │
│  │  Streamlit UI    │        │   REST API       │ │
│  │  (Dashboard)     │        │   (FastAPI)      │ │
│  └──────────────────┘        └──────────────────┘ │
└────────────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────────────┐
│           MIDDLEWARE LAYER                         │
│  ┌──────────────────────────────────────────────┐ │
│  │  Error Handling  │  Logging  │  Validation   │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────────────┐
│        PROCESSING PIPELINE (8 Stages)              │
│  1. Discovery  2. Filtering  3. Enrichment        │
│  4. NLP Analysis  5. Segmentation  6. Scoring     │
│  7. Outreach  8. Automation                       │
└────────────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────────────┐
│           EXTERNAL INTEGRATIONS                    │
│  ├─ YouTube Data API v3                          │
│  ├─ SMTP Email Server                            │
│  ├─ Instagram DM API                             │
│  └─ Future: Database, Queue, Cache               │
└────────────────────────────────────────────────────┘
```

---

## Architecture Layers

### Layer 1: Presentation Layer
- **Streamlit UI** — Interactive web dashboard
- **REST API** — FastAPI endpoints for programmatic access
- Responsible for: Input validation, user interaction, response formatting

### Layer 2: Middleware Layer
- **Error Handler** — Catches exceptions, converts to HTTP responses
- **Logger** — Structured logging across all modules
- **Validators** — Pydantic models for request validation
- Responsible for: Cross-cutting concerns, consistency

### Layer 3: Business Logic Layer
- **Discovery Engine** — Find creators on YouTube & Instagram
- **Filtering Engine** — Apply criteria filters
- **Enrichment Engine** — Extract content metadata
- **NLP Engine** — Analyze content with keyword extraction
- **Segmentation Engine** — Cluster creators by attributes
- **Scoring Engine** — Calculate brand-fit score
- **Outreach Engine** — Generate personalized messages
- **Automation Engine** — Send emails and DMs

### Layer 4: Utility Layer
- **Logging** — Structured log output
- **Exceptions** — Custom exception hierarchy
- **Helpers** — Reusable utility functions
- **Settings** — Configuration management

### Layer 5: Data/External Layer
- **External APIs** — YouTube, Instagram, SMTP
- **Database** — In-memory, MongoDB, PostgreSQL (future)
- **Cache** — Redis (future)
- **Message Queue** — Celery/RabbitMQ (future)

---

## Data Flow

### Complete Pipeline Workflow

```
┌─────────────────────────────────────────────────┐
│  USER INPUT                                     │
│  ├─ Keyword: "skincare routine"               │
│  ├─ Max Results: 15                           │
│  ├─ Platforms: ["youtube", "instagram"]       │
│  └─ Brand Name: "GlowNatural"                 │
└─────────────┬───────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  STAGE 1: DISCOVERY                             │
│  Input: Keyword                                 │
│  Process: Query YouTube API + Instagram mock   │
│  Output: Raw creator objects (30+ creators)    │
│  Execution Time: 2-5 seconds                   │
│  Potential Issues: API rate limit, network     │
└─────────────┬───────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  STAGE 2: FILTERING                             │
│  Input: Raw creators (30)                      │
│  Filters Applied:                              │
│    ├─ Follower range: 5K-100K                 │
│    ├─ Location: India (country="IN")          │
│    ├─ Engagement: ≥1.0%                       │
│    └─ Activity: Last active ≤30 days          │
│  Output: Filtered creators (18)                │
│  Execution Time: ~100ms                        │
│  Pass Rate: 60%                                │
└─────────────┬───────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  STAGE 3: ENRICHMENT                            │
│  Input: Filtered creators (18)                 │
│  Enrichment:                                   │
│    ├─ Extract video titles/descriptions       │
│    ├─ Extract captions & hashtags             │
│    ├─ Build content corpus                    │
│    └─ Estimate contact emails                 │
│  Output: Enriched creators with content       │
│  Execution Time: ~200ms                        │
└─────────────┬───────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  STAGE 4: NLP ANALYSIS                          │
│  Input: Enriched creators (18)                 │
│  Analysis:                                     │
│    ├─ Extract keywords (TF frequency)         │
│    ├─ Detect themes/topics                    │
│    ├─ Classify niche (Beauty, Tech, etc)      │
│    └─ Sentiment analysis (basic)              │
│  Output: Analyzed creators with themes        │
│  Execution Time: ~300ms                        │
│  Example: ["skincare", "product review"]      │
└─────────────┬───────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  STAGE 5: SEGMENTATION                          │
│  Input: Analyzed creators (18)                 │
│  Segmentation:                                 │
│    ├─ Group by niche (Beauty, Tech, etc)      │
│    ├─ Classify engagement tier (HIGH/MED/LOW) │
│    ├─ Classify follower tier (NANO/MICRO)     │
│    └─ Assign collaboration types              │
│  Output: Segmented creators with metadata     │
│  Execution Time: ~50ms                         │
│  Segments: 3 (Beauty: 12, Tech: 4, Food: 2)   │
└─────────────┬───────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  STAGE 6: SCORING                               │
│  Input: Segmented creators (18)                │
│  Scoring (0-100 scale):                        │
│    ├─ Engagement Score (30% weight)           │
│    │  Formula: curve based on engagement %    │
│    ├─ Relevance Score (35% weight)            │
│    │  Formula: keyword match intensity        │
│    ├─ Followers Score (15% weight)            │
│    │  Formula: optimal at 20K-60K range       │
│    └─ Activity Score (20% weight)             │
│       Formula: recency in days                │
│  Output: Scored creators (0-100 score)        │
│  Execution Time: ~50ms                         │
│  Avg Score: 72.5                              │
└─────────────┬───────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  STAGE 7: OUTREACH GENERATION                   │
│  Input: Scored creators (18)                   │
│  Generation:                                   │
│    ├─ Generate email (subject + body)         │
│    ├─ Generate Instagram DM                   │
│    └─ Personalize with creator content refs   │
│  Output: Creators with outreach messages      │
│  Execution Time: ~100ms                        │
│  Email Length: 60-90 words                     │
│  DM Length: 15-30 words                        │
└─────────────┬───────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  STAGE 8: AUTOMATION (Optional)                 │
│  Input: Outreach-ready creators (18)           │
│  Sending:                                      │
│    ├─ Send emails via SMTP (with retry)      │
│    ├─ Send DMs via Instagram API              │
│    └─ Log delivery status                     │
│  Output: Delivery results + status             │
│  Execution Time: Variable (depends on network) │
│  Note: Runs in MOCK mode by default           │
└─────────────┬───────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  FINAL OUTPUT                                   │
│  ├─ List of scored creators                   │
│  ├─ Segmentation statistics                   │
│  ├─ Pipeline metrics                          │
│  ├─ Outreach messages                         │
│  └─ Delivery status (if automation enabled)   │
└─────────────────────────────────────────────────┘

TOTAL EXECUTION TIME: 3-6 seconds (without automation)
```

### Data Structure Evolution

```
Stage 1 (Discovery):
{
  "name": "Priya Sharma",
  "platform": "youtube",
  "subscribers": 45200,
  "last_active": "2026-04-22"
}

Stage 2 (Filtering):
+ filter_status: "PASSED"

Stage 3 (Enrichment):
+ recent_video_titles: [...]
+ channel_description: "..."
+ content_corpus: "skincare makeup beauty..."

Stage 4 (NLP):
+ keywords: [("skincare", 15), ("makeup", 12), ...]
+ themes: ["skincare", "product review"]
+ niche: "Beauty & Skincare"

Stage 5 (Segmentation):
+ segment: {
    "niche": "Beauty & Skincare",
    "engagement_tier": "HIGH",
    "follower_tier": "MICRO_MID",
    "collaboration_types": ["Product Review", "Affiliate"]
  }

Stage 6 (Scoring):
+ fit_score: 87.5
+ score_breakdown: {
    "engagement": 85,
    "relevance": 92,
    "followers": 88,
    "activity": 80
  }

Stage 7 (Outreach):
+ outreach: {
    "email_subject": "...",
    "email_body": "...",
    "dm_message": "..."
  }

Stage 8 (Automation):
+ delivery: {
    "email_result": {...},
    "dm_result": {...}
  }
```

---

## Design Patterns

### 1. Pipeline Pattern
- Processes data through sequential stages
- Each stage transforms data and passes to next
- Easy to add/remove/modify stages
- **Example:** Discovery → Filtering → Enrichment → ...

### 2. Factory Pattern
- Create objects based on platform (YouTube vs Instagram)
- **Example:** Creator objects built differently per platform

### 3. Strategy Pattern
- Different scoring strategies for different creators
- Different filtering criteria based on configuration
- **Example:** `score_engagement()`, `score_followers()`, etc.

### 4. Singleton Pattern
- One instance of configuration throughout app
- **Example:** `settings` object imported everywhere

### 5. Observer Pattern
- Logging system observes all events
- **Example:** Log handler captures all module actions

### 6. Decorator Pattern
- Exception handlers decorate API endpoints
- Pydantic validators decorate request models
- **Example:** `@router.post("/api/discover")`

### 7. Template Method Pattern
- Common processing template with customizable steps
- **Example:** Discovery process template implemented per platform

---

## Module Specifications

### Module: Discovery

**Purpose:** Find creators matching a keyword  
**Input:** Keyword string, max results count  
**Output:** Raw creator objects

**Implementation Details:**
```python
discover_youtube_creators(keyword: str, max_results: int) -> list
- Calls YouTube Data API search endpoint
- Parses channel information
- Returns: name, subscribers, videos, description, etc.

discover_instagram_creators(keyword: str, max_results: int) -> list
- Uses mock data (or Instagrapi for real)
- Returns: handle, followers, bio, hashtags, etc.
```

**Error Handling:**
- API rate limit → Return partial results
- Network error → Fall back to mock data
- Invalid key → Log error, return empty list

### Module: Filtering

**Purpose:** Apply business rules to filter creators  
**Input:** Creator objects  
**Output:** Passed + rejected lists with reasons

**Filters Applied:**
1. **Follower Range** — 5K ≤ followers ≤ 100K
2. **Location** — Country = "IN"
3. **Engagement** — engagement_rate ≥ 1.0%
4. **Activity** — last_active within 30 days

**Scalability Note:**
- O(n) time complexity
- Can filter 10K creators in <1 second

### Module: Enrichment

**Purpose:** Extract content metadata  
**Input:** Creator objects  
**Output:** Creators with content_corpus field

**Operations:**
1. Extract hashtags from captions
2. Extract mentions from descriptions
3. Clean and normalize text
4. Build unified content corpus
5. Estimate email address

**Performance:**
- ~10ms per creator
- 20 creators: ~200ms

### Module: NLP

**Purpose:** Analyze content with keyword extraction  
**Input:** Enriched creators with content_corpus  
**Output:** Keywords, themes, niche classification

**Algorithms:**
- **TF Frequency** — Simple word frequency (no IDF)
- **Theme Detection** — Match against niche keywords
- **Niche Classification** — Scoring-based classification
- **Sentiment** — Basic positive/negative word count

**No LLM Required:**
- Lightweight and fast
- Works offline
- No API costs

### Module: Segmentation

**Purpose:** Cluster creators by attributes  
**Input:** Analyzed creators  
**Output:** Creator segments with metadata

**Segmentation Criteria:**
1. **Niche** — Primary category (Beauty, Tech, etc)
2. **Engagement Tier** — HIGH (>5%), MEDIUM (2-5%), LOW (<2%)
3. **Follower Tier** — NANO, MICRO_LOW, MICRO_MID, MICRO_HIGH
4. **Collaboration Types** — Recommended partnerships

### Module: Scoring

**Purpose:** Calculate brand-fit score (0-100)  
**Input:** Segmented creators + keyword  
**Output:** fit_score + score_breakdown

**Scoring Formula:**
```
fit_score = (
  score_engagement(engagement_rate) × 0.30 +
  score_relevance(creator, keyword) × 0.35 +
  score_followers(followers) × 0.15 +
  score_activity(last_active) × 0.20
)
```

**Weights:** Customizable via .env

### Module: Outreach

**Purpose:** Generate personalized messages  
**Input:** Scored creators + brand_name  
**Output:** Email + DM templates

**Templates:**
- Email: Subject (8-10 words) + Body (60-90 words)
- DM: Single message (15-30 words)
- Personalization: Creator name, platform, niche, themes

### Module: Automation

**Purpose:** Send messages automatically  
**Input:** Creators with outreach  
**Output:** Delivery status

**Methods:**
- **Email** — SMTP (Gmail, SendGrid, AWS SES)
- **DM** — Instagram API (Instagrapi, Apify)

**Features:**
- Retry logic (up to 3 attempts)
- Error logging
- Mock mode for testing

---

## Database Design

### Current: In-Memory Storage
- All data stored in RAM during execution
- Fast but not persistent
- Lost on server restart

### Future: MongoDB Integration
```python
collections = {
  "creators": {
    "_id": ObjectId,
    "name": str,
    "platform": str,
    "fit_score": float,
    "created_at": datetime,
    "updated_at": datetime,
    "outreach": dict,
    "delivery_status": str
  },
  "campaigns": {
    "_id": ObjectId,
    "name": str,
    "keyword": str,
    "creators_count": int,
    "created_at": datetime
  }
}
```

### Future: PostgreSQL Schema
```sql
CREATE TABLE creators (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  platform VARCHAR(50),
  followers INT,
  engagement_rate FLOAT,
  fit_score FLOAT,
  niche VARCHAR(100),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE outreach (
  id SERIAL PRIMARY KEY,
  creator_id INT REFERENCES creators(id),
  email_subject TEXT,
  email_body TEXT,
  dm_message TEXT,
  sent_at TIMESTAMP
);
```

---

## API Design

### REST Principles
- **GET** — Retrieve resources (health check)
- **POST** — Create operations (discover)
- **PUT** — Update operations (future)
- **DELETE** — Remove operations (future)

### Endpoint Structure
```
/api/v1/
  /discover        (POST) - Run full pipeline
  /health          (GET)  - Status check
  /creators        (GET)  - List creators (future)
  /campaigns       (POST) - Create campaign (future)
  /results/{id}    (GET)  - Get results (future)
```

### Response Format (Consistent)
```json
{
  "status": "success|error|pending",
  "data": {},
  "metadata": {
    "timestamp": "2026-04-24T10:30:00Z",
    "version": "1.0.0"
  },
  "error": null
}
```

### Error Responses
```json
{
  "status": "error",
  "error": "VALIDATION_ERROR",
  "message": "Invalid keyword length",
  "status_code": 400,
  "details": {
    "field": "keyword",
    "constraint": "min_length=2"
  }
}
```

---

## Error Handling

### Exception Hierarchy
```
Exception
├── ApplicationError (Custom base)
│   ├── ConfigurationError
│   ├── ValidationError
│   ├── DiscoveryError
│   ├── FilteringError
│   ├── EnrichmentError
│   ├── NLPError
│   ├── ScoringError
│   ├── OutreachError
│   ├── AutomationError
│   └── ExternalServiceError
└── Standard Python Exceptions
```

### Error Handling Strategy

1. **Validation Layer** — Pydantic validates requests
2. **Business Logic** — Try-except with custom exceptions
3. **Middleware** — Convert exceptions to HTTP responses
4. **Logging** — All errors logged with context

### Graceful Degradation
```python
# Example: If YouTube API fails, continue with Instagram
try:
    youtube = discover_youtube_creators(keyword, max_results)
except DiscoveryError as e:
    logger.warning(f"YouTube discovery failed: {e}")
    youtube = []

# Continue with Instagram
instagram = discover_instagram_creators(keyword, max_results)
all_creators = youtube + instagram
```

---

## Scalability Considerations

### Current Limitations
- Single process (no parallelization)
- In-memory storage (RAM limited)
- Synchronous API calls (blocking I/O)
- No caching

### Scaling Strategies

#### 1. Horizontal Scaling (Multiple Servers)
```docker
# Multiple FastAPI instances behind load balancer
- Instance 1 (port 8001)
- Instance 2 (port 8002)
- Instance 3 (port 8003)
- NGINX Load Balancer → distribution
```

#### 2. Vertical Scaling (More Resources)
```bash
# Increase workers per instance
uvicorn backend.main:app --workers 8
```

#### 3. Async/Await
```python
# Convert blocking I/O to async
async def discover_influencers_async(request: DiscoverRequest):
    youtube_task = asyncio.create_task(discover_youtube(...))
    instagram_task = asyncio.create_task(discover_instagram(...))
    results = await asyncio.gather(youtube_task, instagram_task)
```

#### 4. Caching Layer
```python
# Cache YouTube API results
from functools import lru_cache

@lru_cache(maxsize=128)
def discover_youtube_creators_cached(keyword: str, max_results: int):
    return discover_youtube_creators(keyword, max_results)
```

#### 5. Job Queue
```python
# Use Celery + RabbitMQ for long-running tasks
@celery.task
def process_creators_async(keyword: str):
    # Run pipeline in background
    return run_pipeline(keyword)
```

#### 6. Database Indexing
```sql
-- Speed up queries
CREATE INDEX idx_creators_niche ON creators(niche);
CREATE INDEX idx_creators_fit_score ON creators(fit_score DESC);
CREATE INDEX idx_creators_platform ON creators(platform);
```

---

## Future Enhancements

### Short-term (1-2 months)
- [ ] Add Celery task queue for async processing
- [ ] Implement Redis caching
- [ ] Add database persistence (MongoDB/PostgreSQL)
- [ ] Improve error messages and logging
- [ ] Add rate limiting and request throttling

### Medium-term (2-4 months)
- [ ] Real Instagram API integration (Instagrapi)
- [ ] Multi-language support
- [ ] A/B testing for outreach templates
- [ ] Creator analytics dashboard
- [ ] Advanced filtering options (custom rules)

### Long-term (4+ months)
- [ ] Machine learning model for scoring (vs rules-based)
- [ ] AI-powered outreach generation (GPT integration)
- [ ] Webhook support for custom integrations
- [ ] Multi-user accounts and team collaboration
- [ ] Advanced analytics and reporting
- [ ] TikTok and other platform support

---

## Performance Benchmarks

### Current Performance (Single Instance)
```
Discovery:     2-5 seconds (API dependent)
Filtering:     ~100ms for 30 creators
Enrichment:    ~200ms for 20 creators
NLP:           ~300ms for 20 creators
Segmentation:  ~50ms for 20 creators
Scoring:       ~50ms for 20 creators
Outreach:      ~100ms for 20 creators
Total (E2E):   3-6 seconds for 20 creators
```

### Target Performance (After Optimization)
```
With async:    1-2 seconds
With caching:  <500ms (cached)
With DB:       Variable (depends on queries)
```

---

## Conclusion

This architecture provides:
- ✅ Clean separation of concerns
- ✅ Modular, extensible design
- ✅ Production-ready error handling
- ✅ Scalable foundation
- ✅ Easy to maintain and test
- ✅ Ready for future enhancements

For questions or improvements, refer to the main README and deployment guide.

---

**Last Updated:** April 24, 2026  
**Version:** 1.0.0
