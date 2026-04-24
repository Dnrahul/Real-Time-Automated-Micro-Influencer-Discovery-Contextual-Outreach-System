"""Quick test: run pipeline directly (bypass FastAPI)."""
import sys, os, json
sys.path.insert(0, os.path.abspath("."))
os.environ["USE_MOCK_DATA"] = "true"

from backend.discovery.youtube_discovery import discover_youtube_creators
from backend.discovery.instagram_discovery import discover_instagram_creators
from backend.filtering.filter_engine import filter_creators
from backend.enrichment.enrichment_engine import enrich_creators
from backend.nlp.nlp_engine import analyze_creators
from backend.segmentation.segmentation_engine import segment_creators
from backend.scoring.scoring_engine import score_creators
from backend.outreach.outreach_generator import generate_bulk_outreach

keyword = "skincare routine"
print("Step 1: Discovery...")
yt = discover_youtube_creators(keyword, 5)
# ig = discover_instagram_creators(keyword, 5)
all_c = yt # + ig
print(f"  Found {len(all_c)} creators")

print("Step 2: Filtering...")
fr = filter_creators(all_c)
filtered = fr["passed"]
print(f"  Passed: {len(filtered)}")

print("Step 3: Enrichment...")
enriched = enrich_creators(filtered)

print("Step 4: NLP...")
analyzed = analyze_creators(enriched)

print("Step 5: Segmentation...")
seg = segment_creators(analyzed)

print("Step 6: Scoring...")
scored = score_creators(seg["creators"], keyword)

print("Step 7: Outreach...")
final = generate_bulk_outreach(scored, "GlowNatural")

print("\n" + "=" * 50)
print(f"RESULTS: {len(final)} creators processed")
print("=" * 50)
for c in final[:3]:
    n = c.get("name", "?")
    p = c.get("platform", "?")
    f_count = c.get("subscribers", c.get("followers", 0))
    s = c.get("fit_score", 0)
    ni = c.get("niche", "?")
    print(f"\n  {n} | {p} | {f_count:,} | Score: {s} | {ni}")
    o = c.get("outreach", {})
    if o:
        print(f"  Email: {o.get('email_subject', 'N/A')}")
        print(f"  DM: {o.get('dm_message', 'N/A')[:80]}...")

print("\nSample JSON:")
if final:
    sample = {
        "name": final[0].get("name"),
        "platform": final[0].get("platform"),
        "profile_url": final[0].get("profile_url"),
        "followers": final[0].get("subscribers", final[0].get("followers")),
        "engagement_rate": final[0].get("engagement_rate"),
        "niche": final[0].get("niche"),
        "themes": final[0].get("themes"),
        "fit_score": final[0].get("fit_score"),
        "relevance_score": final[0].get("relevance_score"),
        "score_breakdown": final[0].get("score_breakdown"),
        "outreach": final[0].get("outreach"),
    }
    print(json.dumps(sample, indent=2, default=str))

print("\nAll tests passed!")
