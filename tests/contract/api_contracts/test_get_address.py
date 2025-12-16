import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from src.main import app


client = TestClient(app)


def test_get_address_contract_valid_response():
    """Contract test for GET /address/{phone_number} - valid response structure."""
    # This test checks that the endpoint returns the correct response structure
    # We're using mocking since we don't have the full implementation yet
    with patch('src.api.dependencies.get_redis_client') as mock_get_redis:
        mock_redis = AsyncMock()
        mock_get_redis.return_value.__aenter__.return_value = mock_redis
        mock_redis.get.return_value = '{"street": "123 Main St", "city": "Anytown", "state_province": "NY", "postal_code": "12345", "country": "US", "formatted_address": "123 Main St, Anytown, NY 12345, US"}'
        
        response = client.get("/address/+1234567890")
        
        # Check the response structure and types
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


def test_get_address_contract_not_found():
    """Contract test for GET /address/{phone_number} - not found response."""
    with patch('src.api.dependencies.get_redis_client') as mock_get_redis:
        mock_redis = AsyncMock()
        mock_get_redis.return_value.__aenter__.return_value = mock_redis
        mock_redis.get.return_value = None  # Simulate non-existent phone number
        
        response = client.get("/address/+1234567890")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data  # FastAPI's default error response structure