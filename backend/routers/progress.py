"""
Progress Router for Interview Coach
Handles progress tracking and improvement analysis endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
from ..models.progress import Progress, ProgressCreate
from ..services.progress_service import ProgressService
from ..services.auth_service import AuthService

router = APIRouter(tags=["Progress"])


@router.post("/", response_model=dict)
async def create_progress(
    progress: ProgressCreate,
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Create a new progress entry"""
    try:
        created_progress = await ProgressService.create_progress(progress)
        
        return {
            "success": True,
            "message": "Progress entry created successfully",
            "data": created_progress
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{progress_id}", response_model=dict)
async def get_progress(
    progress_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Get progress by ID"""
    try:
        progress = await ProgressService.get_progress(progress_id)
        
        if not progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Progress with ID {progress_id} not found"
            )
        
        return {
            "success": True,
            "message": "Progress retrieved successfully",
            "data": progress
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/candidate/{candidate_id}", response_model=dict)
async def get_progress_by_candidate(
    candidate_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Get all progress entries for a candidate"""
    try:
        progresses = await ProgressService.get_progress_by_candidate(candidate_id, page, page_size)
        
        return {
            "success": True,
            "message": f"Progress for candidate {candidate_id} retrieved successfully",
            "data": progresses,
            "total": len(progresses),
            "page": page,
            "page_size": page_size
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/candidate/{candidate_id}/summary", response_model=dict)
async def get_progress_summary(
    candidate_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Get comprehensive progress summary for a candidate"""
    try:
        summary = await ProgressService.get_progress_summary(candidate_id)
        
        return {
            "success": True,
            "message": "Progress summary retrieved successfully",
            "data": summary
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/candidate/{candidate_id}/competency/{competency}", response_model=dict)
async def get_progress_by_competency(
    candidate_id: int,
    competency: str,
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Get progress for a specific competency"""
    try:
        progresses = await ProgressService.get_progress_by_competency(candidate_id, competency)
        
        return {
            "success": True,
            "message": f"Progress for competency '{competency}' retrieved successfully",
            "data": progresses,
            "total": len(progresses)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/candidate/{candidate_id}/improvement-areas", response_model=dict)
async def get_improvement_areas(
    candidate_id: int,
    threshold: float = Query(default=70.0, description="Score threshold for improvement areas"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Identify areas that need improvement for a candidate"""
    try:
        areas = await ProgressService.get_improvement_areas(candidate_id, threshold)
        
        return {
            "success": True,
            "message": "Improvement areas identified successfully",
            "data": areas,
            "threshold": threshold
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/candidate/{candidate_id}/competency/{competency}/area/{area}", response_model=dict)
async def get_latest_progress(
    candidate_id: int,
    competency: str,
    area: str,
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Get the latest progress for a specific competency and area"""
    try:
        progress = await ProgressService.get_latest_progress(candidate_id, competency, area)
        
        if not progress:
            return {
                "success": True,
                "message": "No progress found for the specified criteria",
                "data": None
            }
        
        return {
            "success": True,
            "message": "Latest progress retrieved successfully",
            "data": progress
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{progress_id}/update", response_model=dict)
async def update_progress_scores(
    progress_id: int,
    current_score: float = Query(..., description="New current score"),
    improvement_percentage: float = Query(..., description="Improvement percentage"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Update progress with new scores"""
    try:
        updated_progress = await ProgressService.update_progress(
            progress_id, current_score, improvement_percentage
        )
        
        if not updated_progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Progress with ID {progress_id} not found"
            )
        
        return {
            "success": True,
            "message": "Progress updated successfully",
            "data": updated_progress
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
