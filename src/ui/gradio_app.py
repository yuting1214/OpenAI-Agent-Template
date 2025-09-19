"""
Gradio UI Application

Modular Gradio Blocks UI for the AI agent interface.
Now properly separated into modules for easy maintenance and scaling.
"""
import gradio as gr
from .gradio.styles import get_modern_dark_theme
from .gradio.components import get_header_component, get_chat_interface_header
from .gradio.event_listeners import (
    handle_user_message,
    handle_agent_message,
    clear_chat
)

def build_gradio_ui():
    """
    Builds the main UI using simple function-based handlers.
    Clean and simple AI agent integration!
    """
    
    # Get the CSS theme
    css = get_modern_dark_theme()

    with gr.Blocks(css=css, title="🤖 AI Agent Chat", theme=gr.themes.Base()) as demo:
        
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
                    lines=1,
                    scale=4,
                    show_label=False,
                    container=False
                )
                clear = gr.Button("🔄 Clear", variant="primary", scale=1, size="sm")

        # Event handlers using event listeners
        msg.submit(
            handle_user_message, 
            [msg, chatbot], 
            [msg, chatbot], 
            queue=False
        ).then(
            handle_agent_message, 
            chatbot, 
            chatbot
        )
        
        clear.click(
            clear_chat, 
            None, 
            chatbot, 
            queue=False
        )

    return demo
