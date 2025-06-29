from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


# Enum for task status
class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled" 

# Enum for task priority
class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"

# Task table model
class Task(SQLModel, table=True):
    id: int = Field(
        default=None,
        primary_key=True,
        description="Unique task identifier"
    )

    title: str = Field(
        max_length=200,
        description="Task title"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description"
    )
    
    status: TaskStatus = Field(
        default=TaskStatus.pending,
        description="Task status"
    )

    priority: TaskPriority = Field(
        default=TaskPriority.medium,
        description="Task priority"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp"
    )
    
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )
    
    due_date: Optional[datetime] = Field(
        default=None,
        description="Task deadline"
    )
    
    assigned_to: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Assignee name"
    )