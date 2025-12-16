import re

ADDRESS_MAX_LENGTH = 300  # Maximum length for address in characters



def validate_phone_format(phone_number: str) -> bool:
    """Validate phone number format supporting both E.164 and Russian formats.

    Args:
        phone_number: Phone number string to validate

    Returns:
        True if format is valid, False otherwise

    """
    # Russian mobile format: +7XXXXXXXXXX, e.g., +79123456789 (exactly 11 digits after +7)
    russian_mobile_pattern = r'^\+7\d{10}$'

    # Alternative Russian format: 8XXXXXXXXXX, e.g., 89123456789
    russian_alt_pattern = r'^8\d{10}$'

    # For non-Russian numbers, use E.164 format: +[country code][number], with min 7 digits after country code for Russian numbers
    e164_pattern = r'^\+[1-9]\d{1,14}$'

    # Check if it's a Russian number starting with +7 or 8
    if phone_number.startswith('+7'):
        # For +7 numbers, it must have exactly 11 digits after the +7
        return bool(re.match(russian_mobile_pattern, phone_number))
    elif phone_number.startswith('8'):
        # For 8 numbers (alternative Russian), it must have exactly 10 digits after the 8
        return bool(re.match(russian_alt_pattern, phone_number))
    else:
        # For non-Russian numbers, check E.164
        return bool(re.match(e164_pattern, phone_number))


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
