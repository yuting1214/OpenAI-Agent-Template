"""
Chat History Demo

This example demonstrates how to use the chat history save/load functionality
with only gr.Chatbot (no gr.ChatInterface needed).

Features:
- Save and load conversations
- Browser-based persistent storage
- Conversation list management
- Auto-save after each exchange
- New chat creation
- Manual save option

"""

import gradio as gr
from src.ui.gradio.chat_demo.styles import create_history_styles
from src.ui.gradio.chat_demo.components import (
    get_demo_header,
    get_chat_interface_header,
    get_demo_footer,
    create_history_sidebar
)
from src.ui.gradio.chat_demo.event_listeners import (
    handle_user_message,
    handle_demo_response,
    demo_create_new_conversation,
    demo_auto_save_conversation,
    demo_update_conversation_list,
    demo_manual_save,
    demo_load_conversation
)
        
def build_chat_ui():
    """Build the demo UI with chat history functionality."""
    
    # CSS with history styles
    css = create_history_styles()
    
    with gr.Blocks(
        css=css, 
        title="🤖 Chat History Demo", 
        theme=gr.themes.Base()
    ) as demo:
        
        # Header
        get_demo_header()
        
        # Browser state for persistent storage
        saved_conversations = gr.BrowserState(
            [], 
            storage_key="demo_chat_conversations"
        )
        conversation_id = gr.State(None)
        
        # Main layout
        with gr.Row():
            # History sidebar
            conversation_list, new_chat_btn, save_btn = create_history_sidebar()
            
            # Main chat area
            with gr.Column(scale=3, elem_classes=["neural-chat"]):
                get_chat_interface_header()
                
                # Chatbot
                chatbot = gr.Chatbot(
                    type="messages",
                    height=400,
                    show_label=False,
                    container=True,
                    show_copy_button=True,
                    bubble_full_width=False,
                    layout="bubble",
                    elem_classes=["chatbot"],
                    value=[]
                )
                
                # Input area
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="Type your message here...",
                        label="",
                        lines=1,
                        scale=4,
                        show_label=False,
                        container=False
                    )
                    clear = gr.Button("🔄 Clear", variant="secondary", scale=1, size="sm")
        
        # Instructions
        get_demo_footer()
        
        # Event handlers
        ## Main chat flow
        msg.submit(
            handle_user_message,
            [msg, chatbot],
            [msg, chatbot],
            queue=False
        ).then(
            handle_demo_response,
            chatbot,
            chatbot,
            queue=True  # Must be True for streaming responses
        ).then(
            # Auto-save after response
            demo_auto_save_conversation,
            [conversation_id, chatbot, saved_conversations],
            [conversation_id, saved_conversations],
            queue=False
        ).then(
            # Update conversation list
            demo_update_conversation_list,
            [saved_conversations],
            [conversation_list],
            queue=False
        )
        
        # Clear button
        clear.click(
            lambda: (None, []),
            None,
            [conversation_id, chatbot],
            queue=False
        )
        
        # History management
        new_chat_btn.click(
            demo_create_new_conversation,
            None,
            [conversation_id, chatbot],
            queue=False
        )
        
        save_btn.click(
            demo_manual_save,
            [conversation_id, chatbot, saved_conversations],
            [conversation_id, saved_conversations],
            queue=False
        ).then(
            demo_update_conversation_list,
            [saved_conversations],
            [conversation_list],
            queue=False
        )
        
        conversation_list.select(
            demo_load_conversation,
            [saved_conversations],
            [conversation_id, chatbot],
            queue=False
        )
        
        # Initialize conversation list on load
        demo.load(
            demo_update_conversation_list,
            [saved_conversations],
            [conversation_list],
            queue=False
        )
    
    return demo
