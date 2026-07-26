# ==========================================
# STAGE 1: Build Dependencies Environment
# ==========================================
FROM python:3.10-slim AS builder

WORKDIR /build

# Install minimal package dependencies if needed for compiling
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

# Prevent Python from writing .pyc files and force unbuffered logging stdout/stderr streams
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a secure, restricted system user group to avoid running container applications as Root
RUN groupadd -g 10002 uiuser && \
    useradd -u 10002 -g uiuser -m -s /bin/bash uiuser

# Retrieve pre-compiled wheels layer from the previous builder stage environment
COPY --from=builder /build/wheels /wheels
COPY --from=builder /build/requirements.txt .
RUN pip install --no-cache /wheels/*

# Pull system codebase scripts into working folder scope
COPY --chown=uiuser:uiuser . .

# Switch application context execution path down to restricted permissions user profile
USER uiuser

EXPOSE 8501

# Streamlit environmental safeguards for running securely inside clean headless containers
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
