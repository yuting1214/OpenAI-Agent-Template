from fastapi import FastAPI
from src.app.api.v1.endpoints import base

def setup_routers(app: FastAPI):
    app.include_router(base.router, prefix="", tags=["main"])