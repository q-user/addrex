from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_update_address_contract_valid_response():
    """Contract test for PUT /address/{phone_number} - valid response structure."""
    with patch('api.dependencies.get_redis_client') as mock_get_redis:
        mock_redis = AsyncMock()
        mock_get_redis.return_value.__aenter__.return_value = mock_redis
        # Simulate phone number exists
        mock_redis.get.return_value = '{"street": "Old St", "city": "Oldtown", "state_province": "OLD", "postal_code": "OLD00", "country": "US", "formatted_address": "Old St, Oldtown, OLD OLD00, US"}'
        mock_redis.set.return_value = True

        test_payload = {
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "state_province": "NY",
                "postal_code": "12345",
                "country": "US"
            }
        }

        response = client.put("/address/+1234567890", json=test_payload)

        # Check the response structure
        assert response.status_code == 200
        data = response.json()
        assert "phone" in data
        assert "address" in data
        assert isinstance(data["phone"], str)
        assert isinstance(data["address"], dict)


def test_update_address_contract_not_found():
    """Contract test for PUT /address/{phone_number} - not found response."""
    with patch('api.dependencies.get_redis_client') as mock_get_redis:
        mock_redis = AsyncMock()
        mock_get_redis.return_value.__aenter__.return_value = mock_redis
        mock_redis.get.return_value = None  # Phone doesn't exist

        test_payload = {
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "state_province": "NY",
                "postal_code": "12345",
                "country": "US"
            }
        }

        response = client.put("/address/+1234567890", json=test_payload)

        assert response.status_code == 404  # Not found
        data = response.json()
        assert "detail" in data


def test_update_address_contract_validation_error():
    """Contract test for PUT /address/{phone_number} - validation error response."""
    with patch('api.dependencies.get_redis_client') as mock_get_redis:
        mock_redis = AsyncMock()
        mock_get_redis.return_value.__aenter__.return_value = mock_redis
        # Simulate phone number exists
        mock_redis.get.return_value = '{"street": "Old St", "city": "Oldtown", "state_province": "OLD", "postal_code": "OLD00", "country": "US", "formatted_address": "Old St, Oldtown, OLD OLD00, US"}'

        test_payload = {
            "address": {
                "street": "A",  # Too short, invalid
                "city": "Anytown",
                "state_province": "NY",
                "postal_code": "12345",
                "country": "US"
            }
        }

        response = client.put("/address/+1234567890", json=test_payload)

        assert response.status_code == 422  # Validation error
        data = response.json()
        assert "detail" in data
