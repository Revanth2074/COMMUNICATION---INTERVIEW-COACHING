"""
Progress Schemas for Interview Coach
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from ..models.progress import Progress


class ProgressResponse(BaseModel):
    """Single progress response schema"""
    success: bool
    message: str
    data: Optional[Progress] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Progress retrieved successfully",
                "data": {
                    "id": 1,
                    "candidate_id": 1,
                    "session_id": 1,
                    "score": 85.5,
                    "metrics": {"communication": 90, "content": 85},
                    "created_at": "2024-01-01T00:00:00"
                }
            }
        }


class ProgressSummaryResponse(BaseModel):
    """Progress summary response schema"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Progress summary retrieved successfully",
                "data": {
                    "total_sessions": 10,
                    "average_score": 82.5,
                    "improvement": 15.2,
                    "scores_by_category": {
                        "communication": 85,
                        "content": 80,
                        "star": 88
                    },
                    "trends": [80, 82, 85, 88, 90]
                }
            }
        }
