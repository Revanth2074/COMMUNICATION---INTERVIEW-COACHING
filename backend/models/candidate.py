"""
Candidate Model for Interview Coach
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import json


class CandidateBase(BaseModel):
    """Base candidate model"""
    name: str = Field(..., description="Candidate's full name")
    email: str = Field(..., description="Candidate's email address")
    target_role: str = Field(..., description="Target job role")
    experience_years: int = Field(default=0, ge=0, le=50, description="Years of experience")
    skills: List[str] = Field(default_factory=list, description="List of skills")
    competencies: List[str] = Field(default_factory=list, description="List of competencies")
    resume_text: Optional[str] = Field(default=None, description="Resume text for analysis")


class CandidateCreate(CandidateBase):
    """Candidate create model"""
    user_id: str = Field(..., description="User ID for authentication")


class CandidateUpdate(BaseModel):
    """Candidate update model"""
    name: Optional[str] = Field(default=None, description="Candidate's full name")
    email: Optional[str] = Field(default=None, description="Candidate's email address")
    target_role: Optional[str] = Field(default=None, description="Target job role")
    experience_years: Optional[int] = Field(default=None, ge=0, le=50, description="Years of experience")
    skills: Optional[List[str]] = Field(default=None, description="List of skills")
    competencies: Optional[List[str]] = Field(default=None, description="List of competencies")
    resume_text: Optional[str] = Field(default=None, description="Resume text for analysis")


class Candidate(CandidateBase):
    """Full candidate model"""
    id: int = Field(..., description="Candidate ID")
    user_id: str = Field(..., description="User ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "user_123",
                "name": "John Doe",
                "email": "john@example.com",
                "target_role": "Software Engineer",
                "experience_years": 5,
                "skills": ["Python", "FastAPI", "React"],
                "competencies": ["Problem Solving", "Communication"],
                "resume_text": "Experienced software engineer...",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }
