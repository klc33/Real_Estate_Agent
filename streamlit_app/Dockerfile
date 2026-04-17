FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app

# Create startup script
RUN echo '#!/bin/bash\n\
PORT=${PORT:-8501}\n\
echo "Starting Streamlit on port $PORT"\n\
echo "API_URL is set to: $API_URL"\n\
exec streamlit run streamlit_app/app.py --server.port $PORT --server.address 0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false' > /start.sh && \
    chmod +x /start.sh

EXPOSE 8501

CMD ["/start.sh"]