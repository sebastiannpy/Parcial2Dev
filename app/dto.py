from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"
    cancelled = "cancelled"

class TaskCreateDTO(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    due_date: Optional[date] = None

class UpdateStatusDTO(BaseModel):
    status: TaskStatus
