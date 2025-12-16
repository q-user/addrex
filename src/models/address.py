from pydantic import BaseModel, Field, field_validator

ADDRESS_MAX_LENGTH = 300  # Maximum length for address in characters


class Address(BaseModel):
    # Increase max lengths so that a combination could potentially exceed 300 characters
    street: str = Field(
        ...,
        min_length=2,
        max_length=200,  # Increased to allow longer streets
        description='Street address including number and street name',
    )
    city: str = Field(..., min_length=2, max_length=100, description='City name')  # Increased
    state_province: str = Field(
        ...,
        min_length=2,
        max_length=50,  # Increased
        description='State or province name',
    )
    postal_code: str = Field(
        ...,
        min_length=3,
        max_length=20,  # Increased
        description='Postal or ZIP code',
    )
    country: str = Field(..., min_length=2, max_length=50, description='Country name')  # Increased
    formatted_address: str = Field(
        default='',
        description='Full formatted address string',
    )

    @field_validator('formatted_address')
    @classmethod
    def validate_address_length(cls, v):
        # Enforce the 300 character limit for the complete address string
        if len(v) > ADDRESS_MAX_LENGTH:
            raise ValueError(
                f'Address exceeds {ADDRESS_MAX_LENGTH} character limit. Current length: {len(v)}',
            )
        return v

    def model_post_init(self, __context):
        """Automatically format the address after validation"""
        self.formatted_address = f'{self.street}, {self.city}, {self.state_province} {self.postal_code}, {self.country}'
        # Check if the formatted address exceeds 300 characters
        if len(self.formatted_address) > ADDRESS_MAX_LENGTH:
            raise ValueError(
                f'Formatted address exceeds {ADDRESS_MAX_LENGTH} character limit. '
                f'Current length: {len(self.formatted_address)}',
            )
