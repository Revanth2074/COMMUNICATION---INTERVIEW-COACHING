"""
Feedback Schemas for Interview Coach
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from ..models.feedback import Feedback


class FeedbackResponse(BaseModel):
    """Single feedback response schema"""
    success: bool
    message: str
    data: Optional[Feedback] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Feedback retrieved successfully",
                "data": {
                    "id": 1,
                    "response_id": 1,
                    "overall_score": 85.5,
                    "feedback_text": "Good response with clear structure...",
                    "suggestions": ["Add more details about results"],
                    "agent_feedback": {},
                    "created_at": "2024-01-01T00:00:00"
                }
            }
        }


class FeedbackDetailResponse(BaseModel):
    """Detailed feedback response schema"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Detailed feedback retrieved successfully",
                "data": {
                    "overall_score": 85.5,
                    "scores": {
                        "communication": 90,
                        "content": 85,
                        "star": 80,
                        "relevance": 95
                    },
                    "strengths": ["Clear communication", "Well structured"],
                    "weaknesses": ["Needs more specifics"],
                    "suggestions": ["Add metrics to results"],
                    "improved_response": "I led a team of 5 developers..."
                }
            }
        }


class FeedbackListResponse(BaseModel):
    """Multiple feedback response schema"""
    success: bool
    message: str
    data: List[Feedback] = []
    total: int = 0
    page: int = 1
    page_size: int = 10
