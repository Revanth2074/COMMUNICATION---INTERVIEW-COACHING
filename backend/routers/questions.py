"""
Question Router for Interview Coach
Handles interview question-related API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from ..models.question import Question, QuestionCreate, QuestionUpdate
from ..schemas.question import QuestionResponse, QuestionsResponse
from ..services.question_service import QuestionService
from ..services.auth_service import AuthService

router = APIRouter(tags=["Questions"])


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    question: QuestionCreate,
    current_user: dict = Depends(AuthService.get_current_user)
) -> QuestionResponse:
    """Create a new interview question"""
    try:
        created_question = await QuestionService.create_question(question)
        
        return QuestionResponse(
            success=True,
            message="Question created successfully",
            data=created_question
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/by-id/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> QuestionResponse:
    """Get a question by ID"""
    try:
        question = await QuestionService.get_question(question_id)
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {question_id} not found"
            )
        
        return QuestionResponse(
            success=True,
            message="Question retrieved successfully",
            data=question
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/list", response_model=QuestionsResponse)
async def get_all_questions(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    role: Optional[str] = Query(default=None),
    competency: Optional[str] = Query(default=None),
    difficulty: Optional[str] = Query(default=None),
    question_type: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    current_user: dict = Depends(AuthService.get_current_user)
) -> QuestionsResponse:
    """Get all questions with optional filtering and pagination"""
    try:
        if role or competency or difficulty or question_type or category:
            questions = await QuestionService.get_questions_by_filters(
                role=role,
                competency=competency,
                difficulty=difficulty,
                question_type=question_type,
                category=category,
                page=page,
                page_size=page_size
            )
        else:
            questions = await QuestionService.get_all_questions(page, page_size)
        
        total = await QuestionService.get_question_count()
        
        return QuestionsResponse(
            success=True,
            message="Questions retrieved successfully",
            data=questions,
            total=total,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/random", response_model=QuestionResponse)
async def get_random_question(
    role: Optional[str] = Query(default=None),
    competency: Optional[str] = Query(default=None),
    difficulty: Optional[str] = Query(default="medium"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> QuestionResponse:
    """Get a random question for practice"""
    try:
        question = await QuestionService.get_random_question(
            role=role,
            competency=competency,
            difficulty=difficulty
        )
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No questions found matching the criteria"
            )
        
        return QuestionResponse(
            success=True,
            message="Random question retrieved successfully",
            data=question
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/roles", response_model=QuestionsResponse)
async def get_questions_by_role(
    role: str = Query(..., description="Target role"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> QuestionsResponse:
    """Get all questions for a specific role"""
    try:
        questions = await QuestionService.get_questions_by_role(role)
        
        return QuestionsResponse(
            success=True,
            message=f"Questions for role '{role}' retrieved successfully",
            data=questions,
            total=len(questions),
            page=1,
            page_size=len(questions)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/stats", response_model=dict)
async def get_question_stats(
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Get statistics about questions"""
    try:
        stats = await QuestionService.get_question_stats()
        
        return {
            "success": True,
            "message": "Question statistics retrieved successfully",
            "data": stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int,
    question: QuestionUpdate,
    current_user: dict = Depends(AuthService.get_current_user)
) -> QuestionResponse:
    """Update a question"""
    try:
        updated_question = await QuestionService.update_question(question_id, question)
        
        if not updated_question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {question_id} not found"
            )
        
        return QuestionResponse(
            success=True,
            message="Question updated successfully",
            data=updated_question
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{question_id}", response_model=QuestionResponse)
async def delete_question(
    question_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> QuestionResponse:
    """Delete a question"""
    try:
        deleted = await QuestionService.delete_question(question_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {question_id} not found"
            )
        
        return QuestionResponse(
            success=True,
            message="Question deleted successfully",
            data=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
