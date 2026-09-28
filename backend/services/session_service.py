"""
Session Service for Interview Coach
Handles interview session management
"""

import logging
from typing import Optional, List
from datetime import datetime
import sqlite3
import json
from ..database import get_db_dict
from ..models.session import Session, SessionCreate, SessionUpdate
from ..models.candidate import Candidate
from ..models.question import Question
from .candidate_service import CandidateService
from .question_service import QuestionService

logger = logging.getLogger(__name__)


class SessionService:
    """Service for managing interview sessions"""
    
    @staticmethod
    async def create_session(session_data: SessionCreate) -> Session:
        """Create a new interview session"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO sessions (candidate_id, question_id, session_type, status)
                VALUES (?, ?, ?, ?)
            """, (
                session_data.candidate_id,
                session_data.question_id,
                session_data.session_type,
                session_data.status
            ))
            
            conn.commit()
            session_id = cursor.lastrowid
            
            # Fetch the created session
            cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
            session_dict = cursor.fetchone()
            conn.close()
            
            return Session(**session_dict)
            
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            raise
    
    @staticmethod
    async def get_session(session_id: int) -> Optional[Session]:
        """Get a session by ID"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
            session_dict = cursor.fetchone()
            conn.close()
            
            if session_dict:
                return Session(**session_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting session {session_id}: {e}")
            raise
    
    @staticmethod
    async def get_sessions_by_candidate(candidate_id: int, page: int = 1, page_size: int = 10) -> List[Session]:
        """Get all sessions for a candidate"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            offset = (page - 1) * page_size
            cursor.execute("SELECT * FROM sessions WHERE candidate_id = ? LIMIT ? OFFSET ?", 
                          (candidate_id, page_size, offset))
            sessions = cursor.fetchall()
            conn.close()
            
            return [Session(**session_dict) for session_dict in sessions]
            
        except Exception as e:
            logger.error(f"Error getting sessions for candidate {candidate_id}: {e}")
            raise
    
    @staticmethod
    async def get_session_with_details(session_id: int) -> Optional[dict]:
        """Get a session with candidate and question details"""
        try:
            session = await SessionService.get_session(session_id)
            if not session:
                return None
            
            candidate = await CandidateService.get_candidate(session.candidate_id)
            question = await QuestionService.get_question(session.question_id)
            
            return {
                "session": session,
                "candidate": candidate,
                "question": question
            }
            
        except Exception as e:
            logger.error(f"Error getting session details for {session_id}: {e}")
            raise
    
    @staticmethod
    async def update_session(session_id: int, update_data: SessionUpdate) -> Optional[Session]:
        """Update a session"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if update_data.session_type is not None:
                updates.append("session_type = ?")
                params.append(update_data.session_type)
            if update_data.status is not None:
                updates.append("status = ?")
                params.append(update_data.status)
            if update_data.completed_at is not None:
                updates.append("completed_at = ?")
                params.append(update_data.completed_at.isoformat())
            
            if updates:
                params.append(session_id)
                query = f"UPDATE sessions SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, params)
                conn.commit()
            
            # Fetch updated session
            cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
            session_dict = cursor.fetchone()
            conn.close()
            
            if session_dict:
                return Session(**session_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error updating session {session_id}: {e}")
            raise
    
    @staticmethod
    async def delete_session(session_id: int) -> bool:
        """Delete a session"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
            conn.commit()
            deleted = cursor.rowcount > 0
            conn.close()
            
            return deleted
            
        except Exception as e:
            logger.error(f"Error deleting session {session_id}: {e}")
            raise
    
    @staticmethod
    async def complete_session(session_id: int) -> Optional[Session]:
        """Mark a session as completed"""
        try:
            update_data = SessionUpdate(
                status="completed",
                completed_at=datetime.now()
            )
            return await SessionService.update_session(session_id, update_data)
            
        except Exception as e:
            logger.error(f"Error completing session {session_id}: {e}")
            raise
    
    @staticmethod
    async def get_active_session(candidate_id: int) -> Optional[Session]:
        """Get the current active session for a candidate"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM sessions 
                WHERE candidate_id = ? AND status = 'in_progress' 
                ORDER BY started_at DESC LIMIT 1
            """, (candidate_id,))
            session_dict = cursor.fetchone()
            conn.close()
            
            if session_dict:
                return Session(**session_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting active session for candidate {candidate_id}: {e}")
            raise
    
    @staticmethod
    async def get_session_count_by_candidate(candidate_id: int) -> int:
        """Get the number of sessions for a candidate"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as count FROM sessions WHERE candidate_id = ?", (candidate_id,))
            result = cursor.fetchone()
            conn.close()
            
            return result['count'] if result else 0
            
        except Exception as e:
            logger.error(f"Error getting session count for candidate {candidate_id}: {e}")
            raise
