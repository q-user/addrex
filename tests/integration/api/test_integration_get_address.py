from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio
async def test_get_address_integration_found():
    """Integration test for address lookup - when phone number exists."""
    with patch('api.dependencies.redis_client_dependency', new_callable=AsyncMock) as mock_dep:
        mock_redis = AsyncMock()
        mock_dep.return_value = mock_redis
        # Mock the Redis response with a sample address
        mock_redis.get = AsyncMock(return_value='{"street": "123 Main St", "city": "Anytown", "state_province": "NY", "postal_code": "12345", "country": "US", "formatted_address": "123 Main St, Anytown, NY 12345, US"}')

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/address/+1234567890")

        assert response.status_code == 200
        data = response.json()
        assert data["phone"] == "+1234567890"
        assert data["address"]["street"] == "123 Main St"
        assert data["address"]["city"] == "Anytown"
        assert data["address"]["state_province"] == "NY"
        assert data["address"]["postal_code"] == "12345"
        assert data["address"]["country"] == "US"


@pytest.mark.asyncio
async def test_get_address_integration_not_found():
    """Integration test for address lookup - when phone number does not exist."""
    with patch('api.dependencies.redis_client_dependency', new_callable=AsyncMock) as mock_dep:
        mock_redis = AsyncMock()
        mock_dep.return_value = mock_redis
        mock_redis.get = AsyncMock(return_value=None)  # Phone number not in database

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/address/+1234567890")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data


@pytest.mark.asyncio
async def test_get_address_integration_invalid_phone_format():
    """Integration test for address lookup - when phone number has invalid format."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/address/invalid_phone")  # Invalid format shouldn't reach Redis

    # This would depend on how you implement input validation in the endpoint
    # For now, assume it returns a validation error
    assert response.status_code == 422
    # This test might need to be adjusted based on actual endpoint implementation
