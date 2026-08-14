# Multi-stage build for Space-API

# Build stage
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and create wheels
COPY requirements.txt .
RUN pip wheel --wheel-dir /wheels -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 spaceapi

# Copy wheels from builder
COPY --from=builder /wheels /wheels

# Install Python dependencies from wheels
COPY requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy application code
COPY . .

# Set ownership
RUN chown -R spaceapi:spaceapi /app

# Switch to non-root user
USER spaceapi

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api.json || exit 1

# Start application
CMD ["python", "run.py"]
