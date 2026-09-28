"""
Session Router for Interview Coach
Handles interview session-related API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from ..models.session import Session, SessionCreate, SessionUpdate
from ..schemas.session import SessionResponse, SessionsResponse
from ..services.session_service import SessionService
from ..services.auth_service import AuthService

router = APIRouter(tags=["Sessions"])


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session: SessionCreate,
    current_user: dict = Depends(AuthService.get_current_user)
) -> SessionResponse:
    """Create a new interview session"""
    try:
        created_session = await SessionService.create_session(session)
        
        return SessionResponse(
            success=True,
            message="Session created successfully",
            data=created_session
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> SessionResponse:
    """Get a session by ID"""
    try:
        session = await SessionService.get_session(session_id)
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with ID {session_id} not found"
            )
        
        return SessionResponse(
            success=True,
            message="Session retrieved successfully",
            data=session
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=SessionsResponse)
async def get_all_sessions(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    current_user: dict = Depends(AuthService.get_current_user)
) -> SessionsResponse:
    """Get all sessions with pagination"""
    try:
        sessions = await SessionService.get_all_sessions(page, page_size)
        total = await SessionService.get_session_count()
        
        return SessionsResponse(
            success=True,
            message="Sessions retrieved successfully",
            data=sessions,
            total=total,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/candidate/{candidate_id}", response_model=SessionsResponse)
async def get_sessions_by_candidate(
    candidate_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    current_user: dict = Depends(AuthService.get_current_user)
) -> SessionsResponse:
    """Get all sessions for a specific candidate"""
    try:
        sessions = await SessionService.get_sessions_by_candidate(candidate_id, page, page_size)
        total = await SessionService.get_session_count_by_candidate(candidate_id)
        
        return SessionsResponse(
            success=True,
            message=f"Sessions for candidate {candidate_id} retrieved successfully",
            data=sessions,
            total=total,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{session_id}/details", response_model=SessionResponse)
async def get_session_details(
    session_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> SessionResponse:
    """Get a session with candidate and question details"""
    try:
        session_details = await SessionService.get_session_with_details(session_id)
        
        if not session_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with ID {session_id} not found"
            )
        
        return SessionResponse(
            success=True,
            message="Session details retrieved successfully",
            data=session_details
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/active/{candidate_id}", response_model=SessionResponse)
async def get_active_session(
    candidate_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> SessionResponse:
    """Get the current active session for a candidate"""
    try:
        session = await SessionService.get_active_session(candidate_id)
        
        if not session:
            return SessionResponse(
                success=True,
                message="No active session found",
                data=None
            )
        
        return SessionResponse(
            success=True,
            message="Active session retrieved successfully",
            data=session
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: int,
    session: SessionUpdate,
    current_user: dict = Depends(AuthService.get_current_user)
) -> SessionResponse:
    """Update a session"""
    try:
        updated_session = await SessionService.update_session(session_id, session)
        
        if not updated_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with ID {session_id} not found"
            )
        
        return SessionResponse(
            success=True,
            message="Session updated successfully",
            data=updated_session
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{session_id}/complete", response_model=SessionResponse)
async def complete_session(
    session_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> SessionResponse:
    """Mark a session as completed"""
    try:
        completed_session = await SessionService.complete_session(session_id)
        
        if not completed_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with ID {session_id} not found"
            )
        
        return SessionResponse(
            success=True,
            message="Session marked as completed successfully",
            data=completed_session
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{session_id}", response_model=SessionResponse)
async def delete_session(
    session_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> SessionResponse:
    """Delete a session"""
    try:
        deleted = await SessionService.delete_session(session_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with ID {session_id} not found"
            )
        
        return SessionResponse(
            success=True,
            message="Session deleted successfully",
            data=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
