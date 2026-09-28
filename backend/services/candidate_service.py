"""
Candidate Service for Interview Coach
Handles candidate CRUD operations and profile management
"""

import logging
from typing import Optional, List
from datetime import datetime
import sqlite3
from ..database import get_db_dict
from ..models.candidate import Candidate, CandidateCreate, CandidateUpdate
from ..config import settings
import json

logger = logging.getLogger(__name__)


class CandidateService:
    """Service for managing candidates"""
    
    @staticmethod
    async def create_candidate(candidate_data: CandidateCreate) -> Candidate:
        """Create a new candidate"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            # Convert lists to JSON strings for storage
            skills_json = json.dumps(candidate_data.skills)
            competencies_json = json.dumps(candidate_data.competencies)
            
            cursor.execute("""
                INSERT INTO candidates (user_id, name, email, target_role, experience_years, skills, competencies, resume_text)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                candidate_data.user_id,
                candidate_data.name,
                candidate_data.email,
                candidate_data.target_role,
                candidate_data.experience_years,
                skills_json,
                competencies_json,
                candidate_data.resume_text
            ))
            
            conn.commit()
            candidate_id = cursor.lastrowid
            
            # Fetch the created candidate
            cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
            candidate_dict = cursor.fetchone()
            conn.close()
            
            # Convert JSON strings back to lists
            if candidate_dict:
                candidate_dict['skills'] = json.loads(candidate_dict['skills'])
                candidate_dict['competencies'] = json.loads(candidate_dict['competencies'])
            
            return Candidate(**candidate_dict)
            
        except Exception as e:
            logger.error(f"Error creating candidate: {e}")
            raise
    
    @staticmethod
    async def get_candidate(candidate_id: int) -> Optional[Candidate]:
        """Get a candidate by ID"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
            candidate_dict = cursor.fetchone()
            conn.close()
            
            if candidate_dict:
                # Convert JSON strings back to lists
                candidate_dict['skills'] = json.loads(candidate_dict['skills'])
                candidate_dict['competencies'] = json.loads(candidate_dict['competencies'])
                return Candidate(**candidate_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting candidate {candidate_id}: {e}")
            raise
    
    @staticmethod
    async def get_candidate_by_user_id(user_id: str) -> Optional[Candidate]:
        """Get a candidate by user ID"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM candidates WHERE user_id = ?", (user_id,))
            candidate_dict = cursor.fetchone()
            conn.close()
            
            if candidate_dict:
                candidate_dict['skills'] = json.loads(candidate_dict['skills'])
                candidate_dict['competencies'] = json.loads(candidate_dict['competencies'])
                return Candidate(**candidate_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting candidate by user_id {user_id}: {e}")
            raise
    
    @staticmethod
    async def get_all_candidates(page: int = 1, page_size: int = 10) -> List[Candidate]:
        """Get all candidates with pagination"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            offset = (page - 1) * page_size
            cursor.execute("SELECT * FROM candidates LIMIT ? OFFSET ?", (page_size, offset))
            candidates = cursor.fetchall()
            conn.close()
            
            # Convert JSON strings back to lists
            result = []
            for candidate_dict in candidates:
                candidate_dict['skills'] = json.loads(candidate_dict['skills'])
                candidate_dict['competencies'] = json.loads(candidate_dict['competencies'])
                result.append(Candidate(**candidate_dict))
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting all candidates: {e}")
            raise
    
    @staticmethod
    async def update_candidate(candidate_id: int, update_data: CandidateUpdate) -> Optional[Candidate]:
        """Update a candidate"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            # Build update query dynamically
            updates = []
            params = []
            
            if update_data.name is not None:
                updates.append("name = ?")
                params.append(update_data.name)
            if update_data.email is not None:
                updates.append("email = ?")
                params.append(update_data.email)
            if update_data.target_role is not None:
                updates.append("target_role = ?")
                params.append(update_data.target_role)
            if update_data.experience_years is not None:
                updates.append("experience_years = ?")
                params.append(update_data.experience_years)
            if update_data.skills is not None:
                updates.append("skills = ?")
                params.append(json.dumps(update_data.skills))
            if update_data.competencies is not None:
                updates.append("competencies = ?")
                params.append(json.dumps(update_data.competencies))
            if update_data.resume_text is not None:
                updates.append("resume_text = ?")
                params.append(update_data.resume_text)
            
            if updates:
                updates.append("updated_at = CURRENT_TIMESTAMP")
                params.append(candidate_id)
                
                query = f"UPDATE candidates SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, params)
                conn.commit()
            
            # Fetch updated candidate
            cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
            candidate_dict = cursor.fetchone()
            conn.close()
            
            if candidate_dict:
                candidate_dict['skills'] = json.loads(candidate_dict['skills'])
                candidate_dict['competencies'] = json.loads(candidate_dict['competencies'])
                return Candidate(**candidate_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error updating candidate {candidate_id}: {e}")
            raise
    
    @staticmethod
    async def delete_candidate(candidate_id: int) -> bool:
        """Delete a candidate"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
            conn.commit()
            deleted = cursor.rowcount > 0
            conn.close()
            
            return deleted
            
        except Exception as e:
            logger.error(f"Error deleting candidate {candidate_id}: {e}")
            raise
    
    @staticmethod
    async def get_candidate_count() -> int:
        """Get total number of candidates"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as count FROM candidates")
            result = cursor.fetchone()
            conn.close()
            
            return result['count'] if result else 0
            
        except Exception as e:
            logger.error(f"Error getting candidate count: {e}")
            raise
