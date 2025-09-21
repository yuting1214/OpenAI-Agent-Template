"""
Gradio UI Application

Modular Gradio Blocks UI for the AI agent interface.
Now properly separated into modules for easy maintenance and scaling.
Includes session state management for persistent conversation memory.
"""
import uuid
import gradio as gr
from .styles import get_modern_dark_theme
from .components import get_header_component, get_chat_interface_header
from .event_listeners import (
    handle_user_message,
    handle_agent_message,
    clear_chat
)

def build_agent_ui():
    """
    Builds the main UI using simple function-based handlers.
    Clean and simple AI agent integration!
    """
    
    # Get the CSS theme
    css = get_modern_dark_theme()

    with gr.Blocks(css=css, title="🤖 AI Agent Chat", theme=gr.themes.Base()) as demo:
        
        # Session State - Generate unique session ID for each user session
        session_id = gr.State(lambda: str(uuid.uuid4()))
        
        # Header Component
        gr.HTML(get_header_component())
        
        # Main Chat Interface
        with gr.Column(elem_classes=["neural-chat"]):
            # Chat interface header
            gr.HTML(get_chat_interface_header())
            
            # Main chatbot with ChatMessage support
            chatbot = gr.Chatbot(
                type="messages", 
                height=500,
                show_label=False,
                container=True,
                show_copy_button=True,
                bubble_full_width=False,
                layout="bubble",
                elem_classes=["chatbot"],
                value=[]  # Initialize with empty ChatMessage list
            )
            
            # Input area with better spacing
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Type your message here...",
                    label="",
                    lines=2,
                    scale=4,
                    show_label=False,
                    container=False
                )
                with gr.Column(scale=1):
                    submit = gr.Button("📤 Send", variant="primary", size="sm")
                    clear = gr.Button("🔄 Clear", variant="secondary", size="sm")

        # Event handlers using event listeners with session state
        # Submit on Enter key (existing functionality)
        msg.submit(
            handle_user_message, 
            [msg, chatbot, session_id], 
            [msg, chatbot], 
            queue=False
        ).then(
            handle_agent_message, 
            [chatbot, session_id], 
            chatbot
        )
        
        # Submit on button click (new functionality for consistency)
        submit.click(
            handle_user_message, 
            [msg, chatbot, session_id], 
            [msg, chatbot], 
            queue=False
        ).then(
            handle_agent_message, 
            [chatbot, session_id], 
            chatbot
        )
        
        # Clear chat history
        clear.click(
            clear_chat, 
            [session_id], 
            chatbot, 
            queue=False
        )

    return demo
