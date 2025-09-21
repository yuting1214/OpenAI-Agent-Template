"""
CSS Styles Module

Contains all CSS styling for the Gradio UI application.
Separated for easy maintenance and theme switching.
"""

def get_modern_dark_theme():
    """
    Returns the eye-friendly modern dark theme CSS.
    Optimized for long reading sessions.
    """
    return """
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    .gradio-container {
        background: #1a1d23;
        font-family: 'Inter', system-ui, sans-serif;
        min-height: 100vh;
        position: relative;
        overflow: hidden;
    }
    
    /* Subtle Ambient Background */
    .gradio-container::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 30%, rgba(99, 102, 241, 0.08) 0%, transparent 60%),
            radial-gradient(circle at 80% 70%, rgba(139, 92, 246, 0.06) 0%, transparent 60%),
            radial-gradient(circle at 40% 80%, rgba(59, 130, 246, 0.05) 0%, transparent 60%);
        animation: subtle-pulse 12s ease-in-out infinite;
        pointer-events: none;
        z-index: 1;
    }
    
    /* Minimal Ambient Particles */
    .gradio-container::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(1px 1px at 20px 30px, rgba(99, 102, 241, 0.3), transparent),
            radial-gradient(1px 1px at 40px 70px, rgba(139, 92, 246, 0.2), transparent),
            radial-gradient(1px 1px at 90px 40px, rgba(59, 130, 246, 0.25), transparent);
        background-repeat: repeat;
        background-size: 200px 150px;
        animation: gentle-float 25s linear infinite;
        pointer-events: none;
        z-index: 1;
    }
    
    @keyframes subtle-pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.02); }
    }
    
    @keyframes gentle-float {
        0% { transform: translateY(0px) translateX(0px); }
        33% { transform: translateY(-8px) translateX(5px); }
        66% { transform: translateY(-4px) translateX(-5px); }
        100% { transform: translateY(0px) translateX(0px); }
    }
    
    /* Modern Header */
    .cyber-header {
        position: relative;
        z-index: 10;
        text-align: center;
        margin: 15px 20px 25px;
        padding: 20px 25px;
        background: linear-gradient(145deg, rgba(30, 35, 42, 0.95), rgba(40, 45, 52, 0.9));
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 15px;
        backdrop-filter: blur(20px);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .cyber-header::before {
        content: '';
        position: absolute;
        top: -1px; left: -1px; right: -1px; bottom: -1px;
        background: linear-gradient(45deg, rgba(99, 102, 241, 0.4), rgba(139, 92, 246, 0.3), rgba(59, 130, 246, 0.4));
        border-radius: 15px;
        z-index: -1;
        animation: gentle-border-glow 6s ease-in-out infinite;
    }
    
    @keyframes gentle-border-glow {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 0.8; }
    }
    
    /* Elegant Title Text */
    .holo-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem;
        font-weight: 600;
        background: linear-gradient(45deg, #a78bfa, #60a5fa, #34d399, #fbbf24);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gentle-shift 8s ease-in-out infinite;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }
    
    @keyframes gentle-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Comfortable Chat Container */
    .neural-chat {
        position: relative;
        z-index: 5;
        background: linear-gradient(145deg, rgba(30, 35, 42, 0.95), rgba(40, 45, 52, 0.9));
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 20px;
        padding: 25px;
        margin: 0 20px 20px;
        backdrop-filter: blur(15px);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        max-width: none;
    }
    
    .neural-chat:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.4),
            0 0 20px rgba(99, 102, 241, 0.1);
        transform: translateY(-2px);
    }
    
    /* Comfortable Button */
    .gradio-button-primary {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.8), rgba(139, 92, 246, 0.8)) !important;
        border: 1px solid rgba(99, 102, 241, 0.6) !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        color: #ffffff !important;
        text-transform: none !important;
        letter-spacing: 0.5px !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.3s ease !important;
        box-shadow: 
            0 4px 12px rgba(99, 102, 241, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    .gradio-button-primary::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent) !important;
        transition: left 0.5s !important;
    }
    
    .gradio-button-primary:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.9), rgba(139, 92, 246, 0.9)) !important;
        border-color: rgba(99, 102, 241, 0.8) !important;
        box-shadow: 
            0 6px 20px rgba(99, 102, 241, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    
    .gradio-button-primary:hover::before {
        left: 100% !important;
    }
    
    /* Subtle Status Indicators */
    .status-grid {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin: 15px 0 10px;
        flex-wrap: wrap;
    }
    
    .status-item {
        background: rgba(30, 35, 42, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 8px;
        padding: 8px 12px;
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        color: #a78bfa;
        text-align: center;
        position: relative;
        overflow: hidden;
        min-width: 100px;
    }
    
    .status-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.6), rgba(139, 92, 246, 0.6));
        animation: gentle-scan 3s linear infinite;
    }
    
    @keyframes gentle-scan {
        0% { transform: translateX(-100%); opacity: 0.5; }
        50% { opacity: 1; }
        100% { transform: translateX(100%); opacity: 0.5; }
    }
    
    /* Chat Bubble Styling - User on Right, Assistant on Left */
    .message-wrap {
        display: flex !important;
        margin: 10px 0 !important;
    }
    
    /* User messages (right side) - Soft Theme */
    .message-wrap:has([data-testid*="user"]) {
        justify-content: flex-end !important;
    }
    
    .message-wrap:has([data-testid*="user"]) .message {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.25), rgba(99, 102, 241, 0.2)) !important;
        color: #e5e7eb !important;
        border-radius: 18px 18px 4px 18px !important;
        padding: 12px 16px !important;
        margin-left: 60px !important;
        margin-right: 0px !important;
        box-shadow: 0 3px 8px rgba(59, 130, 246, 0.15) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        font-family: 'Inter', sans-serif !important;
        max-width: 70% !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Assistant messages (left side) - Soft Theme */
    .message-wrap:has([data-testid*="assistant"]) {
        justify-content: flex-start !important;
    }
    
    .message-wrap:has([data-testid*="assistant"]) .message {
        background: linear-gradient(135deg, rgba(55, 65, 81, 0.8), rgba(75, 85, 99, 0.7)) !important;
        color: #d1d5db !important;
        border-radius: 18px 18px 18px 4px !important;
        padding: 12px 16px !important;
        margin-right: 60px !important;
        margin-left: 0px !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(75, 85, 99, 0.4) !important;
        font-family: 'Inter', sans-serif !important;
        max-width: 70% !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Alternative approach using CSS selectors */
    .chatbot .message-wrap .message {
        border-radius: 18px !important;
        padding: 12px 16px !important;
        margin: 8px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* User message styling (appears on right) - Consistent Soft Theme */
    .chatbot .message-wrap:nth-child(odd) {
        justify-content: flex-end !important;
    }
    
    .chatbot .message-wrap:nth-child(odd) .message {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.25), rgba(99, 102, 241, 0.2)) !important;
        color: #e5e7eb !important;
        border-radius: 18px 18px 4px 18px !important;
        margin-left: 60px !important;
        margin-right: 8px !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        box-shadow: 0 3px 8px rgba(59, 130, 246, 0.15) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Assistant message styling (appears on left) - Consistent Soft Theme */
    .chatbot .message-wrap:nth-child(even) {
        justify-content: flex-start !important;
    }
    
    .chatbot .message-wrap:nth-child(even) .message {
        background: linear-gradient(135deg, rgba(55, 65, 81, 0.8), rgba(75, 85, 99, 0.7)) !important;
        color: #d1d5db !important;
        border-radius: 18px 18px 18px 4px !important;
        margin-right: 60px !important;
        margin-left: 8px !important;
        border: 1px solid rgba(75, 85, 99, 0.4) !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Eye-friendly Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 35, 42, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, rgba(99, 102, 241, 0.6), rgba(139, 92, 246, 0.6));
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, rgba(99, 102, 241, 0.8), rgba(139, 92, 246, 0.8));
    }
    """


def get_cyberpunk_theme():
    """
    Returns the original bright cyberpunk theme CSS.
    High contrast, neon colors for dramatic effect.
    """
    # This could be implemented later for theme switching
    pass


def get_light_theme():
    """
    Returns a light theme CSS for daytime use.
    """
    # This could be implemented later for theme switching
    pass
