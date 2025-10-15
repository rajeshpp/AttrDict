#!/bin/bash
# Script to run LangFlow

echo "========================================"
echo "Starting LangFlow"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found"
    echo "Please create .env from .env.example and add your API keys"
fi

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Start LangFlow
echo "Starting LangFlow on http://127.0.0.1:7860"
echo "Press Ctrl+C to stop"
echo ""

langflow run --host 127.0.0.1 --port 7860
