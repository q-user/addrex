"""Unit tests for the get_address route function."""

from unittest import mock
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from api.v1.routes.get_address import get_address
from services.phonebook_service import PhoneBookService


@pytest.mark.asyncio
async def test_get_address_valid_request():
    """Test get_address with a valid phone number."""
    # Arrange
    phone_number = "+1234567890"
    mock_redis_client = AsyncMock()
    expected_address_data = {"street": "123 Main St", "city": "Anytown", "state_province": "NY", "postal_code": "12345", "country": "US"}

    # Mock the service to return address data
    mock_service = AsyncMock(spec=PhoneBookService)
    mock_service.get_address = AsyncMock(return_value=expected_address_data)

    # Act
    with mock.patch('api.v1.routes.get_address.PhoneBookService', return_value=mock_service):
        result = await get_address(phone_number, mock_redis_client)

    # Assert
    assert result == {"phone": phone_number, "address": expected_address_data}
    mock_service.get_address.assert_called_once_with(phone_number)


@pytest.mark.asyncio
async def test_get_address_phone_not_found():
    """Test get_address when phone number is not found."""
    # Arrange
    phone_number = "+1234567890"
    mock_redis_client = AsyncMock()

    # Mock the service to return None (not found)
    mock_service = AsyncMock(spec=PhoneBookService)
    mock_service.get_address = AsyncMock(return_value=None)

    # Act & Assert
    with mock.patch('api.v1.routes.get_address.PhoneBookService', return_value=mock_service):
        with pytest.raises(HTTPException) as exc_info:
            await get_address(phone_number, mock_redis_client)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Phone number not found"


@pytest.mark.asyncio
async def test_get_address_invalid_phone_format():
    """Test get_address with an invalid phone number format."""
    # Arrange
    phone_number = "invalid-phone"
    mock_redis_client = AsyncMock()

    # Mock validate_phone_format to return False
    with mock.patch('api.v1.routes.get_address.validate_phone_format', return_value=False):
        with mock.patch('api.v1.routes.get_address.normalize_phone_number', return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                await get_address(phone_number, mock_redis_client)

    # Assert
    assert exc_info.value.status_code == 422
    assert "Invalid phone number format" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_address_with_normalized_phone():
    """Test get_address with a phone number that needs normalization."""
    # Arrange
    original_phone = "89123456789"  # Russian format without +
    normalized_phone = "+79123456789"  # What it should normalize to
    mock_redis_client = AsyncMock()
    expected_address_data = {"street": "123 Main St", "city": "Anytown", "state_province": "NY", "postal_code": "12345", "country": "US"}

    # Mock the phone validation and normalization
    with mock.patch('api.v1.routes.get_address.validate_phone_format', side_effect=[False, True]):  # First call False, then True
        with mock.patch('api.v1.routes.get_address.normalize_phone_number', return_value=normalized_phone):
            # Mock the service to return address data
            mock_service = AsyncMock(spec=PhoneBookService)
            mock_service.get_address = AsyncMock(return_value=expected_address_data)

            with mock.patch('api.v1.routes.get_address.PhoneBookService', return_value=mock_service):
                result = await get_address(original_phone, mock_redis_client)

    # Assert
    assert result == {"phone": normalized_phone, "address": expected_address_data}
    mock_service.get_address.assert_called_once_with(normalized_phone)
