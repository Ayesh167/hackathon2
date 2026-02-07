from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Dict
from datetime import timedelta, timezone
from ..database import get_session
from ..models.task_models import User
from ..auth import create_access_token, get_password_hash, verify_password, get_current_user
from pydantic import BaseModel
import uuid
from datetime import datetime
import traceback

router = APIRouter(prefix="/auth", tags=["auth"])

# Pydantic models for request/response
class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

@router.post("/register", response_model=TokenResponse)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Hash the password
        hashed_password = get_password_hash(user_data.password)

        # Create new user with hashed password
        db_user = User(
            id=str(uuid.uuid4()),
            email=user_data.email,
            password=hashed_password,  # Store the hashed password
            name=user_data.name,
            created_at=datetime.now(timezone.utc)
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        # Create access token
        access_token_expires = timedelta(days=7)  # 7 days expiry
        access_token = create_access_token(
            data={"sub": db_user.id}, expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": db_user.id,
                "email": db_user.email,
                "name": db_user.name
            }
        }
    except Exception as e:
        print(f"Registration error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=TokenResponse)
def login(user_credentials: UserLogin, session: Session = Depends(get_session)):
    """Authenticate user and return access token"""
    try:
        # Find user by email
        user = session.exec(select(User).where(User.email == user_credentials.email)).first()

        if not user or not verify_password(user_credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token_expires = timedelta(days=7)  # 7 days expiry
        access_token = create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }
    except Exception as e:
        print(f"Login error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


from pydantic import BaseModel

class UserUpdate(BaseModel):
    name: str
    email: str

@router.get("/me", response_model=dict)
def get_current_user_details(
    current_user: User = Depends(get_current_user)
):
    """Get current user details from the token"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "created_at": current_user.created_at
    }


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


@router.post("/change-password")
def change_password(
    password_change: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Change user's password"""
    # Verify current password
    if not verify_password(password_change.current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Validate new password length
    if len(password_change.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 6 characters long"
        )
    
    # Update password
    current_user.password = get_password_hash(password_change.new_password)
    session.add(current_user)
    session.commit()
    
    return {"message": "Password changed successfully"}


@router.get("/active-sessions")
def get_active_sessions(
    current_user: User = Depends(get_current_user)
):
    """Get user's active sessions (mock implementation)"""
    # In a real implementation, this would fetch from a sessions table
    # For now, returning mock data
    return {
        "sessions": [
            {
                "id": "session_1",
                "device": "Chrome on Windows",
                "ip_address": "192.168.1.100",
                "location": "Local",
                "last_activity": "Just now",
                "is_current": True
            },
            {
                "id": "session_2",
                "device": "Firefox on Mac",
                "ip_address": "203.0.113.45",
                "location": "United States",
                "last_activity": "2 hours ago",
                "is_current": False
            }
        ]
    }


@router.delete("/active-sessions/{session_id}")
def revoke_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Revoke a specific session (mock implementation)"""
    # In a real implementation, this would invalidate the session in the database
    return {"message": f"Session {session_id} revoked successfully"}


@router.get("/two-factor")
def get_two_factor_status(
    current_user: User = Depends(get_current_user)
):
    """Get user's 2FA status"""
    # In a real implementation, this would fetch from user settings
    return {
        "enabled": False,
        "method": None,
        "backup_codes_generated": False
    }


@router.post("/two-factor/setup")
def setup_two_factor(
    current_user: User = Depends(get_current_user)
):
    """Initiate 2FA setup"""
    # In a real implementation, this would generate a QR code and secret
    return {
        "qr_code_url": "mock://qr-code-url",  # This would be a real QR code URL
        "secret": "ABCDEF123456",  # This would be a real secret
        "uri": "otpauth://totp/TodoApp:user@example.com?secret=ABCDEF123456"
    }


class VerifyTwoFactorRequest(BaseModel):
    token: str

@router.post("/two-factor/verify")
def verify_two_factor_setup(
    request: VerifyTwoFactorRequest,
    current_user: User = Depends(get_current_user)
):
    """Verify 2FA setup with token"""
    # In a real implementation, this would verify the token against the secret
    # For now, we'll just accept any token for demonstration
    return {
        "success": True,
        "message": "2FA setup verified successfully"
    }


@router.post("/two-factor/disable")
def disable_two_factor(
    current_user: User = Depends(get_current_user)
):
    """Disable 2FA for user"""
    return {
        "message": "2FA disabled successfully"
    }


@router.put("/me", response_model=dict)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update current user details"""
    # Check if another user with this email already exists (excluding current user)
    existing_user = session.exec(
        select(User).where(User.email == user_update.email).where(User.id != current_user.id)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Update user details
    current_user.name = user_update.name
    current_user.email = user_update.email
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "created_at": current_user.created_at
    }


