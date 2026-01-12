FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create app directory structure
RUN mkdir -p /app/data /app/logs /app/config

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 jaida && \
    chown -R jaida:jaida /app
USER jaida

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Expose ports
EXPOSE 8080

# Entrypoint
ENTRYPOINT ["python3", "unified_orchestrator.py"]
