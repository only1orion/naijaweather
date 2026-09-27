import json
import redis.asyncio as redis

from app import config

# Single shared client — connection pooling handled internally
redis_client = redis.from_url(config.REDIS_URL, decode_responses=True)


async def get_cached(key: str) -> dict | None:
    """Return cached value if it exists, else None."""
    try:
        raw = await redis_client.get(key)
    except redis.RedisError:
        return None  # cache unavailable — fail open, don't break the API

    if raw is None:
        return None

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


async def set_cached(key: str, value: dict, ttl: int = config.CACHE_TTL_SECONDS) -> None:
    """Store a value in cache with a TTL (seconds)."""
    try:
        await redis_client.set(key, json.dumps(value), ex=ttl)
    except redis.RedisError:
        pass  # cache failure shouldn't crash requests


async def ping() -> bool:
    """Health check for Redis."""
    try:
        return await redis_client.ping()
    except redis.RedisError:
        return False