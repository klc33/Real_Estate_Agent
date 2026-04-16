FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p ml data

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV API_URL=http://localhost:8000

# Create startup script that respects Railway's PORT
RUN echo '#!/bin/bash\n\
PORT=${PORT:-8000}\n\
echo "Starting server on port $PORT"\n\
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT' > /start.sh && \
    chmod +x /start.sh

EXPOSE 8000

CMD ["/start.sh"]