"""
UI Components Module

Contains all HTML layout components for the Gradio UI.
Separated for easy maintenance and component reusability.
"""

def get_header_component():
    """
    Returns the main header HTML component.
    """
    return """
    <div class="cyber-header">
        <div class="holo-text">🤖 AI Agent</div>
        <p style="color: #a78bfa; font-family: 'Inter', sans-serif; font-size: 0.85rem; margin: 5px 0; opacity: 0.8;">
            Powered by LLM • Real-time responses
        </p>
        
        <div class="status-grid">
            <div class="status-item">
                <div>🚀 LLM</div>
                <div style="font-size: 0.6rem; opacity: 0.7; margin-top: 2px;">Connected</div>
            </div>
            <div class="status-item">
                <div>💬 Chat</div>
                <div style="font-size: 0.6rem; opacity: 0.7; margin-top: 2px;">Active</div>
            </div>
            <div class="status-item">
                <div>🔒 Secure</div>
                <div style="font-size: 0.6rem; opacity: 0.7; margin-top: 2px;">Online</div>
            </div>
        </div>
    </div>
    """


def get_chat_interface_header():
    """
    Returns the chat interface header HTML component.
    """
    return """
    <div style="border-left: 3px solid rgba(99, 102, 241, 0.6); padding-left: 15px; margin-bottom: 20px;">
        <h3 style="color: #a78bfa; font-family: 'Inter', sans-serif; margin: 0; font-size: 1rem; font-weight: 600;">
            💬 AI Agent Chat
        </h3>
        <p style="color: #9ca3af; font-size: 0.8rem; margin: 3px 0 0; opacity: 0.8;">
            Chat with a real AI agent powered by your favorite LLM
        </p>
    </div>
    """


def get_status_component(ai_status="Ready", chat_status="Active", security_status="Online"):
    """
    Returns a customizable status component.
    
    Args:
        ai_status: Status of AI Core (default: "Ready")
        chat_status: Status of Chat system (default: "Active") 
        security_status: Status of Security (default: "Online")
    """
    return f"""
    <div class="status-grid">
        <div class="status-item">
            <div>🧠 AI Core</div>
            <div style="font-size: 0.6rem; opacity: 0.7; margin-top: 2px;">{ai_status}</div>
        </div>
        <div class="status-item">
            <div>💬 Chat</div>
            <div style="font-size: 0.6rem; opacity: 0.7; margin-top: 2px;">{chat_status}</div>
        </div>
        <div class="status-item">
            <div>🔒 Secure</div>
            <div style="font-size: 0.6rem; opacity: 0.7; margin-top: 2px;">{security_status}</div>
        </div>
    </div>
    """


def get_custom_header(title="🧠 AI Assistant", subtitle="Intelligent conversation system"):
    """
    Returns a customizable header component.
    
    Args:
        title: Main title text (default: "🧠 AI Assistant")
        subtitle: Subtitle text (default: "Intelligent conversation system")
    """
    return f"""
    <div class="cyber-header">
        <div class="holo-text">{title}</div>
        <p style="color: #a78bfa; font-family: 'Inter', sans-serif; font-size: 0.85rem; margin: 5px 0; opacity: 0.8;">
            {subtitle}
        </p>
        {get_status_component()}
    </div>
    """


def get_section_header(title, subtitle, icon_color="rgba(99, 102, 241, 0.6)"):
    """
    Returns a reusable section header component.
    
    Args:
        title: Section title
        subtitle: Section subtitle
        icon_color: Color for the left border accent
    """
    return f"""
    <div style="border-left: 3px solid {icon_color}; padding-left: 15px; margin-bottom: 20px;">
        <h3 style="color: #a78bfa; font-family: 'Inter', sans-serif; margin: 0; font-size: 1rem; font-weight: 600;">
            {title}
        </h3>
        <p style="color: #9ca3af; font-size: 0.8rem; margin: 3px 0 0; opacity: 0.8;">
            {subtitle}
        </p>
    </div>
    """
