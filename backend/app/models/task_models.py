from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone
import uuid


class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, nullable=False)
    password: str  # Hashed password
    name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user")
    conversations: List["Conversation"] = Relationship(back_populates="user")


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(max_length=1000, default=None)
    completed: bool = False


class Task(TaskBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship
    user: User = Relationship(back_populates="tasks")


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class TaskCreate(TaskBase):
    pass


class UserRead(SQLModel):
    id: str
    email: str
    name: str
    created_at: datetime


class TaskRead(SQLModel):
    id: str
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime


class TaskReadWithUser(TaskRead):
    user: UserRead


# Conversation and Message models for AI chatbot
class ConversationBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    user_id: str = Field(foreign_key="user.id", nullable=False)


class Conversation(ConversationBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    user: User = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: str
    created_at: datetime
    updated_at: datetime


class ConversationUpdate(SQLModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)


class MessageBase(SQLModel):
    conversation_id: str = Field(foreign_key="conversation.id", nullable=False)
    role: str  # Either 'user' or 'assistant'
    content: str = Field(nullable=False)


class Message(MessageBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship
    conversation: Conversation = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: str
    timestamp: datetime