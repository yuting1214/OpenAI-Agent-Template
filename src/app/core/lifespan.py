from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.database import init_db
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database connection
    init_db()
    yield