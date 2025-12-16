"""Unit tests for the create_address route function."""

from unittest import mock
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from api.v1.routes.create_address import create_address
from services.phonebook_service import PhoneBookService


@pytest.mark.asyncio
async def test_create_address_valid_request():
    """Test create_address with valid data."""
    # Arrange
    phone_number = "+1234567890"
    address_data = {
        "street": "123 Main St",
        "city": "Anytown",
        "state_province": "NY",
        "postal_code": "12345",
        "country": "US"
    }
    mock_redis_client = AsyncMock()

    # Mock the service to return success
    mock_service = AsyncMock(spec=PhoneBookService)
    # Expected address data after validation will include formatted_address
    expected_address_data = {
        "street": "123 Main St",
        "city": "Anytown",
        "state_province": "NY",
        "postal_code": "12345",
        "country": "US",
        "formatted_address": "123 Main St, Anytown, NY 12345, US"
    }
    mock_service.create_address = AsyncMock(return_value=True)

    # Act
    with mock.patch('api.v1.routes.create_address.PhoneBookService', return_value=mock_service):
        result = await create_address(phone_number, address_data, mock_redis_client)

    # Assert
    assert result == {"phone": phone_number, "address": expected_address_data}
    mock_service.create_address.assert_called_once_with(phone_number, expected_address_data)


@pytest.mark.asyncio
async def test_create_address_conflict():
    """Test create_address when phone number already exists."""
    # Arrange
    phone_number = "+1234567890"
    address_data = {
        "street": "123 Main St",
        "city": "Anytown",
        "state_province": "NY",
        "postal_code": "12345",
        "country": "US"
    }
    mock_redis_client = AsyncMock()

    # Mock the service to return False (conflict)
    mock_service = AsyncMock(spec=PhoneBookService)
    mock_service.create_address = AsyncMock(return_value=False)

    # Act & Assert
    with mock.patch('api.v1.routes.create_address.PhoneBookService', return_value=mock_service):
        with pytest.raises(HTTPException) as exc_info:
            await create_address(phone_number, address_data, mock_redis_client)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Phone number already exists"


@pytest.mark.asyncio
async def test_create_address_invalid_phone_format():
    """Test create_address with an invalid phone number format."""
    # Arrange
    phone_number = "invalid-phone"
    address_data = {
        "street": "123 Main St",
        "city": "Anytown",
        "state_province": "NY",
        "postal_code": "12345",
        "country": "US"
    }
    mock_redis_client = AsyncMock()

    # Mock validate_phone_format to return False and normalization to fail
    with mock.patch('api.v1.routes.create_address.validate_phone_format', return_value=False):
        with mock.patch('api.v1.routes.create_address.normalize_phone_number', return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                await create_address(phone_number, address_data, mock_redis_client)

    # Assert
    assert exc_info.value.status_code == 422
    assert "Invalid phone number format" in exc_info.value.detail


@pytest.mark.asyncio
async def test_create_address_with_normalized_phone():
    """Test create_address with a phone number that needs normalization."""
    # Arrange
    original_phone = "89123456789"  # Russian format without +
    normalized_phone = "+79123456789"  # What it should normalize to
    address_data = {
        "street": "123 Main St",
        "city": "Anytown",
        "state_province": "NY",
        "postal_code": "12345",
        "country": "US"
    }
    mock_redis_client = AsyncMock()

    # Mock the phone validation and normalization
    with mock.patch('api.v1.routes.create_address.validate_phone_format', side_effect=[False, True]):  # First call False, then True
        with mock.patch('api.v1.routes.create_address.normalize_phone_number', return_value=normalized_phone):
            # Mock the service to return success
            mock_service = AsyncMock(spec=PhoneBookService)
            # Expected address data after validation will include formatted_address
            expected_address_data = {
                "street": "123 Main St",
                "city": "Anytown",
                "state_province": "NY",
                "postal_code": "12345",
                "country": "US",
                "formatted_address": "123 Main St, Anytown, NY 12345, US"
            }
            mock_service.create_address = AsyncMock(return_value=True)

            with mock.patch('api.v1.routes.create_address.PhoneBookService', return_value=mock_service):
                result = await create_address(original_phone, address_data, mock_redis_client)

    # Assert
    assert result == {"phone": normalized_phone, "address": expected_address_data}
    mock_service.create_address.assert_called_once_with(normalized_phone, expected_address_data)


@pytest.mark.asyncio
async def test_create_address_invalid_address_data():
    """Test create_address with invalid address data."""
    # Arrange
    phone_number = "+1234567890"
    invalid_address_data = {
        "street": "A",  # Too short
        "city": "Anytown",
        "state_province": "NY",
        "postal_code": "12345",
        "country": "US"
    }
    mock_redis_client = AsyncMock()

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await create_address(phone_number, invalid_address_data, mock_redis_client)

    assert exc_info.value.status_code == 422
    assert "Invalid address data" in exc_info.value.detail
