#!/bin/bash
# Setup script for LangFlow POC

echo "========================================"
echo "LangFlow POC Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Please edit .env and add your OPENAI_API_KEY"
    echo ""
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p chroma_db
mkdir -p logs

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your OPENAI_API_KEY"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Choose one of the following options:"
echo ""
echo "   Option A - Run with LangFlow UI:"
echo "   - Start LangFlow: ./run_langflow.sh"
echo "   - Open browser to http://127.0.0.1:7860"
echo "   - Import flows/customer_support_rag.json"
echo "   - Use scripts/run_chatbot.py to interact"
echo ""
echo "   Option B - Run standalone (no LangFlow UI needed):"
echo "   - python scripts/standalone_rag_chatbot.py"
echo ""
