from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio
async def test_update_address_integration_success():
    """Integration test for updating an existing phone-address record - success case."""
    with patch('api.dependencies.redis_client_dependency', new_callable=AsyncMock) as mock_dep:
        mock_redis = AsyncMock()
        mock_dep.return_value = mock_redis
        mock_redis.get = AsyncMock(return_value='{"street": "Old St", "city": "Oldtown", "state_province": "OLD", "postal_code": "OLD00", "country": "US", "formatted_address": "Old St, Oldtown, OLD OLD00, US"}')
        mock_redis.set = AsyncMock(return_value=True)

        test_payload = {
            "address": {
                "street": "123 New St",
                "city": "Newtown",
                "state_province": "NW",
                "postal_code": "NEW00",
                "country": "US"
            }
        }

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.put("/address/+1234567890", json=test_payload)

        assert response.status_code == 200
        data = response.json()
        assert data["phone"] == "+1234567890"
        assert data["address"]["street"] == "123 New St"
        assert data["address"]["city"] == "Newtown"


@pytest.mark.asyncio
async def test_update_address_integration_not_found():
    """Integration test for updating a record - not found case."""
    with patch('api.dependencies.redis_client_dependency', new_callable=AsyncMock) as mock_dep:
        mock_redis = AsyncMock()
        mock_dep.return_value = mock_redis
        mock_redis.get = AsyncMock(return_value=None)  # Phone doesn't exist

        test_payload = {
            "address": {
                "street": "123 New St",
                "city": "Newtown",
                "state_province": "NW",
                "postal_code": "NEW00",
                "country": "US"
            }
        }

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.put("/address/+1234567890", json=test_payload)

        assert response.status_code == 404  # Not found
        data = response.json()
        assert "detail" in data


@pytest.mark.asyncio
async def test_update_address_integration_invalid_phone():
    """Integration test for updating a record with invalid phone format."""
    test_payload = {
        "address": {
            "street": "123 New St",
            "city": "Newtown",
            "state_province": "NW",
            "postal_code": "NEW00",
            "country": "US"
        }
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.put("/address/invalid_phone", json=test_payload)

    # Should return a validation error
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_address_integration_invalid_address():
    """Integration test for updating a record with invalid address data."""
    with patch('api.dependencies.redis_client_dependency', new_callable=AsyncMock) as mock_dep:
        mock_redis = AsyncMock()
        mock_dep.return_value = mock_redis
        mock_redis.get = AsyncMock(return_value='{"street": "Old St", "city": "Oldtown", "state_province": "OLD", "postal_code": "OLD00", "country": "US", "formatted_address": "Old St, Oldtown, OLD OLD00, US"}')

        test_payload = {
            "address": {
                "street": "A",  # Invalid - too short
                "city": "Newtown",
                "state_province": "NW",
                "postal_code": "NEW00",
                "country": "US"
            }
        }

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.put("/address/+1234567890", json=test_payload)

        assert response.status_code == 422  # Validation error
