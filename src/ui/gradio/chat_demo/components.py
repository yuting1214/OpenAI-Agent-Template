"""
Chat History UI Components

Provides UI components for chat history management including conversation list,
new chat button, and save/load controls.
"""

import gradio as gr
from typing import Tuple

def get_demo_header():
    """
    Returns the demo header HTML component.
    """
    return gr.HTML("""
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: #fff; margin-bottom: 10px;">🤖 Chat History Demo</h1>
            <p style="color: #ccc; margin: 0;">
                Demonstrating save/load chat history with only gr.Chatbot
            </p>
        </div>
    """)

def get_chat_interface_header():
    """
    Returns the chat interface header HTML component.
    """
    return gr.HTML("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h3 style="color: #fff; margin: 0;">💬 Chat Interface</h3>
        </div>
    """)

def get_demo_footer():
    return gr.HTML("""
        <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; margin: 20px;">
            <h4 style="color: #fff; margin-top: 0;">📋 How to Use:</h4>
            <ul style="color: #ccc; margin-bottom: 0;">
                <li><strong>💾 Save Current:</strong> Manually save the current conversation</li>
                <li><strong>➕ New Chat:</strong> Start a fresh conversation</li>
                <li><strong>📚 History List:</strong> Click any saved conversation to load it</li>
                <li><strong>🔄 Auto-save:</strong> Conversations are automatically saved after each exchange</li>
                <li><strong>💾 Persistent:</strong> All conversations are saved in your browser's local storage</li>
            </ul>
        </div>
    """)

def create_history_sidebar() -> Tuple[gr.Button, gr.Dataset, gr.Button]:
    """
    Create the chat history sidebar with conversation management controls.
    
    Returns:
        Tuple of (new_chat_button, conversation_list, save_button)
    """
    
    with gr.Column(scale=1, min_width=250):
        # Header for history panel
        gr.HTML("""
            <div style="padding: 10px; border-bottom: 1px solid #333; margin-bottom: 10px;">
                <h3 style="margin: 0; color: #fff; font-size: 16px;">💬 Chat History</h3>
            </div>
        """)
        
        # New chat button
        new_chat_button = gr.Button(
            "➕ New Chat",
            variant="primary",
            size="sm",
            elem_classes=["new-chat-btn"]
        )
        
        # Save current conversation button
        save_button = gr.Button(
            "💾 Save Current",
            variant="secondary", 
            size="sm",
            elem_classes=["save-chat-btn"]
        )
        
        # Conversation list - keep components but hide empty textbox with CSS
        conversation_list = gr.Dataset(
            components=[gr.Textbox(visible=False)],  # Make textbox invisible
            samples=[],
            elem_classes=["conversation-list"]
        )
        
        # Instructions
        gr.HTML("""
            <div style="padding: 10px; font-size: 12px; color: #888; border-top: 1px solid #333; margin-top: 10px;">
                <p style="margin: 0;">Click on a conversation to load it. Use "New Chat" to start fresh.</p>
            </div>
        """)
    
    return new_chat_button, conversation_list, save_button


def create_compact_history_toggle() -> Tuple[gr.Button, gr.Column]:
    """
    Create a compact history toggle for mobile/small screens.
    
    Returns:
        Tuple of (toggle_button, history_column)
    """
    
    toggle_button = gr.Button(
        "📚 History", 
        variant="secondary", 
        size="sm",
        elem_classes=["history-toggle"]
    )
    
    with gr.Column(visible=False, elem_classes=["compact-history"]) as history_column:
        new_chat_btn, conv_list, save_btn = create_history_sidebar()
    
    return toggle_button, history_column, new_chat_btn, conv_list, save_btn