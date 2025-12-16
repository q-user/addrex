import pytest

from models.phone import Phone


def test_phone_model_creation_valid_e164():
    """Test creating a phone model with valid E.164 format."""
    phone = Phone(
        number="+1234567890",
        raw_input="+1234567890",
        country_code="US"
    )
    assert phone.number == "+1234567890"
    assert phone.country_code == "US"


def test_phone_model_creation_valid_russian():
    """Test creating a phone model with valid Russian format."""
    phone = Phone(
        number="+79123456789",
        raw_input="+79123456789",
        country_code="RU"
    )
    assert phone.number == "+79123456789"
    assert phone.country_code == "RU"


def test_phone_model_creation_valid_russian_alt():
    """Test creating a phone model with valid alternative Russian format."""
    phone = Phone(
        number="+79123456789",
        raw_input="89123456789",
        country_code="RU"
    )
    assert phone.number == "+79123456789"
    assert phone.country_code == "RU"


def test_phone_model_invalid_format():
    """Test creating a phone model with invalid format raises ValueError."""
    with pytest.raises(ValueError):
        Phone(
            number="invalid",
            raw_input="invalid",
            country_code="XX"
        )


def test_phone_model_invalid_country_code():
    """Test creating a phone model with invalid country code raises ValueError."""
    with pytest.raises(ValueError):
        Phone(
            number="+1234567890",
            raw_input="+1234567890",
            country_code="invalid"
        )
