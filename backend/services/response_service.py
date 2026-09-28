"""
Response Service for Interview Coach
Handles candidate response management
"""

import logging
from typing import Optional, List
from datetime import datetime
import sqlite3
import json
import os
from ..database import get_db_dict
from ..models.response import Response, ResponseCreate, ResponseUpdate
from ..config import settings

logger = logging.getLogger(__name__)


class ResponseService:
    """Service for managing candidate responses"""
    
    @staticmethod
    async def create_response(response_data: ResponseCreate) -> Response:
        """Create a new response"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO responses (session_id, candidate_id, question_id, response_text, response_audio_path, response_type)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                response_data.session_id,
                response_data.candidate_id,
                response_data.question_id,
                response_data.response_text,
                response_data.response_audio_path,
                response_data.response_type
            ))
            
            conn.commit()
            response_id = cursor.lastrowid
            
            # Fetch the created response
            cursor.execute("SELECT * FROM responses WHERE id = ?", (response_id,))
            response_dict = cursor.fetchone()
            conn.close()
            
            return Response(**response_dict)
            
        except Exception as e:
            logger.error(f"Error creating response: {e}")
            raise
    
    @staticmethod
    async def get_response(response_id: int) -> Optional[Response]:
        """Get a response by ID"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM responses WHERE id = ?", (response_id,))
            response_dict = cursor.fetchone()
            conn.close()
            
            if response_dict:
                return Response(**response_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting response {response_id}: {e}")
            raise
    
    @staticmethod
    async def get_responses_by_session(session_id: int) -> List[Response]:
        """Get all responses for a session"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM responses WHERE session_id = ?", (session_id,))
            responses = cursor.fetchall()
            conn.close()
            
            return [Response(**response_dict) for response_dict in responses]
            
        except Exception as e:
            logger.error(f"Error getting responses for session {session_id}: {e}")
            raise
    
    @staticmethod
    async def get_responses_by_candidate(candidate_id: int, page: int = 1, page_size: int = 10) -> List[Response]:
        """Get all responses for a candidate"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            offset = (page - 1) * page_size
            cursor.execute("SELECT * FROM responses WHERE candidate_id = ? LIMIT ? OFFSET ?", 
                          (candidate_id, page_size, offset))
            responses = cursor.fetchall()
            conn.close()
            
            return [Response(**response_dict) for response_dict in responses]
            
        except Exception as e:
            logger.error(f"Error getting responses for candidate {candidate_id}: {e}")
            raise
    
    @staticmethod
    async def update_response(response_id: int, update_data: ResponseUpdate) -> Optional[Response]:
        """Update a response"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if update_data.response_text is not None:
                updates.append("response_text = ?")
                params.append(update_data.response_text)
            if update_data.response_audio_path is not None:
                updates.append("response_audio_path = ?")
                params.append(update_data.response_audio_path)
            if update_data.response_type is not None:
                updates.append("response_type = ?")
                params.append(update_data.response_type)
            
            if updates:
                params.append(response_id)
                query = f"UPDATE responses SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, params)
                conn.commit()
            
            # Fetch updated response
            cursor.execute("SELECT * FROM responses WHERE id = ?", (response_id,))
            response_dict = cursor.fetchone()
            conn.close()
            
            if response_dict:
                return Response(**response_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error updating response {response_id}: {e}")
            raise
    
    @staticmethod
    async def delete_response(response_id: int) -> bool:
        """Delete a response"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM responses WHERE id = ?", (response_id,))
            conn.commit()
            deleted = cursor.rowcount > 0
            conn.close()
            
            # Also delete associated audio file if exists
            if deleted:
                try:
                    cursor.execute("SELECT response_audio_path FROM responses WHERE id = ?", (response_id,))
                    result = cursor.fetchone()
                    if result and result['response_audio_path']:
                        audio_path = result['response_audio_path']
                        if os.path.exists(audio_path):
                            os.remove(audio_path)
                except:
                    pass
            
            return deleted
            
        except Exception as e:
            logger.error(f"Error deleting response {response_id}: {e}")
            raise
    
    @staticmethod
    async def get_latest_response(candidate_id: int) -> Optional[Response]:
        """Get the latest response for a candidate"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM responses 
                WHERE candidate_id = ? 
                ORDER BY submitted_at DESC LIMIT 1
            """, (candidate_id,))
            response_dict = cursor.fetchone()
            conn.close()
            
            if response_dict:
                return Response(**response_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting latest response for candidate {candidate_id}: {e}")
            raise
    
    @staticmethod
    async def get_response_count_by_candidate(candidate_id: int) -> int:
        """Get the number of responses for a candidate"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as count FROM responses WHERE candidate_id = ?", (candidate_id,))
            result = cursor.fetchone()
            conn.close()
            
            return result['count'] if result else 0
            
        except Exception as e:
            logger.error(f"Error getting response count for candidate {candidate_id}: {e}")
            raise
