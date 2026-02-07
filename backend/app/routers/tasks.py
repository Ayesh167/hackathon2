from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, delete
from typing import List
from ..database import get_session
from ..models.task_models import (
    Task, TaskCreate, TaskRead, TaskUpdate, User,
    TaskReadWithUser
)
from ..auth import get_current_user
from datetime import datetime, timezone

router = APIRouter(prefix="/api/{user_id}", tags=["tasks"])


@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    user_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all tasks for the authenticated user.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()

    return tasks


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: str,
    task: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new task for the authenticated user.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed if hasattr(task, 'completed') else False,
        user_id=user_id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    user_id: str,
    task_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific task by ID for the authenticated user.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    user_id: str,
    task_id: str,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update a specific task by ID for the authenticated user.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    db_task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update only provided fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    # Update the timestamp
    db_task.updated_at = datetime.now(timezone.utc)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: str,
    task_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a specific task by ID for the authenticated user.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()


@router.patch("/tasks/{task_id}/complete", response_model=TaskRead)
def toggle_task_completion(
    user_id: str,
    task_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Toggle the completion status of a specific task for the authenticated user.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this task"
        )

    db_task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle the completion status
    db_task.completed = not db_task.completed
    db_task.updated_at = datetime.now(timezone.utc)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task