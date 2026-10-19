# -------------------------------------------------------------------
# Dockerfile for Crime Prediction Web Application (BE_PROJECT_GC14)
# -------------------------------------------------------------------

# Step 1: Use official lightweight Python 3.11 slim image
FROM python:3.11-slim

# Step 2: Configure Python environment variables
# - PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files
# - PYTHONUNBUFFERED: Flushes stdout and stderr immediately (essential for docker logs)
# - FLASK_APP: Specifies Flask application entry file
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py

# Step 3: Set working directory inside the container
WORKDIR /app

# Step 4: Install minimal system dependencies (curl for health checks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Leverage Docker layer caching
# Copy only dependencies first so Docker reuses cached pip layers if code changes
COPY requirements.txt .

# Step 6: Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Step 7: Copy the rest of the application files into /app
COPY . .

# Step 8: Expose the Flask listening port
EXPOSE 5000

# Step 9: Start Flask bound to 0.0.0.0 to accept external requests
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
