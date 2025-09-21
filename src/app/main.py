import os
import uvicorn
import gradio as gr
from fastapi import FastAPI
from src.app.core.init_settings import args
from src.app.core.middlewares import setup_cors, setup_session
from src.app.core.lifespan import lifespan
from src.app.core.logging import logger
from src.app.core.routers import setup_routers
from src.ui.gradio.agent_demo.app import build_agent_ui
from src.ui.gradio.chat_demo.app import build_chat_ui

app = FastAPI(lifespan=lifespan)
logger.info("FastAPI application started")

# Set Middleware
setup_cors(app)
setup_session(app)

# Setup Routers
setup_routers(app)

# Gradio app
agent_ui = build_agent_ui()
chat_ui = build_chat_ui()
app = gr.mount_gradio_app(app, agent_ui, path="/agent", root_path="/agent")
app = gr.mount_gradio_app(app, chat_ui, path="/chat", root_path="/chat")

if __name__ == "__main__":
    uvicorn.run(
        app="src.app.main:app",
        host = args.host,
        port=int(os.getenv("PORT", 5000)),
        reload=args.mode == "dev"
    )