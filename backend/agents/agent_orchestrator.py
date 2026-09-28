"""
Agent Orchestrator for Interview Coach
Coordinates the multi-agent system and manages agent handoff
"""

import logging
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
import asyncio
from .base_agent import BaseAgent, AgentResult
from .question_agent import QuestionAgent
from .communication_agent import CommunicationAgent
from .content_agent import ContentAgent
from .star_agent import STARAgent
from .coach_agent import CoachAgent
from ..services.candidate_service import CandidateService
from ..services.question_service import QuestionService
from ..services.session_service import SessionService
from ..services.response_service import ResponseService
from ..services.feedback_service import FeedbackService
from ..services.progress_service import ProgressService

logger = logging.getLogger(__name__)


@dataclass
class OrchestrationResult:
    """Result from orchestrating multiple agents"""
    success: bool
    question: Optional[Dict[str, Any]] = None
    response_analysis: Dict[str, Any] = field(default_factory=dict)
    feedback: Optional[Dict[str, Any]] = None
    agent_results: Dict[str, AgentResult] = field(default_factory=dict)
    improvement_plan: Dict[str, Any] = field(default_factory=dict)
    follow_up_questions: List[str] = field(default_factory=list)
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class AgentOrchestrator:
    """Orchestrates the multi-agent interview coaching system"""
    
    def __init__(self):
        """Initialize the orchestrator"""
        self.question_agent = QuestionAgent()
        self.communication_agent = CommunicationAgent()
        self.content_agent = ContentAgent()
        self.star_agent = STARAgent()
        self.coach_agent = CoachAgent()
        
        self.agents = {
            "question": self.question_agent,
            "communication": self.communication_agent,
            "content": self.content_agent,
            "star": self.star_agent,
            "coach": self.coach_agent
        }
    
    async def initialize(self):
        """Initialize all agents"""
        try:
            tasks = [agent.initialize() for agent in self.agents.values()]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            initialized = all(r for r in results if not isinstance(r, Exception))
            logger.info(f"Agents initialized: {initialized}")
            return initialized
            
        except Exception as e:
            logger.error(f"Error initializing agents: {e}")
            return False
    
    async def start_practice_session(
        self,
        candidate_id: int,
        target_role: Optional[str] = None,
        competency: Optional[str] = None,
        difficulty: str = "medium"
    ) -> OrchestrationResult:
        """Start a new practice session with a selected question"""
        try:
            # Get candidate info
            candidate = await CandidateService.get_candidate(candidate_id)
            if not candidate:
                return OrchestrationResult(
                    success=False,
                    error=f"Candidate {candidate_id} not found"
                )
            
            # Use candidate's target role if not specified
            role = target_role or candidate.target_role
            
            # Get a question from the Question Agent
            question_result = await self.question_agent.get_random_question(
                candidate_id=candidate_id,
                target_role=role,
                competency=competency,
                difficulty=difficulty
            )
            
            if not question_result.success:
                return OrchestrationResult(
                    success=False,
                    error=question_result.error or "Failed to get question"
                )
            
            question_data = question_result.data.get("questions", [{}])[0]
            
            # Create a session
            session_data = {
                "candidate_id": candidate_id,
                "question_id": question_data.get("id"),
                "session_type": "practice",
                "status": "in_progress"
            }
            
            # Note: In a real implementation, we would save the session to the database
            # For now, we'll just return the question
            
            return OrchestrationResult(
                success=True,
                question=question_data,
                metadata={
                    "candidate_id": candidate_id,
                    "session_type": "practice",
                    "question_source": question_result.data.get("source", "database")
                }
            )
            
        except Exception as e:
            logger.error(f"Error starting practice session: {e}")
            return OrchestrationResult(success=False, error=str(e))
    
    async def analyze_response(
        self,
        candidate_id: int,
        session_id: Optional[int] = None,
        question_id: Optional[int] = None,
        response_text: str = "",
        response_type: str = "text"
    ) -> OrchestrationResult:
        """Analyze a candidate's response using all specialist agents"""
        try:
            # Get candidate, question, and session info
            candidate = await CandidateService.get_candidate(candidate_id)
            question = None
            
            if question_id:
                question = await QuestionService.get_question(question_id)
            elif session_id:
                session = await SessionService.get_session(session_id)
                if session:
                    question = await QuestionService.get_question(session.question_id)
                    question_id = session.question_id
            
            if not question:
                return OrchestrationResult(
                    success=False,
                    error="Question not found"
                )
            
            # Prepare input data for all agents
            base_input = {
                "candidate_id": candidate_id,
                "response_text": response_text,
                "question": question.question_text,
                "question_type": question.question_type,
                "competency": question.competency,
                "role": question.role,
                "candidate_info": {
                    "target_role": candidate.target_role if candidate else "",
                    "experience_years": candidate.experience_years if candidate else 0,
                    "skills": candidate.skills if candidate else [],
                    "competencies": candidate.competencies if candidate else []
                }
            }
            
            # Run all specialist agents in parallel
            logger.info("Running specialist agents for response analysis")
            
            tasks = [
                self.communication_agent.analyze(base_input),
                self.content_agent.analyze(base_input),
                self.star_agent.analyze(base_input)
            ]
            
            agent_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            processed_results = {}
            for i, agent_type in enumerate(["communication", "content", "star"]):
                result = agent_results[i]
                if isinstance(result, Exception):
                    processed_results[agent_type] = AgentResult(
                        agent_type=agent_type,
                        success=False,
                        error=str(result)
                    )
                else:
                    processed_results[agent_type] = result
            
            # Check if all agents succeeded
            all_success = all(r.success for r in processed_results.values())
            
            if not all_success:
                errors = [r.error for r in processed_results.values() if not r.success]
                return OrchestrationResult(
                    success=False,
                    error=f"Agent analysis failed: {', '.join(errors)}",
                    agent_results=processed_results
                )
            
            # Run the Coach Agent to consolidate feedback
            coach_input = {
                **base_input,
                "feedback_data": {
                    "agent_feedback": {
                        agent_type: result.data for agent_type, result in processed_results.items()
                    }
                }
            }
            
            coach_result = await self.coach_agent.analyze(coach_input)
            
            if not coach_result.success:
                return OrchestrationResult(
                    success=False,
                    error=coach_result.error or "Coach agent failed",
                    agent_results={**processed_results, "coach": coach_result}
                )
            
            # Store the response and feedback in the database
            try:
                # Create or update session
                if not session_id:
                    session_data = {
                        "candidate_id": candidate_id,
                        "question_id": question_id,
                        "session_type": "practice",
                        "status": "completed"
                    }
                    # Note: In a real implementation, we would save this
                    # session = await SessionService.create_session(session_data)
                    # session_id = session.id
                
                # Save response
                response_data = {
                    "session_id": session_id or 0,
                    "candidate_id": candidate_id,
                    "question_id": question_id,
                    "response_text": response_text,
                    "response_type": response_type
                }
                # response = await ResponseService.create_response(response_data)
                
                # Save feedback
                feedback_data = coach_result.data
                feedback_create = {
                    "response_id": 0,  # Would be response.id in real implementation
                    "session_id": session_id or 0,
                    "candidate_id": candidate_id,
                    "question_id": question_id,
                    "relevance_score": feedback_data.get("agent_feedback_summary", {}).get("content", {}).get("score", 50.0),
                    "clarity_score": feedback_data.get("agent_feedback_summary", {}).get("communication", {}).get("score", 50.0),
                    "structure_score": feedback_data.get("agent_feedback_summary", {}).get("star", {}).get("score", 50.0),
                    "completeness_score": feedback_data.get("agent_feedback_summary", {}).get("content", {}).get("score", 50.0),
                    "communication_score": feedback_data.get("agent_feedback_summary", {}).get("communication", {}).get("score", 50.0),
                    "overall_score": feedback_data.get("overall_score", 50.0),
                    "strengths": feedback_data.get("agent_feedback_summary", {}).get("communication", {}).get("strengths", []),
                    "weaknesses": [],
                    "improvement_suggestions": feedback_data.get("personalized_recommendations", []),
                    "star_analysis": json.dumps(feedback_data.get("agent_feedback_summary", {}).get("star", {})),
                    "content_analysis": json.dumps(feedback_data.get("agent_feedback_summary", {}).get("content", {})),
                    "communication_analysis": json.dumps(feedback_data.get("agent_feedback_summary", {}).get("communication", {})),
                    "improved_response": feedback_data.get("improved_response_example", ""),
                    "follow_up_questions": feedback_data.get("follow_up_questions", []),
                    "agent_feedback": feedback_data
                }
                
                # feedback = await FeedbackService.create_feedback(feedback_create)
                
                # Record progress
                # await ProgressService.record_session_progress(session_id, candidate_id)
                
            except Exception as e:
                logger.warning(f"Error saving to database: {e}")
                # Continue even if database save fails
            
            # Extract follow-up questions
            follow_up_questions = feedback_data.get("follow_up_questions", [])
            
            return OrchestrationResult(
                success=True,
                question={
                    "id": question_id,
                    "text": question.question_text,
                    "role": question.role,
                    "competency": question.competency
                },
                response_analysis=coach_result.data,
                feedback=feedback_data,
                agent_results={**processed_results, "coach": coach_result},
                improvement_plan=feedback_data.get("improvement_plan", {}),
                follow_up_questions=follow_up_questions,
                metadata={
                    "candidate_id": candidate_id,
                    "question_id": question_id,
                    "session_id": session_id,
                    "analysis_method": "multi_agent"
                }
            )
            
        except Exception as e:
            logger.error(f"Error analyzing response: {e}")
            return OrchestrationResult(success=False, error=str(e))
    
    async def get_follow_up_question(
        self,
        candidate_id: int,
        previous_question_id: int,
        previous_response: str
    ) -> OrchestrationResult:
        """Get a follow-up question based on previous response"""
        try:
            # Get the previous question
            previous_question = await QuestionService.get_question(previous_question_id)
            if not previous_question:
                return OrchestrationResult(
                    success=False,
                    error="Previous question not found"
                )
            
            # Generate follow-up question using Question Agent
            follow_up_result = await self.question_agent.get_follow_up_questions(
                original_question=previous_question.question_text,
                candidate_response=previous_response,
                num_questions=1
            )
            
            if not follow_up_result.success:
                return OrchestrationResult(
                    success=False,
                    error=follow_up_result.error or "Failed to generate follow-up question"
                )
            
            follow_up_questions = follow_up_result.data.get("follow_up_questions", [])
            
            if not follow_up_questions:
                return OrchestrationResult(
                    success=False,
                    error="No follow-up questions generated"
                )
            
            # For now, return the first follow-up question
            # In a real implementation, we might create a new session with this question
            
            return OrchestrationResult(
                success=True,
                question={
                    "text": follow_up_questions[0],
                    "type": "follow_up",
                    "original_question_id": previous_question_id
                },
                metadata={
                    "candidate_id": candidate_id,
                    "question_type": "follow_up",
                    "source": "generated"
                }
            )
            
        except Exception as e:
            logger.error(f"Error getting follow-up question: {e}")
            return OrchestrationResult(success=False, error=str(e))
    
    async def generate_improvement_plan(
        self,
        candidate_id: int,
        num_sessions: int = 5
    ) -> OrchestrationResult:
        """Generate a comprehensive improvement plan based on multiple sessions"""
        try:
            # Get candidate's recent feedback
            feedbacks = await FeedbackService.get_feedback_by_candidate(candidate_id, page_size=num_sessions)
            
            if not feedbacks:
                return OrchestrationResult(
                    success=False,
                    error="No feedback data available for candidate"
                )
            
            # Get candidate info
            candidate = await CandidateService.get_candidate(candidate_id)
            
            # Analyze patterns across feedback
            all_strengths = []
            all_weaknesses = []
            all_scores = {
                "relevance": [],
                "clarity": [],
                "structure": [],
                "completeness": [],
                "communication": [],
                "overall": []
            }
            
            for feedback in feedbacks:
                all_strengths.extend(feedback.strengths)
                all_weaknesses.extend(feedback.weaknesses)
                
                all_scores["relevance"].append(feedback.relevance_score)
                all_scores["clarity"].append(feedback.clarity_score)
                all_scores["structure"].append(feedback.structure_score)
                all_scores["completeness"].append(feedback.completeness_score)
                all_scores["communication"].append(feedback.communication_score)
                all_scores["overall"].append(feedback.overall_score)
            
            # Calculate average scores
            avg_scores = {k: sum(v) / len(v) for k, v in all_scores.items()}
            
            # Identify common strengths and weaknesses
            strength_counts = {}
            for strength in all_strengths:
                strength_counts[strength] = strength_counts.get(strength, 0) + 1
            
            weakness_counts = {}
            for weakness in all_weaknesses:
                weakness_counts[weakness] = weakness_counts.get(weakness, 0) + 1
            
            common_strengths = [s for s, count in strength_counts.items() if count >= 2]
            common_weaknesses = [w for w, count in weakness_counts.items() if count >= 2]
            
            # Generate improvement plan
            improvement_plan = {
                "candidate_id": candidate_id,
                "target_role": candidate.target_role if candidate else "",
                "average_scores": avg_scores,
                "common_strengths": common_strengths,
                "common_weaknesses": common_weaknesses,
                "focus_areas": common_weaknesses[:3],  # Top 3 weaknesses to focus on
                "recommended_actions": [],
                "estimated_improvement_timeline": "4-6 weeks"
            }
            
            # Generate recommended actions
            if "communication" in common_weaknesses or avg_scores["clarity"] < 70:
                improvement_plan["recommended_actions"].append(
                    "Practice clear and concise communication with daily exercises"
                )
            
            if "structure" in common_weaknesses or avg_scores["structure"] < 70:
                improvement_plan["recommended_actions"].append(
                    "Learn and practice the STAR method for behavioral questions"
                )
            
            if avg_scores["relevance"] < 70 or avg_scores["completeness"] < 70:
                improvement_plan["recommended_actions"].append(
                    "Focus on directly addressing the question and providing complete answers"
                )
            
            if not improvement_plan["recommended_actions"]:
                improvement_plan["recommended_actions"].append(
                    "Continue practicing to maintain and improve your interview skills"
                )
            
            return OrchestrationResult(
                success=True,
                improvement_plan=improvement_plan,
                metadata={
                    "candidate_id": candidate_id,
                    "sessions_analyzed": len(feedbacks),
                    "analysis_type": "multi_session"
                }
            )
            
        except Exception as e:
            logger.error(f"Error generating improvement plan: {e}")
            return OrchestrationResult(success=False, error=str(e))
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get the status of all agents"""
        return {
            "agents": {
                "question_agent": {"status": "ready", "type": "question_selection"},
                "communication_agent": {"status": "ready", "type": "communication_analysis"},
                "content_agent": {"status": "ready", "type": "content_evaluation"},
                "star_agent": {"status": "ready", "type": "star_analysis"},
                "coach_agent": {"status": "ready", "type": "coaching_consolidation"}
            },
            "all_ready": True,
            "timestamp": datetime.now().isoformat()
        }
    
    async def close(self):
        """Clean up all agents"""
        try:
            tasks = [agent.close() for agent in self.agents.values()]
            await asyncio.gather(*tasks)
            logger.info("All agents closed successfully")
            
        except Exception as e:
            logger.error(f"Error closing agents: {e}")
