from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from api.dependencies import redis_client_provider
from main import app


def _mock_redis(existing_json: str | None):
    mock_redis = AsyncMock()
    mock_redis.get = AsyncMock(return_value=existing_json)
    mock_redis.set = AsyncMock(return_value=True)
    mock_redis.exists = AsyncMock(return_value=bool(existing_json))
    return mock_redis


@pytest.mark.asyncio
async def test_update_address_contract_valid_response():
    """Contract test for PUT /address/{phone_number} - valid response structure."""
    existing = '{"street": "Old St", "city": "Oldtown", "state_province": "OLD", "postal_code": "OLD00", "country": "US", "formatted_address": "Old St, Oldtown, OLD OLD00, US"}'
    mock_redis = _mock_redis(existing_json=existing)

    async def override():
        return mock_redis

    app.dependency_overrides[redis_client_provider] = override
    try:
        test_payload = {
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "state_province": "NY",
                "postal_code": "12345",
                "country": "US"
            }
        }

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.put("/address/+1234567890", json=test_payload)

        assert response.status_code == 200
        data = response.json()
        assert "phone" in data
        assert "address" in data
        assert isinstance(data["address"], dict)
    finally:
        app.dependency_overrides.pop(redis_client_provider, None)


@pytest.mark.asyncio
async def test_update_address_contract_not_found():
    """Contract test for PUT /address/{phone_number} - not found response."""
    mock_redis = _mock_redis(existing_json=None)

    async def override():
        return mock_redis

    app.dependency_overrides[redis_client_provider] = override
    try:
        test_payload = {
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "state_province": "NY",
                "postal_code": "12345",
                "country": "US"
            }
        }

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.put("/address/+1234567890", json=test_payload)

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    finally:
        app.dependency_overrides.pop(redis_client_provider, None)


@pytest.mark.asyncio
async def test_update_address_contract_validation_error():
    """Contract test for PUT /address/{phone_number} - validation error response."""
    existing = '{"street": "Old St", "city": "Oldtown", "state_province": "OLD", "postal_code": "OLD00", "country": "US", "formatted_address": "Old St, Oldtown, OLD OLD00, US"}'
    mock_redis = _mock_redis(existing_json=existing)

    async def override():
        return mock_redis

    app.dependency_overrides[redis_client_provider] = override
    try:
        test_payload = {
            "address": {
                "street": "A",  # Too short, invalid
                "city": "Anytown",
                "state_province": "NY",
                "postal_code": "12345",
                "country": "US"
            }
        }

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.put("/address/+1234567890", json=test_payload)

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    finally:
        app.dependency_overrides.pop(redis_client_provider, None)
