# Database Schema for Conversation State Persistence

## Overview
This document specifies the database schema additions required to persist conversation state for the AI-powered chatbot interface. The schema extends the existing SQLModel-based database structure to include conversation and message entities.

## Entity Definitions

### Conversation Model
Represents a single conversation session between a user and the AI assistant.

```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Fields:**
- `id`: Unique identifier for the conversation (UUID)
- `user_id`: Foreign key linking to the user who owns the conversation
- `title`: Auto-generated or user-provided title for the conversation
- `created_at`: Timestamp when the conversation was created
- `updated_at`: Timestamp when the conversation was last updated

**Indexes:**
- Index on `user_id` for efficient user-based queries
- Composite index on `user_id` and `updated_at` for chronological retrieval

### Message Model
Represents individual messages within a conversation.

```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL,
    role VARCHAR(20) NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);
```

**Fields:**
- `id`: Unique identifier for the message (UUID)
- `conversation_id`: Foreign key linking to the parent conversation
- `role`: Role of the message sender ('user' or 'assistant')
- `content`: The actual message content (text)
- `timestamp`: When the message was created

**Indexes:**
- Index on `conversation_id` for efficient conversation-based queries
- Composite index on `conversation_id` and `timestamp` for chronological ordering

## SQLModel Class Definitions

### Conversation Model Class
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
import uuid

class ConversationBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    user_id: str = Field(nullable=False)

class Conversation(ConversationBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    
    # Indexes would be defined here if needed in SQLModel format

class ConversationCreate(ConversationBase):
    pass

class ConversationRead(ConversationBase):
    id: str
    created_at: datetime
    updated_at: datetime

class ConversationUpdate(SQLModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
```

### Message Model Class
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

class MessageBase(SQLModel):
    conversation_id: str = Field(nullable=False)
    role: str = Field(regex="^(user|assistant)$")  # Either 'user' or 'assistant'
    content: str = Field(nullable=False)

class Message(MessageBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship
    conversation: "Conversation" = Relationship(back_populates="messages")

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: str
    timestamp: datetime
```

## Migration Requirements

### New Tables
- `conversations` table with appropriate foreign key relationship to `users`
- `messages` table with foreign key relationship to `conversations`

### Indexes
- Index on `conversations.user_id` for efficient user-based queries
- Index on `messages.conversation_id` for efficient conversation-based queries
- Composite index on `conversations.user_id` and `updated_at` for chronological retrieval
- Composite index on `messages.conversation_id` and `timestamp` for chronological ordering

### Foreign Key Constraints
- `conversations.user_id` references `users.id` with cascade delete
- `messages.conversation_id` references `conversations.id` with cascade delete

## Access Patterns

### Common Queries
1. **Get all conversations for a user**:
   ```sql
   SELECT * FROM conversations WHERE user_id = ? ORDER BY updated_at DESC;
   ```

2. **Get messages for a specific conversation**:
   ```sql
   SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC;
   ```

3. **Create a new conversation**:
   ```sql
   INSERT INTO conversations (user_id, title) VALUES (?, ?) RETURNING *;
   ```

4. **Add a message to a conversation**:
   ```sql
   INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?) RETURNING *;
   ```

## Security Considerations

### Data Isolation
- Foreign key constraints ensure conversations are linked to specific users
- Application-level checks must verify user ownership before access
- Cascade delete ensures user data is properly cleaned up

### Privacy
- Conversation content is stored encrypted at rest if required by compliance
- Access logs for debugging purposes while maintaining privacy
- Automatic deletion policies for old conversations if required

## Performance Considerations

### Scalability
- UUID primary keys allow for distributed systems
- Proper indexing for efficient queries
- Pagination support for large conversation histories

### Optimization
- Connection pooling for database access
- Potential caching for frequently accessed conversations
- Efficient bulk operations for message history

## Integration with Existing Schema

### Relationship to Existing Models
- `Conversation.user_id` references `User.id` from existing schema
- No modifications needed to existing user/task models
- Follows the same patterns as existing SQLModel definitions

### Consistency with Existing Patterns
- Uses the same UUID generation pattern as existing models
- Follows the same field validation patterns
- Maintains consistency with existing timestamp patterns