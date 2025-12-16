import pytest
from src.models.address import Address


def test_address_model_creation_valid():
    """Test creating an address model with valid data."""
    address = Address(
        street="123 Main St",
        city="Anytown",
        state_province="NY",
        postal_code="12345",
        country="US"
    )
    assert address.street == "123 Main St"
    assert address.city == "Anytown"
    assert address.state_province == "NY"
    assert address.postal_code == "12345"
    assert address.country == "US"
    assert "123 Main St, Anytown, NY 12345, US" == address.formatted_address


def test_address_model_with_long_formatted_address():
    """Test creating an address model with a long formatted address raises ValueError."""
    long_street = "A" * 250  # Create a very long street name
    with pytest.raises(ValueError, match="Formatted address exceeds 300 character limit"):
        Address(
            street=long_street,
            city="Anytown",
            state_province="NY",
            postal_code="12345",
            country="US"
        )


def test_address_model_with_address_over_300_chars():
    """Test creating an address model with data that would exceed 300 chars."""
    # Create address components that would exceed 300 chars when formatted
    long_street = "A" * 280  # This alone would cause formatted address to exceed 300 chars
    with pytest.raises(ValueError, match="Formatted address exceeds 300 character limit"):
        Address(
            street=long_street,
            city="Anytown",
            state_province="NY",
            postal_code="12345",
            country="US"
        )


def test_address_model_invalid_street_length():
    """Test creating an address model with invalid street length raises ValueError."""
    with pytest.raises(ValueError):
        Address(
            street="A",  # Too short
            city="Anytown",
            state_province="NY",
            postal_code="12345",
            country="US"
        )


def test_address_model_invalid_city_length():
    """Test creating an address model with invalid city length raises ValueError."""
    with pytest.raises(ValueError):
        Address(
            street="123 Main St",
            city="A",  # Too short
            state_province="NY",
            postal_code="12345",
            country="US"
        )