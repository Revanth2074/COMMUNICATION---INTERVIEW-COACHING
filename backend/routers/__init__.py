"""
Routers Module for Interview Coach
"""

from .candidates import router as candidates_router
from .questions import router as questions_router
from .sessions import router as sessions_router
from .responses import router as responses_router
from .feedback import router as feedback_router
from .agents import router as agents_router
from .progress import router as progress_router
from .auth import router as auth_router
from .voice import router as voice_router

__all__ = [
    "candidates_router",
    "questions_router",
    "sessions_router",
    "responses_router",
    "feedback_router",
    "agents_router",
    "progress_router",
    "auth_router",
    "voice_router"
]
