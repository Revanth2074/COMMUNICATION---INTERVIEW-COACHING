"""
Agents Router for Interview Coach
Handles multi-agent system endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
from ..services.auth_service import AuthService
from ..agents.agent_orchestrator import AgentOrchestrator, OrchestrationResult
from ..agents.base_agent import AgentResult

router = APIRouter(tags=["Agents"])

# Initialize agent orchestrator
orchestrator = AgentOrchestrator()


@router.get("/status", response_model=dict)
async def get_agent_status(
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Get the status of all agents"""
    try:
        status = await orchestrator.get_agent_status()
        return {
            "success": True,
            "message": "Agent status retrieved successfully",
            "data": status
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/initialize", response_model=dict)
async def initialize_agents(
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Initialize all agents"""
    try:
        initialized = await orchestrator.initialize()
        
        return {
            "success": initialized,
            "message": "Agents initialized successfully" if initialized else "Failed to initialize some agents",
            "data": {"all_initialized": initialized}
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/practice/start", response_model=dict)
async def start_practice_session(
    candidate_id: int = Query(..., description="Candidate ID"),
    target_role: Optional[str] = Query(default=None, description="Target role"),
    competency: Optional[str] = Query(default=None, description="Competency"),
    difficulty: str = Query(default="medium", description="Difficulty level"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """
    Start a new practice session and get a question
    
    This endpoint:
    1. Selects an appropriate question based on candidate profile
    2. Creates a new session
    3. Returns the question for the candidate to answer
    """
    try:
        result = await orchestrator.start_practice_session(
            candidate_id=candidate_id,
            target_role=target_role,
            competency=competency,
            difficulty=difficulty
        )
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.error or "Failed to start practice session"
            )
        
        return {
            "success": True,
            "message": "Practice session started successfully",
            "data": {
                "question": result.question,
                "session": result.metadata
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/practice/analyze", response_model=dict)
async def analyze_practice_response(
    candidate_id: int = Query(..., description="Candidate ID"),
    question_id: int = Query(..., description="Question ID"),
    response_text: str = Query(..., description="Response text"),
    session_id: Optional[int] = Query(default=None, description="Session ID"),
    response_type: str = Query(default="text", description="Response type"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """
    Analyze a practice response using the multi-agent system
    
    This is the main endpoint for getting comprehensive feedback on a response.
    It runs all specialist agents and consolidates the feedback.
    """
    try:
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
        
        return {
            "success": True,
            "message": "Response analyzed successfully with multi-agent system",
            "data": {
                "question": result.question,
                "feedback": result.feedback,
                "response_analysis": result.response_analysis,
                "agent_results": result.agent_results,
                "improvement_plan": result.improvement_plan,
                "follow_up_questions": result.follow_up_questions,
                "metadata": result.metadata
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/follow-up", response_model=dict)
async def get_follow_up_question(
    candidate_id: int = Query(..., description="Candidate ID"),
    previous_question_id: int = Query(..., description="Previous Question ID"),
    previous_response: str = Query(..., description="Previous response text"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """
    Get a follow-up question based on previous response
    
    This endpoint generates a follow-up question to dig deeper into the candidate's
    experience or knowledge based on their previous answer.
    """
    try:
        result = await orchestrator.get_follow_up_question(
            candidate_id=candidate_id,
            previous_question_id=previous_question_id,
            previous_response=previous_response
        )
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.error or "Failed to generate follow-up question"
            )
        
        return {
            "success": True,
            "message": "Follow-up question generated successfully",
            "data": {
                "question": result.question,
                "metadata": result.metadata
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/improvement-plan", response_model=dict)
async def generate_improvement_plan(
    candidate_id: int = Query(..., description="Candidate ID"),
    num_sessions: int = Query(default=5, description="Number of recent sessions to analyze"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """
    Generate a comprehensive improvement plan based on multiple sessions
    
    This endpoint:
    1. Analyzes multiple practice sessions
    2. Identifies patterns in strengths and weaknesses
    3. Generates a personalized improvement plan
    """
    try:
        result = await orchestrator.generate_improvement_plan(
            candidate_id=candidate_id,
            num_sessions=num_sessions
        )
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.error or "Failed to generate improvement plan"
            )
        
        return {
            "success": True,
            "message": "Improvement plan generated successfully",
            "data": result.improvement_plan,
            "metadata": result.metadata
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/communication/analyze", response_model=dict)
async def analyze_communication(
    response_text: str = Query(..., description="Response text"),
    question: str = Query(..., description="The interview question"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Analyze communication quality of a response"""
    try:
        from ..agents.communication_agent import CommunicationAgent
        agent = CommunicationAgent()
        
        input_data = {
            "response_text": response_text,
            "question": question
        }
        
        result = await agent.analyze(input_data)
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.error or "Failed to analyze communication"
            )
        
        return {
            "success": True,
            "message": "Communication analysis completed",
            "data": result.data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/content/analyze", response_model=dict)
async def analyze_content(
    response_text: str = Query(..., description="Response text"),
    question: str = Query(..., description="The interview question"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Analyze content quality of a response"""
    try:
        from ..agents.content_agent import ContentAgent
        agent = ContentAgent()
        
        input_data = {
            "response_text": response_text,
            "question": question
        }
        
        result = await agent.analyze(input_data)
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.error or "Failed to analyze content"
            )
        
        return {
            "success": True,
            "message": "Content analysis completed",
            "data": result.data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/star/analyze", response_model=dict)
async def analyze_star(
    response_text: str = Query(..., description="Response text"),
    question: str = Query(..., description="The interview question"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Analyze STAR compliance of a response"""
    try:
        from ..agents.star_agent import STARAgent
        agent = STARAgent()
        
        input_data = {
            "response_text": response_text,
            "question": question
        }
        
        result = await agent.analyze(input_data)
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.error or "Failed to analyze STAR compliance"
            )
        
        return {
            "success": True,
            "message": "STAR analysis completed",
            "data": result.data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/star/example", response_model=dict)
async def generate_star_example(
    question: str = Query(..., description="The interview question"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Generate an example STAR response for a question"""
    try:
        from ..agents.star_agent import STARAgent
        agent = STARAgent()
        
        result = await agent.generate_star_example(question)
        
        return {
            "success": True,
            "message": "STAR example generated",
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
