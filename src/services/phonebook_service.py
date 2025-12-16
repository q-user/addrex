import json
from typing import Any

from redis.asyncio import Redis


class PhoneBookService:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    async def get_address(self, phone_number: str) -> dict[str, Any] | None:
        """Retrieve an address by phone number from Redis.

        Args:
            phone_number: The phone number to look up

        Returns:
            Address dictionary if found, None otherwise

        """
        # Retrieve the address data from Redis
        address_data = await self.redis_client.get(phone_number)

        if address_data is None:
            return None

        # Parse the JSON address data
        try:
            return json.loads(address_data)
        except json.JSONDecodeError:
            # If there's an error parsing the JSON, return None
            return None

    async def create_address(self, phone_number: str, address: dict[str, Any]) -> bool:
        """Create a new phone-address mapping in Redis.

        Args:
            phone_number: The phone number to store
            address: The address data to store

        Returns:
            True if created successfully, False if phone number already exists

        """
        # Check if the phone number already exists
        existing = await self.redis_client.get(phone_number)
        if existing is not None:
            return False  # Phone number already exists

        # Store the address data in Redis
        address_json = json.dumps(address)
        await self.redis_client.set(phone_number, address_json)
        return True

    async def update_address(self, phone_number: str, address: dict[str, Any]) -> bool:
        """Update an existing phone-address mapping in Redis.

        Args:
            phone_number: The phone number to update
            address: The new address data

        Returns:
            True if updated successfully, False if phone number does not exist

        """
        # Check if the phone number exists
        existing = await self.redis_client.get(phone_number)
        if existing is None:
            return False  # Phone number doesn't exist

        # Update the address data in Redis
        address_json = json.dumps(address)
        await self.redis_client.set(phone_number, address_json)
        return True

    async def delete_address(self, phone_number: str) -> bool:
        """Delete a phone-address mapping from Redis.

        Args:
            phone_number: The phone number to delete

        Returns:
            True if deleted successfully, False if phone number does not exist

        """
        # Check if the phone number exists
        existing = await self.redis_client.get(phone_number)
        if existing is None:
            return False  # Phone number doesn't exist

        # Delete the entry from Redis
        result = await self.redis_client.delete(phone_number)
        return result > 0
