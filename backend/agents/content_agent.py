"""
Content Agent for Interview Coach
Evaluates whether the response addresses the question and demonstrates relevant knowledge or experience
"""

import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from .base_agent import BaseAgent, AgentResult
import re
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class ContentAgent(BaseAgent):
    """Agent for evaluating response content quality"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Content Agent"""
        super().__init__("content_agent", config)
    
    async def get_system_prompt(self) -> str:
        """Get the system prompt for the Content Agent"""
        return """
        You are a Content Evaluation Agent. Your role is to evaluate whether a candidate's
        response addresses the interview question and demonstrates relevant knowledge or experience.
        
        Evaluation Criteria:
        1. Relevance (0-100): How well does the response directly address the question?
           - Does it answer what was asked?
           - Does it stay on topic?
        2. Completeness (0-100): Does the response provide a complete answer?
           - Are all aspects of the question addressed?
           - Are there gaps in the response?
        3. Depth of Knowledge (0-100): Does the response demonstrate appropriate knowledge?
           - Technical accuracy (for technical questions)
           - Appropriate level of detail
           - Relevant examples and experiences
        4. Experience Demonstration (0-100): Does the response show relevant experience?
           - Specific examples from past work
           - Concrete achievements and results
           - Connection to the role requirements
        
        Analysis Approach:
        - Compare the response to the question to assess relevance
        - Identify missing elements or gaps
        - Evaluate the quality and specificity of examples
        - Assess whether the response demonstrates the expected competencies
        
        Output format:
        {
            "relevance_score": 0-100,
            "completeness_score": 0-100,
            "knowledge_score": 0-100,
            "experience_score": 0-100,
            "overall_content_score": 0-100,
            "addresses_question": true/false,
            "missing_elements": ["list", "of", "missing", "elements"],
            "strengths": ["list", "of", "strengths"],
            "weaknesses": ["list", "of", "weaknesses"],
            "suggestions": ["list", "of", "suggestions"],
            "detailed_analysis": "Detailed analysis of content quality"
        }
        """
    
    def get_required_fields(self) -> List[str]:
        """Get required fields for input validation"""
        return ["response_text", "question"]
    
    async def analyze(self, input_data: Dict[str, Any]) -> AgentResult:
        """Analyze the content quality of a response"""
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
            expected_competency = input_data.get("expected_competency", "")
            role = input_data.get("role", "")
            
            # Basic relevance check using text similarity
            rule_based_scores = self._calculate_rule_based_scores(question, response_text)
            
            # Generate LLM-based analysis
            system_prompt = await self.get_system_prompt()
            
            prompt = f"""
            Analyze the following interview response for content quality:
            
            Question: {question}
            Expected Competency: {expected_competency}
            Role: {role}
            Response: {response_text}
            
            Provide a detailed analysis based on the criteria in the system prompt.
            Be specific about what's good and what could be improved.
            """
            
            llm_response = await self._generate_llm_response(prompt, system_prompt)
            
            # Combine scores
            combined_scores = self._combine_scores(rule_based_scores, llm_response)
            
            # Check if response addresses the question
            addresses_question = self._check_addresses_question(question, response_text)
            
            # Format result
            result_data = {
                "scores": combined_scores,
                "analysis": llm_response,
                "addresses_question": addresses_question,
                "missing_elements": llm_response.get("missing_elements", []),
                "strengths": llm_response.get("strengths", []),
                "weaknesses": llm_response.get("weaknesses", []),
                "suggestions": llm_response.get("suggestions", []),
                "text_comparison": {
                    "similarity_score": rule_based_scores.get("similarity_score", 0.0),
                    "question_keywords": self._extract_keywords(question),
                    "response_keywords": self._extract_keywords(response_text)
                }
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
            logger.error(f"Error in ContentAgent.analyze: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                success=False,
                error=str(e)
            )
    
    def _calculate_rule_based_scores(self, question: str, response: str) -> Dict[str, float]:
        """Calculate scores using rule-based analysis"""
        if not response.strip():
            return {
                "relevance_score": 0.0,
                "completeness_score": 0.0,
                "knowledge_score": 0.0,
                "experience_score": 0.0,
                "similarity_score": 0.0
            }
        
        # Calculate text similarity
        similarity = self._calculate_similarity(question.lower(), response.lower())
        
        # Question and response lengths
        question_len = len(question.split())
        response_len = len(response.split())
        
        # Relevance score based on similarity and keyword overlap
        question_keywords = self._extract_keywords(question)
        response_keywords = self._extract_keywords(response)
        keyword_overlap = len(set(question_keywords) & set(response_keywords))
        keyword_score = (keyword_overlap / len(question_keywords)) * 100 if question_keywords else 0
        
        relevance_score = (similarity * 0.4 + keyword_score * 0.6)
        
        # Completeness score based on response length relative to question
        length_ratio = response_len / max(question_len, 1)
        completeness_score = min(100, length_ratio * 20)  # Cap at 100
        
        # Knowledge and experience scores (basic estimation)
        # Look for indicators of knowledge and experience
        knowledge_indicators = ['experience', 'knowledge', 'skill', 'expertise', 'understand', 'know']
        experience_indicators = ['worked', 'developed', 'managed', 'led', 'created', 'built', 'achieved']
        
        knowledge_count = sum(1 for ind in knowledge_indicators if ind in response.lower())
        experience_count = sum(1 for ind in experience_indicators if ind in response.lower())
        
        knowledge_score = min(100, knowledge_count * 15)
        experience_score = min(100, experience_count * 15)
        
        return {
            "relevance_score": round(relevance_score, 2),
            "completeness_score": round(completeness_score, 2),
            "knowledge_score": round(knowledge_score, 2),
            "experience_score": round(experience_score, 2),
            "similarity_score": round(similarity, 2)
        }
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        return SequenceMatcher(None, text1, text2).ratio()
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Remove punctuation and split
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        
        # Common stop words to exclude
        stop_words = {'that', 'this', 'with', 'from', 'have', 'your', 'will', 'what', 'when', 'where'}
        
        return [w for w in words if w not in stop_words]
    
    def _check_addresses_question(self, question: str, response: str) -> bool:
        """Check if response addresses the question"""
        # Basic check: does the response contain keywords from the question?
        question_keywords = self._extract_keywords(question)
        response_keywords = self._extract_keywords(response)
        
        overlap = set(question_keywords) & set(response_keywords)
        
        # If at least 30% of question keywords are in response, consider it addressed
        if question_keywords:
            return len(overlap) / len(question_keywords) >= 0.3
        
        return False
    
    def _combine_scores(self, rule_scores: Dict[str, float], llm_response: Dict[str, Any]) -> Dict[str, float]:
        """Combine rule-based and LLM-based scores"""
        # If LLM response has scores, use them with higher weight
        if isinstance(llm_response, dict):
            llm_scores = {
                "relevance_score": llm_response.get("relevance_score", 50.0),
                "completeness_score": llm_response.get("completeness_score", 50.0),
                "knowledge_score": llm_response.get("knowledge_score", 50.0) or llm_response.get("depth_of_knowledge_score", 50.0),
                "experience_score": llm_response.get("experience_score", 50.0) or llm_response.get("experience_demonstration_score", 50.0)
            }
            
            # Weighted average: 30% rule-based, 70% LLM
            combined = {}
            for key in rule_scores:
                if key in llm_scores:
                    rule_val = rule_scores.get(key, 50.0)
                    llm_val = llm_scores.get(key, 50.0)
                    combined[key] = round((rule_val * 0.3) + (llm_val * 0.7), 2)
                else:
                    combined[key] = rule_scores.get(key, 50.0)
            
            # Calculate overall content score
            relevant_keys = [k for k in combined if k not in ['similarity_score']]
            overall = sum(combined[k] for k in relevant_keys) / len(relevant_keys) if relevant_keys else 0
            combined["overall_content_score"] = round(overall, 2)
            
            return combined
        else:
            # Use only rule-based scores
            relevant_keys = [k for k in rule_scores if k not in ['similarity_score']]
            overall = sum(rule_scores[k] for k in relevant_keys) / len(relevant_keys) if relevant_keys else 0
            rule_scores["overall_content_score"] = round(overall, 2)
            return rule_scores
    
    async def evaluate_technical_accuracy(self, question: str, response: str, competency: str) -> Dict[str, Any]:
        """Evaluate technical accuracy of a response"""
        try:
            prompt = f"""
            Evaluate the technical accuracy of the following response to a {competency} question:
            
            Question: {question}
            Response: {response}
            
            Assess:
            1. Technical correctness
            2. Depth of technical knowledge
            3. Appropriateness of examples
            4. Use of correct terminology
            
            Provide scores (0-100) and specific feedback on any technical inaccuracies.
            """
            
            system_prompt = await self.get_system_prompt()
            response = await self._generate_llm_response(prompt, system_prompt)
            
            return response
            
        except Exception as e:
            logger.error(f"Error evaluating technical accuracy: {e}")
            return {"error": str(e)}
