import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import pool
from alembic import context
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.db import Base, DATABASE_URL

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_online():
    connectable = AsyncEngine(
        poolclass=pool.NullPool,
        url=DATABASE_URL,
    )
    async def run_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(context.configure, url=DATABASE_URL, target_metadata=target_metadata)
            await connection.run_sync(context.run_migrations)
    asyncio.run(run_migrations())

run_migrations_online() 