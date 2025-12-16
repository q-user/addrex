from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from phonebook_api.api.dependencies import get_redis_client
from phonebook_api.models.address import Address
from phonebook_api.services.phonebook_service import PhoneBookService
from phonebook_api.utils.validators import normalize_phone_number, validate_phone_format
from redis.asyncio import Redis

router = APIRouter()


@router.put('/address/{phone_number}')
async def update_address(
    phone_number: str,
    address_data: dict[str, Any],
    redis_client: Redis = Depends(get_redis_client),
) -> dict[str, Any]:
    """Update an existing phone-address record.

    Args:
        phone_number: The phone number in international format
        address_data: The new address information
        redis_client: Redis client dependency

    Returns:
        A dictionary containing the phone number and updated address information

    Raises:
        HTTPException: 404 if phone doesn't exist, 422 if invalid format or data

    """
    # Validate phone number format
    if not validate_phone_format(phone_number):
        # Try to normalize the phone number first
        normalized = normalize_phone_number(phone_number)
        if not normalized:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f'Invalid phone number format: {phone_number}. '
                + 'Must follow E.164 or Russian format (+7XXXXXXXXXX or 8XXXXXXXXXX)',
            )
        phone_number = normalized

    # Validate the address data using the Address model
    try:
        # Create an Address object to trigger validation
        address_obj = Address(**address_data)
        # Get the properly formatted address from the model
        validated_address_data = address_obj.dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Invalid address data: {e!s}',
        )

    # Create service instance
    service = PhoneBookService(redis_client)

    # Try to update the address
    success = await service.update_address(phone_number, validated_address_data)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Phone number not found',
        )

    # Return the updated phone number and address
    return {
        'phone': phone_number,
        'address': validated_address_data,
    }
