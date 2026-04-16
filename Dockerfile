FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories if they don't exist
RUN mkdir -p ml data

# Create startup script
RUN echo '#!/bin/sh\n\
PORT=${PORT:-8000}\n\
echo "Starting server on port $PORT"\n\
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT' > /start.sh && \
    chmod +x /start.sh

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Run startup script
CMD ["/start.sh"]