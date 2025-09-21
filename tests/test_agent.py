"""
Example usage of CustomMemorySession with OpenAI Agent SDK

This example demonstrates how to integrate the CustomMemorySession
with your existing agent runtime for persistent conversation memory.
"""

from agents import Runner
from src.agent import current_agent
from src.agent.memory import get_or_create_memory_session
from src.app.core.logging import get_logger

logger = get_logger(__name__)


async def chat_with_memory_example(session_id: str, user_input: str) -> str:
    """
    Example function showing how to use the memory session with your agent.
    
    Args:
        session_id: Unique identifier for the conversation session
        user_input: User's message content
        
    Returns:
        Agent's response as a string
    """
    try:
        # Get or create memory session using your existing database setup
        memory_session = await get_or_create_memory_session(session_id)
        
        # Run the agent with memory session (async version)
        result = await Runner.run(
            current_agent, 
            input=user_input, 
            session=memory_session
        )
        
        # Get the response content
        response = result.data if hasattr(result, 'data') else str(result)
        
        logger.info(f"Agent response for session {session_id}: {response[:100]}...")
        return response
        
    except Exception as e:
        logger.error(f"Error in chat_with_memory_example: {e}")
        raise


async def get_conversation_info(session_id: str) -> dict:
    """
    Get information about a conversation session.
    
    Args:
        session_id: Unique identifier for the conversation session
        
    Returns:
        Dictionary with conversation metadata
    """
    try:
        memory_session = await get_or_create_memory_session(session_id)
        
        # Get basic session info
        recent_items = await memory_session.get_items()
        
        return {
            "session_id": session_id,
            "recent_items": len(recent_items),
            "memory_limit": memory_session.memory_limit,
        }
        
    except Exception as e:
        logger.error(f"Error getting conversation info: {e}")
        raise


async def get_recent_messages(session_id: str, count: int = 5) -> list:
    """
    Get recent messages from a conversation session.
    
    Args:
        session_id: Unique identifier for the conversation session
        count: Number of recent messages to retrieve
        
    Returns:
        List of recent conversation items
    """
    try:
        memory_session = await get_or_create_memory_session(session_id)
        items = await memory_session.get_items(limit=count)
        
        logger.info(f"Retrieved {len(items)} recent messages from session {session_id}")
        return items
        
    except Exception as e:
        logger.error(f"Error getting recent messages: {e}")
        raise


# Example usage in your FastAPI endpoints or Gradio interface
async def example_usage():
    """
    Example demonstrating the complete workflow.
    """
    session_id = "user_123_conversation"
    
    # First message
    response1 = await chat_with_memory_example(session_id, "Hello, what's the weather like?")
    print(f"Response 1: {response1}")
    
    # Second message - agent should remember previous context
    response2 = await chat_with_memory_example(session_id, "What about tomorrow?")
    print(f"Response 2: {response2}")
    
    # Get conversation info
    info = await get_conversation_info(session_id)
    print(f"Conversation info: {info}")
    
    # Get recent messages
    recent_messages = await get_recent_messages(session_id, count=3)
    print(f"Recent messages: {len(recent_messages)} items")


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())
