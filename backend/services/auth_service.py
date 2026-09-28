"""
Authentication Service for Interview Coach
Handles user authentication and authorization
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
import sqlite3
import json
from ..database import get_db_dict
from ..models.user import User, UserCreate
from ..config import settings

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


class Token(BaseModel):
    """Token model"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model"""
    username: Optional[str] = None
    email: Optional[str] = None


class AuthService:
    """Service for authentication and authorization"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    @staticmethod
    async def create_user(user_data: UserCreate) -> User:
        """Create a new user"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            hashed_password = AuthService.get_password_hash(user_data.password)
            
            cursor.execute("""
                INSERT INTO users (username, email, hashed_password, full_name, is_active, is_admin)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_data.username,
                user_data.email,
                hashed_password,
                user_data.full_name,
                user_data.is_active,
                user_data.is_admin
            ))
            
            conn.commit()
            user_id = cursor.lastrowid
            
            # Fetch the created user
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user_dict = cursor.fetchone()
            conn.close()
            
            if user_dict:
                return User(**user_dict)
            
            raise ValueError("User creation failed")
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    @staticmethod
    async def get_user(username: str) -> Optional[User]:
        """Get user by username"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user_dict = cursor.fetchone()
            conn.close()
            
            if user_dict:
                return User(**user_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting user {username}: {e}")
            raise
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user_dict = cursor.fetchone()
            conn.close()
            
            if user_dict:
                return User(**user_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            raise
    
    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user_dict = cursor.fetchone()
            conn.close()
            
            if user_dict:
                return User(**user_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {e}")
            raise
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    
    @staticmethod
    async def authenticate_user(username: str, password: str) -> Optional[User]:
        """Authenticate a user"""
        try:
            user = await AuthService.get_user(username)
            if not user:
                return None
            
            if not AuthService.verify_password(password, user.hashed_password):
                return None
            
            return user
            
        except Exception as e:
            logger.error(f"Error authenticating user {username}: {e}")
            raise
    
    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
        """Get the current user from the token"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            username: str = payload.get("sub")
            
            if username is None:
                raise credentials_exception
            
            user = await AuthService.get_user(username)
            if user is None:
                raise credentials_exception
            
            return user
            
        except JWTError:
            raise credentials_exception
    
    @staticmethod
    async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
        """Get the current active user"""
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
    
    @staticmethod
    async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
        """Get the current admin user"""
        if not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Admin access required")
        return current_user
    
    @staticmethod
    async def save_api_key(service_name: str, api_key: str, user_id: Optional[int] = None) -> bool:
        """Save an API key for LLM integration"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO api_keys (user_id, service_name, api_key, is_active)
                VALUES (?, ?, ?, TRUE)
            """, (user_id, service_name, api_key))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Error saving API key for {service_name}: {e}")
            raise
    
    @staticmethod
    async def get_api_key(service_name: str, user_id: Optional[int] = None) -> Optional[str]:
        """Get an API key for a service"""
        try:
            conn = await get_db_dict()
            cursor = conn.cursor()
            
            if user_id:
                cursor.execute("SELECT api_key FROM api_keys WHERE user_id = ? AND service_name = ? AND is_active = TRUE", 
                              (user_id, service_name))
            else:
                cursor.execute("SELECT api_key FROM api_keys WHERE service_name = ? AND is_active = TRUE", 
                              (service_name,))
            
            result = cursor.fetchone()
            conn.close()
            
            return result['api_key'] if result else None
            
        except Exception as e:
            logger.error(f"Error getting API key for {service_name}: {e}")
            raise
