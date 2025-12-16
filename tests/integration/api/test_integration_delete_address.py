from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio
async def test_delete_address_integration_success():
    """Integration test for deleting a phone-address record - success case."""
    with patch('api.dependencies.redis_client_dependency', new_callable=AsyncMock) as mock_dep:
        mock_redis = AsyncMock()
        mock_dep.return_value = mock_redis
        mock_redis.get = AsyncMock(return_value='{"street": "Old St", "city": "Oldtown", "state_province": "OLD", "postal_code": "OLD00", "country": "US", "formatted_address": "Old St, Oldtown, OLD OLD00, US"}')
        mock_redis.delete = AsyncMock(return_value=1)

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.delete("/address/+1234567890")

        assert response.status_code == 200  # endpoint returns 200


@pytest.mark.asyncio
async def test_delete_address_integration_not_found():
    """Integration test for deleting a record - not found case."""
    with patch('api.dependencies.redis_client_dependency', new_callable=AsyncMock) as mock_dep:
        mock_redis = AsyncMock()
        mock_dep.return_value = mock_redis
        mock_redis.get = AsyncMock(return_value=None)

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.delete("/address/+1234567890")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data


@pytest.mark.asyncio
async def test_delete_address_integration_invalid_phone():
    """Integration test for deleting a record with invalid phone format."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete("/address/invalid_phone")

    # Should return a validation error
    assert response.status_code == 422
