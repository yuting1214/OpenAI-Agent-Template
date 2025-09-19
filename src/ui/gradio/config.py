"""
Configuration Module

Contains configuration settings for the Gradio UI.
Allows easy customization without touching core code.
"""

# UI Configuration
UI_CONFIG = {
    "title": "🧠 Neural Chatbot",
    "theme": "gr.themes.Base()",
    "chatbot_height": 500,
    "show_copy_button": True,
    "bubble_layout": True,
    "typing_speed": 0.03,  # seconds per character
}

# Header Configuration
HEADER_CONFIG = {
    "title": "🧠 AI Assistant",
    "subtitle": "Intelligent conversation system",
    "status_items": [
        {"icon": "🧠", "name": "AI Core", "status": "Ready"},
        {"icon": "💬", "name": "Chat", "status": "Active"}, 
        {"icon": "🔒", "name": "Secure", "status": "Online"}
    ]
}

# Chat Configuration
CHAT_CONFIG = {
    "interface_title": "💬 Chat Interface",
    "interface_subtitle": "Start a conversation with the AI assistant",
    "placeholder_text": "Type your message here...",
    "clear_button_text": "🔄 Clear",
    "handler_type": "agent"  # "agent", "neural", or "simple"
}

# Theme Configuration
THEME_CONFIG = {
    "current_theme": "modern_dark",  # "modern_dark", "cyberpunk", "light"
    "custom_css": None  # Optional custom CSS override
}

# Response Configuration
RESPONSE_CONFIG = {
    "response_type": "agent",   # "agent", "neural", or "simple"
    "custom_responses": None,   # List of custom responses (optional)
    "enable_typing_animation": True,
    "typing_speed": 0.03
}


def get_ui_config():
    """Returns the current UI configuration."""
    return UI_CONFIG


def get_header_config():
    """Returns the current header configuration."""
    return HEADER_CONFIG


def get_chat_config():
    """Returns the current chat configuration."""
    return CHAT_CONFIG


def get_theme_config():
    """Returns the current theme configuration."""
    return THEME_CONFIG


def get_response_config():
    """Returns the current response configuration."""
    return RESPONSE_CONFIG


def update_config(section, updates):
    """
    Updates a configuration section.
    
    Args:
        section: Configuration section name ("ui", "header", "chat", "theme", "response")
        updates: Dictionary of updates to apply
    """
    config_map = {
        "ui": UI_CONFIG,
        "header": HEADER_CONFIG,
        "chat": CHAT_CONFIG,
        "theme": THEME_CONFIG,
        "response": RESPONSE_CONFIG
    }
    
    if section in config_map:
        config_map[section].update(updates)
    else:
        raise ValueError(f"Unknown configuration section: {section}")



