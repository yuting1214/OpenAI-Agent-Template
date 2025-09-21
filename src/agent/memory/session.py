"""
Custom Memory Session for OpenAI Agent SDK

This module provides a custom memory session implementation that extends
the OpenAI Agents SDK SQLAlchemySession to provide optimized memory usage
for long conversations with automatic limitation to recent conversation items.
"""

import json
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine
from agents.extensions.memory.sqlalchemy_session import SQLAlchemySession, TResponseInputItem
from src.app.core.logging import logger
from src.db.database import async_engine



class CustomMemorySession(SQLAlchemySession):
    """
    Custom memory session for agents with limited conversation history.
    
    This class extends the OpenAI Agents SDK SQLAlchemySession to provide:
    - Automatic limitation to latest 10 conversation items
    - Optimized memory usage for long conversations
    - Agent-specific session management
    
    Features:
    - Inherits all SQLAlchemySession functionality
    - Overrides get_items() to return only latest 10 items by default
    - Maintains full conversation history in database
    - Provides methods to access full history when needed
    """
    
    DEFAULT_MEMORY_LIMIT = 10
    
    def __init__(
        self,
        session_id: str,
        engine: AsyncEngine,
        memory_limit: int = DEFAULT_MEMORY_LIMIT,
        create_tables: bool = False,
    ):
        """
        Initialize Custom Memory Session.
        
        Args:
            session_id: Unique identifier for the conversation session
            engine: SQLAlchemy AsyncEngine instance
            memory_limit: Maximum number of recent items to return (default: 10)
            create_tables: Whether to create tables if they don't exist (default: False)
        """
        # Initialize parent with custom table prefix
        super().__init__(
            session_id=session_id,
            engine=engine,
            create_tables=create_tables,
        )
        
        self.memory_limit = memory_limit

    async def get_items(self, limit: Optional[int] = None) -> List[TResponseInputItem]:
        """
        Get recent conversation items in chronological order with guaranteed user->assistant pattern.
        
        Args:
            limit: Number of recent messages to fetch. If None, uses self.memory_limit
            
        Returns:
            List of conversation items in chronological order (oldest first)
            
        Note:
            This fetches the most recent 'limit' messages and returns them in 
            chronological order, ensuring proper conversation flow.
        """
        effective_limit = limit if limit is not None else self.memory_limit
        
        logger.debug(f"Getting {effective_limit} recent conversation items in chronological order")
        
        await self._ensure_tables()
        
        async with self._session_factory() as sess:
            # Get the most recent 'limit' messages in DESC order (newest first)
            stmt = (
                select(self._messages.c.message_data)
                .where(self._messages.c.session_id == self.session_id)
                .order_by(self._messages.c.created_at.desc())
                .limit(effective_limit)
            )
            
            result = await sess.execute(stmt)
            rows: List[str] = [row[0] for row in result.all()]
            
            # Reverse to get chronological order (oldest first)
            rows.reverse()
            
            # Deserialize items
            items: List[TResponseInputItem] = []
            for raw in rows:
                try:
                    item = await self._deserialize_item(raw)
                    items.append(item)
                except json.JSONDecodeError:
                    # Skip corrupted messages
                    logger.warning(f"Skipping corrupted message in session {self.session_id}")
                    continue

            logger.debug(f"Retrieved {len(items)} conversation items")
            return items
    
    # async def get_all_items(self) -> List[TResponseInputItem]:
    #     """
    #     Get all conversation items without memory limit.
        
    #     Returns:
    #         List of all conversation items in chronological order
            
    #     Note:
    #         Use this method when you need access to full conversation history,
    #         e.g., for analytics, debugging, or conversation export.
    #     """
    #     logger.debug("Getting all conversation items (no limit)")
        
    #     # Call parent method with no limit
    #     items = await super().get_items(limit=None)
        
    #     logger.debug(f"Retrieved {len(items)} total conversation items")
    #     return items
    
    # async def get_recent_items(self, count: int) -> List[TResponseInputItem]:
    #     """
    #     Get a specific number of recent conversation items.
        
    #     Args:
    #         count: Number of recent items to retrieve
            
    #     Returns:
    #         List of recent conversation items
    #     """
    #     logger.debug(f"Getting {count} recent conversation items")
        
    #     items = await self.get_items(limit=count)
        
    #     logger.debug(f"Retrieved {len(items)} recent conversation items")
    #     return items
    
    # async def get_conversation_summary(self) -> dict:
    #     """
    #     Get a summary of the conversation session.
        
    #     Returns:
    #         Dictionary with conversation statistics and metadata
    #     """
    #     all_items = await self.get_all_items()
    #     recent_items = await self.get_items()
        
    #     return {
    #         "session_id": self.session_id,
    #         "total_items": len(all_items),
    #         "recent_items": len(recent_items),
    #         "memory_limit": self.memory_limit,
    #         "has_more_history": len(all_items) > self.memory_limit
    #     }
    
    # def set_memory_limit(self, new_limit: int) -> None:
    #     """
    #     Update the memory limit for this session.
        
    #     Args:
    #         new_limit: New memory limit (must be positive)
            
    #     Raises:
    #         ValueError: If new_limit is not positive
    #     """
    #     if new_limit <= 0:
    #         raise ValueError("Memory limit must be positive")
        
    #     old_limit = self.memory_limit
    #     self.memory_limit = new_limit
        
    #     logger.info(f"Memory limit updated from {old_limit} to {new_limit} for session '{self.session_id}'")
    
    # async def cleanup_old_messages(self, keep_count: int = 50) -> int:
    #     """
    #     Clean up old messages beyond a certain count to manage database size.
        
    #     Args:
    #         keep_count: Number of recent messages to keep (default: 50)
            
    #     Returns:
    #         Number of messages deleted
            
    #     Note:
    #         This is useful for long-running sessions to prevent database bloat.
    #         The current memory limit is unaffected.
    #     """
    #     await self._ensure_tables()
        
    #     # Get messages to delete (beyond keep_count)
    #     async with self._session_factory() as sess:
    #         async with sess.begin():
    #             # Get IDs of messages to delete
    #             from sqlalchemy import delete, func
                
    #             # Count total messages
    #             count_stmt = select(func.count()).select_from(self._messages).where(
    #                 self._messages.c.session_id == self.session_id
    #             )
    #             total_count = await sess.scalar(count_stmt)
                
    #             if total_count <= keep_count:
    #                 logger.debug(f"No cleanup needed: {total_count} <= {keep_count}")
    #                 return 0
                
    #             # Get IDs of oldest messages to delete
    #             delete_count = total_count - keep_count
    #             oldest_ids_stmt = (
    #                 select(self._messages.c.id)
    #                 .where(self._messages.c.session_id == self.session_id)
    #                 .order_by(self._messages.c.created_at.asc())
    #                 .limit(delete_count)
    #             )
                
    #             result = await sess.execute(oldest_ids_stmt)
    #             ids_to_delete = [row[0] for row in result.all()]
                
    #             if not ids_to_delete:
    #                 return 0
                
    #             # Delete old messages
    #             delete_stmt = delete(self._messages).where(
    #                 self._messages.c.id.in_(ids_to_delete)
    #             )
    #             await sess.execute(delete_stmt)
                
    #             logger.info(f"Cleaned up {len(ids_to_delete)} old messages from session '{self.session_id}'")
    #             return len(ids_to_delete)


async def get_or_create_memory_session(session_id: str) -> CustomMemorySession:
    """
    Get or create a memory session for the given session ID.
    
    This function utilizes the existing database engine from your codebase
    to create a CustomMemorySession instance.
    
    Args:
        session_id: Unique identifier for the conversation session
        
    Returns:
        CustomMemorySession instance
    """
    # Use the existing async engine from your database setup
    engine = async_engine
    
    session = CustomMemorySession(
        session_id=session_id,
        engine=engine,
        create_tables=True,
    )
    
    logger.info(f"💾 Memory session created/retrieved for: {session_id}")
    return session
