"""
Coach Agent for Interview Coach
Consolidates outputs from specialist agents and generates personalized coaching feedback
"""

import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from .base_agent import BaseAgent, AgentResult
from .question_agent import QuestionAgent
from .communication_agent import CommunicationAgent
from .content_agent import ContentAgent
from .star_agent import STARAgent

logger = logging.getLogger(__name__)


class CoachAgent(BaseAgent):
    """Agent for consolidating feedback and generating coaching recommendations"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Coach Agent"""
        super().__init__("coach_agent", config)
        self.question_agent = QuestionAgent()
        self.communication_agent = CommunicationAgent()
        self.content_agent = ContentAgent()
        self.star_agent = STARAgent()
    
    async def get_system_prompt(self) -> str:
        """Get the system prompt for the Coach Agent"""
        return """
        You are an Interview Coach Agent. Your role is to consolidate feedback from multiple
        specialist agents and generate comprehensive, personalized coaching feedback.
        
        Your responsibilities:
        1. Analyze feedback from all specialist agents (Question, Communication, Content, STAR)
        2. Identify patterns and recurring issues across multiple responses
        3. Generate a holistic assessment of the candidate's performance
        4. Create personalized improvement recommendations
        5. Develop follow-up questions to address identified gaps
        6. Generate an overall improvement plan
        
        Coaching Approach:
        - Be constructive and encouraging
        - Provide specific, actionable feedback
        - Focus on both strengths and areas for improvement
        - Tailor recommendations to the candidate's target role and experience level
        - Identify patterns across multiple practice sessions
        
        Output format:
        {
            "overall_score": 0-100,
            "performance_summary": "Brief summary of overall performance",
            "agent_feedback_summary": {
                "communication": {"score": 0-100, "strengths": [], "weaknesses": [], "suggestions": []},
                "content": {"score": 0-100, "strengths": [], "weaknesses": [], "suggestions": []},
                "star": {"score": 0-100, "strengths": [], "weaknesses": [], "suggestions": []}
            },
            "recurring_patterns": [
                {"pattern": "pattern description", "frequency": "high|medium|low", "impact": "positive|negative"}
            ],
            "personalized_recommendations": [
                {"area": "area to improve", "action": "specific action", "priority": "high|medium|low"}
            ],
            "follow_up_questions": ["question 1", "question 2"],
            "improvement_plan": {
                "short_term": ["action 1", "action 2"],
                "medium_term": ["action 1", "action 2"],
                "long_term": ["action 1", "action 2"]
            },
            "improved_response_example": "Example of how to improve a response",
            "motivational_feedback": "Encouraging message for the candidate"
        }
        """
    
    def get_required_fields(self) -> List[str]:
        """Get required fields for input validation"""
        return ["candidate_id", "response_text", "question", "feedback_data"]
    
    async def analyze(self, input_data: Dict[str, Any]) -> AgentResult:
        """Analyze and consolidate feedback from all agents"""
        try:
            # Validate input
            if not await self._validate_input(input_data):
                return AgentResult(
                    agent_type=self.agent_type,
                    success=False,
                    error="Invalid input: missing required fields"
                )
            
            candidate_id = input_data.get("candidate_id")
            response_text = input_data.get("response_text", "")
            question = input_data.get("question", "")
            feedback_data = input_data.get("feedback_data", {})
            candidate_info = input_data.get("candidate_info", {})
            
            # If we have individual agent feedback, use it
            if feedback_data:
                agent_feedback = feedback_data.get("agent_feedback", {})
                communication_feedback = agent_feedback.get("communication", {})
                content_feedback = agent_feedback.get("content", {})
                star_feedback = agent_feedback.get("star", {})
            else:
                # Run all agents to get fresh feedback
                logger.info("Running all specialist agents for comprehensive analysis")
                
                # Communication analysis
                comm_input = {
                    "response_text": response_text,
                    "question": question,
                    "candidate_info": candidate_info
                }
                comm_result = await self.communication_agent.analyze(comm_input)
                communication_feedback = comm_result.data if comm_result.success else {}
                
                # Content analysis
                content_input = {
                    "response_text": response_text,
                    "question": question,
                    "expected_competency": candidate_info.get("target_role", ""),
                    "role": candidate_info.get("target_role", "")
                }
                content_result = await self.content_agent.analyze(content_input)
                content_feedback = content_result.data if content_result.success else {}
                
                # STAR analysis
                star_input = {
                    "response_text": response_text,
                    "question": question
                }
                star_result = await self.star_agent.analyze(star_input)
                star_feedback = star_result.data if star_result.success else {}
            
            # Consolidate all feedback
            consolidated_feedback = await self._consolidate_feedback(
                communication_feedback,
                content_feedback,
                star_feedback,
                candidate_info,
                response_text,
                question
            )
            
            return AgentResult(
                agent_type=self.agent_type,
                success=True,
                data=consolidated_feedback,
                confidence=0.95,
                metadata={
                    "input": input_data,
                    "method": "consolidated",
                    "agents_used": ["communication", "content", "star"]
                }
            )
            
        except Exception as e:
            logger.error(f"Error in CoachAgent.analyze: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                success=False,
                error=str(e)
            )
    
    async def _consolidate_feedback(
        self,
        communication_feedback: Dict[str, Any],
        content_feedback: Dict[str, Any],
        star_feedback: Dict[str, Any],
        candidate_info: Dict[str, Any],
        response_text: str,
        question: str
    ) -> Dict[str, Any]:
        """Consolidate feedback from all agents"""
        
        # Extract scores from each agent
        comm_scores = communication_feedback.get("scores", {})
        content_scores = content_feedback.get("scores", {})
        star_scores = star_feedback.get("scores", {})
        
        # Calculate overall score (weighted average)
        # Communication: 30%, Content: 40%, STAR: 30%
        comm_weight = 0.3
        content_weight = 0.4
        star_weight = 0.3
        
        # Get overall scores from each agent
        comm_overall = comm_scores.get("overall_communication_score", 50.0)
        content_overall = content_scores.get("overall_content_score", 50.0)
        star_overall = star_scores.get("overall_star_score", 50.0)
        
        overall_score = round(
            (comm_overall * comm_weight) + 
            (content_overall * content_weight) + 
            (star_overall * star_weight),
            2
        )
        
        # Generate performance summary
        performance_summary = await self._generate_performance_summary(
            overall_score, comm_scores, content_scores, star_scores
        )
        
        # Consolidate agent feedback
        agent_feedback_summary = {
            "communication": {
                "score": comm_overall,
                "strengths": communication_feedback.get("strengths", []),
                "weaknesses": communication_feedback.get("weaknesses", []),
                "suggestions": communication_feedback.get("suggestions", [])
            },
            "content": {
                "score": content_overall,
                "strengths": content_feedback.get("strengths", []),
                "weaknesses": content_feedback.get("weaknesses", []),
                "suggestions": content_feedback.get("suggestions", []),
                "addresses_question": content_feedback.get("addresses_question", True)
            },
            "star": {
                "score": star_overall,
                "strengths": star_feedback.get("strengths", []),
                "weaknesses": star_feedback.get("weaknesses", []),
                "suggestions": star_feedback.get("suggestions", []),
                "uses_star_structure": star_feedback.get("uses_star_structure", False),
                "missing_components": star_feedback.get("missing_components", [])
            }
        }
        
        # Identify recurring patterns (simplified for single response)
        recurring_patterns = await self._identify_patterns(
            communication_feedback, content_feedback, star_feedback
        )
        
        # Generate personalized recommendations
        recommendations = await self._generate_recommendations(
            overall_score,
            agent_feedback_summary,
            candidate_info,
            response_text,
            question
        )
        
        # Generate follow-up questions
        follow_up_questions = await self._generate_follow_up_questions(
            question, response_text, content_feedback
        )
        
        # Generate improvement plan
        improvement_plan = await self._generate_improvement_plan(
            overall_score,
            agent_feedback_summary,
            candidate_info
        )
        
        # Generate improved response example
        improved_response = await self._generate_improved_response(
            question, response_text, agent_feedback_summary
        )
        
        # Generate motivational feedback
        motivational_feedback = await self._generate_motivational_feedback(overall_score)
        
        return {
            "overall_score": overall_score,
            "performance_summary": performance_summary,
            "agent_feedback_summary": agent_feedback_summary,
            "recurring_patterns": recurring_patterns,
            "personalized_recommendations": recommendations,
            "follow_up_questions": follow_up_questions,
            "improvement_plan": improvement_plan,
            "improved_response_example": improved_response,
            "motivational_feedback": motivational_feedback,
            "detailed_scores": {
                "communication": comm_scores,
                "content": content_scores,
                "star": star_scores
            }
        }
    
    async def _generate_performance_summary(
        self,
        overall_score: float,
        comm_scores: Dict[str, float],
        content_scores: Dict[str, float],
        star_scores: Dict[str, float]
    ) -> str:
        """Generate a performance summary"""
        
        # Determine performance level
        if overall_score >= 90:
            level = "Excellent"
            description = "Your response demonstrates strong communication skills, relevant content, and good structure."
        elif overall_score >= 80:
            level = "Good"
            description = "Your response is solid with good communication and content, but there are areas for improvement."
        elif overall_score >= 70:
            level = "Satisfactory"
            description = "Your response addresses the question but needs improvement in communication, content, or structure."
        elif overall_score >= 60:
            level = "Developing"
            description = "Your response shows potential but needs significant improvement in multiple areas."
        else:
            level = "Needs Improvement"
            description = "Your response requires substantial work to meet expectations."
        
        # Identify top strengths
        strengths = []
        if comm_scores.get("clarity_score", 0) >= 80:
            strengths.append("clear communication")
        if content_scores.get("relevance_score", 0) >= 80:
            strengths.append("relevant content")
        if star_scores.get("overall_star_score", 0) >= 80:
            strengths.append("good use of STAR method")
        
        # Identify top areas for improvement
        improvements = []
        if comm_scores.get("clarity_score", 0) < 70:
            improvements.append("clarity")
        if content_scores.get("relevance_score", 0) < 70:
            improvements.append("relevance")
        if star_scores.get("overall_star_score", 0) < 70:
            improvements.append("structure (STAR)")
        
        summary = f"{level} ({overall_score}/100): {description}"
        
        if strengths:
            summary += f" Strengths include: {', '.join(strengths)}."
        if improvements:
            summary += f" Focus on improving: {', '.join(improvements)}."
        
        return summary
    
    async def _identify_patterns(
        self,
        communication_feedback: Dict[str, Any],
        content_feedback: Dict[str, Any],
        star_feedback: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify recurring patterns across feedback"""
        patterns = []
        
        # Check for common issues
        comm_weaknesses = communication_feedback.get("weaknesses", [])
        content_weaknesses = content_feedback.get("weaknesses", [])
        star_weaknesses = star_feedback.get("weaknesses", [])
        
        all_weaknesses = comm_weaknesses + content_weaknesses + star_weaknesses
        
        # Count occurrences
        weakness_counts = {}
        for weakness in all_weaknesses:
            weakness_lower = weakness.lower()
            weakness_counts[weakness_lower] = weakness_counts.get(weakness_lower, 0) + 1
        
        # Identify patterns (simplified)
        for weakness, count in weakness_counts.items():
            if count >= 2:  # Appears in at least 2 agents
                frequency = "high" if count >= 3 else "medium"
                patterns.append({
                    "pattern": weakness,
                    "frequency": frequency,
                    "impact": "negative",
                    "source_agents": count
                })
        
        # Check for common strengths
        comm_strengths = communication_feedback.get("strengths", [])
        content_strengths = content_feedback.get("strengths", [])
        star_strengths = star_feedback.get("strengths", [])
        
        all_strengths = comm_strengths + content_strengths + star_strengths
        
        strength_counts = {}
        for strength in all_strengths:
            strength_lower = strength.lower()
            strength_counts[strength_lower] = strength_counts.get(strength_lower, 0) + 1
        
        for strength, count in strength_counts.items():
            if count >= 2:
                frequency = "high" if count >= 3 else "medium"
                patterns.append({
                    "pattern": strength,
                    "frequency": frequency,
                    "impact": "positive",
                    "source_agents": count
                })
        
        return patterns
    
    async def _generate_recommendations(
        self,
        overall_score: float,
        agent_feedback: Dict[str, Any],
        candidate_info: Dict[str, Any],
        response_text: str,
        question: str
    ) -> List[Dict[str, Any]]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Communication recommendations
        comm_feedback = agent_feedback.get("communication", {})
        if comm_feedback.get("score", 100) < 80:
            for suggestion in comm_feedback.get("suggestions", []):
                recommendations.append({
                    "area": "communication",
                    "action": suggestion,
                    "priority": "high" if comm_feedback.get("score", 0) < 60 else "medium"
                })
        
        # Content recommendations
        content_feedback = agent_feedback.get("content", {})
        if content_feedback.get("score", 100) < 80:
            for suggestion in content_feedback.get("suggestions", []):
                recommendations.append({
                    "area": "content",
                    "action": suggestion,
                    "priority": "high" if content_feedback.get("score", 0) < 60 else "medium"
                })
        
        # STAR recommendations
        star_feedback = agent_feedback.get("star", {})
        if star_feedback.get("score", 100) < 80:
            for suggestion in star_feedback.get("suggestions", []):
                recommendations.append({
                    "area": "structure",
                    "action": suggestion,
                    "priority": "high" if star_feedback.get("score", 0) < 60 else "medium"
                })
        
        # Add general recommendations based on score
        if overall_score < 70:
            recommendations.append({
                "area": "overall",
                "action": "Practice with a variety of question types to build confidence",
                "priority": "high"
            })
        
        if overall_score >= 80:
            recommendations.append({
                "area": "overall",
                "action": "Focus on refining and polishing your responses",
                "priority": "medium"
            })
        
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        recommendations.sort(key=lambda x: priority_order.get(x["priority"], 2))
        
        return recommendations
    
    async def _generate_follow_up_questions(
        self,
        question: str,
        response_text: str,
        content_feedback: Dict[str, Any]
    ) -> List[str]:
        """Generate follow-up questions"""
        questions = []
        
        # If response doesn't fully address the question
        if not content_feedback.get("addresses_question", True):
            questions.append(f"Can you clarify how your experience relates to {question}?")
        
        # If STAR structure is missing components
        missing_components = content_feedback.get("missing_components", [])
        if "action" in missing_components:
            questions.append("What specific actions did you take to address the situation?")
        if "result" in missing_components:
            questions.append("What was the outcome of your actions?")
        
        # Add a general follow-up
        questions.append("Can you provide more details about your approach?")
        
        # Limit to 3 questions
        return questions[:3]
    
    async def _generate_improvement_plan(
        self,
        overall_score: float,
        agent_feedback: Dict[str, Any],
        candidate_info: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Generate an improvement plan"""
        
        short_term = []
        medium_term = []
        long_term = []
        
        # Communication improvements
        comm_score = agent_feedback.get("communication", {}).get("score", 100)
        if comm_score < 80:
            short_term.append("Practice clear and concise communication daily")
            medium_term.append("Record and review your responses for clarity")
        
        # Content improvements
        content_score = agent_feedback.get("content", {}).get("score", 100)
        if content_score < 80:
            short_term.append("Ensure your responses directly address the question")
            medium_term.append("Research common interview questions for your target role")
        
        # STAR improvements
        star_score = agent_feedback.get("star", {}).get("score", 100)
        if star_score < 80:
            short_term.append("Practice using the STAR method for behavioral questions")
            medium_term.append("Review STAR examples and templates")
            long_term.append("Develop a library of STAR stories for common competencies")
        
        # General improvements based on overall score
        if overall_score < 70:
            short_term.append("Complete daily interview practice sessions")
            medium_term.append("Work with a mentor or coach for personalized feedback")
            long_term.append("Build experience in areas where you're weakest")
        elif overall_score < 85:
            short_term.append("Focus on refining your strongest responses")
            medium_term.append("Practice with more challenging questions")
        else:
            short_term.append("Continue practicing to maintain your strong performance")
            medium_term.append("Prepare for advanced or role-specific questions")
        
        return {
            "short_term": short_term[:3],
            "medium_term": medium_term[:3],
            "long_term": long_term[:2]
        }
    
    async def _generate_improved_response(
        self,
        question: str,
        original_response: str,
        agent_feedback: Dict[str, Any]
    ) -> str:
        """Generate an improved response example"""
        
        # Use the STAR agent to generate an example
        star_example = await self.star_agent.generate_star_example(question)
        
        if isinstance(star_example, dict) and "response" in star_example:
            return star_example["response"]
        
        # Fallback: create a simple improved response
        return f"[Improved response based on feedback for: {question}]"
    
    async def _generate_motivational_feedback(self, overall_score: float) -> str:
        """Generate motivational feedback"""
        
        if overall_score >= 90:
            return "Excellent work! You're demonstrating strong interview skills. Keep practicing to maintain this high level of performance."
        elif overall_score >= 80:
            return "Good job! You're on the right track. With continued practice, you'll see even more improvement."
        elif overall_score >= 70:
            return "You're making good progress! Focus on the feedback provided to address the remaining gaps."
        elif overall_score >= 60:
            return "You're developing your interview skills. Keep practicing and applying the feedback to see improvement."
        else:
            return "Everyone starts somewhere! Use this as a learning opportunity. The feedback provided will help you improve significantly with practice."
    
    async def generate_session_summary(
        self,
        candidate_id: int,
        session_data: Dict[str, Any]
    ) -> AgentResult:
        """Generate a summary for a complete practice session"""
        try:
            # This would consolidate feedback from multiple responses in a session
            # For now, return a basic result
            
            result_data = {
                "session_summary": "Summary of practice session",
                "key_achievements": ["Completed practice questions", "Received detailed feedback"],
                "areas_to_focus": ["Communication clarity", "STAR structure"],
                "next_steps": ["Review feedback", "Practice follow-up questions"]
            }
            
            return AgentResult(
                agent_type=self.agent_type,
                success=True,
                data=result_data,
                confidence=0.9
            )
            
        except Exception as e:
            logger.error(f"Error generating session summary: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                success=False,
                error=str(e)
            )
