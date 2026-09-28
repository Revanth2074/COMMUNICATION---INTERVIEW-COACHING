"""
Response Schemas for Interview Coach
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..models.response import Response


class ResponseResponse(BaseModel):
    """Single response response schema"""
    success: bool
    message: str
    data: Optional[Response] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Response retrieved successfully",
                "data": {
                    "id": 1,
                    "session_id": 1,
                    "question_id": 1,
                    "candidate_id": 1,
                    "response_text": "I have 5 years of experience...",
                    "response_type": "text",
                    "submitted_at": "2024-01-01T00:00:00"
                }
            }
        }


class ResponsesResponse(BaseModel):
    """Multiple responses response schema"""
    success: bool
    message: str
    data: List[Response] = []
    total: int = 0
    page: int = 1
    page_size: int = 10
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Responses retrieved successfully",
                "data": [],
                "total": 0,
                "page": 1,
                "page_size": 10
            }
        }
