#!/bin/bash
# Script to run the standalone chatbot (without LangFlow UI)

echo "========================================"
echo "Starting Standalone RAG Chatbot"
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
    echo "Error: .env file not found"
    echo "Please create .env from .env.example and add your OPENAI_API_KEY"
    exit 1
fi

# Run the chatbot
cd scripts
python standalone_rag_chatbot.py "$@"
