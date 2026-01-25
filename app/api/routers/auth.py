from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import datetime, timedelta

router = APIRouter()

# ========== МОДЕЛИ ==========
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None  # поддержка поля name от фронтенда
    full_name: Optional[str] = None  # поддержка поля full_name
    phone: Optional[str] = None

    def __init__(self, **data):
        # Если передано name, но не передано full_name, используем name как full_name
        if 'name' in data and 'full_name' not in data:
            data['full_name'] = data['name']
        super().__init__(**data)

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    phone: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False

class LoginRequest(BaseModel):
    # ✅ ПРИНИМАЕМ И username И email
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str
    
    class Config:
        extra = "ignore"  # игнорируем лишние поля

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600
    user: dict

# ========== IN-MEMORY БД для теста ==========
users_db = []

# ========== ЭНДПОИНТЫ ==========
@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    """Регистрация пользователя"""
    print(f"✅ REGISTER: {user.email}")
    
    # Проверка существующего email
    for existing in users_db:
        if existing["email"] == user.email:
            raise HTTPException(400, "Email already exists")
    
    # Создание пользователя
    new_user = {
        "id": str(uuid.uuid4()),
        "email": user.email,
        "password": user.password,  # В продакшене хэшировать!
        "full_name": user.full_name,
        "phone": user.phone,
        "is_active": True,
        "is_verified": False
    }
    
    users_db.append(new_user)
    print(f"✅ User created: {user.email}, total users: {len(users_db)}")
    
    return UserResponse(**new_user)

@router.post("/login", response_model=TokenResponse)
async def login_user(login_data: LoginRequest):
    """Аутентификация пользователя"""
    print(f"✅ LOGIN attempt: email={login_data.email}, username={login_data.username}")
    
    # Определяем что использовать для поиска
    search_value = login_data.email or login_data.username
    
    if not search_value:
        raise HTTPException(400, "Email or username is required")
    
    # Ищем пользователя
    user = None
    for u in users_db:
        if u["email"] == search_value or u["id"] == search_value:
            user = u
            break
    
    if not user:
        print(f"❌ User not found: {search_value}")
        raise HTTPException(401, "Invalid credentials")
    
    # Простая проверка пароля
    if user["password"] != login_data.password:
        print(f"❌ Invalid password for: {search_value}")
        raise HTTPException(401, "Invalid credentials")
    
    print(f"✅ Successful login: {user['email']}")
    
    # Генерируем токен
    token = f"jwt_{user['id']}_{datetime.now().timestamp()}"
    
    return TokenResponse(
        access_token=token,
        user={
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "is_active": user["is_active"]
        }
    )

@router.get("/test")
async def test():
    """Тестовый эндпоинт"""
    return {
        "status": "ok",
        "router": "auth",
        "users_count": len(users_db)
    }

@router.get("/debug")
async def debug():
    """Отладочная информация"""
    return {
        "users": users_db,
        "timestamp": datetime.now().isoformat()
    }