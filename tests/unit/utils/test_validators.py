from utils.validators import normalize_phone_number, validate_address_length, validate_phone_format


def test_validate_phone_format_valid_e164():
    """Test that valid E.164 phone numbers return True."""
    assert validate_phone_format("+1234567890") is True
    assert validate_phone_format("+442079460000") is True  # UK example


def test_validate_phone_format_valid_russian():
    """Test that valid Russian phone numbers return True."""
    assert validate_phone_format("+79123456789") is True
    assert validate_phone_format("+79876543210") is True


def test_validate_phone_format_valid_russian_alt():
    """Test that valid alternative Russian phone numbers return True."""
    assert validate_phone_format("89123456789") is True
    assert validate_phone_format("89876543210") is True


def test_validate_phone_format_invalid():
    """Test that invalid phone numbers return False."""
    assert validate_phone_format("invalid") is False
    assert validate_phone_format("123") is False
    assert validate_phone_format("") is False
    assert validate_phone_format("+7123") is False  # Too short


def test_normalize_phone_number_valid_e164():
    """Test that valid E.164 numbers are returned as-is."""
    assert normalize_phone_number("+1234567890") == "+1234567890"
    assert normalize_phone_number("+79123456789") == "+79123456789"


def test_normalize_phone_number_russian_alt():
    """Test that alternative Russian numbers are converted to E.164 format."""
    assert normalize_phone_number("89123456789") == "+79123456789"
    assert normalize_phone_number("81234567890") == "+71234567890"


def test_normalize_phone_number_invalid():
    """Test that invalid numbers return None."""
    assert normalize_phone_number("invalid") is None
    assert normalize_phone_number("") is None
    assert normalize_phone_number("123") is None


def test_normalize_phone_number_none():
    """Test that None input returns None."""
    assert normalize_phone_number(None) is None


def test_validate_address_length_valid():
    """Test that valid length addresses return True."""
    assert validate_address_length("") is True
    assert validate_address_length("A" * 250) is True  # Well within 300 char limit
    assert validate_address_length("A" * 300) is True  # Exactly at the limit


def test_validate_address_length_invalid():
    """Test that addresses over 300 chars return False."""
    assert validate_address_length("A" * 301) is False  # Just over the limit
    assert validate_address_length("A" * 500) is False  # Way over the limit
