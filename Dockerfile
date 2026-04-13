# HIV Infection Dating Tool
# Copyright (C) 2025  Eduard Grebe
# Author: Eduard Grebe <eduard@grebe.consulting>
#
# Multi-architecture Docker image for the Streamlit web application
# Supports: linux/amd64, linux/arm64

FROM python:3.14-slim

# Metadata
LABEL org.opencontainers.image.title="HIV Infection Dating Tool"
LABEL org.opencontainers.image.description="Estimates plausible HIV infection intervals from diagnostic test histories"
LABEL org.opencontainers.image.source="https://github.com/eduardgrebe/infection-dating-tool"
LABEL org.opencontainers.image.licenses="GPL-3.0-or-later"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # Streamlit configuration
    STREAMLIT_SERVER_PORT=8502 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true \
    # Application
    APP_HOME=/app

# Install system dependencies (curl needed for health checks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast Python package management
RUN pip install --no-cache-dir uv && \
    uv --version

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash appuser && \
    mkdir -p ${APP_HOME} && \
    chown -R appuser:appuser ${APP_HOME}

# Set working directory
WORKDIR ${APP_HOME}

# Copy Python dependency files
COPY --chown=appuser:appuser pyproject.toml uv.lock ./

# Install Python dependencies using uv
RUN uv sync --frozen

# Copy application code
COPY --chown=appuser:appuser app.py ./
COPY --chown=appuser:appuser core/ ./core/
COPY --chown=appuser:appuser data/ ./data/

# Switch to non-root user
USER appuser

# Expose Streamlit port
EXPOSE 8502

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8502/_stcore/health || exit 1

# Run Streamlit application using uv's virtual environment
CMD [".venv/bin/streamlit", "run", "app.py", \
     "--server.port=8502", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.fileWatcherType=none", \
     "--browser.gatherUsageStats=false"]
