"""Unit tests for the update_address route function."""

from unittest import mock
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from api.v1.routes.update_address import update_address
from models.address import Address
from models.api_models import CreateAddressRequest
from services.phonebook_service import PhoneBookService


def _make_request(data: dict) -> CreateAddressRequest:
    return CreateAddressRequest(address=Address(**data))


@pytest.mark.asyncio
async def test_update_address_valid_request():
    """Test update_address with valid data."""
    # Arrange
    phone_number = "+1234567890"
    address_data = {
        "street": "456 Oak Ave",
        "city": "Newtown",
        "state_province": "CA",
        "postal_code": "54321",
        "country": "US"
    }
    mock_redis_client = AsyncMock()

    # Mock the service to return success
    mock_service = AsyncMock(spec=PhoneBookService)
    # Expected address data after validation will include formatted_address
    expected_address_data = {
        "street": "456 Oak Ave",
        "city": "Newtown",
        "state_province": "CA",
        "postal_code": "54321",
        "country": "US",
        "formatted_address": "456 Oak Ave, Newtown, CA 54321, US"
    }
    mock_service.update_address = AsyncMock(return_value=True)

    # Act
    with mock.patch('api.v1.routes.update_address.PhoneBookService', return_value=mock_service):
        request_data = _make_request(address_data)
        result = await update_address(phone_number, request_data, mock_redis_client)

    # Assert
    assert result == {"phone": phone_number, "address": expected_address_data}
    mock_service.update_address.assert_called_once_with(phone_number, expected_address_data)


@pytest.mark.asyncio
async def test_update_address_not_found():
    """Test update_address when phone number does not exist."""
    # Arrange
    phone_number = "+1234567890"
    address_data = {
        "street": "456 Oak Ave",
        "city": "Newtown",
        "state_province": "CA",
        "postal_code": "54321",
        "country": "US"
    }
    mock_redis_client = AsyncMock()

    # Mock the service to return False (not found)
    mock_service = AsyncMock(spec=PhoneBookService)
    mock_service.update_address = AsyncMock(return_value=False)

    # Act & Assert
    with mock.patch('api.v1.routes.update_address.PhoneBookService', return_value=mock_service):
        with pytest.raises(HTTPException) as exc_info:
            request_data = _make_request(address_data)
            await update_address(phone_number, request_data, mock_redis_client)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Phone number not found"


@pytest.mark.asyncio
async def test_update_address_invalid_phone_format():
    """Test update_address with an invalid phone number format."""
    # Arrange
    phone_number = "invalid-phone"
    address_data = {
        "street": "456 Oak Ave",
        "city": "Newtown",
        "state_province": "CA",
        "postal_code": "54321",
        "country": "US"
    }
    mock_redis_client = AsyncMock()

    # Mock validate_phone_format to return False and normalization to fail
    with mock.patch('api.v1.routes.update_address.validate_phone_format', return_value=False):
        with mock.patch('api.v1.routes.update_address.normalize_phone_number', return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                request_data = _make_request(address_data)
                await update_address(phone_number, request_data, mock_redis_client)

    # Assert
    assert exc_info.value.status_code == 422
    assert "Invalid phone number format" in exc_info.value.detail


@pytest.mark.asyncio
async def test_update_address_with_normalized_phone():
    """Test update_address with a phone number that needs normalization."""
    # Arrange
    original_phone = "89123456789"  # Russian format without +
    normalized_phone = "+79123456789"  # What it should normalize to
    address_data = {
        "street": "456 Oak Ave",
        "city": "Newtown",
        "state_province": "CA",
        "postal_code": "54321",
        "country": "US"
    }
    mock_redis_client = AsyncMock()

    # Mock the phone validation and normalization
    with mock.patch('api.v1.routes.update_address.validate_phone_format', side_effect=[False, True]):  # First call False, then True
        with mock.patch('api.v1.routes.update_address.normalize_phone_number', return_value=normalized_phone):
            # Mock the service to return success
            mock_service = AsyncMock(spec=PhoneBookService)
            # Expected address data after validation will include formatted_address
            expected_address_data = {
                "street": "456 Oak Ave",
                "city": "Newtown",
                "state_province": "CA",
                "postal_code": "54321",
                "country": "US",
                "formatted_address": "456 Oak Ave, Newtown, CA 54321, US"
            }
            mock_service.update_address = AsyncMock(return_value=True)

            with mock.patch('api.v1.routes.update_address.PhoneBookService', return_value=mock_service):
                request_data = _make_request(address_data)
                result = await update_address(original_phone, request_data, mock_redis_client)

    # Assert
    assert result == {"phone": normalized_phone, "address": expected_address_data}
    mock_service.update_address.assert_called_once_with(normalized_phone, expected_address_data)


@pytest.mark.asyncio
async def test_update_address_invalid_address_data():
    """Test update_address with invalid address data."""
    # Arrange
    phone_number = "+1234567890"
    # This data is valid for the Address model, but we will mock the request model to fail
    address_data = {
        "street": "456 Oak Ave",
        "city": "Newtown",
        "state_province": "CA",
        "postal_code": "54321",
        "country": "US"
    }
    mock_redis_client = AsyncMock()
    request_data = _make_request(address_data)

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        with mock.patch('models.address.Address.model_dump', side_effect=Exception('Validation failed')):
            await update_address(phone_number, request_data, mock_redis_client)

    assert exc_info.value.status_code == 422
    assert "Invalid address data" in str(exc_info.value.detail)
