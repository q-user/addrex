from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_delete_address_contract_valid_response():
    """Contract test for DELETE /address/{phone_number} - valid response structure."""
    with patch('api.dependencies.get_redis_client') as mock_get_redis:
        mock_redis = AsyncMock()
        mock_get_redis.return_value.__aenter__.return_value = mock_redis
        # Simulate phone number exists
        mock_redis.get.return_value = '{"street": "Old St", "city": "Oldtown", "state_province": "OLD", "postal_code": "OLD00", "country": "US", "formatted_address": "Old St, Oldtown, OLD OLD00, US"}'
        mock_redis.delete.return_value = 1  # Simulate successful deletion

        response = client.delete("/address/+1234567890")

        # Check the response structure - DELETE should return 204 with no body
        assert response.status_code == 204


def test_delete_address_contract_not_found():
    """Contract test for DELETE /address/{phone_number} - not found response."""
    with patch('api.dependencies.get_redis_client') as mock_get_redis:
        mock_redis = AsyncMock()
        mock_get_redis.return_value.__aenter__.return_value = mock_redis
        mock_redis.get.return_value = None  # Phone doesn't exist

        response = client.delete("/address/+1234567890")

        assert response.status_code == 404  # Not found
        data = response.json()
        assert "detail" in data
