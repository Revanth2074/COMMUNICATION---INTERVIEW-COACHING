"""
STAR Agent for Interview Coach
Evaluates behavioral responses using Situation, Task, Action, Result structure
"""

import logging
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
from .base_agent import BaseAgent, AgentResult
import re

logger = logging.getLogger(__name__)


class STARAgent(BaseAgent):
    """Agent for evaluating STAR method compliance"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the STAR Agent"""
        super().__init__("star_agent", config)
    
    async def get_system_prompt(self) -> str:
        """Get the system prompt for the STAR Agent"""
        return """
        You are a STAR Method Evaluation Agent. Your role is to evaluate behavioral interview
        responses using the STAR framework: Situation, Task, Action, Result.
        
        STAR Framework:
        - Situation: Describe the context and background
        - Task: Explain your responsibility or goal
        - Action: Detail what you did (focus on your actions)
        - Result: Share the outcome and impact
        
        Evaluation Criteria:
        1. Situation Quality (0-100): Is the situation clearly described?
           - Specific context and background
           - Relevant to the question
        2. Task Quality (0-100): Is the task or goal clearly stated?
           - Clear responsibility or objective
           - Appropriate scope
        3. Action Quality (0-100): Are the actions clearly described?
           - Focus on candidate's actions (not team)
           - Specific and detailed
           - Shows problem-solving and initiative
        4. Result Quality (0-100): Are the results clearly stated?
           - Specific outcomes and impact
           - Quantifiable results where possible
           - Connection to the situation and task
        
        Overall STAR Score: Average of all four components
        Uses STAR Structure: Whether all components are present and identifiable
        
        Output format:
        {
            "situation_score": 0-100,
            "task_score": 0-100,
            "action_score": 0-100,
            "result_score": 0-100,
            "overall_star_score": 0-100,
            "uses_star_structure": true/false,
            "missing_components": ["situation", "task", "action", "result"],
            "star_breakdown": {
                "situation": {"text": "...", "score": 0-100},
                "task": {"text": "...", "score": 0-100},
                "action": {"text": "...", "score": 0-100},
                "result": {"text": "...", "score": 0-100}
            },
            "strengths": ["list", "of", "strengths"],
            "weaknesses": ["list", "of", "weaknesses"],
            "suggestions": ["list", "of", "suggestions"],
            "detailed_analysis": "Detailed analysis of STAR compliance"
        }
        """
    
    def get_required_fields(self) -> List[str]:
        """Get required fields for input validation"""
        return ["response_text", "question"]
    
    async def analyze(self, input_data: Dict[str, Any]) -> AgentResult:
        """Analyze the STAR compliance of a response"""
        try:
            # Validate input
            if not await self._validate_input(input_data):
                return AgentResult(
                    agent_type=self.agent_type,
                    success=False,
                    error="Invalid input: missing required fields (response_text, question)"
                )
            
            response_text = input_data.get("response_text", "")
            question = input_data.get("question", "")
            
            # Extract STAR components using rule-based analysis
            star_components = self._extract_star_components(response_text)
            rule_based_scores = self._calculate_rule_based_scores(star_components)
            
            # Generate LLM-based analysis
            system_prompt = await self.get_system_prompt()
            
            prompt = f"""
            Analyze the following interview response for STAR method compliance:
            
            Question: {question}
            Response: {response_text}
            
            Evaluate based on the STAR framework and criteria in the system prompt.
            Identify each STAR component and provide detailed feedback.
            """
            
            llm_response = await self._generate_llm_response(prompt, system_prompt)
            
            # Combine analysis
            combined_result = self._combine_analysis(star_components, rule_based_scores, llm_response)
            
            return AgentResult(
                agent_type=self.agent_type,
                success=True,
                data=combined_result,
                confidence=0.9,
                metadata={
                    "input": input_data,
                    "method": "hybrid",
                    "star_components": star_components
                }
            )
            
        except Exception as e:
            logger.error(f"Error in STARAgent.analyze: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                success=False,
                error=str(e)
            )
    
    def _extract_star_components(self, text: str) -> Dict[str, Any]:
        """Extract STAR components from text using pattern matching"""
        text_lower = text.lower()
        
        # Patterns for identifying STAR components
        situation_patterns = [
            r'when\s+I\s+was\s+at\s+\w+',
            r'while\s+working\s+at\s+\w+',
            r'in\s+my\s+previous\s+role\s+at\s+\w+',
            r'at\s+\w+\s+I\s+was\s+responsible\s+for',
            r'during\s+my\s+time\s+at\s+\w+',
            r'the\s+situation\s+was',
            r'context\s+was'
        ]
        
        task_patterns = [
            r'my\s+task\s+was\s+to',
            r'I\s+was\s+responsible\s+for',
            r'my\s+goal\s+was\s+to',
            r'I\s+needed\s+to',
            r'my\s+objective\s+was',
            r'the\s+challenge\s+was\s+to',
            r'the\s+task\s+was'
        ]
        
        action_patterns = [
            r'I\s+\w+ed\s+',  # I developed, I created, I managed, etc.
            r'I\s+\w+\s+',    # I implemented, I designed, etc.
            r'what\s+I\s+did\s+was',
            r'I\s+took\s+the\s+following\s+actions',
            r'I\s+decided\s+to',
            r'I\s+initially',
            r'my\s+actions\s+were'
        ]
        
        result_patterns = [
            r'as\s+a\s+result',
            r'this\s+resulted\s+in',
            r'the\s+outcome\s+was',
            r'we\s+achieved',
            r'I\s+successfully',
            r'this\s+led\s+to',
            r'the\s+impact\s+was',
            r'finally',
            r'in\s+the\s+end'
        ]
        
        # Extract components
        components = {
            "situation": self._extract_with_patterns(text, situation_patterns),
            "task": self._extract_with_patterns(text, task_patterns),
            "action": self._extract_with_patterns(text, action_patterns),
            "result": self._extract_with_patterns(text, result_patterns)
        }
        
        # Check which components are present
        present_components = [
            comp for comp in ["situation", "task", "action", "result"] 
            if components[comp]["text"]
        ]
        
        components["present_components"] = present_components
        components["uses_star_structure"] = len(present_components) >= 3  # At least 3 for partial STAR
        
        return components
    
    def _extract_with_patterns(self, text: str, patterns: List[str]) -> Dict[str, Any]:
        """Extract text matching any of the patterns"""
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Get the sentence containing the match
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                
                # Find sentence boundaries
                sentence_start = max(0, context.rfind('.', 0, match.start() - start) + 1)
                sentence_end = context.find('.', match.end() - start)
                if sentence_end == -1:
                    sentence_end = len(context)
                
                sentence = context[sentence_start:sentence_end].strip()
                
                return {
                    "text": sentence,
                    "pattern": pattern,
                    "start": match.start(),
                    "end": match.end()
                }
        
        return {"text": "", "pattern": None, "start": -1, "end": -1}
    
    def _calculate_rule_based_scores(self, components: Dict[str, Any]) -> Dict[str, float]:
        """Calculate scores based on extracted components"""
        scores = {}
        
        # Base scores for each component
        for comp in ["situation", "task", "action", "result"]:
            if components[comp]["text"]:
                # Longer, more detailed text gets higher score
                text_length = len(components[comp]["text"].split())
                score = min(100, text_length * 5)  # ~20 words = 100
                scores[f"{comp}_score"] = round(score, 2)
            else:
                scores[f"{comp}_score"] = 0.0
        
        # Overall STAR score
        present_count = len(components.get("present_components", []))
        overall = (sum(scores.values()) / 4) * (present_count / 4)  # Penalize for missing components
        scores["overall_star_score"] = round(overall, 2)
        
        return scores
    
    def _combine_analysis(
        self,
        components: Dict[str, Any],
        rule_scores: Dict[str, float],
        llm_response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Combine rule-based and LLM analysis"""
        combined = {
            "scores": rule_scores,
            "star_breakdown": {},
            "uses_star_structure": components.get("uses_star_structure", False),
            "missing_components": [
                comp for comp in ["situation", "task", "action", "result"] 
                if comp not in components.get("present_components", [])
            ]
        }
        
        # Build STAR breakdown
        for comp in ["situation", "task", "action", "result"]:
            combined["star_breakdown"][comp] = {
                "text": components[comp]["text"],
                "detected": comp in components.get("present_components", []),
                "score": rule_scores.get(f"{comp}_score", 0.0)
            }
        
        # Incorporate LLM analysis
        if isinstance(llm_response, dict):
            combined["analysis"] = llm_response
            
            # Override scores if LLM provides them
            if "situation_score" in llm_response:
                combined["scores"]["situation_score"] = llm_response["situation_score"]
            if "task_score" in llm_response:
                combined["scores"]["task_score"] = llm_response["task_score"]
            if "action_score" in llm_response:
                combined["scores"]["action_score"] = llm_response["action_score"]
            if "result_score" in llm_response:
                combined["scores"]["result_score"] = llm_response["result_score"]
            if "overall_star_score" in llm_response:
                combined["scores"]["overall_star_score"] = llm_response["overall_star_score"]
            
            # Update other fields from LLM
            if "uses_star_structure" in llm_response:
                combined["uses_star_structure"] = llm_response["uses_star_structure"]
            if "missing_components" in llm_response:
                combined["missing_components"] = llm_response["missing_components"]
            
            # Add strengths, weaknesses, suggestions
            combined["strengths"] = llm_response.get("strengths", [])
            combined["weaknesses"] = llm_response.get("weaknesses", [])
            combined["suggestions"] = llm_response.get("suggestions", [])
        else:
            combined["strengths"] = []
            combined["weaknesses"] = []
            combined["suggestions"] = []
        
        return combined
    
    async def generate_star_example(self, question: str) -> Dict[str, Any]:
        """Generate an example STAR response for a question"""
        try:
            prompt = f"""
            Generate an example STAR response for the following interview question:
            
            Question: {question}
            
            Create a well-structured response that includes:
            - Situation: Clear context and background
            - Task: Specific responsibility or goal
            - Action: Detailed actions taken (focus on individual contributions)
            - Result: Specific outcomes and impact
            
            Format the response clearly with STAR labels.
            """
            
            system_prompt = await self.get_system_prompt()
            response = await self._generate_llm_response(prompt, system_prompt)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating STAR example: {e}")
            return {"error": str(e)}
    
    async def improve_star_response(self, original_response: str, question: str) -> Dict[str, Any]:
        """Suggest improvements to make a response more STAR-compliant"""
        try:
            prompt = f"""
            The following response to an interview question needs improvement to better
            follow the STAR method:
            
            Question: {question}
            Original Response: {original_response}
            
            Analyze what's missing or could be improved in each STAR component and provide:
            1. Identified issues with the current response
            2. Suggested improvements for each STAR component
            3. A revised STAR-compliant response
            
            Be specific and constructive.
            """
            
            system_prompt = await self.get_system_prompt()
            response = await self._generate_llm_response(prompt, system_prompt)
            
            return response
            
        except Exception as e:
            logger.error(f"Error improving STAR response: {e}")
            return {"error": str(e)}
