from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import json
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Импорты
from app.api.routers import auth, users, cars, chat
from app.core.config import settings
from app.database import check_db_connection
from app.models import Base
import asyncio

# Lifecycle manager для FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управляет жизненным циклом приложения.
    Выполняет инициализацию при запуске и очистку при завершении.
    """
    # Startup
    logger.info("🚀 Запуск Car Advisor API...")

    # Проверяем подключение к базе данных
    db_connected = await check_db_connection()
    if db_connected:
        logger.info("✅ Подключение к базе данных успешно")
        app.state.db_connected = True
    else:
        logger.error("❌ Не удалось подключиться к базе данных")
        app.state.db_connected = False

    yield  # Здесь работает приложение

    # Shutdown
    logger.info("👋 Остановка Car Advisor API...")

# Создаем приложение FastAPI с lifecycle manager
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Car Advisor API - A chat-based car recommendation service",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# ✅✅✅ ВАЖНО: CORS Middleware ДОЛЖЕН БЫТЬ ПЕРВЫМ!
# Добавляем CORS для Vercel и локальной разработки
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
# Изменяем префикс для auth на /api/v1, а не /api/v1/auth
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(cars.router, prefix="/api/v1", tags=["cars"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

# Главная страница
@app.get("/")
async def root():
    return {
        "message": "Car Advisor API",
        "status": "running",
        "version": settings.VERSION,
        "db_connected": getattr(app.state, 'db_connected', False)
    }

# Health check эндпоинт для диагностики
@app.get("/health")
async def health():
    db_status = getattr(app.state, 'db_connected', False)
    return {
        "status": "ok",
        "service": "car-advisor-api",
        "database": "connected" if db_status else "disconnected"
    }

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