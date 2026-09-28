"""
Voice Service for Interview Coach
Handles voice response processing and transcription
"""

import logging
from typing import Optional, Tuple, BinaryIO
from pathlib import Path
import os
import tempfile
import subprocess
from datetime import datetime
import uuid
from ..config import settings

logger = logging.getLogger(__name__)


class VoiceService:
    """Service for handling voice responses"""
    
    @staticmethod
    async def ensure_upload_dir():
        """Ensure upload directory exists"""
        upload_dir = Path(settings.upload_dir)
        audio_dir = Path(settings.audio_upload_dir)
        
        upload_dir.mkdir(parents=True, exist_ok=True)
        audio_dir.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    async def save_audio_file(audio_data: bytes, filename: Optional[str] = None) -> Tuple[str, str]:
        """Save audio file to disk and return path and filename"""
        try:
            await VoiceService.ensure_upload_dir()
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                unique_id = str(uuid.uuid4())[:8]
                filename = f"audio_{timestamp}_{unique_id}.wav"
            
            filepath = Path(settings.audio_upload_dir) / filename
            
            # Ensure directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Save the file
            with open(filepath, "wb") as f:
                f.write(audio_data)
            
            logger.info(f"Audio file saved: {filepath}")
            return str(filepath), filename
            
        except Exception as e:
            logger.error(f"Error saving audio file: {e}")
            raise
    
    @staticmethod
    async def transcribe_audio(audio_path: str) -> str:
        """Transcribe audio file to text using FFmpeg and speech-to-text"""
        try:
            # Check if FFmpeg is available
            try:
                subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                raise ValueError("FFmpeg is not installed. Please install FFmpeg for audio processing.")
            
            # For now, we'll return a placeholder
            # In a real implementation, you would integrate with a speech-to-text API
            # like Whisper, Google Speech-to-Text, or Azure Speech Services
            
            logger.info(f"Audio transcription requested for: {audio_path}")
            
            # Placeholder: return the audio path as text (for demo purposes)
            return f"[Audio transcription from {os.path.basename(audio_path)}]"
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            raise
    
    @staticmethod
    async def process_voice_response(audio_data: bytes) -> Tuple[str, str]:
        """Process voice response: save and transcribe"""
        try:
            # Save audio file
            audio_path, filename = await VoiceService.save_audio_file(audio_data)
            
            # Transcribe audio
            transcription = await VoiceService.transcribe_audio(audio_path)
            
            return audio_path, transcription
            
        except Exception as e:
            logger.error(f"Error processing voice response: {e}")
            raise
    
    @staticmethod
    async def delete_audio_file(audio_path: str) -> bool:
        """Delete an audio file"""
        try:
            if os.path.exists(audio_path):
                os.remove(audio_path)
                logger.info(f"Audio file deleted: {audio_path}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error deleting audio file {audio_path}: {e}")
            return False
    
    @staticmethod
    async def convert_audio_format(input_path: str, output_format: str = "wav") -> str:
        """Convert audio file to specified format"""
        try:
            output_path = input_path.replace(Path(input_path).suffix, f".{output_format}")
            
            # Use FFmpeg to convert
            cmd = [
                "ffmpeg",
                "-i", input_path,
                "-ac", "1",
                "-ar", "16000",
                output_path
            ]
            
            subprocess.run(cmd, capture_output=True, check=True)
            
            logger.info(f"Audio converted to {output_format}: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error converting audio format: {e}")
            raise
    
    @staticmethod
    async def get_audio_duration(audio_path: str) -> float:
        """Get duration of audio file in seconds"""
        try:
            cmd = [
                "ffprobe",
                "-i", audio_path,
                "-show_entries", "format=duration",
                "-v", "quiet",
                "-of", "csv=p=0"
            ]
            
            result = subprocess.run(cmd, capture_output=True, check=True, text=True)
            duration = float(result.stdout.strip())
            
            return duration
            
        except Exception as e:
            logger.error(f"Error getting audio duration: {e}")
            return 0.0
