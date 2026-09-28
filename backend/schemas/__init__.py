"""
Schemas Module for Interview Coach
Contains Pydantic schemas for request/response validation
"""

from .candidate import CandidateResponse, CandidatesResponse
from .question import QuestionResponse, QuestionsResponse
from .session import SessionResponse, SessionsResponse
from .response import ResponseResponse, ResponsesResponse
from .feedback import FeedbackResponse, FeedbackDetailResponse
from .progress import ProgressResponse, ProgressSummaryResponse
from .auth import TokenResponse, UserResponse
from .agent import AgentFeedbackResponse, MultiAgentResponse

__all__ = [
    "CandidateResponse", "CandidatesResponse",
    "QuestionResponse", "QuestionsResponse",
    "SessionResponse", "SessionsResponse",
    "ResponseResponse", "ResponsesResponse",
    "FeedbackResponse", "FeedbackDetailResponse",
    "ProgressResponse", "ProgressSummaryResponse",
    "TokenResponse", "UserResponse",
    "AgentFeedbackResponse", "MultiAgentResponse"
]
