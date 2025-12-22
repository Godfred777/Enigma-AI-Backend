# 1. Use an official lightweight Python image
# 3.11 is stable and faster than 3.10
FROM python:3.11-slim as builder

# 2. Set Environment Variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Ensures logs are flushed immediately to Cloud Logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# 3. Install System Dependencies
# 'build-essential' is often needed for compiling certain python packages
# 'curl' is useful for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Set the working directory
WORKDIR /app

# 5. Install Python Dependencies
# We copy requirements first to leverage Docker cache layers
COPY requirements.txt .
RUN pip install -r requirements.txt

# 6. Download NLP Models (Critical Step)
# This downloads the 500MB+ model for PII Presidio detection 
# so it doesn't try to download it every time the server starts.
RUN python -m spacy download en_core_web_lg

# 7. Copy Application Code
COPY . .

# 8. Create a non-root user for Security
# Cloud Run recommends not running as root
RUN addgroup --system enigma && adduser --system --group enigma
USER enigma

# 9. Expose the port (Documentation only, Cloud Run ignores this)
EXPOSE 8080

# 10. Start the Application
# We use 'exec' to ensure uvicorn receives Unix signals (like SIGTERM)
# We default to port 8080, but allow Cloud Run to override it via $PORT
CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}