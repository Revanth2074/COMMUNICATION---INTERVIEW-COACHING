"""
Question Agent for Interview Coach
Selects or generates suitable interview questions based on candidate's target role and competency
"""

import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from .base_agent import BaseAgent, AgentResult
from ..services.question_service import QuestionService
from ..models.question import Question

logger = logging.getLogger(__name__)


class QuestionAgent(BaseAgent):
    """Agent for selecting and generating interview questions"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Question Agent"""
        super().__init__("question_agent", config)
        self.question_service = QuestionService
    
    async def get_system_prompt(self) -> str:
        """Get the system prompt for the Question Agent"""
        return """
        You are an Interview Question Agent. Your role is to select or generate suitable 
        interview questions based on the candidate's target role, competencies, and experience level.
        
        Guidelines:
        1. Select questions that are relevant to the candidate's target role
        2. Consider the candidate's experience level when choosing difficulty
        3. Cover a variety of question types (behavioral, technical, situational)
        4. Ensure questions assess the specified competencies
        5. Provide questions that will help assess the candidate's fit for the role
        
        Output format:
        {
            "question": "The interview question text",
            "role": "Target role",
            "competency": "Competency being assessed",
            "difficulty": "easy|medium|hard",
            "question_type": "behavioral|technical|situational|general",
            "expected_competency": "What the question aims to assess",
            "evaluation_criteria": ["list", "of", "criteria"]
        }
        """
    
    def get_required_fields(self) -> List[str]:
        """Get required fields for input validation"""
        return ["candidate_id"]
    
    async def analyze(self, input_data: Dict[str, Any]) -> AgentResult:
        """Analyze input and select/generate appropriate questions"""
        try:
            # Validate input
            if not await self._validate_input(input_data):
                return AgentResult(
                    agent_type=self.agent_type,
                    success=False,
                    error="Invalid input: missing required fields"
                )
            
            candidate_id = input_data.get("candidate_id")
            target_role = input_data.get("target_role")
            competency = input_data.get("competency")
            difficulty = input_data.get("difficulty", "medium")
            question_type = input_data.get("question_type")
            num_questions = input_data.get("num_questions", 1)
            
            # Try to get questions from database first
            questions = []
            
            if candidate_id:
                # Get candidate info to determine role and competencies
                from ..services.candidate_service import CandidateService
                candidate = await CandidateService.get_candidate(candidate_id)
                if candidate:
                    target_role = target_role or candidate.target_role
                    # Use first competency if not specified
                    if not competency and candidate.competencies:
                        competency = candidate.competencies[0]
            
            # Get questions from database
            db_questions = await QuestionService.get_questions_by_filters(
                role=target_role,
                competency=competency,
                difficulty=difficulty,
                question_type=question_type,
                page_size=num_questions * 2  # Get extra to choose from
            )
            
            if db_questions:
                # Select the best questions
                questions = db_questions[:num_questions]
            else:
                # Generate questions using LLM
                logger.info("Generating questions with LLM")
                
                prompt = f"""
                Generate {num_questions} interview question(s) for a {target_role} role.
                Focus on {competency or 'general'} competency.
                Difficulty: {difficulty}
                Question type: {question_type or 'any'}
                
                Return in JSON format with the structure specified in the system prompt.
                """
                
                system_prompt = await self.get_system_prompt()
                response = await self._generate_llm_response(prompt, system_prompt)
                
                # Parse response
                if isinstance(response, dict) and "question" in response:
                    # Single question
                    questions = [Question(**response)]
                elif isinstance(response, list):
                    # Multiple questions
                    questions = [Question(**q) for q in response]
            
            # Format result
            result_data = {
                "questions": [
                    {
                        "id": q.id if hasattr(q, 'id') else None,
                        "text": q.question_text,
                        "role": q.role,
                        "competency": q.competency,
                        "difficulty": q.difficulty,
                        "type": q.question_type,
                        "expected_competency": q.expected_competency,
                        "evaluation_criteria": q.evaluation_criteria
                    }
                    for q in questions
                ],
                "count": len(questions),
                "source": "database" if db_questions else "generated"
            }
            
            return AgentResult(
                agent_type=self.agent_type,
                success=True,
                data=result_data,
                confidence=0.95 if db_questions else 0.85,
                metadata={
                    "input": input_data,
                    "method": "database" if db_questions else "llm"
                }
            )
            
        except Exception as e:
            logger.error(f"Error in QuestionAgent.analyze: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                success=False,
                error=str(e)
            )
    
    async def get_random_question(
        self,
        candidate_id: Optional[int] = None,
        target_role: Optional[str] = None,
        competency: Optional[str] = None,
        difficulty: str = "medium"
    ) -> AgentResult:
        """Get a random question for practice"""
        try:
            input_data = {
                "candidate_id": candidate_id,
                "target_role": target_role,
                "competency": competency,
                "difficulty": difficulty,
                "num_questions": 1
            }
            
            result = await self.analyze(input_data)
            
            if result.success and result.data.get("questions"):
                question_data = result.data["questions"][0]
                
                # Try to get full question from database if ID exists
                if question_data.get("id"):
                    db_question = await QuestionService.get_question(question_data["id"])
                    if db_question:
                        question_data["text"] = db_question.question_text
                        question_data["role"] = db_question.role
                        question_data["competency"] = db_question.competency
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting random question: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                success=False,
                error=str(e)
            )
    
    async def get_follow_up_questions(
        self,
        original_question: str,
        candidate_response: str,
        num_questions: int = 2
    ) -> AgentResult:
        """Generate follow-up questions based on candidate's response"""
        try:
            prompt = f"""
            Based on the following interview question and candidate response,
            generate {num_questions} follow-up questions that would help assess the candidate further.
            
            Question: {original_question}
            Response: {candidate_response}
            
            The follow-up questions should:
            1. Dig deeper into the candidate's experience or knowledge
            2. Clarify any ambiguous points in the response
            3. Assess additional competencies related to the original question
            4. Be specific and targeted
            
            Return in JSON format:
            {{
                "follow_up_questions": ["question 1", "question 2"]
            }}
            """
            
            system_prompt = await self.get_system_prompt()
            response = await self._generate_llm_response(prompt, system_prompt)
            
            return AgentResult(
                agent_type=self.agent_type,
                success=True,
                data=response,
                confidence=0.85,
                metadata={"type": "follow_up"}
            )
            
        except Exception as e:
            logger.error(f"Error generating follow-up questions: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                success=False,
                error=str(e)
            )
