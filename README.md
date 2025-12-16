# Phonebook API Service

A microservice for storing and managing phone-to-address mappings with support for Russian phone number formats.

## Overview

This service provides CRUD operations for phone-to-address mappings using FastAPI and Redis. It supports both E.164 and Russian phone number formats with a 300-character limit for addresses.

## Features

- Retrieve address by phone number (GET /address/{phone_number})
- Create new phone-address records (POST /address/{phone_number})
- Update existing records (PUT /address/{phone_number})
- Delete records (DELETE /address/{phone_number})
- Support for Russian phone number formats (+7XXXXXXXXXX, 8XXXXXXXXXX)
- Address validation with 300 character limit
- Comprehensive error handling
- Input validation and sanitization

## Prerequisites

- Python 3.14
- Docker and Docker Compose
- Redis (for data storage)

## Installation

### Using Docker

```bash
docker-compose up -d
```

The API will be available at: `http://localhost:8000`

### Local Installation

1. Install dependencies using uv:
```bash
uv pip install -e .
```

2. Or install in development mode:
```bash
uv pip install -e '.[dev]'
```

3. Start Redis (using Docker or locally)

4. Run the application:
```bash
uv run uvicorn src.main:app --reload
```

## API Documentation

Interactive API documentation is available at: `http://localhost:8000/docs`
Alternative API documentation (Redoc): `http://localhost:8000/redoc`

## Configuration

The application can be configured through environment variables:
- `REDIS_HOST`: Redis server hostname (default: localhost)
- `REDIS_PORT`: Redis server port (default: 6379)
- `REDIS_DB`: Redis database number (default: 0)
- `LOG_LEVEL`: Logging level (default: INFO)
- `API_VERSION`: API version prefix (default: v1)

## Usage Examples

### Retrieve an address
```bash
curl -X GET "http://localhost:8000/address/+1234567890"
```

### Create a new record
```bash
curl -X POST "http://localhost:8000/address/+1234567890" \
  -H "Content-Type: application/json" \
  -d '{
    "address": {
      "street": "123 Main St",
      "city": "Anytown",
      "state_province": "NY",
      "postal_code": "12345",
      "country": "US"
    }
  }'
```

### Update an existing record
```bash
curl -X PUT "http://localhost:8000/address/+1234567890" \
  -H "Content-Type: application/json" \
  -d '{
    "address": {
      "street": "456 Oak Ave",
      "city": "Newtown",
      "state_province": "CA",
      "postal_code": "67890",
      "country": "US"
    }
  }'
```

### Delete a record
```bash
curl -X DELETE "http://localhost:8000/address/+1234567890"
```

## Testing

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

## Linting

Lint and format code:
```bash
ruff check src tests
ruff format src tests
```

## Development

This project follows Test-Driven Development (TDD) principles. When adding new features:
1. Write tests first
2. Run tests to confirm they fail
3. Implement the feature
4. Run tests to confirm they pass
5. Refactor as needed