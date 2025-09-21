# 🤖 OpenAI SDK Learning Platform

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/openai-agent-sdk?referralCode=jk_FgY&utm_medium=integration&utm_source=template&utm_campaign=generic)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)


**Master both OpenAI SDKs with hands-on examples!**

This project helps developers understand and compare the **OpenAI Agent SDK** and the **traditional OpenAI Python library** through interactive web interfaces. Perfect for learning, prototyping, and building production-ready AI applications.

---

## 🎯 **What You'll Learn**

### **Two OpenAI SDKs, Side by Side:**

| 🔧 **Agent SDK** (`/agent`) | 💬 **Chat SDK** (`/chat`) |
|----------------------------|---------------------------|
| **Advanced AI Agents** | **Simple Chat Completions** |
| Tool calling, memory, streaming | Direct API calls, streaming |
| Persistent conversation history | Session-based chat history |
| Complex multi-step reasoning | Straightforward Q&A |
| Production-ready agent framework | Traditional chat interface |

### **🚀 Key Learning Outcomes:**
- ✅ **Compare** both OpenAI SDKs in action
- ✅ **Understand** when to use each approach
- ✅ **Build** your own AI agents and chat applications
- ✅ **Deploy** production-ready solutions
- ✅ **Customize** agent configurations easily

---

## 🏃‍♂️ **Quick Start**

### **1. Clone & Setup**
```bash
git clone <your-repo>
cd OpenAI-Agent-Template
```

### **2. Install Dependencies**
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### **3. Configure API Keys**
Create a `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
FIREWORKS_API_KEY=your_fireworks_api_key_here  # Optional
```

### **4. Run the Application**
```bash
python main.py
```

### **5. Explore Both Interfaces**
- 🤖 **Agent SDK Demo**: http://localhost:5000/agent
- 💬 **Chat SDK Demo**: http://localhost:5000/chat

---

## 🎮 **How to Use**

### **🤖 Agent Interface (`/agent`)**
**Experience the full power of OpenAI's Agent SDK:**

- **Persistent Memory**: Conversations remember context across sessions
- **Tool Integration**: Weather tools, web search, and more
- **Streaming Responses**: Real-time AI responses
- **Session Management**: Each browser session maintains separate memory
- **Advanced Features**: Multi-turn reasoning, complex workflows

**Try asking:**
- *"What's the weather like today?"*
- *"Remember that I like coffee. What should I drink tomorrow?"*
- *"Can you help me plan a trip to Japan?"*

### **💬 Chat Interface (`/chat`)**
**Learn traditional OpenAI API usage:**

- **Direct API Calls**: Simple request-response pattern
- **Chat History**: Save and load conversations
- **Streaming**: Real-time response generation
- **Session Storage**: Browser-based conversation management
- **Clean & Simple**: Perfect for learning API basics

**Try asking:**
- *"Explain quantum computing in simple terms"*
- *"Write a Python function to sort a list"*
- *"What are the benefits of renewable energy?"*

---

## ⚙️ **Customization Guide**

### **🔧 Agent Configuration**
Want to customize your AI agent? Edit `src/agent/registry.py`:

```python
# Add your custom agent configuration
AGENT_CONFIGS = {
    "openai": {
        "name": "Agent (OpenAI)",
        "model_factory": openai_model_factory,
        "model_settings": chat_model_settings,
        "instructions": INSTRUCTIONS,  # ← Edit your agent's personality
        "tools": [fetch_weather],      # ← Add your custom tools
    },
    "your_custom_agent": {
        "name": "My Custom Agent",
        "model_factory": openai_model_factory,
        "model_settings": your_custom_settings,
        "instructions": "You are a helpful coding assistant...",
        "tools": [your_custom_tools],
    }
}
```

### **🎛️ Switch Between Agents**
```bash
# Use environment variable to switch agents
AGENT_TYPE=openai python main.py      # Default OpenAI
AGENT_TYPE=fireworks python main.py   # Fireworks AI
AGENT_TYPE=your_custom_agent python main.py  # Your custom agent
```

### **🛠️ Add Custom Tools**
Create new tools in `src/agent/tools/`:
```python
def your_custom_tool():
    """Your custom tool implementation"""
    pass

# Add to registry.py
"tools": [fetch_weather, your_custom_tool]
```

---

## 🌟 **Features**

### **🔥 Production Ready**
- ✅ **FastAPI Backend**: High-performance async web server
- ✅ **Database Integration**: SQLite (dev) / PostgreSQL (prod)
- ✅ **Session Management**: Persistent conversation memory
- ✅ **Error Handling**: Graceful fallbacks and user feedback
- ✅ **Logging**: Structured logging for debugging
- ✅ **Docker Support**: Easy deployment anywhere

### **🎨 Beautiful UI**
- ✅ **Modern Design**: Clean, responsive Gradio interface
- ✅ **Dark Theme**: Easy on the eyes
- ✅ **Real-time Streaming**: Watch AI responses generate live
- ✅ **Chat History**: Save and manage conversations
- ✅ **Mobile Friendly**: Works great on all devices

### **🧠 Smart Memory**
- ✅ **Persistent Sessions**: Conversations survive page refreshes
- ✅ **Memory Limits**: Optimized for performance (10 recent messages)
- ✅ **Database Storage**: All conversations safely stored
- ✅ **Session Isolation**: Each user gets private memory

---

## 🚀 **Deployment**

### **Environment Variables**
```bash
# Required
OPENAI_API_KEY=your_key_here

# Optional
FIREWORKS_API_KEY=your_fireworks_key
AGENT_TYPE=openai  # or fireworks
DB_URL=your_database_url
```

### **Docker Deployment**
```bash
docker build -t openai-agent-platform .
docker run -p 5000:5000 -e OPENAI_API_KEY=your_key openai-agent-platform
```

### **Railway/Heroku Deployment**
1. Fork this repository
2. Connect to Railway/Heroku
3. Set environment variables
4. Deploy! 🚀

---

## 🎓 **Learning Path**

### **Beginner → Start with Chat SDK** (`/chat`)
1. Understand basic OpenAI API calls
2. Learn about streaming responses  
3. Explore chat history management
4. Practice with different prompts

### **Intermediate → Explore Agent SDK** (`/agent`)
1. Experience persistent memory
2. See tool calling in action
3. Understand session management
4. Compare with traditional approach

### **Advanced → Customize Everything**
1. Modify agent configurations
2. Add custom tools and capabilities
3. Implement your own business logic
4. Deploy to production

---

## ❓ **FAQ**

**Q: Which SDK should I use for my project?**
A: Use **Agent SDK** for complex, multi-step workflows with memory. Use **Chat SDK** for simple, stateless interactions.

**Q: Can I add my own AI models?**
A: Yes! Edit `src/agent/registry.py` to add new model configurations.

**Q: How do I add custom tools?**
A: Create functions in `src/agent/tools/` and add them to your agent configuration.

**Q: Is this production ready?**
A: Yes! Includes proper error handling, logging, database integration, and deployment configurations.

---

## 📄 **License**

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

### **What this means:**
- ✅ **Commercial Use**: Use this project in commercial applications
- ✅ **Modification**: Modify and distribute your changes
- ✅ **Distribution**: Share this project with others
- ✅ **Private Use**: Use privately without restrictions
- ⚠️ **Attribution**: Include copyright notice and license
- ⚠️ **State Changes**: Document significant changes you make

---

**🎉 Happy Learning! Start exploring both interfaces and discover which OpenAI SDK fits your needs best!**
