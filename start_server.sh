#!/bin/bash

# Start Text Classification MCP Server

echo "Starting Text Classification MCP Server..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check arguments
TRANSPORT=${1:-http}
PORT=${2:-8000}
HOST=${3:-127.0.0.1}

echo "Transport: $TRANSPORT"
echo "Host: $HOST"
echo "Port: $PORT"

if [ "$TRANSPORT" = "stdio" ]; then
    echo "Running with stdio transport..."
    python text_classifier_server.py
else
    echo "Running with HTTP transport..."
    echo "Server will be accessible at: http://$HOST:$PORT/sse"
    echo "Use Ctrl+C to stop the server"
    python run_http_server.py --transport $TRANSPORT --host $HOST --port $PORT
fi