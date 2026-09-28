"""
Candidate Schemas for Interview Coach
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..models.candidate import Candidate


class CandidateResponse(BaseModel):
    """Single candidate response schema"""
    success: bool
    message: str
    data: Optional[Candidate] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Candidate retrieved successfully",
                "data": {
                    "id": 1,
                    "user_id": "user_123",
                    "name": "John Doe",
                    "email": "john@example.com",
                    "target_role": "Software Engineer",
                    "experience_years": 5,
                    "skills": ["Python", "FastAPI", "React"],
                    "competencies": ["Problem Solving", "Communication"],
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                }
            }
        }


class CandidatesResponse(BaseModel):
    """Multiple candidates response schema"""
    success: bool
    message: str
    data: List[Candidate] = []
    total: int = 0
    page: int = 1
    page_size: int = 10
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Candidates retrieved successfully",
                "data": [],
                "total": 0,
                "page": 1,
                "page_size": 10
            }
        }
