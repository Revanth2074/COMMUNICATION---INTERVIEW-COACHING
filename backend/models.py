"""
Pydantic models for the Interview Coaching System.
Defines data schemas for questions, responses, evaluations, and coaching.
"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


# ──────────────────────────────────────────────────────────────
# Candidate Profile
# ──────────────────────────────────────────────────────────────
class CandidateProfile(BaseModel):
    """Candidate information for personalized coaching."""
    name: str = ""
    target_role: str = "Software Engineer"
    experience_years: int = 0
    skills: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    areas_to_improve: list[str] = Field(default_factory=list)
    bio: str = ""


# ──────────────────────────────────────────────────────────────
# Interview Questions
# ──────────────────────────────────────────────────────────────
class InterviewQuestion(BaseModel):
    """A single interview question with metadata."""
    id: str = ""
    question: str
    role: str = "General"
    competency: str = "General"
    difficulty: str = "intermediate"
    question_type: str = "technical"
    expected_competencies: list[str] = Field(default_factory=list)
    follow_up_questions: list[str] = Field(default_factory=list)
    hints: list[str] = Field(default_factory=list)
    reference_answer: Optional[str] = ""
    language: Optional[str] = ""
    source: Optional[str] = "question_bank"


class QuestionRequest(BaseModel):
    """Request to get an interview question."""
    role: str = "Software Engineer"
    competency: str = ""
    difficulty: str = "intermediate"
    question_type: str = ""
    candidate_profile: Optional[CandidateProfile] = None
    source_preference: Optional[str] = "auto"  # "auto", "csv_bank", "ai_generated"


# ──────────────────────────────────────────────────────────────
# Candidate Response & Evaluation
# ──────────────────────────────────────────────────────────────
class CandidateResponse(BaseModel):
    """Candidate's response to an interview question."""
    question_id: str = ""
    question_text: str
    response_text: str
    candidate_profile: Optional[CandidateProfile] = None


class CriterionScore(BaseModel):
    """Score for a single evaluation criterion."""
    criterion: str
    score: float = Field(ge=0, le=10)
    weight: float
    feedback: str


class EvaluationResult(BaseModel):
    """Complete evaluation of a candidate's response."""
    overall_score: float = Field(ge=0, le=10)
    criteria_scores: list[CriterionScore] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    areas_for_improvement: list[str] = Field(default_factory=list)
    improved_response: str = ""
    coaching_tips: list[str] = Field(default_factory=list)
    follow_up_questions: list[str] = Field(default_factory=list)


# ──────────────────────────────────────────────────────────────
# Multi-Agent Specific
# ──────────────────────────────────────────────────────────────
class CommunicationAnalysis(BaseModel):
    """Output from the Communication Analysis Agent."""
    clarity_score: float = Field(ge=0, le=10)
    structure_score: float = Field(ge=0, le=10)
    conciseness_score: float = Field(ge=0, le=10)
    tone_score: float = Field(ge=0, le=10)
    overall_communication_score: float = Field(ge=0, le=10)
    feedback: str = ""
    suggestions: list[str] = Field(default_factory=list)


class ContentAnalysis(BaseModel):
    """Output from the Content Evaluation Agent."""
    relevance_score: float = Field(ge=0, le=10)
    completeness_score: float = Field(ge=0, le=10)
    knowledge_depth_score: float = Field(ge=0, le=10)
    examples_score: float = Field(ge=0, le=10)
    overall_content_score: float = Field(ge=0, le=10)
    feedback: str = ""
    missing_points: list[str] = Field(default_factory=list)


class STARAnalysis(BaseModel):
    """Output from the STAR/Response Structure Agent."""
    has_situation: bool = False
    has_task: bool = False
    has_action: bool = False
    has_result: bool = False
    star_score: float = Field(ge=0, le=10, default=0)
    structure_feedback: str = ""
    restructured_response: str = ""


class CoachingFeedback(BaseModel):
    """Consolidated output from the Interview Coach Agent."""
    overall_score: float = Field(ge=0, le=10)
    communication_analysis: Optional[CommunicationAnalysis] = None
    content_analysis: Optional[ContentAnalysis] = None
    star_analysis: Optional[STARAnalysis] = None
    consolidated_strengths: list[str] = Field(default_factory=list)
    consolidated_improvements: list[str] = Field(default_factory=list)
    improved_response: str = ""
    personalized_tips: list[str] = Field(default_factory=list)
    follow_up_questions: list[str] = Field(default_factory=list)
    improvement_plan: list[str] = Field(default_factory=list)
    recurring_gaps: list[str] = Field(default_factory=list)


# ──────────────────────────────────────────────────────────────
# Session & Progress Tracking
# ──────────────────────────────────────────────────────────────
class PracticeSession(BaseModel):
    """A single practice session record."""
    session_id: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    question: InterviewQuestion
    response_text: str
    coaching_feedback: Optional[CoachingFeedback] = None


class ProgressReport(BaseModel):
    """Aggregate progress report across sessions."""
    total_sessions: int = 0
    average_score: float = 0.0
    score_trend: list[float] = Field(default_factory=list)
    top_strengths: list[str] = Field(default_factory=list)
    persistent_gaps: list[str] = Field(default_factory=list)
    improvement_areas: dict = Field(default_factory=dict)
    recommendations: list[str] = Field(default_factory=list)
