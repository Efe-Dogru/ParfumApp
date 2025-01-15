import asyncio
import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db.init_db import init_and_seed_db

if __name__ == "__main__":
    asyncio.run(init_and_seed_db()) 