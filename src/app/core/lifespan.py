from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.database import init_db
from src.app.core.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting application lifespan...")
    try:
        # Initialize the database connection
        init_db()
        logger.info("✅ Database initialization successful")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise
    
    logger.info("🚀 Application startup complete")
    
    yield