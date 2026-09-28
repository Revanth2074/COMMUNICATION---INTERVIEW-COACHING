"""
Question Model for Interview Coach
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import json


class QuestionBase(BaseModel):
    """Base question model"""
    question_text: str = Field(..., description="The interview question text")
    role: str = Field(..., description="Target role for this question")
    competency: str = Field(..., description="Competency being assessed")
    difficulty: str = Field(default="medium", description="Question difficulty level")
    question_type: str = Field(..., description="Type of question (behavioral, technical, situational, etc.)")
    expected_competency: str = Field(..., description="Expected competency demonstration")
    evaluation_criteria: List[str] = Field(default_factory=list, description="Evaluation criteria for this question")
    category: str = Field(default="general", description="Question category")
    is_active: bool = Field(default=True, description="Whether the question is active")


class QuestionCreate(QuestionBase):
    """Question create model"""
    pass


class QuestionUpdate(BaseModel):
    """Question update model"""
    question_text: Optional[str] = Field(default=None, description="The interview question text")
    role: Optional[str] = Field(default=None, description="Target role for this question")
    competency: Optional[str] = Field(default=None, description="Competency being assessed")
    difficulty: Optional[str] = Field(default=None, description="Question difficulty level")
    question_type: Optional[str] = Field(default=None, description="Type of question")
    expected_competency: Optional[str] = Field(default=None, description="Expected competency demonstration")
    evaluation_criteria: Optional[List[str]] = Field(default=None, description="Evaluation criteria")
    category: Optional[str] = Field(default=None, description="Question category")
    is_active: Optional[bool] = Field(default=None, description="Whether the question is active")


class Question(QuestionBase):
    """Full question model"""
    id: int = Field(..., description="Question ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
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
