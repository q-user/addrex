import re

from pydantic import BaseModel, Field, field_validator


class Phone(BaseModel):
    number: str = Field(..., description='Phone number in international format')
    raw_input: str = Field(..., description='Original input for validation purposes')
    country_code: str = Field(..., description='ISO country code (e.g., RU, US, GB)')

    @field_validator('number')
    @classmethod
    def validate_phone_format(cls, v):
        # Check if it's a standard E.164 format or Russian format
        # Russian formats: +7-XXX-XXX-XX-XX, +7XXXXXXXXXX, 8-XXX-XXX-XX-XX, 8XXXXXXXXXX
        # Standard E.164: +[country code][number]
        e164_pattern = r'^\+[1-9]\d{1,14}$'
        russian_mobile_pattern = r'^\+7\d{10}$'
        russian_alt_pattern = r'^8\d{10}$'

        if not (re.match(e164_pattern, v) or re.match(russian_mobile_pattern, v) or re.match(russian_alt_pattern, v)):
            raise ValueError(
                f'Invalid phone number format: {v}. Must follow E.164 or Russian format (+7XXXXXXXXXX or 8XXXXXXXXXX)',
            )

        return v

    @field_validator('country_code')
    @classmethod
    def validate_country_code(cls, v):
        # Basic validation for country codes (2 uppercase letters)
        if not re.match(r'^[A-Z]{2}$', v):
            raise ValueError(
                f'Invalid country code format: {v}. Must be 2 uppercase letters (e.g., RU, US)',
            )
        return v
