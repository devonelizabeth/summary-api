"""Database models and async CRUD operations for summaries."""
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, func, desc
from sqlalchemy.future import select
from datetime import datetime
from app.schemas import TaskStatus
from typing import List

DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class Summary(Base):
    """SQLAlchemy model for the summaries table."""
    __tablename__ = "summaries"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    source = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class Task(Base):
    """SQLAlchemy model for background tasks."""
    __tablename__ = "tasks"
    id = Column(String(36), primary_key=True)  # UUID
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    result_id = Column(Integer, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

def summary_to_dict(obj):
    """Convert a Summary object to a dictionary."""
    return {
        "id": obj.id,
        "content": obj.content,
        "summary": obj.summary,
        "source": obj.source,
        "created_at": obj.created_at,
    }

async def init_db():
    """Initialize the database and create tables if they do not exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def create_summary(content: str, summary: str, source: str):
    """Create a new summary record in the database."""
    async with SessionLocal() as session:
        obj = Summary(content=content, summary=summary, source=source)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

async def get_summary_by_id(id: int):
    """Retrieve a summary record by its ID."""
    async with SessionLocal() as session:
        result = await session.execute(select(Summary).where(Summary.id == id))
        obj = result.scalar_one_or_none()
        return obj

async def get_recent_summaries(limit: int = 5) -> List[Summary]:
    """Retrieve the most recent summaries.
    
    Args:
        limit (int): Maximum number of summaries to return. Defaults to 5.
    
    Returns:
        List[Summary]: List of recent summaries, ordered by creation date (newest first).
    """
    async with SessionLocal() as session:
        result = await session.execute(
            select(Summary)
            .order_by(desc(Summary.created_at))
            .limit(limit)
        )
        return result.scalars().all()

async def get_total_summaries() -> int:
    """Get the total count of summaries in the database."""
    async with SessionLocal() as session:
        result = await session.execute(select(func.count()).select_from(Summary))
        return result.scalar_one()

async def create_task(task_id: str):
    """Create a new task record."""
    async with SessionLocal() as session:
        task = Task(id=task_id, status=TaskStatus.PENDING)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

async def update_task_status(task_id: str, status: TaskStatus, result_id: int | None = None, error: str | None = None):
    """Update task status and result."""
    async with SessionLocal() as session:
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if task:
            task.status = status
            task.result_id = result_id
            task.error = error
            task.updated_at = func.now()
            await session.commit()
            await session.refresh(task)
        return task

async def get_task_status(task_id: str):
    """Get task status by ID."""
    async with SessionLocal() as session:
        result = await session.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none() 