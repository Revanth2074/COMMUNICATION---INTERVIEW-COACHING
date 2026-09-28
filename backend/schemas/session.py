"""
Session Schemas for Interview Coach
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..models.session import Session


class SessionResponse(BaseModel):
    """Single session response schema"""
    success: bool
    message: str
    data: Optional[Session] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Session retrieved successfully",
                "data": {
                    "id": 1,
                    "candidate_id": 1,
                    "question_id": 1,
                    "started_at": "2024-01-01T00:00:00",
                    "completed_at": "2024-01-01T00:05:00",
                    "is_completed": True
                }
            }
        }


class SessionsResponse(BaseModel):
    """Multiple sessions response schema"""
    success: bool
    message: str
    data: List[Session] = []
    total: int = 0
    page: int = 1
    page_size: int = 10
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Sessions retrieved successfully",
                "data": [],
                "total": 0,
                "page": 1,
                "page_size": 10
            }
        }
