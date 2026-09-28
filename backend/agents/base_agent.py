"""
Base Agent for Interview Coach
Abstract base class for all agents in the multi-agent system
"""

import logging
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import json
import asyncio
from ..config import settings, llm_settings
from ..services.auth_service import AuthService

logger = logging.getLogger(__name__)


@dataclass
class AgentResult:
    """Result from an agent's analysis"""
    agent_type: str
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Base class for all interview coaching agents"""
    
    def __init__(self, agent_type: str, config: Optional[Dict[str, Any]] = None):
        """Initialize the agent"""
        self.agent_type = agent_type
        self.config = config or {}
        self.timeout = getattr(settings, 'agent_timeout', 60)
        self.model = getattr(llm_settings, 'model', 'kiro')
        self.provider = getattr(llm_settings, 'provider', 'omniroute')
        
        # Set up LLM client
        self.llm_client = None
        
    async def initialize(self):
        """Initialize the agent (load models, etc.)"""
        try:
            # Initialize LLM client
            await self._initialize_llm()
            logger.info(f"{self.agent_type} initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing {self.agent_type}: {e}")
            return False
    
    async def _initialize_llm(self):
        """Initialize the LLM client"""
        # Get API key from settings or database
        api_key = settings.omniroute_api_key or settings.kiro_llm_api_key
        
        if not api_key:
            # Try to get from database
            api_key = await AuthService.get_api_key("omniroute")
        
        if api_key:
            # In a real implementation, you would initialize the LLM client here
            # For now, we'll just store the API key
            self.api_key = api_key
            logger.info(f"LLM client initialized for {self.agent_type}")
        else:
            logger.warning(f"No API key found for LLM in {self.agent_type}")
    
    @abstractmethod
    async def analyze(self, input_data: Dict[str, Any]) -> AgentResult:
        """Analyze the input data and return results"""
        pass
    
    @abstractmethod
    async def get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        pass
    
    async def _generate_llm_response(
        self,
        prompt: str,
        system_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Dict[str, Any]:
        """Generate a response from the LLM"""
        try:
            # In a real implementation, this would call the LLM API
            # For demo purposes, we'll return a mock response
            
            logger.info(f"Generating LLM response for {self.agent_type}")
            
            # Mock response based on agent type
            mock_responses = {
                "question_agent": {
                    "question": "Tell me about a challenging project you worked on.",
                    "role": "Software Engineer",
                    "competency": "Problem Solving",
                    "difficulty": "medium"
                },
                "communication_agent": {
                    "clarity_score": 85.0,
                    "structure_score": 80.0,
                    "conciseness_score": 75.0,
                    "suggestions": ["Use shorter sentences", "Improve flow"]
                },
                "content_agent": {
                    "relevance_score": 90.0,
                    "completeness_score": 85.0,
                    "addresses_question": True,
                    "demonstrates_knowledge": True
                },
                "star_agent": {
                    "situation_score": 80.0,
                    "task_score": 85.0,
                    "action_score": 75.0,
                    "result_score": 70.0,
                    "uses_star_structure": True,
                    "suggestions": ["Provide more detail in action section"]
                },
                "coach_agent": {
                    "overall_score": 82.5,
                    "strengths": ["Clear communication", "Relevant experience"],
                    "weaknesses": ["Needs more detail in action section"],
                    "improvement_plan": ["Practice STAR method", "Work on providing more details"]
                }
            }
            
            # Return mock response
            return mock_responses.get(self.agent_type, {"response": "Analysis complete"})
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return {"error": str(e)}
    
    async def _validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for the agent"""
        # Basic validation - can be overridden by specific agents
        required_fields = self.get_required_fields()
        
        for field in required_fields:
            if field not in input_data:
                logger.error(f"Missing required field for {self.agent_type}: {field}")
                return False
        
        return True
    
    def get_required_fields(self) -> List[str]:
        """Get list of required fields for input validation"""
        return []
    
    async def _format_response(self, raw_response: Dict[str, Any]) -> Dict[str, Any]:
        """Format the raw LLM response"""
        # Basic formatting - can be overridden by specific agents
        return raw_response
    
    async def close(self):
        """Clean up resources"""
        pass
