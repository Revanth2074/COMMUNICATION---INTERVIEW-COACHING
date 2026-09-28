"""
Agent Schemas for Interview Coach
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class AgentFeedbackResponse(BaseModel):
    """Single agent feedback response schema"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Agent feedback retrieved successfully",
                "data": {
                    "agent_type": "communication",
                    "score": 85,
                    "feedback": "Clear and well-structured response",
                    "suggestions": ["Add more examples"],
                    "strengths": ["Clarity", "Conciseness"],
                    "weaknesses": ["Lacks depth"]
                }
            }
        }


class MultiAgentResponse(BaseModel):
    """Multi-agent analysis response schema"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Multi-agent analysis completed",
                "data": {
                    "overall_score": 85.5,
                    "agent_scores": {
                        "communication": 90,
                        "content": 85,
                        "star": 80,
                        "relevance": 95
                    },
                    "strengths": ["Clear communication", "Well structured"],
                    "weaknesses": ["Needs more specifics"],
                    "suggestions": ["Add metrics to results"],
                    "improved_response": "I led a team of 5 developers...",
                    "follow_up_questions": ["Can you elaborate on the results?"],
                    "improvement_plan": {
                        "focus_areas": ["STAR method", "Technical depth"],
                        "recommended_practice": ["Behavioral questions", "Technical questions"]
                    }
                }
            }
        }
