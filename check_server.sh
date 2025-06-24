#!/bin/bash

HOST=${1:-127.0.0.1}
PORT=${2:-8000}

echo "Checking Text Classification MCP Server status..."
echo "Host: $HOST"
echo "Port: $PORT"

# Check if server is responding
if curl -s "http://$HOST:$PORT/sse" > /dev/null; then
    echo "✅ Server is running and accessible"
    echo "SSE Endpoint: http://$HOST:$PORT/sse"
    echo "Messages Endpoint: http://$HOST:$PORT/messages"
else
    echo "❌ Server is not responding"
    echo "Make sure the server is running with: ./start_server.sh"
fi

# Check if process is running
if pgrep -f "text_classifier_server.py\|run_http_server.py" > /dev/null; then
    echo "✅ Server process is running"
    echo "PIDs: $(pgrep -f 'text_classifier_server.py\|run_http_server.py')"
else
    echo "❌ No server process found"
fi