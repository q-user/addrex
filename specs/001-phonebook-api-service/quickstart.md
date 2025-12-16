# Quickstart Guide: Phonebook API Service

**Feature**: Phonebook API Service
**Version**: 1.0.0
**Date**: 2025-12-16

## Overview

This guide provides essential information to quickly set up, run, and test the Phonebook API Service. It includes setup instructions, API usage examples, and basic troubleshooting tips. The service supports both E.164 and Russian phone number formats with a 300-character limit for addresses.

## Prerequisites

- Python 3.14 or higher
- uv package manager
- Docker and Docker Compose (for containerized setup)
- Redis (either local or containerized)
- pyproject.toml for project configuration

## Local Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
git checkout 001-phonebook-api-service
```

### 2. Install Dependencies with uv
```bash
# Navigate to project root
cd /path/to/project

# Install dependencies using uv
uv sync

# Or install in development mode
uv develop
```

### 3. Start Redis
Choose one of the following methods:

**Option A: Using Docker Compose**
```bash
docker-compose up -d redis
```

**Option B: Using Local Redis**
```bash
# Ensure Redis is installed and running on default port 6379
redis-server
```

### 4. Environment Configuration
Create a `.env` file in the project root with the following content:
```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
LOG_LEVEL=INFO
API_VERSION=v1
```

### 5. Run the Application
```bash
# Using uv
uv run python src/main.py

# Or using Python directly
python src/main.py
```

The API will be available at: `http://localhost:8000`

## API Usage Examples

### 1. Create a New Phone-Address Record
```bash
curl -X POST "http://localhost:8000/address/+7-912-345-67-89" \
  -H "Content-Type: application/json" \
  -d '{
    "address": {
      "street": "Тверская улица, 1",
      "city": "Москва",
      "state_province": "Москва",
      "postal_code": "12345",
      "country": "RU"
    }
  }'
```

### 2. Retrieve an Address by Phone Number
```bash
curl -X GET "http://localhost:8000/address/+7-912-345-67-89"
```

### 3. Update an Existing Record
```bash
curl -X PUT "http://localhost:8000/address/+7-912-345-67-89" \
  -H "Content-Type: application/json" \
  -d '{
    "address": {
      "street": "Новый Арбат, 22",
      "city": "Москва",
      "state_province": "Москва",
      "postal_code": "54321",
      "country": "RU"
    }
  }'
```

### 4. Delete a Record
```bash
curl -X DELETE "http://localhost:8000/address/+7-912-345-67-89"
```

### 5. Attempt to Create Duplicate (Will Return 409 Conflict)
```bash
curl -X POST "http://localhost:8000/address/+7-912-345-67-89" \
  -H "Content-Type: application/json" \
  -d '{
    "address": {
      "street": "Другой адрес, 10",
      "city": "СПб",
      "state_province": "ЛО",
      "postal_code": "56789",
      "country": "RU"
    }
  }'
```

## Configuration with pyproject.toml

The project uses pyproject.toml for configuration. Example configuration with ruff:

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "phonebook-api"
version = "1.0.0"
description = "API service for storing and managing phone-to-address mappings"
dependencies = [
    "fastapi>=0.100.0",
    "uv>=0.1.0",
    "redis>=4.5.0",
    "pydantic>=2.0.0",
    "python-multipart>=0.0.6"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "mypy>=1.0",
    "ruff>=0.1.0"
]
test = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "pytest-asyncio>=0.21"
]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = ["-v", "--cov=src", "--cov-report=html"]

[tool.mypy]
python_version = "3.14"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.ruff]
line-length = 88
target-version = "py314"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "C",  # complexity
    "B",  # bugbear
    "UP", # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by formatter)
]

[tool.ruff.format]
quote-style = "single"
indent-style = "space"
```

## Testing

### Run Unit Tests
```bash
uv run pytest tests/unit/
```

### Run Integration Tests
```bash
uv run pytest tests/integration/
```

### Run All Tests
```bash
uv run pytest
```

### Linting with Ruff
```bash
uv run ruff check .
uv run ruff format .
```

## Docker Setup

### 1. Build the Docker Image
```bash
docker build -t phonebook-api .
```

### 2. Run with Docker Compose
```bash
docker-compose up -d
```

The API will be available at: `http://localhost:8000`
Redis will be available at: `http://localhost:6379`

## API Documentation

Interactive API documentation is available at: `http://localhost:8000/docs`
Alternative API documentation (Redoc): `http://localhost:8000/redoc`

## Performance Testing

To test the performance requirements mentioned in the spec:

```bash
# Using Apache Bench (ab) for load testing
ab -n 1000 -c 10 http://localhost:8000/address/+7-912-345-67-89

# Using wrk for more advanced testing
wrk -t12 -c400 -d30s --timeout 8 http://localhost:8000/address/+7-912-345-67-89
```

## Troubleshooting

### Common Issues

1. **Redis Connection Error**: Ensure Redis is running and accessible at the configured host/port
2. **Port Already in Use**: Try a different port or stop conflicting services
3. **Validation Errors**: Check that phone numbers follow E.164 or Russian format (+7-XXX-XXX-XX-XX)

### Logs
Check application logs by running with verbose flag:
```bash
uv run python src/main.py --log-level DEBUG
```

## Configuration

### Application Settings
The application can be configured through these environment variables:
- `REDIS_HOST`: Redis server hostname (default: localhost)
- `REDIS_PORT`: Redis server port (default: 6379)
- `REDIS_DB`: Redis database number (default: 0)
- `LOG_LEVEL`: Logging level (default: INFO)
- `API_VERSION`: API version prefix (default: v1)

### Performance Settings
- The API is designed to handle 1000 concurrent users
- Target response time: <100ms for 95% of requests

## Next Steps

1. Review the API contracts in `/contracts/openapi.yaml`
2. Check the data models in `/data-model.md`
3. Examine the detailed implementation plan in `/plan.md`
4. Run the full test suite to ensure all functionality is working
5. Explore the source code structure defined in the implementation plan