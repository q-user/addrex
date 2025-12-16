"""Unit tests for the delete_address route function."""

from unittest import mock
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from api.v1.routes.delete_address import delete_address
from services.phonebook_service import PhoneBookService


@pytest.mark.asyncio
async def test_delete_address_valid_request():
    """Test delete_address with a valid phone number."""
    # Arrange
    phone_number = "+1234567890"
    mock_redis_client = AsyncMock()

    # Mock the service to return success
    mock_service = AsyncMock(spec=PhoneBookService)
    mock_service.delete_address = AsyncMock(return_value=True)

    # Act
    with mock.patch('api.v1.routes.delete_address.PhoneBookService', return_value=mock_service):
        # For delete, the function returns None (204 No Content)
        result = await delete_address(phone_number, mock_redis_client)

    # Assert
    assert result is None  # DELETE operations return 204, which is None in FastAPI
    mock_service.delete_address.assert_called_once_with(phone_number)


@pytest.mark.asyncio
async def test_delete_address_not_found():
    """Test delete_address when phone number does not exist."""
    # Arrange
    phone_number = "+1234567890"
    mock_redis_client = AsyncMock()

    # Mock the service to return False (not found)
    mock_service = AsyncMock(spec=PhoneBookService)
    mock_service.delete_address = AsyncMock(return_value=False)

    # Act & Assert
    with mock.patch('api.v1.routes.delete_address.PhoneBookService', return_value=mock_service):
        with pytest.raises(HTTPException) as exc_info:
            await delete_address(phone_number, mock_redis_client)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Phone number not found"


@pytest.mark.asyncio
async def test_delete_address_invalid_phone_format():
    """Test delete_address with an invalid phone number format."""
    # Arrange
    phone_number = "invalid-phone"
    mock_redis_client = AsyncMock()

    # Mock validate_phone_format to return False and normalization to fail
    with mock.patch('api.v1.routes.delete_address.validate_phone_format', return_value=False):
        with mock.patch('api.v1.routes.delete_address.normalize_phone_number', return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                await delete_address(phone_number, mock_redis_client)

    # Assert
    assert exc_info.value.status_code == 422
    assert "Invalid phone number format" in exc_info.value.detail


@pytest.mark.asyncio
async def test_delete_address_with_normalized_phone():
    """Test delete_address with a phone number that needs normalization."""
    # Arrange
    original_phone = "89123456789"  # Russian format without +
    normalized_phone = "+79123456789"  # What it should normalize to
    mock_redis_client = AsyncMock()

    # Mock the phone validation and normalization
    with mock.patch('api.v1.routes.delete_address.validate_phone_format', side_effect=[False, True]):  # First call False, then True
        with mock.patch('api.v1.routes.delete_address.normalize_phone_number', return_value=normalized_phone):
            # Mock the service to return success
            mock_service = AsyncMock(spec=PhoneBookService)
            mock_service.delete_address = AsyncMock(return_value=True)

            with mock.patch('api.v1.routes.delete_address.PhoneBookService', return_value=mock_service):
                result = await delete_address(original_phone, mock_redis_client)

    # Assert
    assert result is None  # DELETE operations return 204, which is None in FastAPI
    mock_service.delete_address.assert_called_once_with(normalized_phone)
