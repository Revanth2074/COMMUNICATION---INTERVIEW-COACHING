"""
Agent Analysis Model for Interview Coach
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class AgentAnalysisBase(BaseModel):
    """Base agent analysis model"""
    feedback_id: int = Field(..., description="Feedback ID")
    agent_type: str = Field(..., description="Type of agent (question, communication, content, star, coach)")
    analysis_data: Dict[str, Any] = Field(..., description="Analysis data from the agent")
    confidence_score: float = Field(default=0.0, ge=0, le=100, description="Confidence score of the analysis")


class AgentAnalysisCreate(AgentAnalysisBase):
    """Agent analysis create model"""
    pass


class AgentAnalysis(AgentAnalysisBase):
    """Full agent analysis model"""
    id: int = Field(..., description="Agent Analysis ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "feedback_id": 1,
                "agent_type": "communication",
                "analysis_data": {
                    "clarity_score": 85.0,
                    "structure_score": 80.0,
                    "conciseness_score": 75.0,
                    "suggestions": ["Use shorter sentences", "Improve flow"]
                },
                "confidence_score": 95.0,
                "created_at": "2024-01-01T00:00:00"
            }
        }
