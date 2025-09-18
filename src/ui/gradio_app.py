"""
Gradio UI Application

Modular Gradio Blocks UI for the AI agent interface.
Now properly separated into modules for easy maintenance and scaling.
"""
import gradio as gr
from .gradio.styles import get_modern_dark_theme
from .gradio.components import get_header_component, get_chat_interface_header
from .gradio.handlers import create_agent_handlers

def build_gradio_ui():
    """
    Builds the main UI using modular components.
    Now with real AI agent integration!
    """
    
    # Get the CSS theme
    css = get_modern_dark_theme()
    
    # Initialize handler
    bot_handlers = create_agent_handlers()

    with gr.Blocks(css=css, title="🤖 AI Agent Chat", theme=gr.themes.Base()) as demo:
        
        # Header Component
        gr.HTML(get_header_component())
        
        # Main Chat Interface
        with gr.Column(elem_classes=["neural-chat"]):
            # Chat interface header
            gr.HTML(get_chat_interface_header())
            
            # Main chatbot with bubble styling
            chatbot = gr.Chatbot(
                type="messages", 
                height=500,
                show_label=False,
                container=True,
                show_copy_button=True,
                bubble_full_width=False,
                layout="bubble",
                elem_classes=["chatbot"]
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

        # Event handlers using modular handlers
        msg.submit(
            bot_handlers.handle_user_message, 
            [msg, chatbot], 
            [msg, chatbot], 
            queue=False
        ).then(
            bot_handlers.generate_bot_response, 
            chatbot, 
            chatbot
        )
        
        clear.click(
            bot_handlers.clear_chat, 
            None, 
            chatbot, 
            queue=False
        )

    return demo
