from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Dict, Any, Optional
from pydantic import BaseModel
from uuid import UUID
import json
from datetime import datetime
from ..database import get_session
from ..models.task_models import (
    Conversation, ConversationCreate, Message, MessageCreate, User
)
from ..auth import get_current_user
from ..services.openai_agent_service import process_natural_language_request

router = APIRouter(prefix="/api", tags=["chat"])

# Request and response models for chat
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None  # Optional for new conversations


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    action_result: Dict[str, Any] = None


@router.post("/chat", response_model=ChatResponse)
def chat(
    chat_request: ChatRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Main chat endpoint that handles natural language requests for task management.
    This endpoint integrates with OpenAI agents and MCP tools.
    """
    try:
        # Validate that the user can access the conversation if provided
        conversation = None
        if chat_request.conversation_id:
            # Check if the conversation belongs to the current user
            conversation = session.exec(
                select(Conversation)
                .where(Conversation.id == chat_request.conversation_id)
                .where(Conversation.user_id == current_user.id)
            ).first()

            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found or access denied"
                )

        # If no conversation ID provided, create a new one
        if not conversation:
            new_conversation = Conversation(
                title=chat_request.message[:50] + "..." if len(chat_request.message) > 50 else chat_request.message,
                user_id=current_user.id
            )
            session.add(new_conversation)
            session.commit()
            session.refresh(new_conversation)
            conversation = new_conversation

        # Create user message entry
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=chat_request.message
        )
        session.add(user_message)
        session.commit()

        # Get conversation history for context
        conversation_history = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.timestamp.asc())
        ).all()

        # Convert to the format expected by the agent service
        formatted_history = [{"role": msg.role, "content": msg.content} for msg in conversation_history[:-1]]  # Exclude the current message

        # Process the natural language request using OpenAI agent
        result = process_natural_language_request(
            session=session,
            user_id=current_user.id,
            user_message=chat_request.message,
            conversation_history=formatted_history
        )

        ai_response = result.get("response", "I processed your request.")
        action_results = result.get("action_results", [])

        # Create AI message entry
        ai_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=ai_response
        )
        session.add(ai_message)
        session.commit()

        # The updated_at field should be automatically updated by SQLModel
        # No need to manually set it here
        session.add(conversation)
        session.commit()

        return ChatResponse(
            response=ai_response,
            conversation_id=conversation.id,
            action_result=action_results[0] if action_results else {}
        )
    except Exception as e:
        # Log the error for debugging
        import traceback
        print(f"Error in chat endpoint: {e}")
        print(traceback.format_exc())
        
        # Return a meaningful error response
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred processing your request: {str(e)}"
        )


@router.get("/conversations", response_model=list)
def get_user_conversations(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all conversations for the authenticated user.
    """
    conversations = session.exec(
        select(Conversation)
        .where(Conversation.user_id == current_user.id)
        .order_by(Conversation.updated_at.desc())
    ).all()
    
    return conversations


@router.get("/conversations/{conversation_id}", response_model=dict)
def get_conversation_messages(
    conversation_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all messages for a specific conversation.
    """
    # Verify the conversation belongs to the current user
    conversation = session.exec(
        select(Conversation)
        .where(Conversation.id == conversation_id)
        .where(Conversation.user_id == current_user.id)
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )
    
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.timestamp.asc())
    ).all()
    
    return {
        "conversation": conversation,
        "messages": messages
    }