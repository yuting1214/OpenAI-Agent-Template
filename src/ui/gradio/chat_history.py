"""
Chat History Management Module

Provides save/load functionality for chat conversations using only gr.Chatbot.
Implements similar functionality to gr.ChatInterface's save_history feature.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from gradio import ChatMessage


class ChatHistoryManager:
    """Manages chat history persistence and conversation management."""
    
    def __init__(self, storage_key: str = "chat_conversations"):
        self.storage_key = storage_key
    
    @staticmethod
    def serialize_chat_messages(messages: List[ChatMessage]) -> List[Dict[str, Any]]:
        """
        Serialize ChatMessage objects to JSON-serializable format.
        Similar to ChatInterface.serialize_components but for ChatMessage.
        """
        serialized = []
        for msg in messages:
            if hasattr(msg, 'role') and hasattr(msg, 'content'):
                # Handle ChatMessage objects
                msg_dict = {
                    "role": msg.role,
                    "content": msg.content,
                    "metadata": getattr(msg, 'metadata', None)
                }
                serialized.append(msg_dict)
            elif isinstance(msg, dict):
                # Handle dict format messages
                serialized.append(msg)
        return serialized
    
    @staticmethod
    def deserialize_chat_messages(serialized_messages: List[Dict[str, Any]]) -> List[ChatMessage]:
        """
        Deserialize JSON format back to ChatMessage objects.
        """
        messages = []
        for msg_dict in serialized_messages:
            if isinstance(msg_dict, dict) and "role" in msg_dict and "content" in msg_dict:
                metadata = msg_dict.get("metadata")
                messages.append(ChatMessage(
                    role=msg_dict["role"],
                    content=msg_dict["content"],
                    metadata=metadata
                ))
        return messages
    
    @staticmethod
    def gradio_to_openai_messages(history: List[ChatMessage]) -> List[Dict[str, Any]]:
        """
        Convert Gradio ChatMessage objects to OpenAI API format.
        Similar to ChatHistoryManager.serialize_chat_messages but for OpenAI API.
        """
        messages = []
        for msg in history:
            if hasattr(msg, 'role') and hasattr(msg, 'content'):
                # Handle ChatMessage objects
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
            elif isinstance(msg, dict) and "role" in msg and "content" in msg:
                # Handle dict format messages
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        return messages
    
    @staticmethod
    def generate_conversation_title(messages: List[ChatMessage], max_length: int = 40) -> str:
        """
        Generate a title for a conversation based on the first user message.
        Similar to ChatInterface._generate_chat_title.
        """
        title = ""
        has_files = False
        
        for message in messages:
            if hasattr(message, 'role') and message.role == "user":
                content = getattr(message, 'content', '')
                if isinstance(content, str) and content.strip():
                    title = content.strip()
                    break
                # Check if there are files (indicated by metadata or special content)
                metadata = getattr(message, 'metadata', {})
                if metadata and any('file' in str(k).lower() or 'file' in str(v).lower() 
                                 for k, v in metadata.items()):
                    has_files = True
        
        if has_files and title:
            title = "📎 " + title
        elif has_files and not title:
            title = "📎 Conversation with files"
        
        if len(title) > max_length:
            title = title[:max_length] + "..."
        
        return title or "New Conversation"
    
    @staticmethod
    def save_conversation(
        conversation_id: Optional[int], 
        messages: List[ChatMessage], 
        saved_conversations: List[Dict[str, Any]]
    ) -> Tuple[int, List[Dict[str, Any]]]:
        """
        Save or update a conversation in the saved conversations list.
        
        Args:
            conversation_id: Index of existing conversation or None for new
            messages: Current chat messages
            saved_conversations: List of saved conversations
            
        Returns:
            Tuple of (conversation_id, updated_saved_conversations)
        """
        if not messages:
            return conversation_id, saved_conversations
        
        # Serialize the conversation
        serialized_messages = ChatHistoryManager.serialize_chat_messages(messages)
        title = ChatHistoryManager.generate_conversation_title(messages)
        
        conversation_data = {
            "title": title,
            "messages": serialized_messages,
            "timestamp": datetime.now().isoformat(),
            "message_count": len(messages)
        }
        
        saved_conversations = saved_conversations or []
        
        if conversation_id is not None and 0 <= conversation_id < len(saved_conversations):
            # Update existing conversation
            saved_conversations[conversation_id] = conversation_data
        else:
            # Add new conversation at the beginning
            saved_conversations.insert(0, conversation_data)
            conversation_id = 0
        
        return conversation_id, saved_conversations
    
    @staticmethod
    def load_conversation(
        index: int, 
        saved_conversations: List[Dict[str, Any]]
    ) -> Tuple[int, List[ChatMessage]]:
        """
        Load a conversation by index.
        
        Args:
            index: Index of conversation to load
            saved_conversations: List of saved conversations
            
        Returns:
            Tuple of (conversation_id, chat_messages)
        """
        if not saved_conversations or index < 0 or index >= len(saved_conversations):
            return None, []
        
        conversation_data = saved_conversations[index]
        messages = ChatHistoryManager.deserialize_chat_messages(
            conversation_data.get("messages", [])
        )
        
        return index, messages
    
    @staticmethod
    def delete_conversation(
        conversation_id: Optional[int], 
        saved_conversations: List[Dict[str, Any]]
    ) -> Tuple[Optional[int], List[Dict[str, Any]]]:
        """
        Delete a conversation by ID.
        
        Args:
            conversation_id: Index of conversation to delete
            saved_conversations: List of saved conversations
            
        Returns:
            Tuple of (None, updated_saved_conversations)
        """
        if (conversation_id is not None and 
            saved_conversations and 
            0 <= conversation_id < len(saved_conversations)):
            saved_conversations.pop(conversation_id)
        
        return None, saved_conversations
    
    @staticmethod
    def get_conversation_list(saved_conversations: List[Dict[str, Any]]) -> List[List[str]]:
        """
        Get formatted conversation list for display in gr.Dataset.
        Conversations are sorted by timestamp (newest first).
        
        Args:
            saved_conversations: List of saved conversations
            
        Returns:
            List of conversation entries for gr.Dataset, sorted by timestamp descending
        """
        if not saved_conversations:
            return []
        
        # Sort conversations by timestamp (newest first)
        def get_timestamp_for_sorting(conv):
            timestamp = conv.get("timestamp", "")
            try:
                if timestamp:
                    return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                else:
                    # Use epoch time (1970) for conversations without timestamp
                    return datetime.fromtimestamp(0)
            except (ValueError, TypeError, KeyError):
                # Fallback to epoch time if timestamp parsing fails
                return datetime.fromtimestamp(0)
        
        sorted_conversations = sorted(
            saved_conversations, 
            key=get_timestamp_for_sorting, 
            reverse=True  # Newest first
        )
        
        conversation_list = []
        for i, conv in enumerate(sorted_conversations):
            title = conv.get("title", f"Conversation {i+1}")
            timestamp = conv.get("timestamp", "")
            message_count = conv.get("message_count", 0)
            
            # Format timestamp for display
            try:
                if timestamp:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    formatted_time = dt.strftime("%m/%d %H:%M")
                else:
                    formatted_time = ""
            except (ValueError, TypeError):
                formatted_time = ""
            
            # Create display entry
            display_text = f"{title}"
            if formatted_time:
                display_text += f" • {formatted_time}"
            if message_count > 0:
                display_text += f" • {message_count} msgs"
            
            conversation_list.append([display_text])
        
        return conversation_list
    
    @staticmethod
    def new_conversation() -> Tuple[Optional[int], List[ChatMessage]]:
        """
        Create a new conversation (clear current chat).
        
        Returns:
            Tuple of (None, empty_messages_list)
        """
        return None, []
