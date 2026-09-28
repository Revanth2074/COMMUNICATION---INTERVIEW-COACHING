"""
Authentication Router for Interview Coach
Handles user authentication and authorization endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Optional
from ..models.user import User, UserCreate, UserUpdate
from ..services.auth_service import AuthService
from ..config import settings

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate) -> dict:
    """Register a new user"""
    try:
        # Check if username or email already exists
        existing_user = await AuthService.get_user(user.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        existing_email = await AuthService.get_user_by_email(user.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        # Create the user
        created_user = await AuthService.create_user(user)
        
        return {
            "success": True,
            "message": "User registered successfully",
            "data": {
                "id": created_user.id,
                "username": created_user.username,
                "email": created_user.email,
                "full_name": created_user.full_name
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/token", response_model=dict)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    """Get access token for authenticated user"""
    try:
        user = await AuthService.authenticate_user(
            form_data.username, 
            form_data.password
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = AuthService.create_access_token(
            data={"sub": user.username, "email": user.email},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "is_admin": user.is_admin
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=dict)
async def get_current_user(
    current_user: User = Depends(AuthService.get_current_active_user)
) -> dict:
    """Get current user information"""
    try:
        return {
            "success": True,
            "message": "Current user retrieved successfully",
            "data": {
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email,
                "full_name": current_user.full_name,
                "is_active": current_user.is_active,
                "is_admin": current_user.is_admin,
                "created_at": current_user.created_at
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put("/me", response_model=dict)
async def update_current_user(
    user: UserUpdate,
    current_user: User = Depends(AuthService.get_current_active_user)
) -> dict:
    """Update current user information"""
    try:
        # In a real implementation, we would update the user in the database
        # For now, we'll just return the updated data
        
        return {
            "success": True,
            "message": "User updated successfully",
            "data": {
                "id": current_user.id,
                "username": user.username or current_user.username,
                "email": user.email or current_user.email,
                "full_name": user.full_name or current_user.full_name,
                "is_active": user.is_active if user.is_active is not None else current_user.is_active,
                "is_admin": user.is_admin if user.is_admin is not None else current_user.is_admin
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/api-keys", response_model=dict)
async def save_api_key(
    service_name: str = Query(..., description="Service name (e.g., omniroute)"),
    api_key: str = Query(..., description="API key"),
    current_user: User = Depends(AuthService.get_current_active_user)
) -> dict:
    """Save an API key for LLM integration"""
    try:
        saved = await AuthService.save_api_key(
            service_name=service_name,
            api_key=api_key,
            user_id=current_user.id
        )
        
        if not saved:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to save API key"
            )
        
        return {
            "success": True,
            "message": "API key saved successfully",
            "data": {
                "service": service_name,
                "user_id": current_user.id
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/api-keys/{service_name}", response_model=dict)
async def get_api_key(
    service_name: str,
    current_user: User = Depends(AuthService.get_current_active_user)
) -> dict:
    """Get an API key for a service"""
    try:
        api_key = await AuthService.get_api_key(service_name, current_user.id)
        
        if not api_key:
            return {
                "success": True,
                "message": "No API key found for this service",
                "data": None
            }
        
        # For security, we don't return the actual API key in the response
        # Just confirm that it exists
        return {
            "success": True,
            "message": "API key exists for this service",
            "data": {
                "service": service_name,
                "exists": True
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
