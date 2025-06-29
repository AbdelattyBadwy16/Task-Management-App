from datetime import datetime
from typing import List, Optional
from app import models
from fastapi import APIRouter, HTTPException, Depends, Query, Body
from sqlalchemy.orm import Session
from . import schemas, service
from .database import get_session

# Create router for all /tasks endpoints
router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)
# Create a new task and return the created task data
@router.post("/", response_model=schemas.TaskResponse, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_session)):
    return service.create_task_service(db, task)


# Retrieve list of tasks with filtering, sorting, search, and pagination
@router.get("/", response_model=List[schemas.TaskResponse])
def list_tasks(
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    status: Optional[models.TaskStatus] = Query(None),
    priority: Optional[models.TaskPriority] = Query(None),
    assigned_to: Optional[str] = Query(None),
    from_due_date: Optional[datetime] = Query(None),
    to_due_date: Optional[datetime] = Query(None),
    search: Optional[str] = Query(None),
    order_by: Optional[str] = Query(None),
    desc: Optional[bool] = Query(False),
    db: Session = Depends(get_session)
):
    return service.list_tasks_service(
        db, limit, offset, status, priority, assigned_to,
        from_due_date, to_due_date, search, order_by, desc
    )


# Delete multiple tasks at once by IDs
@router.delete("/bulk", status_code=200)
def bulk_delete_tasks(
    ids: List[int] = Body(..., embed=True),
    db: Session = Depends(get_session)
):
    return service.bulk_delete_tasks_service(db, ids)


# Update multiple tasks with specified fields by IDs
@router.put("/bulk", status_code=200)
def bulk_update_tasks(
    ids: List[int] = Body(..., embed=True),
    data: dict = Body(...),
    db: Session = Depends(get_session)
):
    return service.bulk_update_tasks_service(db, ids, data)


# Retrieve a task by its ID
@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task_by_id(task_id: int, db: Session = Depends(get_session)):
    return service.get_task_by_id_service(db, task_id)


# Update task fields by ID and return updated task
@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_data: schemas.TaskUpdate, db: Session = Depends(get_session)):
    return service.update_task_service(db, task_id, task_data)


# Delete a task by its ID, no content returned
@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_session)):
    service.delete_task_service(db, task_id)


# Retrieve all tasks with the specified status
@router.get("/status/{status}", response_model=List[schemas.TaskResponse])
def get_tasks_by_status(
    status: models.TaskStatus,
    db: Session = Depends(get_session)
):
    return service.get_tasks_by_status_service(db, status)


# Retrieve all tasks with the specified priority
@router.get("/priority/{priority}", response_model=List[schemas.TaskResponse])
def get_tasks_by_priority(
    priority: models.TaskPriority,
    db: Session = Depends(get_session)
):
    return service.get_tasks_by_priority_service(db, priority)
