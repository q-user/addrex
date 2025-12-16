ADDRESS_MAX_LENGTH = 300  # Maximum length for address in characters
import re


def validate_phone_format(phone_number: str) -> bool:
    """Validate phone number format supporting both E.164 and Russian formats.

    Args:
        phone_number: Phone number string to validate

    Returns:
        True if format is valid, False otherwise

    """
    # E.164 format: +[country code][number], e.g., +1234567890
    e164_pattern = r'^\+[1-9]\d{1,14}$'

    # Russian mobile format: +7XXXXXXXXXX, e.g., +79123456789
    russian_mobile_pattern = r'^\+7\d{10}$'

    # Alternative Russian format: 8XXXXXXXXXX, e.g., 89123456789
    russian_alt_pattern = r'^8\d{10}$'

    return (
        bool(re.match(e164_pattern, phone_number))
        or bool(re.match(russian_mobile_pattern, phone_number))
        or bool(re.match(russian_alt_pattern, phone_number))
    )


def normalize_phone_number(phone_number: str) -> str | None:
    """Normalize phone number to standard international format.

    Args:
        phone_number: Phone number string to normalize

    Returns:
        Normalized phone number in E.164 format, or None if invalid

    """
    if not phone_number:
        return None

    # If it's in the alternative Russian format (8XXXXXXXXXX), convert to +7XXXXXXXXXX
    if re.match(r'^8\d{10}$', phone_number):
        return f'+7{phone_number[1:]}'  # Replace '8' with '+7'

    # If it's already in E.164 or valid Russian format, return as-is if valid
    if validate_phone_format(phone_number):
        return phone_number

    return None


def validate_address_length(address_data: str) -> bool:
    """Validate that address data does not exceed 300 characters.

    Args:
        address_data: Address string to validate

    Returns:
        True if length is valid, False otherwise

    """
    return len(address_data) <= ADDRESS_MAX_LENGTH if address_data else True
