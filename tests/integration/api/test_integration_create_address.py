from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio
async def test_create_address_integration_success():
    """Integration test for creating a new phone-address record - success case."""
    with patch('api.dependencies.redis_client_dependency', new_callable=AsyncMock) as mock_dep:
        mock_redis = AsyncMock()
        mock_dep.return_value = mock_redis
        mock_redis.get = AsyncMock(return_value=None)  # Phone doesn't exist yet
        mock_redis.set = AsyncMock(return_value=True)  # для успеха

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
            response = await client.post("/address/+1234567890", json=test_payload)

        assert response.status_code == 201
        data = response.json()
        assert data["phone"] == "+1234567890"
        assert data["address"]["street"] == "123 Main St"
        assert data["address"]["city"] == "Anytown"


@pytest.mark.asyncio
async def test_create_address_integration_conflict():
    """Integration test for creating a new phone-address record - conflict case."""
    with patch('api.dependencies.redis_client_dependency', new_callable=AsyncMock) as mock_dep:
        mock_redis = AsyncMock()
        mock_dep.return_value = mock_redis
        mock_redis.get = AsyncMock(return_value='{"street": "Old St", "city": "Oldtown", "state_province": "OLD", "postal_code": "OLD00", "country": "US", "formatted_address": "Old St, Oldtown, OLD OLD00, US"}')

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
            response = await client.post("/address/+1234567890", json=test_payload)

        assert response.status_code == 409  # Conflict
        data = response.json()
        assert "detail" in data


@pytest.mark.asyncio
async def test_create_address_integration_invalid_phone():
    """Integration test for creating a record with invalid phone format."""
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
        response = await client.post("/address/invalid_phone", json=test_payload)

    # Should return a validation error
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_address_integration_invalid_address():
    """Integration test for creating a record with invalid address data."""
    with patch('api.dependencies.redis_client_dependency', new_callable=AsyncMock) as mock_dep:
        mock_redis = AsyncMock()
        mock_dep.return_value = mock_redis
        mock_redis.get = AsyncMock(return_value=None)  # Phone doesn't exist yet

        test_payload = {
            "address": {
                "street": "A",  # Invalid - too short
                "city": "Anytown",
                "state_province": "NY",
                "postal_code": "12345",
                "country": "US"
            }
        }

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/address/+1234567890", json=test_payload)

        assert response.status_code == 422  # Validation error
