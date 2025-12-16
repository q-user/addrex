import pytest

from models.address import Address


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
    # We need a total formatted address > 300 chars
    # Format: f'{street}, {city}, {state_province} {postal_code}, {country}'
    # So: len(street) + len(city) + len(state_province) + len(postal_code) + len(country) + 7 > 300
    # Total field lengths must be > 293

    # Use maximum length fields to exceed 300 total when formatted
    # New max lengths: street=200, city=100, state_province=50, postal_code=20, country=50
    # To reach over 300 total, we need at least 294 combined field lengths
    # Use large but valid values for each field that will exceed 300 when formatted
    street = "A" * 150  # Large but within limit
    city = "B" * 80     # Large but within limit
    state_province = "C" * 40  # Large but within limit
    postal_code = "D" * 15     # Large but within limit
    country = "E" * 20         # Large but within limit
    # Total: 150 + 80 + 40 + 15 + 20 = 305; with formatting: 305 + 7 = 312 > 300

    with pytest.raises(ValueError, match="Formatted address exceeds 300 character limit"):
        Address(
            street=street,
            city=city,
            state_province=state_province,
            postal_code=postal_code,
            country=country
        )


def test_address_model_with_address_over_300_chars():
    """Test creating an address model with data that would exceed 300 chars."""
    # Create valid fields that result in a formatted address over 300 chars
    # Need total field lengths > 293 to exceed 300 when formatted
    street = "A" * 200  # Max for street
    city = "B" * 50     # Significant value for city
    state_province = "C" * 20   # Value for state_province
    postal_code = "D" * 10      # Standard postal code
    country = "E" * 25          # Value for country
    # Total: 200 + 50 + 20 + 10 + 25 = 305; with formatting: 305 + 7 = 312 > 300

    with pytest.raises(ValueError, match="Formatted address exceeds 300 character limit"):
        Address(
            street=street,
            city=city,
            state_province=state_province,
            postal_code=postal_code,
            country=country
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
