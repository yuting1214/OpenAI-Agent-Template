import gradio as gr
from gradio import ChatMessage
from src.ui.gradio.chat_history import ChatHistoryManager
from src.chain.runtime import call_llm_api
from src.app.core.logging import logger


def handle_user_message(user_message: str, history):
    """Handle user message input."""
    if not user_message.strip():
        return "", history
    
    # Add user message to history
    updated_history = history + [ChatMessage(role="user", content=user_message)]
    return "", updated_history


async def handle_demo_response(history):
    """Handle AI response using OpenAI API."""
    # Include all previous messages into llm api call
    messages = ChatHistoryManager.gradio_to_openai_messages(history)
    
    try:
        response = await call_llm_api(messages)
        
        # Flag to track if we've added the initial message
        message_started = False

        async for chunk in response:
            choices = getattr(chunk, "choices", [])
            if choices and (delta := getattr(choices[0], "delta", None)):
                if content := getattr(delta, "content", None):
                    if not message_started:
                        history.append(ChatMessage(role="assistant", content=""))
                        message_started = True
                    
                    # Update the content of the current message
                    history[-1] = ChatMessage(
                        role="assistant", 
                        content=history[-1].content + content
                    )
                    yield history
                
                elif tool_calls := getattr(delta, "tool_calls", None):
                    if not message_started:
                        history.append(ChatMessage(role="assistant", content=""))
                        message_started = True
                    
                    # Handle tool calls - for now, append as text content
                    tools_text = f"\n[Tool calls: {str(tool_calls)}]"
                    history[-1] = ChatMessage(
                        role="assistant", 
                        content=history[-1].content + tools_text
                    )
                    yield history

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

def demo_create_new_conversation():
    """Create a new conversation."""
    return ChatHistoryManager.new_conversation()


def demo_auto_save_conversation(conversation_id, messages, saved_conversations):
    """
    Auto-save conversation after each message exchange.
    Fixed version for the demo.
    """
    logger.debug(f"Auto-save called with {len(messages)} messages")
    
    # Only auto-save if we have at least one complete exchange (user + assistant)
    if len(messages) >= 2:
        logger.info("Auto-saving conversation...")
        new_id, updated_conversations = ChatHistoryManager.save_conversation(
            conversation_id, messages, saved_conversations
        )
        logger.info(f"Saved as conversation {new_id}, total conversations: {len(updated_conversations)}")
        return new_id, updated_conversations
    
    logger.debug("Not enough messages to auto-save")
    return conversation_id, saved_conversations


def demo_update_conversation_list(saved_conversations):
    """
    Update the conversation list for display.
    Fixed version for the demo.
    """
    logger.debug(f"Updating conversation list with {len(saved_conversations)} conversations")
    
    conversation_samples = ChatHistoryManager.get_conversation_list(saved_conversations)
    logger.debug(f"Generated {len(conversation_samples)} conversation samples")
    
    return gr.Dataset(samples=conversation_samples)


def demo_manual_save(conversation_id, messages, saved_conversations):
    """Manually save the current conversation."""
    logger.info(f"Manual save requested: {len(messages)} messages")
    if messages:
        new_id, updated = ChatHistoryManager.save_conversation(
            conversation_id, messages, saved_conversations
        )
        logger.info(f"Manually saved as conversation {new_id}")
        return new_id, updated
    else:
        logger.warning("No messages to save")
        return conversation_id, saved_conversations
    

def demo_load_conversation(evt: gr.SelectData, saved_conversations):
    """Load selected conversation from the list."""
    logger.info(f"Loading conversation at index {evt.index}")
    if saved_conversations and 0 <= evt.index < len(saved_conversations):
        new_id, messages = ChatHistoryManager.load_conversation(evt.index, saved_conversations)
        logger.info(f"Loaded conversation {new_id} with {len(messages)} messages")
        return new_id, messages
    return None, []