import os
import uvicorn
import gradio as gr
from fastapi import FastAPI
from src.app.core.init_settings import args
from src.app.core.middlewares import setup_cors, setup_session
from src.app.core.lifespan import lifespan
from src.app.core.logging import logger
from src.app.core.routers import setup_routers
from src.ui.gradio_app import build_gradio_ui

app = FastAPI(lifespan=lifespan)
logger.info("FastAPI application started")

# Set Middleware
setup_cors(app)
setup_session(app)

# Setup Routers
setup_routers(app)

# Gradio app
audio_ui = build_gradio_ui()
app = gr.mount_gradio_app(app, audio_ui, path="/chatbot", root_path="/chatbot")

if __name__ == "__main__":
    uvicorn.run(
        app="src.app.main:app",
        host = args.host,
        port=int(os.getenv("PORT", 5000)),
        reload=args.mode == "dev"
    )