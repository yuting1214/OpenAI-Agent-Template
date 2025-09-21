from typing import List
import json
from agents import Runner
from gradio import ChatMessage
from openai.types.responses import ResponseTextDeltaEvent
from src.agent import current_agent
from src.agent.memory import get_or_create_memory_session
from src.app.core.logging import logger

        
def clear_chat(session_id: str):
    """Clear the chat history and optionally clear memory session."""
    # Note: We could add memory session clearing here if needed
    # For now, just clear the UI - memory persists for session continuity
    return None

def handle_user_message(user_message: str, history: List[ChatMessage], session_id: str) -> tuple:
    """
    Handles user message input and updates chat history.
    
    Args:
        user_message: The user's input message
        history: Current chat history
        session_id: Unique session identifier for memory persistence
        
    Returns:
        Tuple of (empty_string, updated_history)
    """
    # Add user message to UI history
    updated_history = history + [ChatMessage(role="user", content=user_message)]
    return "", updated_history

async def handle_agent_message(history: List[ChatMessage], session_id: str):
    """
    Handle agent message with real AI streaming using ChatMessage format and memory session.
    
    Args:
        history: Current chat history from Gradio UI
        session_id: Unique session identifier for memory persistence
    """
    # Get the latest user message from history
    if history:
        last_message = history[-1]
        if hasattr(last_message, 'content'):
            user_input = last_message.content
        else:
            # Fallback for dict format
            user_input = last_message.get('content', '') if isinstance(last_message, dict) else ""
    else:
        user_input = ""
    
    try:
        # Get or create memory session for this user session
        memory_session = await get_or_create_memory_session(session_id)
        
        # Run agent with memory session for persistent conversation history
        result = Runner.run_streamed(
            current_agent,
            input=user_input,
            session=memory_session
        )
        
        # Flag to track if we've added the initial message
        message_started = False

        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                # Add empty assistant message only when we start getting content
                if not message_started:
                    history.append(ChatMessage(role="assistant", content=""))
                    message_started = True
                
                # Update the content of the current message
                history[-1] = ChatMessage(
                    role="assistant", 
                    content=history[-1].content + event.data.delta
                )
                yield history
                
            elif event.type == "run_item_stream_event":
                if getattr(event, "name", None) == "tool_called" and getattr(event.item, "type", "") == "tool_call_item":
                    raw_item = getattr(event.item, "raw_item", None)
                    tool_name = (
                        getattr(raw_item, "name", None)
                        or getattr(raw_item, "tool_name", None)
                        or "tool"
                    )
                    tool_args = getattr(raw_item, "arguments", None)
                    
                    # Format tool arguments concisely
                    if tool_args:
                        try:
                            # Parse and format JSON
                            args_data = json.loads(tool_args) if isinstance(tool_args, str) else tool_args
                            tool_content = f"```json\n{json.dumps(args_data, indent=2)}\n```"
                        except (json.JSONDecodeError, TypeError, AttributeError):
                            tool_content = f"```\n{str(tool_args)}\n```"
                    else:
                        tool_content = "No arguments"
                    
                    history.append(
                        ChatMessage(
                            role="assistant",
                            content=tool_content,
                            metadata={"title": f"🛠️ Using tool '{tool_name}'"}
                        )
                    )
                    yield history
                    
                    # Reset flag so next response content gets a new message
                    message_started = False
            else:
                pass
                
    except Exception as e:
        logger.error(f"Error in agent response: {e}")
        history[-1] = ChatMessage(
            role="assistant",
            content="Sorry, I'm having trouble responding right now.",
            metadata={"title": "💥 Error"}
        )
        yield history