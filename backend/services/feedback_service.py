"""
Feedback Service for Interview Coach
Handles feedback generation and management
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import sqlite3
import json
from ..database import get_db_dict
from ..models.feedback import Feedback, FeedbackCreate, FeedbackUpdate
from ..models.response import Response
from ..models.question import Question
from ..models.candidate import Candidate
from .response_service import ResponseService
from .question_service import QuestionService
from .candidate_service import CandidateService

logger = logging.getLogger(__name__)


class FeedbackService:
    """Service for managing feedback"""
    
    @staticmethod
    async def create_feedback(feedback_data: FeedbackCreate) -> Feedback:
        """Create new feedback"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            # Convert lists to JSON strings for storage
            strengths_json = json.dumps(feedback_data.strengths)
            weaknesses_json = json.dumps(feedback_data.weaknesses)
            suggestions_json = json.dumps(feedback_data.improvement_suggestions)
            follow_up_json = json.dumps(feedback_data.follow_up_questions)
            agent_feedback_json = json.dumps(feedback_data.agent_feedback)
            
            cursor.execute("""
                INSERT INTO feedback (
                    response_id, session_id, candidate_id, question_id,
                    relevance_score, clarity_score, structure_score, completeness_score,
                    communication_score, overall_score, strengths, weaknesses,
                    improvement_suggestions, star_analysis, content_analysis,
                    communication_analysis, improved_response, follow_up_questions,
                    agent_feedback
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                feedback_data.response_id,
                feedback_data.session_id,
                feedback_data.candidate_id,
                feedback_data.question_id,
                feedback_data.relevance_score,
                feedback_data.clarity_score,
                feedback_data.structure_score,
                feedback_data.completeness_score,
                feedback_data.communication_score,
                feedback_data.overall_score,
                strengths_json,
                weaknesses_json,
                suggestions_json,
                feedback_data.star_analysis,
                feedback_data.content_analysis,
                feedback_data.communication_analysis,
                feedback_data.improved_response,
                follow_up_json,
                agent_feedback_json
            ))
            
            conn.commit()
            feedback_id = cursor.lastrowid
            
            # Fetch the created feedback
            cursor.execute("SELECT * FROM feedback WHERE id = ?", (feedback_id,))
            feedback_dict = cursor.fetchone()
            conn.close()
            
            if feedback_dict:
                feedback_dict['strengths'] = json.loads(feedback_dict['strengths'])
                feedback_dict['weaknesses'] = json.loads(feedback_dict['weaknesses'])
                feedback_dict['improvement_suggestions'] = json.loads(feedback_dict['improvement_suggestions'])
                feedback_dict['follow_up_questions'] = json.loads(feedback_dict['follow_up_questions'])
                feedback_dict['agent_feedback'] = json.loads(feedback_dict['agent_feedback'])
            
            return Feedback(**feedback_dict)
            
        except Exception as e:
            logger.error(f"Error creating feedback: {e}")
            raise
    
    @staticmethod
    async def get_feedback(feedback_id: int) -> Optional[Feedback]:
        """Get feedback by ID"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM feedback WHERE id = ?", (feedback_id,))
            feedback_dict = cursor.fetchone()
            conn.close()
            
            if feedback_dict:
                feedback_dict['strengths'] = json.loads(feedback_dict['strengths'])
                feedback_dict['weaknesses'] = json.loads(feedback_dict['weaknesses'])
                feedback_dict['improvement_suggestions'] = json.loads(feedback_dict['improvement_suggestions'])
                feedback_dict['follow_up_questions'] = json.loads(feedback_dict['follow_up_questions'])
                feedback_dict['agent_feedback'] = json.loads(feedback_dict['agent_feedback'])
                return Feedback(**feedback_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting feedback {feedback_id}: {e}")
            raise
    
    @staticmethod
    async def get_feedback_by_response(response_id: int) -> Optional[Feedback]:
        """Get feedback for a specific response"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM feedback WHERE response_id = ?", (response_id,))
            feedback_dict = cursor.fetchone()
            conn.close()
            
            if feedback_dict:
                feedback_dict['strengths'] = json.loads(feedback_dict['strengths'])
                feedback_dict['weaknesses'] = json.loads(feedback_dict['weaknesses'])
                feedback_dict['improvement_suggestions'] = json.loads(feedback_dict['improvement_suggestions'])
                feedback_dict['follow_up_questions'] = json.loads(feedback_dict['follow_up_questions'])
                feedback_dict['agent_feedback'] = json.loads(feedback_dict['agent_feedback'])
                return Feedback(**feedback_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting feedback for response {response_id}: {e}")
            raise
    
    @staticmethod
    async def get_feedback_by_session(session_id: int) -> List[Feedback]:
        """Get all feedback for a session"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM feedback WHERE session_id = ?", (session_id,))
            feedbacks = cursor.fetchall()
            conn.close()
            
            result = []
            for feedback_dict in feedbacks:
                feedback_dict['strengths'] = json.loads(feedback_dict['strengths'])
                feedback_dict['weaknesses'] = json.loads(feedback_dict['weaknesses'])
                feedback_dict['improvement_suggestions'] = json.loads(feedback_dict['improvement_suggestions'])
                feedback_dict['follow_up_questions'] = json.loads(feedback_dict['follow_up_questions'])
                feedback_dict['agent_feedback'] = json.loads(feedback_dict['agent_feedback'])
                result.append(Feedback(**feedback_dict))
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting feedback for session {session_id}: {e}")
            raise
    
    @staticmethod
    async def get_feedback_by_candidate(candidate_id: int, page: int = 1, page_size: int = 10) -> List[Feedback]:
        """Get all feedback for a candidate"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            offset = (page - 1) * page_size
            cursor.execute("SELECT * FROM feedback WHERE candidate_id = ? LIMIT ? OFFSET ?", 
                          (candidate_id, page_size, offset))
            feedbacks = cursor.fetchall()
            conn.close()
            
            result = []
            for feedback_dict in feedbacks:
                feedback_dict['strengths'] = json.loads(feedback_dict['strengths'])
                feedback_dict['weaknesses'] = json.loads(feedback_dict['weaknesses'])
                feedback_dict['improvement_suggestions'] = json.loads(feedback_dict['improvement_suggestions'])
                feedback_dict['follow_up_questions'] = json.loads(feedback_dict['follow_up_questions'])
                feedback_dict['agent_feedback'] = json.loads(feedback_dict['agent_feedback'])
                result.append(Feedback(**feedback_dict))
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting feedback for candidate {candidate_id}: {e}")
            raise
    
    @staticmethod
    async def update_feedback(feedback_id: int, update_data: FeedbackUpdate) -> Optional[Feedback]:
        """Update feedback"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if update_data.relevance_score is not None:
                updates.append("relevance_score = ?")
                params.append(update_data.relevance_score)
            if update_data.clarity_score is not None:
                updates.append("clarity_score = ?")
                params.append(update_data.clarity_score)
            if update_data.structure_score is not None:
                updates.append("structure_score = ?")
                params.append(update_data.structure_score)
            if update_data.completeness_score is not None:
                updates.append("completeness_score = ?")
                params.append(update_data.completeness_score)
            if update_data.communication_score is not None:
                updates.append("communication_score = ?")
                params.append(update_data.communication_score)
            if update_data.overall_score is not None:
                updates.append("overall_score = ?")
                params.append(update_data.overall_score)
            if update_data.strengths is not None:
                updates.append("strengths = ?")
                params.append(json.dumps(update_data.strengths))
            if update_data.weaknesses is not None:
                updates.append("weaknesses = ?")
                params.append(json.dumps(update_data.weaknesses))
            if update_data.improvement_suggestions is not None:
                updates.append("improvement_suggestions = ?")
                params.append(json.dumps(update_data.improvement_suggestions))
            if update_data.star_analysis is not None:
                updates.append("star_analysis = ?")
                params.append(update_data.star_analysis)
            if update_data.content_analysis is not None:
                updates.append("content_analysis = ?")
                params.append(update_data.content_analysis)
            if update_data.communication_analysis is not None:
                updates.append("communication_analysis = ?")
                params.append(update_data.communication_analysis)
            if update_data.improved_response is not None:
                updates.append("improved_response = ?")
                params.append(update_data.improved_response)
            if update_data.follow_up_questions is not None:
                updates.append("follow_up_questions = ?")
                params.append(json.dumps(update_data.follow_up_questions))
            if update_data.agent_feedback is not None:
                updates.append("agent_feedback = ?")
                params.append(json.dumps(update_data.agent_feedback))
            
            if updates:
                params.append(feedback_id)
                query = f"UPDATE feedback SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, params)
                conn.commit()
            
            # Fetch updated feedback
            cursor.execute("SELECT * FROM feedback WHERE id = ?", (feedback_id,))
            feedback_dict = cursor.fetchone()
            conn.close()
            
            if feedback_dict:
                feedback_dict['strengths'] = json.loads(feedback_dict['strengths'])
                feedback_dict['weaknesses'] = json.loads(feedback_dict['weaknesses'])
                feedback_dict['improvement_suggestions'] = json.loads(feedback_dict['improvement_suggestions'])
                feedback_dict['follow_up_questions'] = json.loads(feedback_dict['follow_up_questions'])
                feedback_dict['agent_feedback'] = json.loads(feedback_dict['agent_feedback'])
                return Feedback(**feedback_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error updating feedback {feedback_id}: {e}")
            raise
    
    @staticmethod
    async def delete_feedback(feedback_id: int) -> bool:
        """Delete feedback"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM feedback WHERE id = ?", (feedback_id,))
            conn.commit()
            deleted = cursor.rowcount > 0
            conn.close()
            
            return deleted
            
        except Exception as e:
            logger.error(f"Error deleting feedback {feedback_id}: {e}")
            raise
    
    @staticmethod
    async def get_feedback_with_context(feedback_id: int) -> Optional[Dict[str, Any]]:
        """Get feedback with associated response, question, and candidate"""
        try:
            feedback = await FeedbackService.get_feedback(feedback_id)
            if not feedback:
                return None
            
            response = await ResponseService.get_response(feedback.response_id)
            question = await QuestionService.get_question(feedback.question_id)
            candidate = await CandidateService.get_candidate(feedback.candidate_id)
            
            return {
                "feedback": feedback,
                "response": response,
                "question": question,
                "candidate": candidate
            }
            
        except Exception as e:
            logger.error(f"Error getting feedback context for {feedback_id}: {e}")
            raise
    
    @staticmethod
    async def get_average_scores(candidate_id: int) -> Dict[str, float]:
        """Get average scores for a candidate across all feedback"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    AVG(relevance_score) as avg_relevance,
                    AVG(clarity_score) as avg_clarity,
                    AVG(structure_score) as avg_structure,
                    AVG(completeness_score) as avg_completeness,
                    AVG(communication_score) as avg_communication,
                    AVG(overall_score) as avg_overall
                FROM feedback 
                WHERE candidate_id = ?
            """, (candidate_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    "relevance": result['avg_relevance'] or 0.0,
                    "clarity": result['avg_clarity'] or 0.0,
                    "structure": result['avg_structure'] or 0.0,
                    "completeness": result['avg_completeness'] or 0.0,
                    "communication": result['avg_communication'] or 0.0,
                    "overall": result['avg_overall'] or 0.0
                }
            
            return {
                "relevance": 0.0,
                "clarity": 0.0,
                "structure": 0.0,
                "completeness": 0.0,
                "communication": 0.0,
                "overall": 0.0
            }
            
        except Exception as e:
            logger.error(f"Error getting average scores for candidate {candidate_id}: {e}")
            raise
