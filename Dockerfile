# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VERSION=1.7.1
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Generate lock file if it doesn't exist and install dependencies
RUN if [ ! -f poetry.lock ]; then poetry lock; fi && \
    poetry install --only main --no-interaction --no-ansi

# Copy application code
COPY . .

# Create directory for logs
RUN mkdir -p logs

# Set environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Run gunicorn with increased timeout
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "300", "main:app"] 