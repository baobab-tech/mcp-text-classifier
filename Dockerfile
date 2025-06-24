FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY text_classifier_server.py .
COPY run_http_server.py .

# Expose port
EXPOSE 8000

# Run the server
CMD ["python", "run_http_server.py", "--host", "0.0.0.0", "--port", "8000"]
