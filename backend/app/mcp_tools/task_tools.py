"""
MCP Tools for Task Management Operations

These tools provide stateless interfaces to task management operations
that can be used by AI agents. All tools validate user ownership
before performing operations.
"""

from typing import List, Optional, Dict, Any
from sqlmodel import Session, select
from ..models.task_models import Task, User, Conversation, Message
from datetime import datetime
import warnings


def create_task_tool(
    session: Session,
    user_id: str,
    title: str,
    description: Optional[str] = None,
    completed: bool = False
) -> Dict[str, Any]:
    """
    MCP Tool to create a new task for a user.
    
    Args:
        session: Database session
        user_id: ID of the user creating the task
        title: Title of the task
        description: Optional description of the task
        completed: Whether the task is initially completed
    
    Returns:
        Dictionary with task creation result
    """
    # Verify user exists
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        return {
            "success": False,
            "error": "User not found"
        }
    
    # Create the task
    db_task = Task(
        title=title,
        description=description,
        completed=completed,
        user_id=user_id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    return {
        "success": True,
        "task": {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "completed": db_task.completed,
            "created_at": db_task.created_at.isoformat() if hasattr(db_task.created_at, 'isoformat') else str(db_task.created_at)
        }
    }


def get_tasks_tool(
    session: Session,
    user_id: str,
    status_filter: Optional[str] = None  # "all", "pending", "completed"
) -> Dict[str, Any]:
    """
    MCP Tool to retrieve tasks for a user with optional filtering.
    
    Args:
        session: Database session
        user_id: ID of the user whose tasks to retrieve
        status_filter: Optional filter for task status
    
    Returns:
        Dictionary with list of tasks
    """
    # Verify user exists
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        return {
            "success": False,
            "error": "User not found"
        }
    
    # Build query based on filters
    query = select(Task).where(Task.user_id == user_id)
    
    if status_filter == "pending":
        query = query.where(Task.completed == False)
    elif status_filter == "completed":
        query = query.where(Task.completed == True)
    
    tasks = session.exec(query).all()
    
    return {
        "success": True,
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if hasattr(task.created_at, 'isoformat') else str(task.created_at),
                "updated_at": task.updated_at.isoformat() if hasattr(task.updated_at, 'isoformat') else str(task.updated_at)
            }
            for task in tasks
        ]
    }


def get_task_tool(
    session: Session,
    user_id: str,
    task_id: str
) -> Dict[str, Any]:
    """
    MCP Tool to retrieve a specific task for a user.
    
    Args:
        session: Database session
        user_id: ID of the user
        task_id: ID of the task to retrieve
    
    Returns:
        Dictionary with task details
    """
    # Verify user exists
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        return {
            "success": False,
            "error": "User not found"
        }
    
    # Get the specific task
    task = session.exec(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == user_id)
    ).first()
    
    if not task:
        return {
            "success": False,
            "error": "Task not found or access denied"
        }
    
    return {
        "success": True,
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat() if hasattr(task.created_at, 'isoformat') else str(task.created_at),
            "updated_at": task.updated_at.isoformat() if hasattr(task.updated_at, 'isoformat') else str(task.updated_at)
        }
    }


def update_task_tool(
    session: Session,
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None
) -> Dict[str, Any]:
    """
    MCP Tool to update a specific task for a user.
    
    Args:
        session: Database session
        user_id: ID of the user
        task_id: ID of the task to update
        title: New title (optional)
        description: New description (optional)
        completed: New completion status (optional)
    
    Returns:
        Dictionary with update result
    """
    # Verify user exists
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        return {
            "success": False,
            "error": "User not found"
        }
    
    # Get the task to update
    db_task = session.exec(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == user_id)
    ).first()
    
    if not db_task:
        return {
            "success": False,
            "error": "Task not found or access denied"
        }
    
    # Update provided fields
    if title is not None:
        db_task.title = title
    if description is not None:
        db_task.description = description
    if completed is not None:
        db_task.completed = completed
    
    # Update timestamp
    from datetime import datetime
    db_task.updated_at = datetime.utcnow()
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return {
        "success": True,
        "task": {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "completed": db_task.completed,
            "created_at": db_task.created_at.isoformat() if hasattr(db_task.created_at, 'isoformat') else str(db_task.created_at),
            "updated_at": db_task.updated_at.isoformat() if hasattr(db_task.updated_at, 'isoformat') else str(db_task.updated_at)
        }
    }


def delete_task_tool(
    session: Session,
    user_id: str,
    task_id: str
) -> Dict[str, Any]:
    """
    MCP Tool to delete a specific task for a user.
    
    Args:
        session: Database session
        user_id: ID of the user
        task_id: ID of the task to delete
    
    Returns:
        Dictionary with deletion result
    """
    # Verify user exists
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        return {
            "success": False,
            "error": "User not found"
        }
    
    # Get the task to delete
    task = session.exec(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == user_id)
    ).first()
    
    if not task:
        return {
            "success": False,
            "error": "Task not found or access denied"
        }
    
    session.delete(task)
    session.commit()
    
    return {
        "success": True,
        "message": "Task deleted successfully"
    }


def toggle_task_completion_tool(
    session: Session,
    user_id: str,
    task_id: str
) -> Dict[str, Any]:
    """
    MCP Tool to toggle the completion status of a specific task for a user.
    
    Args:
        session: Database session
        user_id: ID of the user
        task_id: ID of the task to toggle
    
    Returns:
        Dictionary with toggle result
    """
    # Verify user exists
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        return {
            "success": False,
            "error": "User not found"
        }
    
    # Get the task to toggle
    db_task = session.exec(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == user_id)
    ).first()
    
    if not db_task:
        return {
            "success": False,
            "error": "Task not found or access denied"
        }
    
    # Toggle completion status
    db_task.completed = not db_task.completed
    db_task.updated_at = datetime.utcnow()
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    return {
        "success": True,
        "task": {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "completed": db_task.completed,
            "created_at": db_task.created_at.isoformat() if hasattr(db_task.created_at, 'isoformat') else str(db_task.created_at),
            "updated_at": db_task.updated_at.isoformat() if hasattr(db_task.updated_at, 'isoformat') else str(db_task.updated_at)
        }
    }


def get_user_info_tool(
    session: Session,
    user_id: str
) -> Dict[str, Any]:
    """
    MCP Tool to retrieve user information.
    
    Args:
        session: Database session
        user_id: ID of the user to retrieve
    
    Returns:
        Dictionary with user information
    """
    user = session.exec(select(User).where(User.id == user_id)).first()
    
    if not user:
        return {
            "success": False,
            "error": "User not found"
        }
    
    return {
        "success": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at.isoformat() if hasattr(user.created_at, 'isoformat') else str(user.created_at)
        }
    }