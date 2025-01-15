from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import Base
from app.db.session import engine

async def init_db() -> None:
    """Initialize database tables if they don't exist."""
    async with engine.begin() as conn:
        # Create tables if they don't exist, without dropping existing data
        await conn.run_sync(Base.metadata.create_all)
        print("Database tables initialized successfully!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db()) 