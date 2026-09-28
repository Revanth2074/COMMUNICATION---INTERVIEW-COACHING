"""
LLM Configuration for Interview Coach
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any


class LLMConfig(BaseModel):
    """LLM Configuration"""
    
    # Provider settings
    provider: str = "omniroute"
    model: str = "kiro"
    
    # API settings
    api_key: Optional[str] = None
    base_url: str = "https://api.omniroute.com/v1"
    
    # Model parameters
    temperature: float = 0.7
    max_tokens: int = 4096
    top_p: float = 0.9
    frequency_penalty: float = 0.1
    presence_penalty: float = 0.1
    
    # Timeout settings
    timeout: int = 60  # seconds
    max_retries: int = 3
    
    # Agent-specific settings
    agent_system_prompts: Dict[str, str] = {}
    agent_temperatures: Dict[str, float] = {}
    
    # Response formatting
    response_format: str = "json"
    

class AgentConfig(BaseModel):
    """Agent-specific configuration"""
    
    # Interview Question Agent
    question_agent: Dict[str, Any] = {
        "role": "Interview Question Agent",
        "description": "Selects or generates suitable interview questions based on candidate's target role and competency",
        "temperature": 0.3,
        "max_tokens": 2048
    }
    
    # Communication Analysis Agent
    communication_agent: Dict[str, Any] = {
        "role": "Communication Analysis Agent",
        "description": "Evaluates clarity, structure, conciseness and communication quality",
        "temperature": 0.5,
        "max_tokens": 2048
    }
    
    # Content Evaluation Agent
    content_agent: Dict[str, Any] = {
        "role": "Content Evaluation Agent",
        "description": "Evaluates whether the response addresses the question and demonstrates relevant knowledge or experience",
        "temperature": 0.4,
        "max_tokens": 2048
    }
    
    # STAR/Response Structure Agent
    star_agent: Dict[str, Any] = {
        "role": "STAR/Response Structure Agent",
        "description": "Evaluates behavioral responses using Situation, Task, Action, Result structure",
        "temperature": 0.4,
        "max_tokens": 2048
    }
    
    # Interview Coach Agent
    coach_agent: Dict[str, Any] = {
        "role": "Interview Coach Agent",
        "description": "Consolidates outputs from specialist agents and generates personalized coaching feedback",
        "temperature": 0.6,
        "max_tokens": 4096
    }


# Create LLM settings instance
llm_settings = LLMConfig()
agent_config = AgentConfig()
