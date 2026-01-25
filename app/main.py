from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Импорты
from app.api.routers import auth, users, cars, chat
from app.core.config import settings

# Создаем приложение FastAPI БЕЗ lifespan для serverless
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Car Advisor API - A chat-based car recommendation service",
    docs_url="/docs",
    redoc_url="/redoc"
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

# Подключаем роутеры (ПОСЛЕ CORS!)
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
        "version": settings.VERSION
    }

# Health check эндпоинт для диагностики
@app.get("/health")
async def health():
    # В serverless среде не проверяем подключение к БД при каждом запросе
    # Проверка будет выполняться только при необходимости в роутах
    return {
        "status": "ok",
        "service": "car-advisor-api",
        "database": "serverless-mode"
    }

# Запуск приложения (только для локальной разработки)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # ВАЖНО: 0.0.0.0, не localhost!
        port=8000,
        reload=True,
        log_level="debug",  # Включаем подробные логи
        access_log=True     # Логируем все запросы
    )