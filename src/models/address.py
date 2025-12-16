from pydantic import BaseModel, Field, field_validator


ADDRESS_MAX_LENGTH = 300  # Maximum length for address in characters


class Address(BaseModel):
    street: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description='Street address including number and street name',
    )
    city: str = Field(..., min_length=2, max_length=50, description='City name')
    state_province: str = Field(
        ...,
        min_length=2,
        max_length=30,
        description='State or province name',
    )
    postal_code: str = Field(
        ...,
        min_length=3,
        max_length=10,
        description='Postal or ZIP code',
    )
    country: str = Field(..., min_length=2, max_length=30, description='Country name')
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
