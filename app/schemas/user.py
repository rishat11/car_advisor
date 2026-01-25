from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3 or len(v) > 50:
            raise ValueError('Username must be between 3 and 50 characters')
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserInDB(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserPublic(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Car Schemas
class CarBase(BaseModel):
    make: str
    model: str
    year: int
    body_type: str
    fuel_type: str
    transmission: str
    engine_size: Optional[float] = None
    horsepower: Optional[int] = None
    price: Optional[float] = None
    description: Optional[str] = None
    features: Optional[str] = None


class CarCreate(CarBase):
    pass


class CarUpdate(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    body_type: Optional[str] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    engine_size: Optional[float] = None
    horsepower: Optional[int] = None
    price: Optional[float] = None
    description: Optional[str] = None
    features: Optional[str] = None


class CarInDB(CarBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CarPublic(CarBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Chat Session Schemas
class ChatSessionBase(BaseModel):
    title: Optional[str] = None
    is_active: bool = True


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionUpdate(BaseModel):
    title: Optional[str] = None
    is_active: Optional[bool] = None


class ChatSessionInDB(ChatSessionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatSessionPublic(ChatSessionBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Message Schemas
class MessageBase(BaseModel):
    chat_session_id: int
    content: str
    role: str  # 'user' or 'assistant'


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    content: Optional[str] = None


class MessageInDB(MessageBase):
    id: int
    user_id: Optional[int] = None
    timestamp: datetime

    class Config:
        from_attributes = True


class MessagePublic(MessageBase):
    id: int
    user_id: Optional[int] = None
    timestamp: datetime

    class Config:
        from_attributes = True


# Recommendation Schemas
class RecommendationBase(BaseModel):
    chat_session_id: int
    car_id: int
    reason: Optional[str] = None


class RecommendationCreate(RecommendationBase):
    pass


class RecommendationInDB(RecommendationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class RecommendationPublic(RecommendationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# Response Schemas
class SuccessResponse(BaseModel):
    success: bool
    message: str


class ErrorResponse(BaseModel):
    success: bool
    message: str
    detail: Optional[str] = None


# Chat Request/Response Schemas
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[int] = None


class ChatResponse(BaseModel):
    response: str
    session_id: int
    car_recommendations: Optional[List[CarPublic]] = None