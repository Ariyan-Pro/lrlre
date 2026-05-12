FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p data logs

# Expose ports
EXPOSE 8007 8009 8013

# Run the application (default to v10.0)
CMD ["uvicorn", "ultimate_v10_fixed:app", "--host", "0.0.0.0", "--port", "8013"]
