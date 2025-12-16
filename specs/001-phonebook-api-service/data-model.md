# Data Model: Phonebook API Service

**Feature**: Phonebook API Service
**Date**: 2025-12-16
**Modeler**: Qwen

## Overview

Data models for the Phonebook API Service, defining the structure of phone-address mappings and related entities with validation rules as required by the feature specification and clarifications.

## Entity Models

### Phone Number Model
**Entity**: Phone Number
**Purpose**: Unique identifier for phone-address mappings
**Structure**:
- `number: str` - The phone number in international format (e.g., "+7-912-345-67-89" for Russian format)
- `raw_input: str` - Original input for validation purposes
- `country_code: str` - ISO country code (e.g., "RU" for Russian numbers, "US", "GB")

**Validation Rules**:
- Must follow either E.164 standard or Russian format (+7-XXX-XXX-XX-XX, 8-XXX-XXX-XX-XX)
- Russian mobile numbers typically start with +7-9XX or +7-495/+7-499 for Moscow area
- Minimum 7 digits after country code for Russian numbers
- Maximum 15 characters total for standard E.164 format
- Must contain only digits, hyphens, parentheses, and plus sign
- Required field

**Relationships**: One-to-One with Address (as value in Redis key-value store)

### Address Model
**Entity**: Address
**Purpose**: Physical address information mapped to phone number
**Structure**:
- `street`: str - Street address including number and street name
- `city`: str - City name
- `state_province`: str - State or province name
- `postal_code`: str - Postal or ZIP code
- `country`: str - Country name (default: inferred from phone number)
- `formatted_address`: str - Full formatted address string

**Validation Rules**:
- Street: 2-100 characters, required
- City: 2-50 characters, required
- State/Province: 2-30 characters, required
- Postal Code: 3-10 characters, required
- Country: 2-30 characters, required
- Total address string: maximum 300 characters (as per clarification)
- Russian addresses: Must comply with Russian address format standards

**Relationships**: One-to-One with Phone Number (as value in Redis key-value store)

### Phone-Address Model
**Entity**: Phone Address (Combined)
**Purpose**: Combined model for creating and updating phone-address mappings
**Structure**:
- `phone`: Phone Number model (validated separately)
- `address`: Address model (validated separately)

**Validation Rules**:
- Both phone and address components must be valid
- Combined data must pass all individual validations
- When creating: reject if phone number already exists (per clarification)
- When updating: allow changes to address while keeping the same phone number

## Redis Data Structure

### Key-Value Schema
**Storage Pattern**: `phone_number:address_json`
- **Key**: Phone number in normalized international format (e.g., +79123456789)
- **Value**: JSON string representation of Address model

**Example**:
```
Key: "+79123456789"
Value: {"street": "Тверская улица, 1", "city": "Москва", "state_province": "Москва", "postal_code": "125001", "country": "RU", "formatted_address": "Тверская улица, 1, Москва, 125001, RU"}
```

### Redis Configuration
- **Persistence**: Enabled to prevent data loss
- **Max Memory**: Configured with appropriate limits to prevent overflow
- **Eviction Policy**: `noeviction` to ensure data integrity
- **TTL**: Optional expiration policy for records (configurable)

## Validation Implementation

### International Phone Format with Russian Support
- Uses regex patterns for both E.164 and Russian formats:
  - Standard: `^\+[1-9]\d{1,14}$`
  - Russian mobile: `^\+7[0-9]{10}$` or `^8[0-9]{10}$`
  - Russian landline: Format validation for regional codes
- Supports normalization function to convert various input formats to standard format
- Validates country codes against ISO standards
- Special handling for Russian formats including area codes and mobile prefixes

### Address Validation
- Implements length restrictions per field with total character limit of 300
- Validates against common address formats including Russian addresses
- Provides standardization functions for consistent storage
- Russian address validation includes support for Cyrillic characters where appropriate

## State Transitions

### Record Lifecycle
1. **Creation**: New phone-address mapping added to Redis
   - Validate phone number (E.164 or Russian format)
   - Validate address (max 300 characters)
   - Check for existing phone number (reject if exists per clarification)
2. **Active**: Record exists and is accessible via API
3. **Update**: Address information modified (phone number as key remains constant)
4. **Deletion**: Record removed from Redis (marking as deleted vs. physical removal)

## Data Integrity

### Consistency Rules
- Phone number uniqueness enforced by Redis key structure
- Address validation ensures data quality with 300-character limit
- Error handling for malformed input with appropriate response codes
- Duplicate phone number prevention during create operations

### Error Handling
- Invalid phone numbers return specific error codes
- Invalid addresses return validation errors
- Storage errors trigger appropriate fallback responses
- Russian format validation errors return specific error messages