"""Unit tests for the create_address route function."""

from unittest import mock
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from api.v1.routes.create_address import create_address
from models.address import Address
from models.api_models import CreateAddressRequest
from services.phonebook_service import PhoneBookService


def _make_request(data: dict) -> CreateAddressRequest:
    return CreateAddressRequest(address=Address(**data))


@pytest.mark.asyncio
async def test_create_address_valid_request():
    phone_number = "+1234567890"
    address_data = {
        "street": "123 Main St",
        "city": "Anytown",
        "state_province": "NY",
        "postal_code": "12345",
        "country": "US",
    }
    mock_redis_client = AsyncMock()

    mock_service = AsyncMock(spec=PhoneBookService)
    expected_address_data = {
        "street": "123 Main St",
        "city": "Anytown",
        "state_province": "NY",
        "postal_code": "12345",
        "country": "US",
        "formatted_address": "123 Main St, Anytown, NY 12345, US",
    }
    mock_service.create_address = AsyncMock(return_value=True)

    with mock.patch("api.v1.routes.create_address.PhoneBookService", return_value=mock_service):
        request_data = _make_request(address_data)
        result = await create_address(phone_number, request_data, mock_redis_client)

    assert result == {"phone": phone_number, "address": expected_address_data}
    mock_service.create_address.assert_called_once_with(phone_number, expected_address_data)


@pytest.mark.asyncio
async def test_create_address_conflict():
    phone_number = "+1234567890"
    address_data = {
        "street": "123 Main St",
        "city": "Anytown",
        "state_province": "NY",
        "postal_code": "12345",
        "country": "US",
    }
    mock_redis_client = AsyncMock()
    mock_service = AsyncMock(spec=PhoneBookService)
    mock_service.create_address = AsyncMock(return_value=False)

    with mock.patch("api.v1.routes.create_address.PhoneBookService", return_value=mock_service):
        with pytest.raises(HTTPException) as exc_info:
            request_data = _make_request(address_data)
            await create_address(phone_number, request_data, mock_redis_client)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Phone number already exists"


@pytest.mark.asyncio
async def test_create_address_invalid_phone_format():
    phone_number = "invalid-phone"
    address_data = {
        "street": "123 Main St",
        "city": "Anytown",
        "state_province": "NY",
        "postal_code": "12345",
        "country": "US",
    }
    mock_redis_client = AsyncMock()

    with mock.patch("api.v1.routes.create_address.validate_phone_format", return_value=False):
        with mock.patch("api.v1.routes.create_address.normalize_phone_number", return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                request_data = _make_request(address_data)
                await create_address(phone_number, request_data, mock_redis_client)

    assert exc_info.value.status_code == 422
    assert "Invalid phone number format" in exc_info.value.detail


@pytest.mark.asyncio
async def test_create_address_with_normalized_phone():
    original_phone = "89123456789"
    normalized_phone = "+79123456789"
    address_data = {
        "street": "123 Main St",
        "city": "Anytown",
        "state_province": "NY",
        "postal_code": "12345",
        "country": "US",
    }
    mock_redis_client = AsyncMock()

    with mock.patch("api.v1.routes.create_address.validate_phone_format", side_effect=[False, True]):
        with mock.patch("api.v1.routes.create_address.normalize_phone_number", return_value=normalized_phone):
            mock_service = AsyncMock(spec=PhoneBookService)
            expected_address_data = {
                "street": "123 Main St",
                "city": "Anytown",
                "state_province": "NY",
                "postal_code": "12345",
                "country": "US",
                "formatted_address": "123 Main St, Anytown, NY 12345, US",
            }
            mock_service.create_address = AsyncMock(return_value=True)

            with mock.patch("api.v1.routes.create_address.PhoneBookService", return_value=mock_service):
                request_data = _make_request(address_data)
                result = await create_address(original_phone, request_data, mock_redis_client)

    assert result == {"phone": normalized_phone, "address": expected_address_data}
    mock_service.create_address.assert_called_once_with(normalized_phone, expected_address_data)


@pytest.mark.asyncio
async def test_create_address_invalid_address_data():
    phone_number = "+1234567890"
    invalid_address_data = {
        "street": "123 Main St",
        "city": "Anytown",
        "state_province": "NY",
        "postal_code": "12345",
        "country": "US",
    }
    mock_redis_client = AsyncMock()
    request_data = _make_request(invalid_address_data)

    with pytest.raises(HTTPException) as exc_info:
        with mock.patch("models.address.Address.model_dump", side_effect=Exception("Validation failed"), create=True):
            await create_address(phone_number, request_data, mock_redis_client)

    assert exc_info.value.status_code == 422
    assert "Invalid address data" in str(exc_info.value.detail)
