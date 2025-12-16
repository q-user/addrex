from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_delete_address_integration_success():
    """Integration test for deleting a phone-address record - success case."""
    with patch('api.dependencies.get_redis_client') as mock_get_redis:
        mock_redis = AsyncMock()
        mock_get_redis.return_value.__aenter__.return_value = mock_redis
        # Simulate phone number exists
        mock_redis.get.return_value = '{"street": "Old St", "city": "Oldtown", "state_province": "OLD", "postal_code": "OLD00", "country": "US", "formatted_address": "Old St, Oldtown, OLD OLD00, US"}'
        mock_redis.delete.return_value = 1  # Simulate successful deletion

        response = client.delete("/address/+1234567890")

        assert response.status_code == 204  # No content for successful deletion


def test_delete_address_integration_not_found():
    """Integration test for deleting a record - not found case."""
    with patch('api.dependencies.get_redis_client') as mock_get_redis:
        mock_redis = AsyncMock()
        mock_get_redis.return_value.__aenter__.return_value = mock_redis
        mock_redis.get.return_value = None  # Phone doesn't exist

        response = client.delete("/address/+1234567890")

        assert response.status_code == 404  # Not found
        data = response.json()
        assert "detail" in data


def test_delete_address_integration_invalid_phone():
    """Integration test for deleting a record with invalid phone format."""
    response = client.delete("/address/invalid_phone")

    # Should return a validation error
    assert response.status_code == 422
