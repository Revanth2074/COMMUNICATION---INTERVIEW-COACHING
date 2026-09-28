"""
Voice Router for Interview Coach
Handles voice response endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from typing import Optional, Dict, Any
from ..services.voice_service import VoiceService
from ..services.auth_service import AuthService

router = APIRouter(tags=["Voice"])


@router.post("/transcribe", response_model=dict)
async def transcribe_audio(
    audio_file: UploadFile = File(..., description="Audio file to transcribe"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """
    Transcribe an audio file to text
    
    This endpoint accepts an audio file and returns the transcribed text.
    """
    try:
        # Read audio data
        audio_data = await audio_file.read()
        
        # Save and transcribe
        audio_path, transcription = await VoiceService.process_voice_response(audio_data)
        
        return {
            "success": True,
            "message": "Audio transcribed successfully",
            "data": {
                "transcription": transcription,
                "audio_path": audio_path,
                "filename": audio_file.filename
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/upload", response_model=dict)
async def upload_audio(
    audio_file: UploadFile = File(..., description="Audio file to upload"),
    session_id: int = Query(..., description="Session ID"),
    candidate_id: int = Query(..., description="Candidate ID"),
    question_id: int = Query(..., description="Question ID"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """
    Upload an audio response and create a response record
    
    This endpoint:
    1. Saves the audio file
    2. Transcribes it to text
    3. Creates a response record in the database
    """
    try:
        # Read audio data
        audio_data = await audio_file.read()
        
        # Process voice response
        audio_path, transcription = await VoiceService.process_voice_response(audio_data)
        
        # Create response in database
        from ..models.response import ResponseCreate
        from ..services.response_service import ResponseService
        
        response_data = ResponseCreate(
            session_id=session_id,
            candidate_id=candidate_id,
            question_id=question_id,
            response_text=transcription,
            response_audio_path=audio_path,
            response_type="voice"
        )
        
        response = await ResponseService.create_response(response_data)
        
        return {
            "success": True,
            "message": "Voice response uploaded and transcribed successfully",
            "data": {
                "response_id": response.id,
                "transcription": transcription,
                "audio_path": audio_path,
                "filename": audio_file.filename,
                "session_id": session_id,
                "candidate_id": candidate_id,
                "question_id": question_id
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/duration/{audio_path:path}", response_model=dict)
async def get_audio_duration(
    audio_path: str,
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """Get the duration of an audio file"""
    try:
        duration = await VoiceService.get_audio_duration(audio_path)
        
        return {
            "success": True,
            "message": "Audio duration retrieved successfully",
            "data": {
                "path": audio_path,
                "duration_seconds": duration
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/convert", response_model=dict)
async def convert_audio_format(
    audio_file: UploadFile = File(..., description="Audio file to convert"),
    output_format: str = Query(default="wav", description="Output format (wav, mp3, etc.)"),
    current_user: dict = Depends(AuthService.get_current_user)
) -> dict:
    """
    Convert an audio file to a different format
    
    This endpoint converts the uploaded audio file to the specified format.
    """
    try:
        # Save the uploaded file temporarily
        import tempfile
        import os
        
        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_file.filename.split('.')[-1]}") as tmp_file:
            tmp_path = tmp_file.name
            tmp_file.write(await audio_file.read())
        
        try:
            # Convert the file
            converted_path = await VoiceService.convert_audio_format(tmp_path, output_format)
            
            # Read the converted file
            with open(converted_path, "rb") as f:
                converted_data = f.read()
            
            # Clean up temp files
            os.unlink(tmp_path)
            os.unlink(converted_path)
            
            return {
                "success": True,
                "message": "Audio converted successfully",
                "data": {
                    "original_filename": audio_file.filename,
                    "converted_format": output_format,
                    "converted_data": converted_data
                }
            }
        except Exception as e:
            # Clean up temp file if it exists
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
