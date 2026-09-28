"""
Improvement Plan Model for Interview Coach
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ImprovementPlanBase(BaseModel):
    """Base improvement plan model"""
    candidate_id: int = Field(..., description="Candidate ID")
    plan_name: str = Field(..., description="Name of the improvement plan")
    description: Optional[str] = Field(default=None, description="Plan description")
    focus_areas: List[str] = Field(default_factory=list, description="Areas to focus on")
    action_items: List[str] = Field(default_factory=list, description="Action items for improvement")
    timeline: str = Field(default="30_days", description="Timeline for improvement")
    status: str = Field(default="active", description="Plan status (active, completed, archived)")


class ImprovementPlanCreate(ImprovementPlanBase):
    """Improvement plan create model"""
    pass


class ImprovementPlanUpdate(BaseModel):
    """Improvement plan update model"""
    plan_name: Optional[str] = Field(default=None, description="Plan name")
    description: Optional[str] = Field(default=None, description="Plan description")
    focus_areas: Optional[List[str]] = Field(default=None, description="Focus areas")
    action_items: Optional[List[str]] = Field(default=None, description="Action items")
    timeline: Optional[str] = Field(default=None, description="Timeline")
    status: Optional[str] = Field(default=None, description="Plan status")


class ImprovementPlan(ImprovementPlanBase):
    """Full improvement plan model"""
    id: int = Field(..., description="Improvement Plan ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "candidate_id": 1,
                "plan_name": "Communication Skills Improvement",
                "description": "Focus on improving clarity and structure in responses",
                "focus_areas": ["Clarity", "Structure", "Conciseness"],
                "action_items": [
                    "Practice STAR method daily",
                    "Record and review responses",
                    "Work on vocabulary expansion"
                ],
                "timeline": "30_days",
                "status": "active",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }
