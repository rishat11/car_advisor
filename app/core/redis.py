import redis.asyncio as redis
from app.core.config import settings


# Create Redis connection pool
redis_pool = redis.ConnectionPool.from_url(settings.REDIS_URL)
redis_client = redis.Redis(connection_pool=redis_pool)


async def get_redis():
    """Dependency to get Redis client"""
    return redis_client


async def cache_get(key: str):
    """Get value from Redis cache"""
    value = await redis_client.get(key)
    return value


async def cache_set(key: str, value: str, expire: int = None):
    """Set value in Redis cache"""
    if expire is None:
        expire = settings.REDIS_TTL
    await redis_client.set(key, value, ex=expire)


async def cache_delete(key: str):
    """Delete key from Redis cache"""
    await redis_client.delete(key)


async def cache_exists(key: str):
    """Check if key exists in Redis cache"""
    return await redis_client.exists(key)