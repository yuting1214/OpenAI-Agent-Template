"""
Agent Registry

Central registry for all agent instances and configurations.
This provides a single source of truth for agent management across the application.

Benefits:
- Single place to configure which agent is active
- Easy to switch between different agent configurations
- Centralized agent management for testing and deployment
- Follows the Single Responsibility Principle
"""

import os
from agents import Agent, set_tracing_export_api_key

from .models.fireworks import model as fireworks_model
from .models.openai import model as openai_model
from .models.settings import reasoning_model_settings, chat_model_settings
from .prompt.example import INSTRUCTIONS
from .tools.example import fetch_weather
from src.app.core.logging import logger

# Enable OpenAI tracing (with placeholder if key is missing)
set_tracing_export_api_key(os.getenv('OPENAI_API_KEY', 'placeholder-key-for-tracing'))

# Agent Configurations
AGENT_CONFIGS = {
    "openai": {
        "name": "Agent (OpenAI)",
        "model": openai_model,
        "model_settings": chat_model_settings,
        "instructions": INSTRUCTIONS,
        "tools": [fetch_weather],
    },
    "fireworks": {
        "name": "Agent (Fireworks AI)",
        "model": fireworks_model,
        "model_settings": reasoning_model_settings,
        "instructions": INSTRUCTIONS,
        "tools": [fetch_weather],
    }
}

# Default agent configuration
DEFAULT_AGENT = "openai"

# Current active agent (can be changed via environment variable)
CURRENT_AGENT_KEY = os.getenv('AGENT_TYPE', DEFAULT_AGENT)

def create_agent(agent_key: str = None) -> Agent:
    """
    Create an agent instance based on the configuration key.
    
    Args:
        agent_key: Agent configuration key (defaults to CURRENT_AGENT_KEY)
        
    Returns:
        Agent instance
        
    Raises:
        KeyError: If agent_key is not found in AGENT_CONFIGS
    """
    key = agent_key or CURRENT_AGENT_KEY
    
    if key not in AGENT_CONFIGS:
        available_keys = list(AGENT_CONFIGS.keys())
        raise KeyError(f"Agent '{key}' not found. Available agents: {available_keys}")
    
    config = AGENT_CONFIGS[key]
    logger.info(f"Creating agent: {config['name']} (key: {key})")
    
    return Agent(**config)

def get_current_agent() -> Agent:
    """
    Get the current active agent instance.
    
    Returns:
        Current agent instance
    """
    return create_agent(CURRENT_AGENT_KEY)

def get_available_agents() -> list[str]:
    """
    Get list of available agent configuration keys.
    
    Returns:
        List of agent configuration keys
    """
    return list(AGENT_CONFIGS.keys())

# Create the default agent instance
# This is the main export that other modules will import
current_agent = get_current_agent()