from typing import List
import json
from agents import Runner
from openai.types.responses import ResponseTextDeltaEvent
from gradio import ChatMessage
from src.agent.runtime import ai_agent

        
def clear_chat():
    """Clear the chat history."""
    return None

def handle_user_message(user_message: str, history: List[ChatMessage]) -> tuple:
    """
    Handles user message input and updates chat history.
    
    Args:
        user_message: The user's input message
        history: Current chat history
        
    Returns:
        Tuple of (empty_string, updated_history)
    """
    return "", history + [ChatMessage(role="user", content=user_message)]

async def handle_agent_message(history: List[ChatMessage]):
    """Handle agent message with real AI streaming using ChatMessage format."""
    # Handle both ChatMessage and dict formats for compatibility
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
        result = Runner.run_streamed(
            ai_agent,
            user_input,
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
        print(f"Error in agent response: {e}")
        history[-1] = ChatMessage(
            role="assistant",
            content="Sorry, I'm having trouble responding right now.",
            metadata={"title": "💥 Error"}
        )
        yield history