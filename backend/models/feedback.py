"""
Feedback Model for Interview Coach
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import json


class FeedbackBase(BaseModel):
    """Base feedback model"""
    response_id: int = Field(..., description="Response ID")
    session_id: int = Field(..., description="Session ID")
    candidate_id: int = Field(..., description="Candidate ID")
    question_id: int = Field(..., description="Question ID")
    
    # Scores (0-100)
    relevance_score: float = Field(default=0.0, ge=0, le=100, description="Relevance to question score")
    clarity_score: float = Field(default=0.0, ge=0, le=100, description="Clarity score")
    structure_score: float = Field(default=0.0, ge=0, le=100, description="Response structure score")
    completeness_score: float = Field(default=0.0, ge=0, le=100, description="Completeness score")
    communication_score: float = Field(default=0.0, ge=0, le=100, description="Communication quality score")
    overall_score: float = Field(default=0.0, ge=0, le=100, description="Overall score")
    
    # Analysis
    strengths: List[str] = Field(default_factory=list, description="List of strengths")
    weaknesses: List[str] = Field(default_factory=list, description="List of weaknesses")
    improvement_suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    
    # Agent-specific analyses
    star_analysis: Optional[str] = Field(default=None, description="STAR method analysis")
    content_analysis: Optional[str] = Field(default=None, description="Content evaluation analysis")
    communication_analysis: Optional[str] = Field(default=None, description="Communication analysis")
    
    # Additional feedback
    improved_response: Optional[str] = Field(default=None, description="Suggested improved response")
    follow_up_questions: List[str] = Field(default_factory=list, description="Follow-up questions")
    agent_feedback: Dict[str, Any] = Field(default_factory=dict, description="Detailed feedback from each agent")


class FeedbackCreate(FeedbackBase):
    """Feedback create model"""
    pass


class FeedbackUpdate(BaseModel):
    """Feedback update model"""
    relevance_score: Optional[float] = Field(default=None, ge=0, le=100)
    clarity_score: Optional[float] = Field(default=None, ge=0, le=100)
    structure_score: Optional[float] = Field(default=None, ge=0, le=100)
    completeness_score: Optional[float] = Field(default=None, ge=0, le=100)
    communication_score: Optional[float] = Field(default=None, ge=0, le=100)
    overall_score: Optional[float] = Field(default=None, ge=0, le=100)
    strengths: Optional[List[str]] = Field(default=None)
    weaknesses: Optional[List[str]] = Field(default=None)
    improvement_suggestions: Optional[List[str]] = Field(default=None)
    star_analysis: Optional[str] = Field(default=None)
    content_analysis: Optional[str] = Field(default=None)
    communication_analysis: Optional[str] = Field(default=None)
    improved_response: Optional[str] = Field(default=None)
    follow_up_questions: Optional[List[str]] = Field(default=None)
    agent_feedback: Optional[Dict[str, Any]] = Field(default=None)


class Feedback(FeedbackBase):
    """Full feedback model"""
    id: int = Field(..., description="Feedback ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "response_id": 1,
                "session_id": 1,
                "candidate_id": 1,
                "question_id": 1,
                "relevance_score": 85.5,
                "clarity_score": 75.0,
                "structure_score": 80.0,
                "completeness_score": 70.0,
                "communication_score": 85.0,
                "overall_score": 79.1,
                "strengths": ["Clear articulation", "Relevant experience"],
                "weaknesses": ["Could be more concise"],
                "improvement_suggestions": ["Use STAR method for better structure"],
                "star_analysis": "Good situation description, needs better action details",
                "content_analysis": "Response addresses the question well",
                "communication_analysis": "Clear and professional tone",
                "improved_response": "I have 5 years of experience...",
                "follow_up_questions": ["Can you elaborate on your biggest achievement?"],
                "agent_feedback": {},
                "created_at": "2024-01-01T00:00:00"
            }
        }
