"""
Question Schemas for Interview Coach
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..models.question import Question


class QuestionResponse(BaseModel):
    """Single question response schema"""
    success: bool
    message: str
    data: Optional[Question] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Question retrieved successfully",
                "data": {
                    "id": 1,
                    "question_text": "Tell me about yourself.",
                    "role": "Software Engineer",
                    "competency": "Communication",
                    "difficulty": "easy",
                    "question_type": "behavioral",
                    "expected_competency": "Clear and concise self-introduction",
                    "evaluation_criteria": ["Clarity", "Relevance", "Structure"],
                    "category": "general",
                    "is_active": True,
                    "created_at": "2024-01-01T00:00:00"
                }
            }
        }


class QuestionsResponse(BaseModel):
    """Multiple questions response schema"""
    success: bool
    message: str
    data: List[Question] = []
    total: int = 0
    page: int = 1
    page_size: int = 10
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Questions retrieved successfully",
                "data": [],
                "total": 0,
                "page": 1,
                "page_size": 10
            }
        }
