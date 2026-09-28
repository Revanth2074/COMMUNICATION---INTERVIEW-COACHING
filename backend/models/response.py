"""
Response Model for Interview Coach
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ResponseBase(BaseModel):
    """Base response model"""
    session_id: int = Field(..., description="Session ID")
    candidate_id: int = Field(..., description="Candidate ID")
    question_id: int = Field(..., description="Question ID")
    response_text: Optional[str] = Field(default=None, description="Text response from candidate")
    response_audio_path: Optional[str] = Field(default=None, description="Path to audio file if voice response")
    response_type: str = Field(default="text", description="Type of response (text, voice)")


class ResponseCreate(ResponseBase):
    """Response create model"""
    pass


class ResponseUpdate(BaseModel):
    """Response update model"""
    response_text: Optional[str] = Field(default=None, description="Text response")
    response_audio_path: Optional[str] = Field(default=None, description="Audio file path")
    response_type: Optional[str] = Field(default=None, description="Response type")


class Response(ResponseBase):
    """Full response model"""
    id: int = Field(..., description="Response ID")
    submitted_at: datetime = Field(..., description="Submission timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "session_id": 1,
                "candidate_id": 1,
                "question_id": 1,
                "response_text": "I have 5 years of experience in software development...",
                "response_audio_path": None,
                "response_type": "text",
                "submitted_at": "2024-01-01T00:00:00"
            }
        }
