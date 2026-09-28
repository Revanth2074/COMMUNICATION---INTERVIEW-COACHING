"""
Feedback Router for Interview Coach
Handles feedback-related API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
from ..models.feedback import Feedback, FeedbackCreate, FeedbackUpdate
from ..schemas.feedback import FeedbackResponse, FeedbackDetailResponse
from ..services.feedback_service import FeedbackService
from ..services.auth_service import AuthService
from ..agents.agent_orchestrator import AgentOrchestrator
import json

router = APIRouter(tags=["Feedback"])

# Initialize agent orchestrator
orchestrator = AgentOrchestrator()


@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def create_feedback(
    feedback: FeedbackCreate,
    current_user: dict = Depends(AuthService.get_current_user)
) -> FeedbackResponse:
    """Create new feedback"""
    try:
        created_feedback = await FeedbackService.create_feedback(feedback)
        
        return FeedbackResponse(
            success=True,
            message="Feedback created successfully",
            data=created_feedback
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback(
    feedback_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> FeedbackResponse:
    """Get feedback by ID"""
    try:
        feedback = await FeedbackService.get_feedback(feedback_id)
        
        if not feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Feedback with ID {feedback_id} not found"
            )
        
        return FeedbackResponse(
            success=True,
            message="Feedback retrieved successfully",
            data=feedback
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/response/{response_id}", response_model=FeedbackResponse)
async def get_feedback_by_response(
    response_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> FeedbackResponse:
    """Get feedback for a specific response"""
    try:
        feedback = await FeedbackService.get_feedback_by_response(response_id)
        
        if not feedback:
            return FeedbackResponse(
                success=True,
                message="No feedback found for this response",
                data=None
            )
        
        return FeedbackResponse(
            success=True,
            message="Feedback retrieved successfully",
            data=feedback
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/session/{session_id}", response_model=dict)
async def get_feedback_by_session(
    session_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Get all feedback for a session"""
    try:
        feedbacks = await FeedbackService.get_feedback_by_session(session_id)
        
        return {
            "success": True,
            "message": f"Feedback for session {session_id} retrieved successfully",
            "data": feedbacks,
            "total": len(feedbacks)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/candidate/{candidate_id}", response_model=dict)
async def get_feedback_by_candidate(
    candidate_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Get all feedback for a candidate"""
    try:
        feedbacks = await FeedbackService.get_feedback_by_candidate(candidate_id, page, page_size)
        
        return {
            "success": True,
            "message": f"Feedback for candidate {candidate_id} retrieved successfully",
            "data": feedbacks,
            "total": len(feedbacks),
            "page": page,
            "page_size": page_size
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/candidate/{candidate_id}/average-scores", response_model=dict)
async def get_average_scores(
    candidate_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Get average scores for a candidate"""
    try:
        scores = await FeedbackService.get_average_scores(candidate_id)
        
        return {
            "success": True,
            "message": "Average scores retrieved successfully",
            "data": scores
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/analyze", response_model=FeedbackDetailResponse)
async def analyze_response(
    candidate_id: int = Query(..., description="Candidate ID"),
    question_id: int = Query(..., description="Question ID"),
    response_text: str = Query(..., description="Response text"),
    session_id: Optional[int] = Query(default=None, description="Session ID"),
    response_type: str = Query(default="text", description="Response type (text/voice)"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> FeedbackDetailResponse:
    """
    Analyze a candidate's response using the multi-agent system
    
    This endpoint:
    1. Runs all specialist agents (Communication, Content, STAR)
    2. Consolidates feedback with the Coach Agent
    3. Returns comprehensive analysis and improvement recommendations
    """
    try:
        # Analyze the response using the multi-agent system
        result = await orchestrator.analyze_response(
            candidate_id=candidate_id,
            session_id=session_id,
            question_id=question_id,
            response_text=response_text,
            response_type=response_type
        )
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.error or "Failed to analyze response"
            )
        
        return FeedbackDetailResponse(
            success=True,
            message="Response analyzed successfully using multi-agent system",
            feedback=result.response_analysis,
            agent_analysis=result.agent_results,
            multi_agent_summary={
                "overall_score": result.response_analysis.get("overall_score", 0),
                "performance_summary": result.response_analysis.get("performance_summary", ""),
                "improvement_plan": result.improvement_plan,
                "follow_up_questions": result.follow_up_questions
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/quick-analyze", response_model=FeedbackResponse)
async def quick_analyze_response(
    response_text: str = Query(..., description="Response text"),
    question: str = Query(..., description="The interview question"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> FeedbackResponse:
    """
    Quick analysis of a response without saving to database
    
    This is a lightweight endpoint for quick feedback without persistence.
    """
    try:
        # Create temporary input for analysis
        input_data = {
            "candidate_id": 0,
            "response_text": response_text,
            "question": question,
            "question_type": "general",
            "competency": "general",
            "role": "general",
            "candidate_info": {}
        }
        
        # Run analysis with coach agent
        from ..agents.coach_agent import CoachAgent
        coach = CoachAgent()
        coach_result = await coach.analyze(input_data)
        
        if not coach_result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=coach_result.error or "Failed to analyze response"
            )
        
        # Create a feedback object from the result
        feedback_data = coach_result.data
        
        # Create a simple feedback response
        feedback = Feedback(
            id=0,
            response_id=0,
            session_id=0,
            candidate_id=0,
            question_id=0,
            relevance_score=feedback_data.get("agent_feedback_summary", {}).get("content", {}).get("score", 50.0),
            clarity_score=feedback_data.get("agent_feedback_summary", {}).get("communication", {}).get("score", 50.0),
            structure_score=feedback_data.get("agent_feedback_summary", {}).get("star", {}).get("score", 50.0),
            completeness_score=feedback_data.get("agent_feedback_summary", {}).get("content", {}).get("score", 50.0),
            communication_score=feedback_data.get("agent_feedback_summary", {}).get("communication", {}).get("score", 50.0),
            overall_score=feedback_data.get("overall_score", 50.0),
            strengths=feedback_data.get("agent_feedback_summary", {}).get("communication", {}).get("strengths", []),
            weaknesses=[],
            improvement_suggestions=feedback_data.get("personalized_recommendations", []),
            star_analysis=json.dumps(feedback_data.get("agent_feedback_summary", {}).get("star", {})),
            content_analysis=json.dumps(feedback_data.get("agent_feedback_summary", {}).get("content", {})),
            communication_analysis=json.dumps(feedback_data.get("agent_feedback_summary", {}).get("communication", {})),
            improved_response=feedback_data.get("improved_response_example", ""),
            follow_up_questions=feedback_data.get("follow_up_questions", []),
            agent_feedback=feedback_data,
            created_at=None
        )
        
        return FeedbackResponse(
            success=True,
            message="Quick analysis completed successfully",
            data=feedback
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{feedback_id}", response_model=FeedbackResponse)
async def update_feedback(
    feedback_id: int,
    feedback: FeedbackUpdate,
    current_user: dict = Depends(AuthService.get_current_user)
) -> FeedbackResponse:
    """Update feedback"""
    try:
        updated_feedback = await FeedbackService.update_feedback(feedback_id, feedback)
        
        if not updated_feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Feedback with ID {feedback_id} not found"
            )
        
        return FeedbackResponse(
            success=True,
            message="Feedback updated successfully",
            data=updated_feedback
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{feedback_id}", response_model=FeedbackResponse)
async def delete_feedback(
    feedback_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> FeedbackResponse:
    """Delete feedback"""
    try:
        deleted = await FeedbackService.delete_feedback(feedback_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Feedback with ID {feedback_id} not found"
            )
        
        return FeedbackResponse(
            success=True,
            message="Feedback deleted successfully",
            data=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{feedback_id}/context", response_model=dict)
async def get_feedback_context(
    feedback_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Get feedback with associated response, question, and candidate"""
    try:
        context = await FeedbackService.get_feedback_with_context(feedback_id)
        
        if not context:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Feedback with ID {feedback_id} not found"
            )
        
        return {
            "success": True,
            "message": "Feedback context retrieved successfully",
            "data": context
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
