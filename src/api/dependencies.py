import logging

from fastapi import HTTPException
from redis.asyncio import Redis

from config.settings import settings

# Set up logging
logger = logging.getLogger(__name__)

# Redis connection pool
redis_pool = None


async def get_redis_pool():
    global redis_pool
    if redis_pool is None:
        redis_pool = Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            decode_responses=True,
        )
    return redis_pool


async def get_redis_client() -> Redis:
    """Return a shared Redis client instance."""
    return await get_redis_pool()


async def redis_client_dependency() -> Redis:
    """Wrapper to allow dynamic monkeypatching of get_redis_client in tests."""
    return await get_redis_client()


async def redis_client_provider() -> Redis:
    """Indirect provider so tests patching `redis_client_dependency` take effect."""
    return await redis_client_dependency()


# Error handling infrastructure
def handle_error(error_code: int, message: str):
    return HTTPException(
        status_code=error_code,
        detail=message,
    )


# Request/Response validation and logging middleware components
def log_request_response(
    endpoint_name: str,
    request_data: dict | None = None,
    response_data: dict | None = None,
):
    """Log request and response data for monitoring and debugging."""
    if request_data:
        logger.info(f'Request to {endpoint_name}: {request_data}')
    if response_data:
        logger.info(f'Response from {endpoint_name}: {response_data}')


# Rate limiting could be implemented here if needed
async def check_rate_limit(client_id: str) -> bool:
    """Check if client has exceeded rate limits.
    This is a placeholder - implement actual rate limiting as needed.
    """
    # For now, always return True (no rate limiting)
    return True
