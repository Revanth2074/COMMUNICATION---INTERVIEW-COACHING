"""
AI-Powered Communication & Interview Coaching System
Configuration module for OmniRoute API integration.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    OMNIROUTE_API_KEY: str = os.getenv("OMNIROUTE_API_KEY", "")
    OMNIROUTE_BASE_URL: str = os.getenv("OMNIROUTE_BASE_URL", "http://localhost:20128/v1")
    PREFERRED_MODEL: str = os.getenv("PREFERRED_MODEL", "")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Evaluation criteria weights
    EVALUATION_CRITERIA = {
        "relevance": {"weight": 0.20, "description": "How well the response addresses the question"},
        "clarity": {"weight": 0.15, "description": "How clear and easy to understand the response is"},
        "structure": {"weight": 0.15, "description": "How well-organized and logically structured the response is"},
        "completeness": {"weight": 0.20, "description": "How thoroughly the response covers all aspects of the question"},
        "communication_quality": {"weight": 0.15, "description": "Professional tone, confidence, and delivery quality"},
        "examples_evidence": {"weight": 0.15, "description": "Use of specific examples, metrics, or evidence"},
    }

    # Question categories
    QUESTION_TYPES = [
        "behavioral",
        "technical",
        "situational",
        "competency",
        "motivational",
        "case_study",
    ]

    DIFFICULTY_LEVELS = ["entry", "intermediate", "advanced", "expert"]

    ROLES = [
        "Software Engineer",
        "Java Developer",
        "PHP Developer",
        "Magento Developer",
        "Backend Developer",
        "Full Stack Developer",
        "Data Scientist",
        "Product Manager",
        "Business Analyst",
        "DevOps Engineer",
        "Marketing Manager",
        "HR Manager",
        "Finance Analyst",
        "Consultant",
        "UX Designer",
        "Project Manager",
    ]


settings = Settings()
