from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from redis.asyncio import Redis

from api.dependencies import get_redis_client
from services.phonebook_service import PhoneBookService
from utils.validators import normalize_phone_number, validate_phone_format

router = APIRouter()


@router.get('/address/{phone_number}')
async def get_address(
    phone_number: str,
    redis_client: Redis = Depends(get_redis_client),
) -> dict[str, Any]:
    """Retrieve an address by phone number.

    Args:
        phone_number: The phone number in international format
        redis_client: Redis client dependency

    Returns:
        A dictionary containing the phone number and address information

    Raises:
        HTTPException: 404 if phone number not found, 422 if invalid format

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

    # Create service instance
    service = PhoneBookService(redis_client)

    # Get the address
    address_data = await service.get_address(phone_number)

    if address_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Phone number not found',
        )

    # Return the phone number and address
    return {
        'phone': phone_number,
        'address': address_data,
    }
