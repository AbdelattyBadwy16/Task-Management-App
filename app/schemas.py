from datetime import datetime,timezone
from typing import Optional
from pydantic import BaseModel, validator
from .models import TaskStatus, TaskPriority

# Schema for creating a new task
class TaskCreate(BaseModel):
    title: str
    description: str = None
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.medium
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None
    updated_at: Optional[datetime] = None 
    # Validator to ensure title is not empty or just whitespace
    @validator("title")
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip()

    # Validator to ensure due date is in the future
    @validator("due_date")
    def due_date_in_future(cls, v):
        if v and v <= datetime.now(timezone.utc):
            raise ValueError("Due date must be in the future")
        return v

# Schema for updating an existing task
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None

    # Validator to ensure title is not empty if provided
    @validator("title")
    def title_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip() if v else v

    # Validator to ensure due date is in the future if provided
    @validator("due_date")
    def due_date_in_future(cls, v):
        if v and v <= datetime.now(timezone.utc):
            raise ValueError("Due date must be in the future")
        return v

# Schema for the response 
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: Optional[datetime]
    due_date: Optional[datetime]
    assigned_to: Optional[str]

    # Enables ORM mode 
    class Config:
        orm_mode = True
