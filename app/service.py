from datetime import datetime
from http.client import HTTPException
from typing import List, Optional

from app import schemas
from . import models
from sqlalchemy.orm import Session

def create_task_service(db, task):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def list_tasks_service(
    db: Session,
    limit: int,
    offset: int,
    status: Optional[models.TaskStatus],
    priority: Optional[models.TaskPriority],
    assigned_to: Optional[str],
    from_due_date: Optional[datetime],
    to_due_date: Optional[datetime],
    search: Optional[str],
    order_by: Optional[str],
    desc: Optional[bool]
):
    query = db.query(models.Task)

    # Filtering
    if status:
        query = query.filter(models.Task.status == status)
    if priority:
        query = query.filter(models.Task.priority == priority)
    if assigned_to:
        query = query.filter(models.Task.assigned_to == assigned_to)
    if from_due_date:
        query = query.filter(models.Task.due_date >= from_due_date)
    if to_due_date:
        query = query.filter(models.Task.due_date <= to_due_date)
    if search:
        query = query.filter(
            models.Task.title.ilike(f"%{search}%") |
            models.Task.description.ilike(f"%{search}%")
        )

    # Sorting
    if order_by:
        column = getattr(models.Task, order_by, None)
        if column is not None:
            if desc:
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column)

    # Pagination
    query = query.offset(offset).limit(limit)

    return query.all()




def get_task_by_id_service(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def update_task_service(db: Session, task_id: int, task_data: schemas.TaskUpdate):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for field, value in task_data.dict(exclude_unset=True).items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task


def delete_task_service(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}

def get_tasks_by_status_service(db: Session, status: models.TaskStatus):
    return db.query(models.Task).filter(models.Task.status == status).all()


def get_tasks_by_priority_service(db: Session, priority: models.TaskPriority):
    return db.query(models.Task).filter(models.Task.priority == priority).all()


def bulk_delete_tasks_service(db: Session, ids: List[int]):
    tasks = db.query(models.Task).filter(models.Task.id.in_(ids)).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for given IDs.")
    for task in tasks:
        db.delete(task)
    db.commit()
    return {"detail": f"Deleted {len(tasks)} tasks."}

def bulk_update_tasks_service(db: Session, ids: List[int], data: dict):
    tasks = db.query(models.Task).filter(models.Task.id.in_(ids)).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for given IDs.")
    
    updated_count = 0
    for task in tasks:
        for field, value in data.items():
            if hasattr(task, field):
                setattr(task, field, value)
        task.updated_at = datetime.utcnow()
        updated_count += 1
    
    db.commit()
    return {"detail": f"Updated {updated_count} tasks."}
