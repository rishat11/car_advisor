import os
import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Базовый класс для SQLAlchemy моделей
Base = DeclarativeBase()

# Глобальные переменные для движка и сессии
engine = None
async_session = None

def initialize_db():
    """
    Инициализирует подключение к базе данных.
    Вызывается при первом обращении к БД.
    """
    global engine, async_session

    if engine is not None and async_session is not None:
        return  # Уже инициализировано

    # Определение URL базы данных в зависимости от среды
    database_url = os.getenv("DATABASE_URL")

    # Для Vercel Functions может потребоваться специфический формат URL
    if database_url:
        # Преобразование URL для asyncpg если необходимо
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif database_url.startswith("postgresql://") and not database_url.startswith("postgresql+asyncpg://"):
            database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    else:
        # Fallback для локальной разработки
        if os.getenv("VERCEL"):
            # На Vercel используем SQLite как fallback, т.к. подключение к PostgreSQL может быть проблематичным
            database_url = "sqlite+aiosqlite:///./vercel_fallback.db"
            logger.warning("DATABASE_URL not set, using SQLite fallback for Vercel")
        else:
            # Локальная разработка
            database_url = "postgresql+asyncpg://caradvisor:caradvisor@localhost:5432/caradvisor"
            logger.info("Using default local PostgreSQL URL")

    try:
        # Создание асинхронного движка
        # Для serverless среды уменьшаем размер пула и отключаем пул соединений
        engine = create_async_engine(
            database_url,
            # Параметры для serverless среды
            pool_pre_ping=True,  # Проверяет соединение перед использованием
            pool_recycle=300,    # Пересоздает соединения каждые 5 минут
            pool_size=1,         # Минимальный размер пула для serverless
            max_overflow=0,      # Отключаем overflow для serverless
            echo=bool(os.getenv("DB_ECHO", False)),  # Логирование SQL запросов
            # Для SQLite нужно отключить poolclass
            **({'poolclass': NullPool} if database_url.startswith('sqlite') else {})
        )

        # Создаем асинхронную сессию
        async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        logger.info(f"Database engine created successfully with URL: {database_url.replace('@', '[AT]').replace('://', '[COLON_DOUBLE_SLASH]')}")
    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")
        # В случае ошибки создаем сессию с SQLite для fallback
        engine = create_async_engine("sqlite+aiosqlite:///./fallback.db")
        async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        logger.info("Fallback database engine created with SQLite")

# Импортируем NullPool для использования в serverless среде
from sqlalchemy.pool import NullPool

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор сессии базы данных для DI в FastAPI.
    Инициализирует БД при первом обращении.
    """
    # Инициализируем БД при необходимости
    initialize_db()

    async with async_session() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Database error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
        finally:
            await session.close()

async def check_db_connection():
    """
    Проверяет подключение к базе данных.
    """
    try:
        initialize_db()  # Убедимся, что БД инициализирована
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False