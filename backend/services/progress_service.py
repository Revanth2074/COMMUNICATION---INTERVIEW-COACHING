"""
Progress Service for Interview Coach
Handles progress tracking and improvement analysis
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import sqlite3
import json
from ..database import get_db_dict
from ..models.progress import Progress, ProgressCreate
from ..services.feedback_service import FeedbackService

logger = logging.getLogger(__name__)


class ProgressService:
    """Service for tracking candidate progress"""
    
    @staticmethod
    async def create_progress(progress_data: ProgressCreate) -> Progress:
        """Create a new progress entry"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO progress (candidate_id, session_id, competency, score, area, baseline_score, current_score, improvement_percentage)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                progress_data.candidate_id,
                progress_data.session_id,
                progress_data.competency,
                progress_data.score,
                progress_data.area,
                progress_data.baseline_score,
                progress_data.current_score,
                progress_data.improvement_percentage
            ))
            
            conn.commit()
            progress_id = cursor.lastrowid
            
            # Fetch the created progress
            cursor.execute("SELECT * FROM progress WHERE id = ?", (progress_id,))
            progress_dict = cursor.fetchone()
            conn.close()
            
            return Progress(**progress_dict)
            
        except Exception as e:
            logger.error(f"Error creating progress: {e}")
            raise
    
    @staticmethod
    async def get_progress(progress_id: int) -> Optional[Progress]:
        """Get progress by ID"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM progress WHERE id = ?", (progress_id,))
            progress_dict = cursor.fetchone()
            conn.close()
            
            if progress_dict:
                return Progress(**progress_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting progress {progress_id}: {e}")
            raise
    
    @staticmethod
    async def get_progress_by_candidate(candidate_id: int, page: int = 1, page_size: int = 10) -> List[Progress]:
        """Get all progress entries for a candidate"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            offset = (page - 1) * page_size
            cursor.execute("SELECT * FROM progress WHERE candidate_id = ? LIMIT ? OFFSET ?", 
                          (candidate_id, page_size, offset))
            progresses = cursor.fetchall()
            conn.close()
            
            return [Progress(**progress_dict) for progress_dict in progresses]
            
        except Exception as e:
            logger.error(f"Error getting progress for candidate {candidate_id}: {e}")
            raise
    
    @staticmethod
    async def get_progress_by_competency(candidate_id: int, competency: str) -> List[Progress]:
        """Get progress for a specific competency"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM progress WHERE candidate_id = ? AND competency = ? ORDER BY last_updated", 
                          (candidate_id, competency))
            progresses = cursor.fetchall()
            conn.close()
            
            return [Progress(**progress_dict) for progress_dict in progresses]
            
        except Exception as e:
            logger.error(f"Error getting progress for competency {competency}: {e}")
            raise
    
    @staticmethod
    async def get_latest_progress(candidate_id: int, competency: str, area: str) -> Optional[Progress]:
        """Get the latest progress for a specific competency and area"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM progress 
                WHERE candidate_id = ? AND competency = ? AND area = ?
                ORDER BY last_updated DESC LIMIT 1
            """, (candidate_id, competency, area))
            progress_dict = cursor.fetchone()
            conn.close()
            
            if progress_dict:
                return Progress(**progress_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting latest progress: {e}")
            raise
    
    @staticmethod
    async def update_progress(progress_id: int, current_score: float, improvement_percentage: float) -> Optional[Progress]:
        """Update progress with new scores"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE progress 
                SET current_score = ?, improvement_percentage = ?, last_updated = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (current_score, improvement_percentage, progress_id))
            
            conn.commit()
            
            # Fetch updated progress
            cursor.execute("SELECT * FROM progress WHERE id = ?", (progress_id,))
            progress_dict = cursor.fetchone()
            conn.close()
            
            if progress_dict:
                return Progress(**progress_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error updating progress {progress_id}: {e}")
            raise
    
    @staticmethod
    async def record_session_progress(session_id: int, candidate_id: int) -> List[Progress]:
        """Record progress from a completed session"""
        try:
            # Get feedback for this session
            feedbacks = await FeedbackService.get_feedback_by_session(session_id)
            
            if not feedbacks:
                return []
            
            created_progresses = []
            
            for feedback in feedbacks:
                # Get the question to determine competency
                question = await QuestionService.get_question(feedback.question_id)
                if not question:
                    continue
                
                # Record progress for each scoring area
                areas = [
                    ('relevance', feedback.relevance_score),
                    ('clarity', feedback.clarity_score),
                    ('structure', feedback.structure_score),
                    ('completeness', feedback.completeness_score),
                    ('communication', feedback.communication_score)
                ]
                
                for area, score in areas:
                    # Check if baseline exists
                    baseline_progress = await ProgressService.get_latest_progress(
                        candidate_id, question.competency, area
                    )
                    
                    baseline_score = baseline_progress.current_score if baseline_progress else 0.0
                    
                    # Calculate improvement
                    if baseline_score > 0:
                        improvement = ((score - baseline_score) / baseline_score) * 100
                    else:
                        improvement = 0.0
                    
                    progress_data = ProgressCreate(
                        candidate_id=candidate_id,
                        session_id=session_id,
                        competency=question.competency,
                        score=score,
                        area=area,
                        baseline_score=baseline_score,
                        current_score=score,
                        improvement_percentage=improvement
                    )
                    
                    created_progress = await ProgressService.create_progress(progress_data)
                    created_progresses.append(created_progress)
            
            return created_progresses
            
        except Exception as e:
            logger.error(f"Error recording session progress for session {session_id}: {e}")
            raise
    
    @staticmethod
    async def get_progress_summary(candidate_id: int) -> Dict[str, Any]:
        """Get comprehensive progress summary for a candidate"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            summary = {
                "overall": {
                    "average_score": 0.0,
                    "total_sessions": 0,
                    "improvement_trend": "stable"
                },
                "by_competency": {},
                "by_area": {},
                "recent_trend": []
            }
            
            # Get all progress entries
            cursor.execute("SELECT * FROM progress WHERE candidate_id = ? ORDER BY last_updated", (candidate_id,))
            progresses = cursor.fetchall()
            
            if progresses:
                # Calculate overall statistics
                all_scores = [p['current_score'] for p in progresses]
                summary['overall']['average_score'] = sum(all_scores) / len(all_scores)
                summary['overall']['total_sessions'] = len(set(p['session_id'] for p in progresses if p['session_id']))
                
                # Group by competency
                for progress in progresses:
                    competency = progress['competency']
                    area = progress['area']
                    score = progress['current_score']
                    
                    if competency not in summary['by_competency']:
                        summary['by_competency'][competency] = {
                            "scores": [],
                            "average": 0.0,
                            "count": 0
                        }
                    
                    summary['by_competency'][competency]['scores'].append(score)
                    summary['by_competency'][competency]['count'] += 1
                
                # Calculate competency averages
                for competency, data in summary['by_competency'].items():
                    data['average'] = sum(data['scores']) / len(data['scores'])
                
                # Group by area
                for progress in progresses:
                    area = progress['area']
                    score = progress['current_score']
                    
                    if area not in summary['by_area']:
                        summary['by_area'][area] = {
                            "scores": [],
                            "average": 0.0,
                            "count": 0
                        }
                    
                    summary['by_area'][area]['scores'].append(score)
                    summary['by_area'][area]['count'] += 1
                
                # Calculate area averages
                for area, data in summary['by_area'].items():
                    data['average'] = sum(data['scores']) / len(data['scores'])
                
                # Get recent trend (last 5 sessions)
                cursor.execute("""
                    SELECT session_id, current_score, last_updated 
                    FROM progress 
                    WHERE candidate_id = ? 
                    ORDER BY last_updated DESC 
                    LIMIT 5
                """, (candidate_id,))
                
                recent = cursor.fetchall()
                for entry in recent:
                    summary['recent_trend'].append({
                        "session_id": entry['session_id'],
                        "score": entry['current_score'],
                        "date": entry['last_updated']
                    })
            
            conn.close()
            return summary
            
        except Exception as e:
            logger.error(f"Error getting progress summary for candidate {candidate_id}: {e}")
            raise
    
    @staticmethod
    async def get_improvement_areas(candidate_id: int, threshold: float = 70.0) -> List[Dict[str, Any]]:
        """Identify areas that need improvement"""
        try:
            summary = await ProgressService.get_progress_summary(candidate_id)
            
            improvement_areas = []
            
            # Check overall areas
            for area, data in summary['by_area'].items():
                if data['average'] < threshold:
                    improvement_areas.append({
                        "type": "area",
                        "name": area,
                        "current_score": data['average'],
                        "deficit": threshold - data['average']
                    })
            
            # Check competencies
            for competency, data in summary['by_competency'].items():
                if data['average'] < threshold:
                    improvement_areas.append({
                        "type": "competency",
                        "name": competency,
                        "current_score": data['average'],
                        "deficit": threshold - data['average']
                    })
            
            # Sort by deficit (most needing improvement first)
            improvement_areas.sort(key=lambda x: x['deficit'], reverse=True)
            
            return improvement_areas
            
        except Exception as e:
            logger.error(f"Error getting improvement areas for candidate {candidate_id}: {e}")
            raise
