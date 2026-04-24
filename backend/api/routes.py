"""
========================================
🌐 API Routes
========================================
FastAPI route definitions for the influencer discovery system.

Endpoints:
- POST /api/discover     — Run full discovery pipeline
- POST /api/outreach     — Generate outreach for results
- POST /api/send         — Execute automated sending
- GET  /api/health       — Health check
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from backend.discovery.youtube_discovery import discover_youtube_creators
from backend.discovery.instagram_discovery import discover_instagram_creators
from backend.filtering.filter_engine import filter_creators
from backend.enrichment.enrichment_engine import enrich_creators
from backend.nlp.nlp_engine import analyze_creators
from backend.segmentation.segmentation_engine import segment_creators
from backend.scoring.scoring_engine import score_creators
from backend.outreach.outreach_generator import generate_bulk_outreach
from backend.automation.automation_engine import execute_outreach

router = APIRouter(prefix="/api", tags=["Influencer Discovery"])


# ── Request/Response Models ───────────────────────────────────

class DiscoverRequest(BaseModel):
    keyword: str = Field(..., description="Search keyword", min_length=2)
    max_results: Optional[int] = Field(15, description="Max results per platform")
    platforms: Optional[list] = Field(["youtube", "instagram"], description="Platforms to search")
    brand_name: Optional[str] = Field("Our Brand", description="Brand name for outreach")


class OutreachRequest(BaseModel):
    creators: list = Field(..., description="List of scored creator dicts")
    brand_name: Optional[str] = Field("Our Brand", description="Brand name")


class SendRequest(BaseModel):
    creators: list = Field(..., description="Creators with outreach messages")


# ── Health Check ──────────────────────────────────────────────

@router.get("/health")
async def health_check():
    """System health check endpoint."""
    return {"status": "healthy", "service": "Micro-Influencer Discovery System"}


# ── Full Discovery Pipeline ──────────────────────────────────

@router.post("/discover")
async def discover_influencers(request: DiscoverRequest):
    """
    Run the complete discovery pipeline:
    keyword → discovery → filtering → enrichment → NLP → segmentation → scoring → outreach
    """
    try:
        keyword = request.keyword
        print(f"\n{'='*60}")
        print(f"Starting Discovery Pipeline for: '{keyword}'")
        print(f"{'='*60}\n")

        # Step 1: Discovery — find creators on each platform
        all_creators = []
        if "youtube" in request.platforms:
            yt = discover_youtube_creators(keyword, request.max_results)
            all_creators.extend(yt)
            
        # DISABLED INSTAGRAM MOCK DATA: 
        # The mock data uses the same 15 creators and injects the keyword 
        # into fake captions, causing the "same results" bug.
        # if "instagram" in request.platforms:
        #     ig = discover_instagram_creators(keyword, request.max_results)
        #     all_creators.extend(ig)

        if not all_creators:
            raise HTTPException(status_code=404, detail="No real creators found for this keyword via YouTube API. Please ensure your API key is valid.")

        # Step 2: Filtering
        filter_result = filter_creators(all_creators)
        filtered = filter_result["passed"]
        if not filtered:
            return {
                "status": "no_results_after_filter",
                "filter_stats": filter_result["stats"],
                "rejected": filter_result["rejected"][:5]
            }

        # Step 3: Enrichment
        enriched = enrich_creators(filtered)

        # Step 4: NLP Analysis
        analyzed = analyze_creators(enriched)

        # Step 5: Segmentation
        seg_result = segment_creators(analyzed)
        segmented = seg_result["creators"]

        # Step 6: Scoring
        scored = score_creators(segmented, keyword)

        # Step 7: Outreach Generation
        with_outreach = generate_bulk_outreach(scored, request.brand_name)

        # Build response
        response = {
            "status": "success",
            "keyword": keyword,
            "pipeline_stats": {
                "discovered": len(all_creators),
                "filtered": len(filtered),
                "filter_pass_rate": filter_result["stats"]["pass_rate"],
                "segments": len(seg_result["segment_stats"]),
                "avg_fit_score": round(
                    sum(c["fit_score"] for c in scored) / max(len(scored), 1), 1
                ),
            },
            "segment_stats": seg_result["segment_stats"],
            "creators": [
                {
                    "name": c.get("name"),
                    "platform": c.get("platform"),
                    "followers": c.get("subscribers", c.get("followers")),
                    "engagement_rate": c.get("engagement_rate"),
                    "location": c.get("location"),
                    "niche": c.get("niche"),
                    "themes": c.get("themes", [])[:5],
                    "fit_score": c.get("fit_score"),
                    "score_breakdown": c.get("score_breakdown"),
                    "segment": c.get("segment"),
                    "profile_url": c.get("profile_url"),
                    "email": c.get("estimated_email", c.get("email")),
                    "outreach": c.get("outreach"),
                    "last_active": c.get("last_active"),
                }
                for c in with_outreach
            ],
            "filter_rejected": filter_result["rejected"][:5]
        }

        print(f"\n{'='*60}")
        print(f"Pipeline Complete - {len(scored)} creators scored")
        print(f"{'='*60}\n")

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Generate Outreach Only ────────────────────────────────────

@router.post("/outreach")
async def generate_outreach_endpoint(request: OutreachRequest):
    """Generate outreach messages for pre-scored creators."""
    try:
        with_outreach = generate_bulk_outreach(request.creators, request.brand_name)
        return {"status": "success", "creators": with_outreach}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Execute Automated Sending ─────────────────────────────────

@router.post("/send")
async def send_outreach_endpoint(request: SendRequest):
    """Execute automated outreach sending (email + DM)."""
    try:
        result = execute_outreach(request.creators)
        return {"status": "success", **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
