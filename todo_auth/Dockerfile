# Use Python 3.12-slim as the base image
FROM python:3.12-slim-bookworm

# Copy `uv` package manager from Astral's repository
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory inside the container
WORKDIR /app

# Copy the entire project into the container
ADD . /app

# Install dependencies using `uv`
RUN uv sync --frozen

# Expose the port FastAPI will run on
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
