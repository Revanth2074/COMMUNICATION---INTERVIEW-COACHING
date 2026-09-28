"""
Candidate Router for Interview Coach
Handles candidate-related API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from ..models.candidate import Candidate, CandidateCreate, CandidateUpdate
from ..schemas.candidate import CandidateResponse, CandidatesResponse
from ..services.candidate_service import CandidateService
from ..services.auth_service import AuthService
from ..config import settings

router = APIRouter(tags=["Candidates"])


@router.post("/", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
async def create_candidate(
    candidate: CandidateCreate,
    current_user: dict = Depends(AuthService.get_current_user)
) -> CandidateResponse:
    """Create a new candidate"""
    try:
        # Use user_id from authenticated user if not provided
        if not candidate.user_id and current_user:
            candidate.user_id = str(current_user.get("id", ""))
        
        created_candidate = await CandidateService.create_candidate(candidate)
        
        return CandidateResponse(
            success=True,
            message="Candidate created successfully",
            data=created_candidate
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> CandidateResponse:
    """Get a candidate by ID"""
    try:
        candidate = await CandidateService.get_candidate(candidate_id)
        
        if not candidate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Candidate with ID {candidate_id} not found"
            )
        
        return CandidateResponse(
            success=True,
            message="Candidate retrieved successfully",
            data=candidate
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=CandidatesResponse)
async def get_all_candidates(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    current_user: dict = Depends(AuthService.get_current_user)
) -> CandidatesResponse:
    """Get all candidates with pagination"""
    try:
        candidates = await CandidateService.get_all_candidates(page, page_size)
        total = await CandidateService.get_candidate_count()
        
        return CandidatesResponse(
            success=True,
            message="Candidates retrieved successfully",
            data=candidates,
            total=total,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me", response_model=CandidateResponse)
async def get_current_candidate(
    current_user: dict = Depends(AuthService.get_current_user)
) -> CandidateResponse:
    """Get the current user's candidate profile"""
    try:
        user_id = str(current_user.get("id", ""))
        candidate = await CandidateService.get_candidate_by_user_id(user_id)
        
        if not candidate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No candidate profile found for current user"
            )
        
        return CandidateResponse(
            success=True,
            message="Current candidate profile retrieved successfully",
            data=candidate
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(
    candidate_id: int,
    candidate: CandidateUpdate,
    current_user: dict = Depends(AuthService.get_current_user)
) -> CandidateResponse:
    """Update a candidate"""
    try:
        updated_candidate = await CandidateService.update_candidate(candidate_id, candidate)
        
        if not updated_candidate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Candidate with ID {candidate_id} not found"
            )
        
        return CandidateResponse(
            success=True,
            message="Candidate updated successfully",
            data=updated_candidate
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{candidate_id}", response_model=CandidateResponse)
async def delete_candidate(
    candidate_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> CandidateResponse:
    """Delete a candidate"""
    try:
        deleted = await CandidateService.delete_candidate(candidate_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Candidate with ID {candidate_id} not found"
            )
        
        return CandidateResponse(
            success=True,
            message="Candidate deleted successfully",
            data=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
