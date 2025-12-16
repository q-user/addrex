from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from redis.asyncio import Redis

from api.dependencies import redis_client_provider
from services.phonebook_service import PhoneBookService
from utils.validators import normalize_phone_number, validate_phone_format

router = APIRouter()


@router.delete('/address/{phone_number}')
async def delete_address(
    phone_number: str,
    redis_client: Annotated[Redis, Depends(redis_client_provider)],
):
    """Delete a phone-address record.

    Args:
        phone_number: The phone number in international format
        redis_client: Redis client dependency

    Raises:
        HTTPException: 404 if phone doesn't exist, 422 if invalid format

    """
    # Validate phone number format
    if not validate_phone_format(phone_number):
        # Try to normalize the phone number first
        normalized = normalize_phone_number(phone_number)
        if not normalized:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f'Invalid phone number format: {phone_number}. '
                + 'Must follow E.164 or Russian format (+7XXXXXXXXXX or 8XXXXXXXXXX)',
            )
        phone_number = normalized

    # Create service instance
    service = PhoneBookService(redis_client)

    # Try to delete the address
    success = await service.delete_address(phone_number)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Phone number not found',
        )

    # Return 204 No Content for successful deletion
