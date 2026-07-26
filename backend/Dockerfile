# ==========================================
# STAGE 1: Build Dependencies Environment
# ==========================================
FROM python:3.10-slim AS builder

WORKDIR /build

# Install any basic C-compilers or system requirements if needed for scientific packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Cache Python dependencies in an isolated wheels path
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt


# ==========================================
# STAGE 2: Final High-Security Runtime Layer
# ==========================================
FROM python:3.10-slim

WORKDIR /app

# Prevent Python from writing .pyc files to disk and ensure stdout/stderr are unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a secure, restricted system user group to avoid running container applications as Root
RUN groupadd -g 10001 appuser && \
    useradd -u 10001 -g appuser -m -s /bin/bash appuser

# Retrieve pre-compiled wheels layer from the previous builder stage environment
COPY --from=builder /build/wheels /wheels
COPY --from=builder /build/requirements.txt .
RUN pip install --no-cache /wheels/*

# Pull system codebase scripts into working folder scope
COPY --chown=appuser:appuser . .

# Switch application context execution path down to restricted permissions user profile
USER appuser

EXPOSE 8000

# Run Uvicorn routing loops across all container networks
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
