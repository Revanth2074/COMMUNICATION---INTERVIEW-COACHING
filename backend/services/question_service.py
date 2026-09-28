"""
Question Service for Interview Coach
Handles interview question management and selection
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import sqlite3
import json
from ..database import get_db_dict
from ..models.question import Question, QuestionCreate, QuestionUpdate
from ..config import settings

logger = logging.getLogger(__name__)


class QuestionService:
    """Service for managing interview questions"""
    
    @staticmethod
    async def create_question(question_data: QuestionCreate) -> Question:
        """Create a new interview question"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            # Convert list to JSON string for storage
            evaluation_criteria_json = json.dumps(question_data.evaluation_criteria)
            
            cursor.execute("""
                INSERT INTO questions (question_text, role, competency, difficulty, question_type, expected_competency, evaluation_criteria, category, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                question_data.question_text,
                question_data.role,
                question_data.competency,
                question_data.difficulty,
                question_data.question_type,
                question_data.expected_competency,
                evaluation_criteria_json,
                question_data.category,
                question_data.is_active
            ))
            
            conn.commit()
            question_id = cursor.lastrowid
            
            # Fetch the created question
            cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
            question_dict = cursor.fetchone()
            conn.close()
            
            if question_dict:
                question_dict['evaluation_criteria'] = json.loads(question_dict['evaluation_criteria'])
            
            return Question(**question_dict)
            
        except Exception as e:
            logger.error(f"Error creating question: {e}")
            raise
    
    @staticmethod
    async def get_question(question_id: int) -> Optional[Question]:
        """Get a question by ID"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
            question_dict = cursor.fetchone()
            conn.close()
            
            if question_dict:
                question_dict['evaluation_criteria'] = json.loads(question_dict['evaluation_criteria'])
                return Question(**question_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting question {question_id}: {e}")
            raise
    
    @staticmethod
    async def get_all_questions(page: int = 1, page_size: int = 10) -> List[Question]:
        """Get all questions with pagination"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            offset = (page - 1) * page_size
            cursor.execute("SELECT * FROM questions LIMIT ? OFFSET ?", (page_size, offset))
            questions = cursor.fetchall()
            conn.close()
            
            result = []
            for question_dict in questions:
                question_dict['evaluation_criteria'] = json.loads(question_dict['evaluation_criteria'])
                result.append(Question(**question_dict))
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting all questions: {e}")
            raise
    
    @staticmethod
    async def get_questions_by_filters(
        role: Optional[str] = None,
        competency: Optional[str] = None,
        difficulty: Optional[str] = None,
        question_type: Optional[str] = None,
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> List[Question]:
        """Get questions filtered by various criteria"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            conditions = []
            params = []
            
            if role:
                conditions.append("role = ?")
                params.append(role)
            if competency:
                conditions.append("competency = ?")
                params.append(competency)
            if difficulty:
                conditions.append("difficulty = ?")
                params.append(difficulty)
            if question_type:
                conditions.append("question_type = ?")
                params.append(question_type)
            if category:
                conditions.append("category = ?")
                params.append(category)
            
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            
            offset = (page - 1) * page_size
            query = f"SELECT * FROM questions WHERE {where_clause} LIMIT ? OFFSET ?"
            params.extend([page_size, offset])
            
            cursor.execute(query, params)
            questions = cursor.fetchall()
            conn.close()
            
            result = []
            for question_dict in questions:
                question_dict['evaluation_criteria'] = json.loads(question_dict['evaluation_criteria'])
                result.append(Question(**question_dict))
            
            return result
            
        except Exception as e:
            logger.error(f"Error filtering questions: {e}")
            raise
    
    @staticmethod
    async def get_random_question(
        role: Optional[str] = None,
        competency: Optional[str] = None,
        difficulty: Optional[str] = None
    ) -> Optional[Question]:
        """Get a random question matching the criteria"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            conditions = []
            params = []
            
            if role:
                conditions.append("role = ?")
                params.append(role)
            if competency:
                conditions.append("competency = ?")
                params.append(competency)
            if difficulty:
                conditions.append("difficulty = ?")
                params.append(difficulty)
            
            conditions.append("is_active = TRUE")
            
            where_clause = " AND ".join(conditions) if conditions else "is_active = TRUE"
            
            query = f"SELECT * FROM questions WHERE {where_clause} ORDER BY RANDOM() LIMIT 1"
            cursor.execute(query, params)
            question_dict = cursor.fetchone()
            conn.close()
            
            if question_dict:
                question_dict['evaluation_criteria'] = json.loads(question_dict['evaluation_criteria'])
                return Question(**question_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting random question: {e}")
            raise
    
    @staticmethod
    async def update_question(question_id: int, update_data: QuestionUpdate) -> Optional[Question]:
        """Update a question"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if update_data.question_text is not None:
                updates.append("question_text = ?")
                params.append(update_data.question_text)
            if update_data.role is not None:
                updates.append("role = ?")
                params.append(update_data.role)
            if update_data.competency is not None:
                updates.append("competency = ?")
                params.append(update_data.competency)
            if update_data.difficulty is not None:
                updates.append("difficulty = ?")
                params.append(update_data.difficulty)
            if update_data.question_type is not None:
                updates.append("question_type = ?")
                params.append(update_data.question_type)
            if update_data.expected_competency is not None:
                updates.append("expected_competency = ?")
                params.append(update_data.expected_competency)
            if update_data.evaluation_criteria is not None:
                updates.append("evaluation_criteria = ?")
                params.append(json.dumps(update_data.evaluation_criteria))
            if update_data.category is not None:
                updates.append("category = ?")
                params.append(update_data.category)
            if update_data.is_active is not None:
                updates.append("is_active = ?")
                params.append(update_data.is_active)
            
            if updates:
                params.append(question_id)
                query = f"UPDATE questions SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, params)
                conn.commit()
            
            # Fetch updated question
            cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
            question_dict = cursor.fetchone()
            conn.close()
            
            if question_dict:
                question_dict['evaluation_criteria'] = json.loads(question_dict['evaluation_criteria'])
                return Question(**question_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error updating question {question_id}: {e}")
            raise
    
    @staticmethod
    async def delete_question(question_id: int) -> bool:
        """Delete a question"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
            conn.commit()
            deleted = cursor.rowcount > 0
            conn.close()
            
            return deleted
            
        except Exception as e:
            logger.error(f"Error deleting question {question_id}: {e}")
            raise
    
    @staticmethod
    async def get_question_count() -> int:
        """Get total number of questions"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as count FROM questions")
            result = cursor.fetchone()
            conn.close()
            
            return result['count'] if result else 0
            
        except Exception as e:
            logger.error(f"Error getting question count: {e}")
            raise
    
    @staticmethod
    async def get_questions_by_role(role: str) -> List[Question]:
        """Get all questions for a specific role"""
        return await QuestionService.get_questions_by_filters(role=role, page_size=1000)
    
    @staticmethod
    async def get_question_stats() -> Dict[str, Any]:
        """Get statistics about questions"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            stats = {}
            
            # Count by role
            cursor.execute("SELECT role, COUNT(*) as count FROM questions GROUP BY role")
            stats['by_role'] = {row['role']: row['count'] for row in cursor.fetchall()}
            
            # Count by competency
            cursor.execute("SELECT competency, COUNT(*) as count FROM questions GROUP BY competency")
            stats['by_competency'] = {row['competency']: row['count'] for row in cursor.fetchall()}
            
            # Count by difficulty
            cursor.execute("SELECT difficulty, COUNT(*) as count FROM questions GROUP BY difficulty")
            stats['by_difficulty'] = {row['difficulty']: row['count'] for row in cursor.fetchall()}
            
            # Count by question type
            cursor.execute("SELECT question_type, COUNT(*) as count FROM questions GROUP BY question_type")
            stats['by_type'] = {row['question_type']: row['count'] for row in cursor.fetchall()}
            
            conn.close()
            return stats
            
        except Exception as e:
            logger.error(f"Error getting question stats: {e}")
            raise
