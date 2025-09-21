def create_history_styles() -> str:
    """
    Create CSS styles for the history components.
    
    Returns:
        CSS string for styling history components
    """
    
    return """
    .gradio-container {
        max-width: 1200px !important;
        margin: 0 auto;
    }
    
    .neural-chat {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 10px;
    }

    .conversation-list {
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #333;
        border-radius: 8px;
        background: #1a1a1a;
    }
    
    .conversation-list .sample {
        padding: 8px 12px;
        border-bottom: 1px solid #333;
        cursor: pointer;
        transition: background-color 0.2s;
        font-size: 13px;
        line-height: 1.4;
    }
    
    .conversation-list .sample:hover {
        background-color: #2a2a2a;
    }
    
    .conversation-list .sample:last-child {
        border-bottom: none;
    }
    
    .new-chat-btn, .save-chat-btn {
        width: 100%;
        margin-bottom: 8px;
        font-size: 13px;
        padding: 8px 12px;
    }
    
    .new-chat-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
    }
    
    .save-chat-btn {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border: none;
        color: white;
    }
    
    .new-chat-btn:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        transform: translateY(-1px);
    }
    
    .save-chat-btn:hover {
        background: linear-gradient(135deg, #ec7eed 0%, #f24e5f 100%);
        transform: translateY(-1px);
    }
    """
