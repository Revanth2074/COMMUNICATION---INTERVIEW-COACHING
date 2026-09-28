"""
Session Model for Interview Coach
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SessionBase(BaseModel):
    """Base session model"""
    candidate_id: int = Field(..., description="Candidate ID")
    question_id: int = Field(..., description="Question ID")
    session_type: str = Field(default="practice", description="Type of session (practice, mock, evaluation)")
    status: str = Field(default="in_progress", description="Session status")


class SessionCreate(SessionBase):
    """Session create model"""
    pass


class SessionUpdate(BaseModel):
    """Session update model"""
    session_type: Optional[str] = Field(default=None, description="Type of session")
    status: Optional[str] = Field(default=None, description="Session status")
    completed_at: Optional[datetime] = Field(default=None, description="Completion timestamp")


class Session(SessionBase):
    """Full session model"""
    id: int = Field(..., description="Session ID")
    started_at: datetime = Field(..., description="Start timestamp")
    completed_at: Optional[datetime] = Field(default=None, description="Completion timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "candidate_id": 1,
                "question_id": 1,
                "session_type": "practice",
                "status": "in_progress",
                "started_at": "2024-01-01T00:00:00",
                "completed_at": None
            }
        }
