"""
========================================
🚀 FastAPI Application Entry Point
========================================
Main application for the Micro-Influencer
Discovery & Contextual Outreach System.

Run with:
    uvicorn backend.main:app --reload --port 8000

Then visit:
    http://localhost:8000/docs  (Swagger UI)
    http://localhost:8000/api/health
"""

import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router
from backend.utils import get_logger, configure_logging
from backend.middleware import setup_error_handlers
from config.settings import settings

# ── Configure Logging ─────────────────────────────────────────
configure_logging(
    log_level=settings.LOG_LEVEL,
    log_file=settings.LOG_FILE,
    format_type="detailed"
)
logger = get_logger(__name__)
logger.info(f"🚀 Application startup - Environment: {settings.ENVIRONMENT}")

# ── Create FastAPI App ────────────────────────────────────────
app = FastAPI(
    title="🎯 Micro-Influencer Discovery System",
    description=(
        "Real-Time Automated Micro-Influencer Discovery & "
        "Contextual Outreach System. Discovers Indian micro-influencers, "
        "analyzes content with NLP, scores brand-fit, and generates "
        "personalized outreach — all automated."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ── CORS Middleware (allow Streamlit to connect) ──────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Setup Error Handlers ──────────────────────────────────────
setup_error_handlers(app)
logger.info("✅ Error handling middleware registered")

# ── Register API Routes ──────────────────────────────────────
app.include_router(router)


# ── Root Endpoint ─────────────────────────────────────────────
@app.get("/")
async def root():
    return {
        "message": "🎯 Micro-Influencer Discovery System is running!",
        "status": "operational",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "docs": "Visit /docs for Swagger UI",
        "health": "Visit /api/health for detailed status"
    }


# ── Health Check Endpoint ─────────────────────────────────────
@app.get("/api/health")
async def health_check():
    """
    Health check endpoint for monitoring and deployment verification.
    
    Returns:
        dict: System status including timestamp, environment, and uptime
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0",
        "debug_mode": settings.DEBUG
    }


# ── Startup & Shutdown Events ────────────────────────────────
@app.on_event("startup")
async def startup_event():
    """Log application startup."""
    logger.info("=" * 60)
    logger.info("🚀 APPLICATION STARTUP")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    logger.info(f"Server: {settings.SERVER_HOST}:{settings.SERVER_PORT}")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Log application shutdown."""
    logger.info("=" * 60)
    logger.info("🛑 APPLICATION SHUTDOWN")
    logger.info("=" * 60)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
