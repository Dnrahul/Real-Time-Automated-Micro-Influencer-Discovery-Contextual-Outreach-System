"""
========================================
🎨 Streamlit UI — Micro-Influencer Discovery System
========================================
Beautiful web interface for:
- Entering search keywords
- Viewing discovered creators
- Seeing scores and segments
- Reading generated outreach messages
- Executing automated sending

Run with:
    streamlit run ui/streamlit_app.py
"""

import sys
import os
import json

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd

# Import pipeline modules directly (no need for FastAPI server)
from backend.discovery.youtube_discovery import discover_youtube_creators
from backend.discovery.instagram_discovery import discover_instagram_creators
from backend.filtering.filter_engine import filter_creators
from backend.enrichment.enrichment_engine import enrich_creators
from backend.nlp.nlp_engine import analyze_creators
from backend.segmentation.segmentation_engine import segment_creators
from backend.scoring.scoring_engine import score_creators
from backend.outreach.outreach_generator import generate_bulk_outreach
from backend.automation.automation_engine import execute_outreach

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Micro-Influencer Discovery System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS for Premium Look ───────────────────────────────
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }

    /* Stat cards */
    .stat-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    .stat-card h3 {
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
        margin: 0;
    }
    .stat-card p {
        color: #718096;
        margin: 0.3rem 0 0 0;
        font-size: 0.9rem;
    }

    /* Creator card */
    .creator-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .creator-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    }

    /* Score badge */
    .score-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1.1rem;
        color: white;
    }
    .score-high { background: linear-gradient(135deg, #48bb78, #38a169); }
    .score-medium { background: linear-gradient(135deg, #ed8936, #dd6b20); }
    .score-low { background: linear-gradient(135deg, #fc8181, #e53e3e); }

    /* Pipeline animation */
    .pipeline-step {
        background: linear-gradient(135deg, #ebf4ff, #c3dafe);
        border-left: 4px solid #667eea;
        padding: 0.8rem 1.2rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        font-weight: 500;
    }

    /* Niche tag */
    .niche-tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Theme tag */
    .theme-tag {
        display: inline-block;
        background: #edf2f7;
        color: #4a5568;
        padding: 0.2rem 0.6rem;
        border-radius: 10px;
        font-size: 0.8rem;
        margin: 0.1rem;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a202c 0%, #2d3748 100%);
    }
</style>
""", unsafe_allow_html=True)


def render_header():
    """Render the main application header."""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Micro-Influencer Discovery System</h1>
        <p>Real-Time AI-Powered Creator Discovery & Contextual Outreach for Indian Brands</p>
    </div>
    """, unsafe_allow_html=True)


def render_pipeline_animation():
    """Render animated pipeline visualization."""
    steps = [
        ("🔍", "Discovery", "Searching YouTube + Instagram..."),
        ("🔎", "Filtering", "Applying micro-influencer filters..."),
        ("📝", "Enrichment", "Extracting content context..."),
        ("🧠", "NLP Analysis", "Detecting themes & niches..."),
        ("📊", "Segmentation", "Clustering creators..."),
        ("⭐", "Scoring", "Calculating brand-fit scores..."),
        ("✉️", "Outreach", "Generating personalized messages..."),
    ]

    cols = st.columns(len(steps))
    for i, (icon, name, desc) in enumerate(steps):
        with cols[i]:
            st.markdown(f"""
            <div style="text-align:center; padding:0.5rem;">
                <div style="font-size:1.8rem;">{icon}</div>
                <div style="font-weight:600; font-size:0.85rem;">{name}</div>
            </div>
            """, unsafe_allow_html=True)


def render_stats(pipeline_stats: dict, segment_stats: dict):
    """Render pipeline statistics."""
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{pipeline_stats['discovered']}</h3>
            <p>Discovered</p>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{pipeline_stats['filtered']}</h3>
            <p>Filtered</p>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{pipeline_stats['filter_pass_rate']}%</h3>
            <p>Pass Rate</p>
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{pipeline_stats['segments']}</h3>
            <p>Segments</p>
        </div>""", unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{pipeline_stats['avg_fit_score']}</h3>
            <p>Avg Score</p>
        </div>""", unsafe_allow_html=True)


def get_score_class(score: float) -> str:
    if score >= 70:
        return "score-high"
    elif score >= 40:
        return "score-medium"
    return "score-low"


def render_creator_card(creator: dict, index: int):
    """Render a single creator card."""
    name = creator.get("name", "Unknown")
    platform = creator.get("platform", "unknown")
    followers = creator.get("followers", 0)
    engagement = creator.get("engagement_rate", 0)
    niche = creator.get("niche", "General")
    themes = creator.get("themes", [])
    fit_score = creator.get("fit_score", 0)
    location = creator.get("location", "India")
    score_class = get_score_class(fit_score)
    segment = creator.get("segment", {})
    outreach = creator.get("outreach", {})

    platform_icon = "📺" if platform == "youtube" else "📸"
    theme_tags = " ".join(
        f'<span class="theme-tag">{t}</span>' for t in themes[:5]
    )

    st.markdown(f"""
    <div class="creator-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <h3 style="margin:0; font-size:1.3rem;">{platform_icon} {name}</h3>
                <p style="color:#718096; margin:0.2rem 0;">
                    {location} · {platform.capitalize()} · {followers:,} followers
                </p>
            </div>
            <div class="score-badge {score_class}">{fit_score}</div>
        </div>
        <div style="margin-top:0.8rem;">
            <span class="niche-tag">{niche}</span>
            <span style="margin-left:0.5rem; color:#a0aec0;">
                Engagement: {engagement}%
            </span>
            <span style="margin-left:0.5rem; color:#a0aec0;">
                {segment.get('engagement_tier', 'N/A')} tier
            </span>
        </div>
        <div style="margin-top:0.5rem;">{theme_tags}</div>
    </div>
    """, unsafe_allow_html=True)

    # Expandable details
    with st.expander(f"📋 Details & Outreach — {name}"):
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("**📊 Score Breakdown**")
            breakdown = creator.get("score_breakdown", {})
            for factor, value in breakdown.items():
                st.progress(value / 100, text=f"{factor.capitalize()}: {value}")

            st.markdown("**🤝 Collaboration Types**")
            collab_types = segment.get("collaboration_types", [])
            st.write(", ".join(collab_types))

        with col_b:
            if outreach:
                st.markdown("**📧 Email**")
                st.info(f"**Subject:** {outreach.get('email_subject', '')}")
                st.text_area(
                    "Email Body",
                    outreach.get("email_body", ""),
                    height=150,
                    key=f"email_{index}",
                    disabled=True
                )

                st.markdown("**💬 Instagram DM**")
                st.success(outreach.get("dm_message", ""))


def run_pipeline(keyword: str, platforms: list,
                 max_results: int, brand_name: str) -> dict:
    """Run the full discovery pipeline."""
    # Step 1: Discovery
    all_creators = []
    if "YouTube" in platforms:
        yt = discover_youtube_creators(keyword, max_results)
        all_creators.extend(yt)
    if "Instagram" in platforms:
        ig = discover_instagram_creators(keyword, max_results)
        all_creators.extend(ig)

    if not all_creators:
        return None

    # Step 2: Filtering
    filter_result = filter_creators(all_creators)
    filtered = filter_result["passed"]
    if not filtered:
        return {"status": "no_results", "filter_stats": filter_result["stats"]}

    # Step 3–7: Enrich → NLP → Segment → Score → Outreach
    enriched = enrich_creators(filtered)
    analyzed = analyze_creators(enriched)
    seg_result = segment_creators(analyzed)
    scored = score_creators(seg_result["creators"], keyword)
    with_outreach = generate_bulk_outreach(scored, brand_name)

    return {
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
        ]
    }


# ══════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════

def main():
    render_header()

    # ── Sidebar ───────────────────────────────────────────
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        st.markdown("---")

        keyword = st.text_input(
            "🔍 Search Keyword",
            placeholder="e.g., skincare routine, fintech, fitness",
            help="Enter a keyword to discover micro-influencers"
        )

        platforms = st.multiselect(
            "📱 Platforms",
            ["YouTube", "Instagram"],
            default=["YouTube", "Instagram"]
        )

        max_results = st.slider("📊 Max Results per Platform", 5, 30, 15)

        brand_name = st.text_input(
            "🏷️ Brand Name",
            value="Our Brand",
            help="Your brand name for outreach personalization"
        )

        st.markdown("---")
        discover_btn = st.button(
            "🚀 Discover Influencers",
            use_container_width=True,
            type="primary"
        )

        st.markdown("---")
        st.markdown("### 📖 How It Works")
        st.markdown("""
        1. Enter a keyword related to your niche
        2. Select platforms to search
        3. Click **Discover Influencers**
        4. View scored creators with outreach
        5. Export or send outreach automatically
        """)

    # ── Main Content ──────────────────────────────────────
    if discover_btn and keyword:
        render_pipeline_animation()

        with st.spinner("🔄 Running discovery pipeline... This may take a moment."):
            results = run_pipeline(keyword, platforms, max_results, brand_name)

        if results is None:
            st.error("❌ No creators found. Try a different keyword.")
            return

        if results.get("status") == "no_results":
            st.warning("⚠️ All discovered creators were filtered out.")
            st.json(results.get("filter_stats", {}))
            return

        # ── Success: Show Results ─────────────────────────
        st.success(f"✅ Found {len(results['creators'])} qualified creators for '{keyword}'!")

        # Pipeline Stats
        st.markdown("### 📊 Pipeline Statistics")
        render_stats(results["pipeline_stats"], results["segment_stats"])
        st.markdown("")

        # Segment Distribution
        st.markdown("### 📈 Segment Distribution")
        seg_data = results.get("segment_stats", {})
        if seg_data:
            seg_df = pd.DataFrame([
                {
                    "Niche": niche,
                    "Creators": stats["count"],
                    "Avg Engagement": stats["avg_engagement"],
                    "Avg Followers": stats["avg_followers"],
                }
                for niche, stats in seg_data.items()
            ])
            st.dataframe(seg_df, use_container_width=True, hide_index=True)

        st.markdown("---")

        # Creator Cards
        st.markdown("### 🏆 Top Creators (Sorted by Brand-Fit Score)")

        # Filter controls
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            min_score = st.slider("Min Score", 0, 100, 0)
        with col_f2:
            niche_filter = st.selectbox(
                "Filter by Niche",
                ["All"] + list(seg_data.keys())
            )
        with col_f3:
            platform_filter = st.selectbox(
                "Filter by Platform",
                ["All", "youtube", "instagram"]
            )

        # Apply filters
        display_creators = results["creators"]
        if min_score > 0:
            display_creators = [c for c in display_creators if c["fit_score"] >= min_score]
        if niche_filter != "All":
            display_creators = [c for c in display_creators if c["niche"] == niche_filter]
        if platform_filter != "All":
            display_creators = [c for c in display_creators if c["platform"] == platform_filter]

        st.markdown(f"*Showing {len(display_creators)} creators*")

        for i, creator in enumerate(display_creators):
            render_creator_card(creator, i)

        # ── Export Section ────────────────────────────────
        st.markdown("---")
        st.markdown("### 📥 Export Results")

        col_e1, col_e2 = st.columns(2)
        with col_e1:
            json_str = json.dumps(results["creators"], indent=2, default=str)
            st.download_button(
                "📄 Download JSON",
                json_str,
                file_name=f"influencers_{keyword}.json",
                mime="application/json",
                use_container_width=True
            )
        with col_e2:
            csv_data = pd.DataFrame([
                {
                    "Name": c["name"],
                    "Platform": c["platform"],
                    "Followers": c["followers"],
                    "Engagement": c["engagement_rate"],
                    "Niche": c["niche"],
                    "Fit Score": c["fit_score"],
                    "Email": c.get("email", ""),
                    "Profile": c.get("profile_url", ""),
                }
                for c in results["creators"]
            ])
            st.download_button(
                "📊 Download CSV",
                csv_data.to_csv(index=False),
                file_name=f"influencers_{keyword}.csv",
                mime="text/csv",
                use_container_width=True
            )

        # Store results in session for automation
        st.session_state["results"] = results

    elif not keyword and discover_btn:
        st.warning("⚠️ Please enter a keyword to search.")

    # ── Automation Section ────────────────────────────────
    if st.session_state.get("results"):
        st.markdown("---")
        st.markdown("### 🤖 Automation")
        st.info("💡 Click below to simulate sending outreach to all discovered creators.")

        if st.button("📤 Execute Automated Outreach (Mock)", use_container_width=True):
            with st.spinner("Sending outreach..."):
                result = execute_outreach(st.session_state["results"]["creators"])
            summary = result["summary"]
            st.success(
                f"✅ Outreach Complete! "
                f"📧 {summary['emails_sent']} emails · "
                f"💬 {summary['dms_sent']} DMs · "
                f"❌ {summary['failed']} failed"
            )

    # ── Footer ────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#a0aec0; padding:1rem;'>"
        "Built with ❤️ | Micro-Influencer Discovery System v1.0"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
