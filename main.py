import asyncio
from app.bot import start_bot
from app.database import init_db
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    init_db()
    asyncio.run(start_bot())
