import gradio as gr
from gradio import ChatMessage
from src.ui.gradio.chat_history import ChatHistoryManager

def simple_echo_response(message: str, history):
    """Simple echo response for demo purposes."""
    return f"You said: {message}"


def handle_user_message(user_message: str, history):
    """Handle user message input."""
    if not user_message.strip():
        return "", history
    
    # Add user message to history
    updated_history = history + [ChatMessage(role="user", content=user_message)]
    return "", updated_history


def handle_demo_response(history):
    """Handle demo AI response (simple echo)."""
    if not history:
        return history
    
    # Get the last user message
    last_message = history[-1]
    if hasattr(last_message, 'content'):
        user_input = last_message.content
    else:
        user_input = last_message.get('content', '') if isinstance(last_message, dict) else ""
    
    # Generate simple response
    response = simple_echo_response(user_input, history)
    
    # Add assistant response
    updated_history = history + [ChatMessage(role="assistant", content=response)]
    return updated_history


def demo_create_new_conversation():
    """Create a new conversation."""
    return ChatHistoryManager.new_conversation()


def demo_auto_save_conversation(conversation_id, messages, saved_conversations):
    """
    Auto-save conversation after each message exchange.
    Fixed version for the demo.
    """
    print(f"Auto-save called with {len(messages)} messages")
    
    # Only auto-save if we have at least one complete exchange (user + assistant)
    if len(messages) >= 2:
        print("Auto-saving conversation...")
        new_id, updated_conversations = ChatHistoryManager.save_conversation(
            conversation_id, messages, saved_conversations
        )
        print(f"Saved as conversation {new_id}, total conversations: {len(updated_conversations)}")
        return new_id, updated_conversations
    
    print("Not enough messages to auto-save")
    return conversation_id, saved_conversations


def demo_update_conversation_list(saved_conversations):
    """
    Update the conversation list for display.
    Fixed version for the demo.
    """
    print(f"Updating conversation list with {len(saved_conversations)} conversations")
    
    conversation_samples = ChatHistoryManager.get_conversation_list(saved_conversations)
    print(f"Generated {len(conversation_samples)} conversation samples")
    
    return gr.Dataset(samples=conversation_samples)


def demo_manual_save(conversation_id, messages, saved_conversations):
    """Manually save the current conversation."""
    print(f"Manual save requested: {len(messages)} messages")
    if messages:
        new_id, updated = ChatHistoryManager.save_conversation(
            conversation_id, messages, saved_conversations
        )
        print(f"Manually saved as conversation {new_id}")
        return new_id, updated
    else:
        print("No messages to save")
        return conversation_id, saved_conversations
    

def demo_load_conversation(evt: gr.SelectData, saved_conversations):
    """Load selected conversation from the list."""
    print(f"Loading conversation at index {evt.index}")
    if saved_conversations and 0 <= evt.index < len(saved_conversations):
        new_id, messages = ChatHistoryManager.load_conversation(evt.index, saved_conversations)
        print(f"Loaded conversation {new_id} with {len(messages)} messages")
        return new_id, messages
    return None, []