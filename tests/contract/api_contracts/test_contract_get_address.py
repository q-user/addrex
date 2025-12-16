from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from api.dependencies import redis_client_provider
from main import app


@pytest.mark.asyncio
async def test_get_address_contract_valid_response():
    """Contract test for GET /address/{phone_number} - valid response structure."""
    # This test checks that the endpoint returns the correct response structure
    # We're using mocking since we don't have the full implementation yet
    mock_redis = AsyncMock()
    mock_redis.get = AsyncMock(return_value='{"street": "123 Main St", "city": "Anytown", "state_province": "NY", "postal_code": "12345", "country": "US", "formatted_address": "123 Main St, Anytown, NY 12345, US"}')

    async def override():
        return mock_redis

    app.dependency_overrides[redis_client_provider] = override
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/address/+1234567890")

        assert response.status_code == 200
        data = response.json()
        assert "phone" in data
        assert "address" in data
        assert isinstance(data["phone"], str)
        assert isinstance(data["address"], dict)
        assert "street" in data["address"]
        assert "city" in data["address"]
        assert "state_province" in data["address"]
        assert "postal_code" in data["address"]
        assert "country" in data["address"]
        assert "formatted_address" in data["address"]
    finally:
        app.dependency_overrides.pop(redis_client_provider, None)


@pytest.mark.asyncio
async def test_get_address_contract_not_found():
    """Contract test for GET /address/{phone_number} - not found response."""
    mock_redis = AsyncMock()
    mock_redis.get = AsyncMock(return_value=None)  # Phone number not in database

    async def override():
        return mock_redis

    app.dependency_overrides[redis_client_provider] = override
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/address/+1234567890")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    finally:
        app.dependency_overrides.pop(redis_client_provider, None)
