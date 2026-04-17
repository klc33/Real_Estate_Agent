FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including supervisor
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories and copy model
RUN mkdir -p ml data
COPY ml/best_model.pkl /app/ml/ 2>/dev/null || true
COPY ml/training_stats.json /app/ml/ 2>/dev/null || true

# Create supervisor config
RUN echo '[supervisord]\n\
nodaemon=true\n\
user=root\n\
\n\
[program:api]\n\
command=uvicorn app.main:app --host 0.0.0.0 --port 8000\n\
directory=/app\n\
autostart=true\n\
autorestart=true\n\
stdout_logfile=/dev/stdout\n\
stdout_logfile_maxbytes=0\n\
stderr_logfile=/dev/stderr\n\
stderr_logfile_maxbytes=0\n\
environment=PYTHONPATH="/app"\n\
\n\
[program:ui]\n\
command=streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false --server.headless=true\n\
directory=/app\n\
autostart=true\n\
autorestart=true\n\
stdout_logfile=/dev/stdout\n\
stdout_logfile_maxbytes=0\n\
stderr_logfile=/dev/stderr\n\
stderr_logfile_maxbytes=0\n\
environment=API_URL="http://localhost:8000",PYTHONPATH="/app"\n' > /etc/supervisor/conf.d/supervisord.conf

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose both ports
EXPOSE 8000 8501

# Run supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]