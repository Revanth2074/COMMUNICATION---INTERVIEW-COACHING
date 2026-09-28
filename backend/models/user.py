"""
User Model for Interview Coach Authentication
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user model"""
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    full_name: Optional[str] = Field(default=None, description="Full name")
    is_active: bool = Field(default=True, description="Whether user is active")
    is_admin: bool = Field(default=False, description="Whether user is admin")


class UserCreate(UserBase):
    """User create model"""
    password: str = Field(..., description="Password")


class UserUpdate(BaseModel):
    """User update model"""
    username: Optional[str] = Field(default=None, description="Username")
    email: Optional[str] = Field(default=None, description="Email address")
    full_name: Optional[str] = Field(default=None, description="Full name")
    is_active: Optional[bool] = Field(default=None, description="User active status")
    is_admin: Optional[bool] = Field(default=None, description="User admin status")


class User(UserBase):
    """Full user model"""
    id: int = Field(..., description="User ID")
    hashed_password: str = Field(..., description="Hashed password")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "hashed_password": "hashed_value",
                "is_active": True,
                "is_admin": False,
                "created_at": "2024-01-01T00:00:00"
            }
        }
