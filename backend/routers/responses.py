"""
Response Router for Interview Coach
Handles candidate response-related API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from typing import List, Optional
from ..models.response import Response, ResponseCreate, ResponseUpdate
from ..schemas.response import ResponseResponse, ResponsesResponse
from ..services.response_service import ResponseService
from ..services.auth_service import AuthService
from ..services.voice_service import VoiceService
import json

router = APIRouter(prefix="/responses", tags=["Responses"])


@router.post("/", response_model=ResponseResponse, status_code=status.HTTP_201_CREATED)
async def create_response(
    response: ResponseCreate,
    current_user: dict = Depends(AuthService.get_current_user)
) -> ResponseResponse:
    """Create a new response"""
    try:
        created_response = await ResponseService.create_response(response)
        
        return ResponseResponse(
            success=True,
            message="Response created successfully",
            data=created_response
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{response_id}", response_model=ResponseResponse)
async def get_response(
    response_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> ResponseResponse:
    """Get a response by ID"""
    try:
        response = await ResponseService.get_response(response_id)
        
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Response with ID {response_id} not found"
            )
        
        return ResponseResponse(
            success=True,
            message="Response retrieved successfully",
            data=response
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=ResponsesResponse)
async def get_all_responses(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    current_user: dict = Depends(AuthService.get_current_user)
) -> ResponsesResponse:
    """Get all responses with pagination"""
    try:
        responses = await ResponseService.get_all_responses(page, page_size)
        total = await ResponseService.get_response_count()
        
        return ResponsesResponse(
            success=True,
            message="Responses retrieved successfully",
            data=responses,
            total=total,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/session/{session_id}", response_model=ResponsesResponse)
async def get_responses_by_session(
    session_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> ResponsesResponse:
    """Get all responses for a specific session"""
    try:
        responses = await ResponseService.get_responses_by_session(session_id)
        
        return ResponsesResponse(
            success=True,
            message=f"Responses for session {session_id} retrieved successfully",
            data=responses,
            total=len(responses),
            page=1,
            page_size=len(responses)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/candidate/{candidate_id}", response_model=ResponsesResponse)
async def get_responses_by_candidate(
    candidate_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    current_user: dict = Depends(AuthService.get_current_user)
) -> ResponsesResponse:
    """Get all responses for a specific candidate"""
    try:
        responses = await ResponseService.get_responses_by_candidate(candidate_id, page, page_size)
        total = await ResponseService.get_response_count_by_candidate(candidate_id)
        
        return ResponsesResponse(
            success=True,
            message=f"Responses for candidate {candidate_id} retrieved successfully",
            data=responses,
            total=total,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/candidate/{candidate_id}/latest", response_model=ResponseResponse)
async def get_latest_response(
    candidate_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> ResponseResponse:
    """Get the latest response for a candidate"""
    try:
        response = await ResponseService.get_latest_response(candidate_id)
        
        if not response:
            return ResponseResponse(
                success=True,
                message="No responses found for candidate",
                data=None
            )
        
        return ResponseResponse(
            success=True,
            message="Latest response retrieved successfully",
            data=response
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/voice", response_model=ResponseResponse, status_code=status.HTTP_201_CREATED)
async def create_voice_response(
    audio_file: UploadFile = File(...),
    session_id: int = Query(..., description="Session ID"),
    candidate_id: int = Query(..., description="Candidate ID"),
    question_id: int = Query(..., description="Question ID"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> ResponseResponse:
    """Create a response from voice input"""
    try:
        # Read and process audio file
        audio_data = await audio_file.read()
        
        # Process voice response (save and transcribe)
        audio_path, transcription = await VoiceService.process_voice_response(audio_data)
        
        # Create response with transcription
        response_data = ResponseCreate(
            session_id=session_id,
            candidate_id=candidate_id,
            question_id=question_id,
            response_text=transcription,
            response_audio_path=audio_path,
            response_type="voice"
        )
        
        created_response = await ResponseService.create_response(response_data)
        
        return ResponseResponse(
            success=True,
            message="Voice response created successfully",
            data=created_response
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{response_id}", response_model=ResponseResponse)
async def update_response(
    response_id: int,
    response: ResponseUpdate,
    current_user: dict = Depends(AuthService.get_current_user)
) -> ResponseResponse:
    """Update a response"""
    try:
        updated_response = await ResponseService.update_response(response_id, response)
        
        if not updated_response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Response with ID {response_id} not found"
            )
        
        return ResponseResponse(
            success=True,
            message="Response updated successfully",
            data=updated_response
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{response_id}", response_model=ResponseResponse)
async def delete_response(
    response_id: int,
    current_user: dict = Depends(AuthService.get_current_user)
) -> ResponseResponse:
    """Delete a response"""
    try:
        deleted = await ResponseService.delete_response(response_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Response with ID {response_id} not found"
            )
        
        return ResponseResponse(
            success=True,
            message="Response deleted successfully",
            data=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
