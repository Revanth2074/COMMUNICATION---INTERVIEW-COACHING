"""
Progress Model for Interview Coach
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProgressBase(BaseModel):
    """Base progress model"""
    candidate_id: int = Field(..., description="Candidate ID")
    competency: str = Field(..., description="Competency being tracked")
    score: float = Field(..., ge=0, le=100, description="Current score")
    area: str = Field(..., description="Area of assessment (relevance, clarity, structure, etc.)")
    baseline_score: float = Field(default=0.0, ge=0, le=100, description="Baseline score")
    current_score: float = Field(default=0.0, ge=0, le=100, description="Current score")
    improvement_percentage: float = Field(default=0.0, ge=0, description="Improvement percentage")


class ProgressCreate(ProgressBase):
    """Progress create model"""
    session_id: Optional[int] = Field(default=None, description="Associated session ID")


class ProgressUpdate(BaseModel):
    """Progress update model"""
    score: Optional[float] = Field(default=None, ge=0, le=100)
    baseline_score: Optional[float] = Field(default=None, ge=0, le=100)
    current_score: Optional[float] = Field(default=None, ge=0, le=100)
    improvement_percentage: Optional[float] = Field(default=None, ge=0)


class Progress(ProgressBase):
    """Full progress model"""
    id: int = Field(..., description="Progress ID")
    session_id: Optional[int] = Field(default=None, description="Associated session ID")
    last_updated: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "candidate_id": 1,
                "session_id": 1,
                "competency": "Communication",
                "score": 85.5,
                "area": "clarity",
                "baseline_score": 70.0,
                "current_score": 85.5,
                "improvement_percentage": 22.14,
                "last_updated": "2024-01-01T00:00:00"
            }
        }
