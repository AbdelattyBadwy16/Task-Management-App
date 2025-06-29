from datetime import datetime
from http.client import HTTPException
from typing import Optional

from app import schemas
from . import models
from sqlalchemy.orm import Session

def create_task_service(db, task):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def list_tasks_service(db, limit, offset, status=None, priority=None):
    query = db.query(models.Task)

    if status:
        query = query.filter(models.Task.status == status)

    if priority:
        query = query.filter(models.Task.priority == priority)

    return query.offset(offset).limit(limit).all()


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