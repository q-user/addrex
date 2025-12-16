import pytest

from models.address import Address
from models.phone import Phone
from models.phone_address import PhoneAddress


def test_phone_address_model_creation_valid():
    """Test creating a phone_address model with valid phone and address."""
    phone = Phone(
        number="+1234567890",
        raw_input="+1234567890",
        country_code="US"
    )
    address = Address(
        street="123 Main St",
        city="Anytown",
        state_province="NY",
        postal_code="12345",
        country="US"
    )

    phone_address = PhoneAddress(phone=phone, address=address)
    assert phone_address.phone.number == "+1234567890"
    assert phone_address.address.street == "123 Main St"


def test_phone_address_model_with_invalid_phone():
    """Test creating a phone_address model with invalid phone raises ValueError."""
    address = Address(
        street="123 Main St",
        city="Anytown",
        state_province="NY",
        postal_code="12345",
        country="US"
    )

    with pytest.raises(ValueError):
        PhoneAddress(
            phone=Phone(
                number="invalid",
                raw_input="invalid",
                country_code="XX"
            ),
            address=address
        )


def test_phone_address_model_with_invalid_address():
    """Test creating a phone_address model with invalid address raises ValueError."""
    phone = Phone(
        number="+1234567890",
        raw_input="+1234567890",
        country_code="US"
    )

    with pytest.raises(ValueError):
        PhoneAddress(
            phone=phone,
            address=Address(
                street="A",  # Invalid - too short
                city="Anytown",
                state_province="NY",
                postal_code="12345",
                country="US"
            )
        )
