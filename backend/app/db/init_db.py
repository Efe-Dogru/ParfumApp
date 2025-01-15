from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import Base
from app.db.session import engine, AsyncSessionLocal
from app.models.perfume import Perfume

async def init_db() -> None:
    """Initialize database tables if they don't exist."""
    async with engine.begin() as conn:
        # Create tables if they don't exist, without dropping existing data
        await conn.run_sync(Base.metadata.create_all)

async def init_and_seed_db():
    """Initialize the database tables without seeding (preserving existing data)."""
    try:
        await init_db()
        print("Database tables initialized successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

# Run the initialization
if __name__ == "__main__":
    import asyncio
    asyncio.run(init_and_seed_db()) 