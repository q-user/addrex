<!-- SYNC IMPACT REPORT
Version change: 1.6.0 → 1.6.1
Added sections: Updated Development Workflow to include absolute import and test coverage requirements
Modified principles: Enhanced Development Workflow principle
Templates requiring updates: ⚠ pending - plan-template.md, spec-template.md, tasks-template.md need review
Follow-up TODOs: Complete performance and concurrency testing tasks (T062-T063) in tasks.md
-->
# Phonebook API Service Constitution

## Core Principles

### API-First Design
Every feature starts with a well-defined API contract; APIs must be self-documented, follow RESTful principles, have clear purpose - no internal-only endpoints without external contracts

### Data Persistence via Redis
All data operations must go through Redis; Key-value store patterns: phone as key → address as value; Support both JSON and plain text formats

### Test-Driven Development (NON-NEGOTIABLE)
TDD mandatory: Feature requirements defined → Unit tests written → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced; All functionality must have corresponding tests before implementation; Test coverage must exceed 85%

### FastAPI Framework Compliance
Focus areas requiring FastAPI best practices: Request/response validation with Pydantic models, Proper status codes, Type hints for all endpoints, Async support for Redis operations

### Performance & Scalability
Redis caching ensures low latency; Response times under 100ms for 95% of requests; Support for high-throughput scenarios with proper connection pooling

## Technology Stack

Python 3.14+, uv for package management, pyproject.toml for project configuration, FastAPI, Redis, Docker for containerization, Pydantic for request/response validation, AsyncIO for non-blocking operations

## Development Workflow

Code review requirements: All PRs must include tests; Testing gates: Coverage over 85%, All tests passing; Deployment: CI/CD pipeline with health checks; Package management via uv with pyproject.toml configuration; Dependencies managed exclusively through pyproject.toml; Import paths must not contain 'src' prefix and must use absolute imports (e.g., 'from phonebook_api.services.phonebook_service import PhoneBookService' rather than relative imports or 'src' prefixed paths); Ruff must be run on all files after any updates to ensure code formatting and linting compliance; All tools (ruff, pytest, mypy, etc.) must be executed via uv (e.g., 'uv run ruff', 'uv run pytest'); Line lengths must be 120 characters maximum

## Governance

All PRs/reviews must verify compliance with API contracts; Complexity must be justified with performance benchmarks; Use FastAPI documentation for runtime development guidance; All projects must use uv and pyproject.toml for dependency management

**Version**: 1.6.1 | **Ratified**: 2025-12-16 | **Last Amended**: 2025-12-16