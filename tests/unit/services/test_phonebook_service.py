import pytest
from unittest.mock import AsyncMock
from src.services.phonebook_service import PhoneBookService


@pytest.mark.asyncio
async def test_create_address_success():
    """Test creating a new address successfully when phone number doesn't exist."""
    # Mock the Redis client
    mock_redis = AsyncMock()
    mock_redis.get.return_value = None  # Phone doesn't exist
    mock_redis.set.return_value = True
    
    service = PhoneBookService(mock_redis)
    result = await service.create_address(
        "+1234567890", 
        {
            "street": "123 Main St", 
            "city": "Anytown", 
            "state_province": "NY", 
            "postal_code": "12345", 
            "country": "US",
            "formatted_address": "123 Main St, Anytown, NY 12345, US"
        }
    )
    
    assert result is True
    mock_redis.get.assert_called_once_with("+1234567890")
    mock_redis.set.assert_called_once()


@pytest.mark.asyncio
async def test_create_address_conflict():
    """Test creating an address when the phone number already exists."""
    # Mock the Redis client
    mock_redis = AsyncMock()
    mock_redis.get.return_value = '{"street": "Old St", "city": "Oldtown", "state_province": "OLD", "postal_code": "OLD00", "country": "US", "formatted_address": "Old St, Oldtown, OLD OLD00, US"}'  # Phone already exists

    service = PhoneBookService(mock_redis)
    result = await service.create_address(
        "+1234567890",
        {
            "street": "123 Main St",
            "city": "Anytown",
            "state_province": "NY",
            "postal_code": "12345",
            "country": "US",
            "formatted_address": "123 Main St, Anytown, NY 12345, US"
        }
    )

    assert result is False  # Should return False when phone already exists
    mock_redis.get.assert_called_once_with("+1234567890")
    # set should not have been called since phone already exists
    mock_redis.set.assert_not_called()


@pytest.mark.asyncio
async def test_create_address_with_russian_format():
    """Test creating an address with Russian phone format."""
    # Mock the Redis client
    mock_redis = AsyncMock()
    mock_redis.get.return_value = None  # Phone doesn't exist
    mock_redis.set.return_value = True

    service = PhoneBookService(mock_redis)
    result = await service.create_address(
        "+79123456789",
        {
            "street": "Тверская улица, 1",
            "city": "Москва",
            "state_province": "Москва",
            "postal_code": "125001",
            "country": "RU",
            "formatted_address": "Тверская улица, 1, Москва, 125001, RU"
        }
    )

    assert result is True
    mock_redis.get.assert_called_once_with("+79123456789")
    mock_redis.set.assert_called_once()


@pytest.mark.asyncio
async def test_update_address_success():
    """Test updating an existing address successfully."""
    # Mock the Redis client
    mock_redis = AsyncMock()
    mock_redis.get.return_value = '{"street": "Old St", "city": "Oldtown", "state_province": "OLD", "postal_code": "OLD00", "country": "US", "formatted_address": "Old St, Oldtown, OLD OLD00, US"}'  # Phone exists
    mock_redis.set.return_value = True

    service = PhoneBookService(mock_redis)
    result = await service.update_address(
        "+1234567890",
        {
            "street": "123 Main St",
            "city": "Anytown",
            "state_province": "NY",
            "postal_code": "12345",
            "country": "US",
            "formatted_address": "123 Main St, Anytown, NY 12345, US"
        }
    )

    assert result is True
    mock_redis.get.assert_called_once_with("+1234567890")
    mock_redis.set.assert_called_once()


@pytest.mark.asyncio
async def test_update_address_not_found():
    """Test updating an address when the phone number doesn't exist."""
    # Mock the Redis client
    mock_redis = AsyncMock()
    mock_redis.get.return_value = None  # Phone doesn't exist

    service = PhoneBookService(mock_redis)
    result = await service.update_address(
        "+1234567890",
        {
            "street": "123 Main St",
            "city": "Anytown",
            "state_province": "NY",
            "postal_code": "12345",
            "country": "US",
            "formatted_address": "123 Main St, Anytown, NY 12345, US"
        }
    )

    assert result is False  # Should return False when phone doesn't exist
    mock_redis.get.assert_called_once_with("+1234567890")
    # set should not have been called since phone doesn't exist
    mock_redis.set.assert_not_called()


@pytest.mark.asyncio
async def test_update_address_with_russian_format():
    """Test updating an address with Russian phone format."""
    # Mock the Redis client
    mock_redis = AsyncMock()
    mock_redis.get.return_value = '{"street": "Старая улица, 1", "city": "СтарыйГород", "state_province": "СтараяОбл", "postal_code": "OLD01", "country": "RU", "formatted_address": "Старая улица, 1, СтарыйГород, СтараяОбл OLD01, RU"}'  # Phone exists with Russian address
    mock_redis.set.return_value = True

    service = PhoneBookService(mock_redis)
    result = await service.update_address(
        "+79123456789",
        {
            "street": "Тверская улица, 1",
            "city": "Москва",
            "state_province": "Москва",
            "postal_code": "125001",
            "country": "RU",
            "formatted_address": "Тверская улица, 1, Москва, 125001, RU"
        }
    )

    assert result is True
    mock_redis.get.assert_called_once_with("+79123456789")
    mock_redis.set.assert_called_once()


@pytest.mark.asyncio
async def test_delete_address_success():
    """Test deleting an existing address successfully."""
    # Mock the Redis client
    mock_redis = AsyncMock()
    mock_redis.get.return_value = '{"street": "Old St", "city": "Oldtown", "state_province": "OLD", "postal_code": "OLD00", "country": "US", "formatted_address": "Old St, Oldtown, OLD OLD00, US"}'  # Phone exists
    mock_redis.delete.return_value = 1  # Simulate successful deletion

    service = PhoneBookService(mock_redis)
    result = await service.delete_address("+1234567890")

    assert result is True
    mock_redis.get.assert_called_once_with("+1234567890")
    mock_redis.delete.assert_called_once_with("+1234567890")


@pytest.mark.asyncio
async def test_delete_address_not_found():
    """Test deleting an address when the phone number doesn't exist."""
    # Mock the Redis client
    mock_redis = AsyncMock()
    mock_redis.get.return_value = None  # Phone doesn't exist

    service = PhoneBookService(mock_redis)
    result = await service.delete_address("+1234567890")

    assert result is False  # Should return False when phone doesn't exist
    mock_redis.get.assert_called_once_with("+1234567890")
    # delete should not have been called since phone doesn't exist
    mock_redis.delete.assert_not_called()


@pytest.mark.asyncio
async def test_delete_address_with_russian_format():
    """Test deleting an address with Russian phone format."""
    # Mock the Redis client
    mock_redis = AsyncMock()
    mock_redis.get.return_value = '{"street": "Старая улица, 1", "city": "СтарыйГород", "state_province": "СтараяОбл", "postal_code": "OLD01", "country": "RU", "formatted_address": "Старая улица, 1, СтарыйГород, СтараяОбл OLD01, RU"}'  # Phone exists with Russian address
    mock_redis.delete.return_value = 1  # Simulate successful deletion

    service = PhoneBookService(mock_redis)
    result = await service.delete_address("+79123456789")

    assert result is True
    mock_redis.get.assert_called_once_with("+79123456789")
    mock_redis.delete.assert_called_once_with("+79123456789")