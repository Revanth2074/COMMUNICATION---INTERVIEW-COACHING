"""
Interview Coach Backend - FastAPI Application
Main entry point for the Interview Coaching System
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import routers
from .routers import (
    questions,
    candidates,
    sessions,
    feedback,
    agents,
    progress,
    auth,
    voice
)

# Lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Interview Coach Backend...")
    
    # Initialize database
    from .database import init_db
    await init_db()
    
    logger.info("Backend started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Interview Coach Backend...")
    logger.info("Backend shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="Interview Coach API",
    description="AI-powered Communication & Interview Coaching System",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth")
app.include_router(candidates.router, prefix="/api/candidates")
app.include_router(questions.router, prefix="/api/questions")
app.include_router(sessions.router, prefix="/api/sessions")
app.include_router(feedback.router, prefix="/api/feedback")
app.include_router(agents.router, prefix="/api/agents")
app.include_router(progress.router, prefix="/api/progress")
app.include_router(voice.router, prefix="/api/voice")

# Root endpoint
@app.get("/api/", tags=["Health"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Interview Coach API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "OK"
    }

# Health check endpoint
@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Interview Coach Backend is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
