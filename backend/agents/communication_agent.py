"""
Communication Agent for Interview Coach
Evaluates clarity, structure, conciseness and communication quality
"""

import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from .base_agent import BaseAgent, AgentResult
import re

logger = logging.getLogger(__name__)


class CommunicationAgent(BaseAgent):
    """Agent for evaluating communication quality"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Communication Agent"""
        super().__init__("communication_agent", config)
    
    async def get_system_prompt(self) -> str:
        """Get the system prompt for the Communication Agent"""
        return """
        You are a Communication Analysis Agent. Your role is to evaluate the clarity,
        structure, conciseness, and overall communication quality of interview responses.
        
        Evaluation Criteria:
        1. Clarity (0-100): How clear and understandable is the response?
           - Consider vocabulary, sentence structure, and coherence
        2. Structure (0-100): How well-organized is the response?
           - Look for logical flow, paragraph structure, and organization
        3. Conciseness (0-100): How concise and to-the-point is the response?
           - Avoid unnecessary details, but ensure completeness
        4. Professional Tone (0-100): Does the response use appropriate professional language?
        
        Analysis Approach:
        - Identify specific examples of good and poor communication
        - Provide actionable suggestions for improvement
        - Consider the context of the question and expected response length
        
        Output format:
        {
            "clarity_score": 0-100,
            "structure_score": 0-100,
            "conciseness_score": 0-100,
            "tone_score": 0-100,
            "overall_communication_score": 0-100,
            "strengths": ["list", "of", "strengths"],
            "weaknesses": ["list", "of", "weaknesses"],
            "suggestions": ["list", "of", "suggestions"],
            "detailed_analysis": "Detailed analysis of communication quality"
        }
        """
    
    def get_required_fields(self) -> List[str]:
        """Get required fields for input validation"""
        return ["response_text", "question"]
    
    async def analyze(self, input_data: Dict[str, Any]) -> AgentResult:
        """Analyze the communication quality of a response"""
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
            candidate_info = input_data.get("candidate_info", {})
            
            # Basic text analysis
            word_count = len(response_text.split())
            sentence_count = len(re.split(r'[.!?]+', response_text))
            avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
            
            # Calculate scores using both rule-based and LLM-based analysis
            rule_based_scores = self._calculate_rule_based_scores(response_text)
            
            # Generate LLM-based analysis
            system_prompt = await self.get_system_prompt()
            
            prompt = f"""
            Analyze the following interview response for communication quality:
            
            Question: {question}
            Response: {response_text}
            
            Candidate Info: {candidate_info}
            
            Provide a detailed analysis based on the criteria in the system prompt.
            Be specific and provide actionable feedback.
            """
            
            llm_response = await self._generate_llm_response(prompt, system_prompt)
            
            # Combine scores (weighted average)
            combined_scores = self._combine_scores(rule_based_scores, llm_response)
            
            # Format result
            result_data = {
                "scores": combined_scores,
                "analysis": llm_response,
                "text_metrics": {
                    "word_count": word_count,
                    "sentence_count": sentence_count,
                    "avg_sentence_length": round(avg_sentence_length, 2),
                    "character_count": len(response_text)
                },
                "strengths": llm_response.get("strengths", []),
                "weaknesses": llm_response.get("weaknesses", []),
                "suggestions": llm_response.get("suggestions", [])
            }
            
            return AgentResult(
                agent_type=self.agent_type,
                success=True,
                data=result_data,
                confidence=0.9,
                metadata={
                    "input": input_data,
                    "method": "hybrid"
                }
            )
            
        except Exception as e:
            logger.error(f"Error in CommunicationAgent.analyze: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                success=False,
                error=str(e)
            )
    
    def _calculate_rule_based_scores(self, text: str) -> Dict[str, float]:
        """Calculate scores using rule-based analysis"""
        if not text.strip():
            return {
                "clarity_score": 0.0,
                "structure_score": 0.0,
                "conciseness_score": 0.0,
                "tone_score": 0.0
            }
        
        word_count = len(text.split())
        sentence_count = len(re.split(r'[.!?]+', text))
        
        # Clarity score (based on sentence length and vocabulary)
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        clarity_score = max(0, 100 - (avg_sentence_length - 15))  # Target ~15 words per sentence
        clarity_score = min(100, max(0, clarity_score))
        
        # Structure score (based on paragraph structure)
        paragraphs = text.split('\n\n')
        structure_score = min(100, len(paragraphs) * 20)  # More paragraphs = better structure
        
        # Conciseness score (based on word count - assume ideal is 100-200 words)
        if word_count < 50:
            conciseness_score = 80.0
        elif word_count < 100:
            conciseness_score = 90.0
        elif word_count < 200:
            conciseness_score = 100.0
        elif word_count < 300:
            conciseness_score = 85.0
        else:
            conciseness_score = max(0, 100 - (word_count - 300) * 2)
        
        # Tone score (basic check for professional language)
        professional_words = ['experience', 'achieved', 'developed', 'managed', 'led', 'created']
        tone_score = 0.0
        for word in professional_words:
            if word.lower() in text.lower():
                tone_score += 10
        tone_score = min(100, tone_score)
        
        return {
            "clarity_score": round(clarity_score, 2),
            "structure_score": round(structure_score, 2),
            "conciseness_score": round(conciseness_score, 2),
            "tone_score": round(tone_score, 2)
        }
    
    def _combine_scores(self, rule_scores: Dict[str, float], llm_response: Dict[str, Any]) -> Dict[str, float]:
        """Combine rule-based and LLM-based scores"""
        # If LLM response has scores, use them with higher weight
        if isinstance(llm_response, dict):
            llm_scores = {
                "clarity_score": llm_response.get("clarity_score", 50.0),
                "structure_score": llm_response.get("structure_score", 50.0),
                "conciseness_score": llm_response.get("conciseness_score", 50.0),
                "tone_score": llm_response.get("tone_score", 50.0)
            }
            
            # Weighted average: 40% rule-based, 60% LLM
            combined = {}
            for key in rule_scores:
                rule_val = rule_scores.get(key, 50.0)
                llm_val = llm_scores.get(key, 50.0)
                combined[key] = round((rule_val * 0.4) + (llm_val * 0.6), 2)
            
            # Calculate overall communication score
            overall = sum(combined.values()) / len(combined)
            combined["overall_communication_score"] = round(overall, 2)
            
            return combined
        else:
            # Use only rule-based scores
            overall = sum(rule_scores.values()) / len(rule_scores)
            rule_scores["overall_communication_score"] = round(overall, 2)
            return rule_scores
    
    async def analyze_clarity(self, text: str) -> Dict[str, Any]:
        """Specifically analyze clarity of text"""
        try:
            prompt = f"""
            Analyze the clarity of the following text:
            {text}
            
            Evaluate:
            1. Vocabulary appropriateness
            2. Sentence structure complexity
            3. Coherence and flow
            4. Ease of understanding
            
            Provide scores (0-100) and specific feedback.
            """
            
            system_prompt = await self.get_system_prompt()
            response = await self._generate_llm_response(prompt, system_prompt)
            
            return response
            
        except Exception as e:
            logger.error(f"Error analyzing clarity: {e}")
            return {"error": str(e)}
    
    async def analyze_structure(self, text: str) -> Dict[str, Any]:
        """Specifically analyze structure of text"""
        try:
            prompt = f"""
            Analyze the structure of the following text:
            {text}
            
            Evaluate:
            1. Logical organization
            2. Paragraph structure
            3. Flow between ideas
            4. Use of transitions
            
            Provide scores (0-100) and specific feedback.
            """
            
            system_prompt = await self.get_system_prompt()
            response = await self._generate_llm_response(prompt, system_prompt)
            
            return response
            
        except Exception as e:
            logger.error(f"Error analyzing structure: {e}")
            return {"error": str(e)}
