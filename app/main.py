from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import json

# Ваш код импортов
from app.api.routers import auth, users, cars, chat
from app.core.config import settings
from app.db.session import engine
from app.models import Base
import asyncio

# Создание таблиц
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Запуск Car Advisor API...")
    await create_tables()
    yield
    # Shutdown
    print("👋 Остановка Car Advisor API...")

# Создаем приложение
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Car Advisor API - A chat-based car recommendation service",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# ✅✅✅ ВАЖНО: CORS Middleware ДОЛЖЕН БЫТЬ ПЕРВЫМ!
# Добавляем ПРОСТОЙ И РАБОЧИЙ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем ВСЕ источники для теста
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

# ✅ Дополнительно: ручной CORS middleware для надежности
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    # Обрабатываем OPTIONS (preflight) запросы
    if request.method == "OPTIONS":
        response = Response(
            content=json.dumps({"message": "CORS preflight OK"}),
            status_code=200,
            media_type="application/json"
        )
    else:
        response = await call_next(request)
    
    # Добавляем CORS заголовки ко ВСЕМ ответам
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Max-Age"] = "600"
    
    return response

# Подключаем роутеры (ПОСЛЕ CORS!)
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(cars.router, prefix="/api/v1", tags=["cars"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

# Health check эндпоинты
@app.get("/")
async def root():
    return {"message": "Car Advisor API", "status": "running", "version": settings.VERSION}

@app.get("/health")
async def health():
    return {"status": "ok", "service": "car-advisor-api"}

# CORS тестовый эндпоинт
@app.options("/{path:path}")
async def options_handler(path: str):
    """Обработчик OPTIONS запросов для CORS"""
    return {"message": "CORS preflight request handled"}

@app.get("/cors-test")
async def cors_test(request: Request):
    """Тестовый эндпоинт для проверки CORS"""
    return {
        "cors_working": True,
        "request_origin": request.headers.get("origin"),
        "allowed_origins": ["*"],
        "timestamp": "2024-01-01T00:00:00Z"
    }

# Запуск приложения
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # ВАЖНО: 0.0.0.0, не localhost!
        port=8000,
        reload=True,
        log_level="debug",  # Включаем подробные логи
        access_log=True     # Логируем все запросы
    )