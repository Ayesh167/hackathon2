# MCP Tools API Specification for Task Management

## Overview
This document specifies the API for MCP (Model Context Protocol) tools that enable AI agents to perform task management operations. These tools are stateless and store state in the database.

## Tool Definitions

### 1. create_task_tool
**Purpose**: Creates a new task for a user
**Function Signature**:
```python
def create_task_tool(
    session: Session,
    user_id: str,
    title: str,
    description: Optional[str] = None,
    completed: bool = False
) -> Dict[str, Any]
```

**Parameters**:
- `session`: Database session for the operation
- `user_id`: ID of the user creating the task
- `title`: Title of the task (required, 1-200 chars)
- `description`: Optional description (max 1000 chars)
- `completed`: Boolean indicating if task is initially completed (default: False)

**Returns**:
```json
{
  "success": true,
  "task": {
    "id": "uuid-string",
    "title": "task title",
    "description": "task description or null",
    "completed": false,
    "created_at": "iso-timestamp"
  }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "error message"
}
```

### 2. get_tasks_tool
**Purpose**: Retrieves all tasks for a user with optional filtering
**Function Signature**:
```python
def get_tasks_tool(
    session: Session,
    user_id: str,
    status_filter: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters**:
- `session`: Database session for the operation
- `user_id`: ID of the user whose tasks to retrieve
- `status_filter`: Optional filter ("all", "pending", "completed")

**Returns**:
```json
{
  "success": true,
  "tasks": [
    {
      "id": "uuid-string",
      "title": "task title",
      "description": "task description or null",
      "completed": false,
      "created_at": "iso-timestamp",
      "updated_at": "iso-timestamp"
    }
  ]
}
```

### 3. get_task_tool
**Purpose**: Retrieves a specific task for a user
**Function Signature**:
```python
def get_task_tool(
    session: Session,
    user_id: str,
    task_id: str
) -> Dict[str, Any]
```

**Parameters**:
- `session`: Database session for the operation
- `user_id`: ID of the user
- `task_id`: ID of the specific task to retrieve

**Returns**:
```json
{
  "success": true,
  "task": {
    "id": "uuid-string",
    "title": "task title",
    "description": "task description or null",
    "completed": false,
    "created_at": "iso-timestamp",
    "updated_at": "iso-timestamp"
  }
}
```

### 4. update_task_tool
**Purpose**: Updates a specific task for a user
**Function Signature**:
```python
def update_task_tool(
    session: Session,
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None
) -> Dict[str, Any]
```

**Parameters**:
- `session`: Database session for the operation
- `user_id`: ID of the user
- `task_id`: ID of the task to update
- `title`: New title (optional)
- `description`: New description (optional)
- `completed`: New completion status (optional)

**Returns**:
```json
{
  "success": true,
  "task": {
    "id": "uuid-string",
    "title": "updated title",
    "description": "updated description or null",
    "completed": true,
    "created_at": "iso-timestamp",
    "updated_at": "iso-timestamp"
  }
}
```

### 5. delete_task_tool
**Purpose**: Deletes a specific task for a user
**Function Signature**:
```python
def delete_task_tool(
    session: Session,
    user_id: str,
    task_id: str
) -> Dict[str, Any]
```

**Parameters**:
- `session`: Database session for the operation
- `user_id`: ID of the user
- `task_id`: ID of the task to delete

**Returns**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

### 6. toggle_task_completion_tool
**Purpose**: Toggles the completion status of a specific task
**Function Signature**:
```python
def toggle_task_completion_tool(
    session: Session,
    user_id: str,
    task_id: str
) -> Dict[str, Any]
```

**Parameters**:
- `session`: Database session for the operation
- `user_id`: ID of the user
- `task_id`: ID of the task to toggle

**Returns**:
```json
{
  "success": true,
  "task": {
    "id": "uuid-string",
    "title": "task title",
    "description": "task description or null",
    "completed": true,
    "created_at": "iso-timestamp",
    "updated_at": "iso-timestamp"
  }
}
```

### 7. get_user_info_tool
**Purpose**: Retrieves user information
**Function Signature**:
```python
def get_user_info_tool(
    session: Session,
    user_id: str
) -> Dict[str, Any]
```

**Parameters**:
- `session`: Database session for the operation
- `user_id`: ID of the user to retrieve

**Returns**:
```json
{
  "success": true,
  "user": {
    "id": "uuid-string",
    "name": "user name",
    "email": "user@example.com",
    "created_at": "iso-timestamp"
  }
}
```

## Security Requirements

### User Validation
- Each tool must validate that the user exists before performing operations
- Each tool must verify that the user owns the resources they're trying to access
- Tools must return appropriate error messages for unauthorized access attempts

### Data Isolation
- Users can only access their own tasks and conversations
- Tools must enforce foreign key relationships at the database level
- Tools must validate user ownership at the application level

## Error Handling

### Common Error Cases
- Invalid user ID: Return "User not found" error
- Invalid resource ID: Return "Resource not found or access denied" error
- Invalid parameters: Return appropriate validation error
- Database errors: Return generic error message to avoid exposing system details

### Error Response Format
All tools return a standardized error response:
```json
{
  "success": false,
  "error": "descriptive error message"
}
```

## Integration with AI Agents

### Tool Registration
- Tools must be registered with the OpenAI Agent framework
- Each tool should have a clear, descriptive name and purpose
- Tools should include proper parameter validation and documentation

### State Management
- Tools are stateless and rely on database for persistence
- Tools must update database state immediately upon successful operations
- Tools must handle concurrent access appropriately through database transactions

## Performance Considerations

### Efficiency
- Tools should minimize database queries where possible
- Tools should use appropriate indexing strategies
- Tools should implement proper pagination for large datasets

### Transaction Safety
- Each tool operation should be atomic
- Tools should handle database transaction failures gracefully
- Tools should implement proper rollback mechanisms when needed