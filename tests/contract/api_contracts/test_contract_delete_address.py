from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from api.dependencies import redis_client_provider
from main import app


@pytest.mark.asyncio
async def test_delete_address_contract_valid_response():
    """Contract test for DELETE /address/{phone_number} - valid response structure."""
    mock_redis = AsyncMock()
    mock_redis.get = AsyncMock(return_value='{"street": "Old St", "city": "Oldtown", "state_province": "OLD", "postal_code": "OLD00", "country": "US", "formatted_address": "Old St, Oldtown, OLD OLD00, US"}')
    mock_redis.delete = AsyncMock(return_value=1)

    async def override():
        return mock_redis

    app.dependency_overrides[redis_client_provider] = override
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.delete("/address/+1234567890")

        assert response.status_code == 200
    finally:
        app.dependency_overrides.pop(redis_client_provider, None)


@pytest.mark.asyncio
async def test_delete_address_contract_not_found():
    """Contract test for DELETE /address/{phone_number} - not found response."""
    mock_redis = AsyncMock()
    mock_redis.get = AsyncMock(return_value=None)

    async def override():
        return mock_redis

    app.dependency_overrides[redis_client_provider] = override
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.delete("/address/+1234567890")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    finally:
        app.dependency_overrides.pop(redis_client_provider, None)
