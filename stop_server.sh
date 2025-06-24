#!/bin/bash

echo "Stopping Text Classification MCP Server..."

# Find and kill the server process
pkill -f "text_classifier_server.py"
pkill -f "run_http_server.py"

echo "Server stopped."