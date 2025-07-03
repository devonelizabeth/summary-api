from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import List

class SummarizeRequest(BaseModel):
    content: str
    source: str

class SummarizeResponse(BaseModel):
    summary: str
    id: int
    created_at: datetime

class SummaryDetail(BaseModel):
    id: int
    content: str
    summary: str
    source: str
    created_at: datetime

class SummaryList(BaseModel):
    summaries: List[SummaryDetail]
    total: int

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    result_id: int | None = None
    error: str | None = None 