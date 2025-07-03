from fastapi import APIRouter, HTTPException, BackgroundTasks, status, Query
from app.schemas import (
    SummarizeRequest, SummarizeResponse, SummaryDetail,
    TaskResponse, TaskStatus, SummaryList
)
from app.openai_client import summarize_text
from app.db import (
    create_summary, get_summary_by_id, create_task,
    update_task_status, get_task_status, get_recent_summaries,
    get_total_summaries
)
import uuid

router = APIRouter()
"""API router for summary endpoints."""

async def process_summarization(task_id: str, content: str, source: str):
    """Background task to process summarization request."""
    try:
        # Update task to processing
        await update_task_status(task_id, TaskStatus.PROCESSING)
        
        # Generate summary
        summary = await summarize_text(content)
        
        # Save to database
        result = await create_summary(content, summary, source)
        
        # Update task as completed with result ID
        await update_task_status(task_id, TaskStatus.COMPLETED, result_id=result.id)
    except Exception as e:
        # Update task as failed with error message
        await update_task_status(task_id, TaskStatus.FAILED, error=str(e))
        raise

@router.post("/summarize", response_model=TaskResponse, status_code=status.HTTP_202_ACCEPTED)
async def summarize(request: SummarizeRequest, background_tasks: BackgroundTasks):
    """Start an asynchronous summarization task."""
    # Create task ID and record
    task_id = str(uuid.uuid4())
    await create_task(task_id)
    
    # Add summarization to background tasks
    background_tasks.add_task(
        process_summarization,
        task_id=task_id,
        content=request.content,
        source=request.source
    )
    
    return TaskResponse(task_id=task_id, status=TaskStatus.PENDING)

@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get the status of a summarization task."""
    task = await get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(
        task_id=task.id,
        status=task.status,
        result_id=task.result_id,
        error=task.error
    )

@router.get("/summaries/recent", response_model=SummaryList)
async def get_recent(limit: int = Query(default=5, le=20, gt=0)):
    """Get the most recent summaries.
    
    Args:
        limit: Number of summaries to return (max 20, default 5)
    
    Returns:
        List of summaries ordered by creation date (newest first)
    """
    summaries = await get_recent_summaries(limit)
    total = await get_total_summaries()
    
    # Convert SQLAlchemy models to Pydantic models
    summary_details = [
        SummaryDetail(
            id=summary.id,
            content=summary.content,
            summary=summary.summary,
            source=summary.source,
            created_at=summary.created_at
        )
        for summary in summaries
    ]
    
    return SummaryList(summaries=summary_details, total=total)

@router.get("/summaries/{id}", response_model=SummaryDetail)
async def get_summary(id: int):
    """Retrieve the original and summarized content by summary ID."""
    db_obj = await get_summary_by_id(id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Summary not found")
    return db_obj 