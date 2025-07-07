# Dockerfile  — Build image for both “api” and “worker” services
FROM python:3.12-slim AS base

# ------------- system & Python setup -------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# ------------- install Poetry & deps -------------
# Copy the dependency files first to leverage Docker layer-cache
COPY pyproject.toml poetry.lock* /app/

RUN pip install --no-cache-dir poetry \
 && poetry config virtualenvs.create false \
 && poetry install --only main --no-root

# ------------- copy application code -------------
COPY . /app

# ------------- default command (overridden for worker) -------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
