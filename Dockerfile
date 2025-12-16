FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml .

# Install dependencies using uv
RUN uv pip install --system --no-cache -e .

# Copy the rest of the application code
COPY src/ src/
COPY README.md .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]