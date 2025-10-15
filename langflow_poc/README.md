# LangFlow POC: Customer Support RAG Chatbot

A complete end-to-end proof of concept demonstrating LangFlow with a Retrieval Augmented Generation (RAG) chatbot for customer support.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This POC demonstrates a customer support chatbot built using LangFlow that can:
- Answer customer questions based on a knowledge base
- Use RAG (Retrieval Augmented Generation) for accurate, context-aware responses
- Maintain conversation context
- Handle common customer inquiries about products, shipping, returns, etc.

The POC includes **two modes**:
1. **LangFlow UI Mode**: Visual flow builder with drag-and-drop interface
2. **Standalone Mode**: Pure Python implementation without the UI

## ✨ Features

- **RAG Implementation**: Combines retrieval from a vector database with LLM generation
- **Vector Store**: Uses ChromaDB for efficient document retrieval
- **OpenAI Integration**: Leverages GPT-3.5-turbo for natural responses
- **Interactive Chat**: Command-line interface for testing
- **Automated Testing**: Predefined test cases for validation
- **Production-Ready**: Includes proper error handling, logging, and environment management

## 🏗️ Architecture

```
┌─────────────┐
│ User Query  │
└──────┬──────┘
       │
       v
┌─────────────────────┐
│ Document Loader     │ Load knowledge_base.txt
│ & Text Splitter     │ Split into chunks
└──────┬──────────────┘
       │
       v
┌─────────────────────┐
│ OpenAI Embeddings   │ Convert text to vectors
└──────┬──────────────┘
       │
       v
┌─────────────────────┐
│ ChromaDB Vector     │ Store & retrieve
│ Store               │ relevant chunks
└──────┬──────────────┘
       │
       v
┌─────────────────────┐
│ Prompt Template     │ Format context + query
└──────┬──────────────┘
       │
       v
┌─────────────────────┐
│ OpenAI ChatGPT      │ Generate response
└──────┬──────────────┘
       │
       v
┌─────────────────────┐
│ Final Answer        │
└─────────────────────┘
```

## 📦 Prerequisites

- Python 3.8 or higher
- OpenAI API key
- 2GB free disk space (for vector store)
- Internet connection

## 🚀 Installation

### 1. Clone or navigate to the project

```bash
cd langflow_poc
```

### 2. Run setup script

```bash
chmod +x setup.sh
./setup.sh
```

### 3. Configure environment variables

Edit the `.env` file and add your OpenAI API key:

```bash
nano .env
```

Add:
```
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
LANGFLOW_HOST=127.0.0.1
LANGFLOW_PORT=7860
```

## 💻 Usage

### Option A: Standalone Mode (Recommended for Quick Start)

This mode runs the chatbot directly without needing LangFlow UI:

```bash
# Make script executable
chmod +x run_standalone.sh

# Interactive mode
./run_standalone.sh

# Test mode (runs predefined test cases)
./run_standalone.sh --test
```

Or directly with Python:

```bash
source venv/bin/activate
cd scripts
python standalone_rag_chatbot.py           # Interactive mode
python standalone_rag_chatbot.py --test    # Test mode
```

### Option B: LangFlow UI Mode

This mode uses the full LangFlow visual interface:

#### 1. Start LangFlow

```bash
chmod +x run_langflow.sh
./run_langflow.sh
```

Or manually:
```bash
source venv/bin/activate
langflow run --host 127.0.0.1 --port 7860
```

#### 2. Access LangFlow UI

Open your browser and navigate to: `http://127.0.0.1:7860`

#### 3. Import the Flow

1. Click on "Import" or "Upload Flow"
2. Select `flows/customer_support_rag.json`
3. The flow will be loaded into the canvas

#### 4. Configure the Flow

1. Click on the **OpenAI Embeddings** node
   - Add your OpenAI API key

2. Click on the **ChatOpenAI** node
   - Add your OpenAI API key
   - Optionally adjust temperature (0.7 is default)

3. Click on the **File** node
   - Ensure path is set to `./data/knowledge_base.txt`

#### 5. Run the Flow

Click the "Run" button in the UI, or use the Python client:

```bash
# Get flow ID from the UI
python scripts/run_chatbot.py <flow-id>           # Interactive mode
python scripts/run_chatbot.py <flow-id> --test    # Test mode
```

## 📁 Project Structure

```
langflow_poc/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .env                              # Your environment variables (create this)
├── setup.sh                          # Installation script
├── run_langflow.sh                   # Start LangFlow UI
├── run_standalone.sh                 # Run standalone chatbot
│
├── data/
│   └── knowledge_base.txt            # Customer support knowledge base
│
├── flows/
│   └── customer_support_rag.json     # LangFlow flow definition
│
├── scripts/
│   ├── __init__.py
│   ├── langflow_client.py            # Client to interact with LangFlow API
│   ├── run_chatbot.py                # Run chatbot via LangFlow
│   └── standalone_rag_chatbot.py     # Standalone implementation
│
└── chroma_db/                        # Vector database (created at runtime)
```

## 🔍 How It Works

### RAG Pipeline Steps

1. **Document Loading**: The knowledge base (`knowledge_base.txt`) contains product information, FAQs, and policies

2. **Text Splitting**: Documents are split into chunks (1000 chars with 200 char overlap) for better retrieval

3. **Embedding Creation**: Each chunk is converted to a vector using OpenAI's `text-embedding-ada-002` model

4. **Vector Storage**: Embeddings are stored in ChromaDB for fast similarity search

5. **Query Processing**: When a user asks a question:
   - The question is converted to an embedding
   - Top 3 most relevant chunks are retrieved from ChromaDB
   - Retrieved context + question are formatted in a prompt template

6. **Response Generation**: GPT-3.5-turbo generates a natural response based on the context

7. **Answer Delivery**: The response is returned to the user

### Example Interactions

**User**: "What is the price of SmartWidget Pro?"

**Bot**: "The SmartWidget Pro is priced at $299.99. We also offer free shipping on orders over $50. Is there anything else you'd like to know about the SmartWidget Pro?"

---

**User**: "How do I reset my device?"

**Bot**: "To reset your SmartWidget Pro, press and hold the power button for 10 seconds until the LED blinks red, then release. The device will restart automatically. If you continue to have issues, please don't hesitate to contact our 24/7 support team."

## 🛠️ Troubleshooting

### Common Issues

#### 1. "OPENAI_API_KEY not found"

**Solution**: Make sure you've created `.env` file and added your API key:
```bash
cp .env.example .env
nano .env  # Add your API key
```

#### 2. "Cannot connect to LangFlow"

**Solution**: Ensure LangFlow is running:
```bash
./run_langflow.sh
```
Check that it's accessible at `http://127.0.0.1:7860`

#### 3. "Module not found" errors

**Solution**: Activate virtual environment and install dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. ChromaDB permissions error

**Solution**: Ensure the `chroma_db` directory is writable:
```bash
chmod -R 755 chroma_db
```

#### 5. Slow responses

**Causes**:
- First run creates embeddings (takes 30-60 seconds)
- Subsequent runs are faster as vectors are cached
- OpenAI API latency

**Solution**: Be patient on first run, responses will be faster afterward

### Getting Help

If you encounter issues:

1. Check the error message carefully
2. Verify your `.env` file has valid API keys
3. Ensure all dependencies are installed
4. Check that you have internet connectivity
5. Review the logs in the terminal

## 📊 Testing

### Automated Tests

Run predefined test cases:

```bash
# Standalone mode
./run_standalone.sh --test

# LangFlow mode
python scripts/run_chatbot.py <flow-id> --test
```

Test cases include:
- Product pricing queries
- Technical support questions
- Policy information requests
- Troubleshooting scenarios
- Contact information requests

## 🎓 Learning Resources

- [LangFlow Documentation](https://docs.langflow.org/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)

## 📝 Customization

### Adding More Knowledge

Edit `data/knowledge_base.txt` to add more product information, FAQs, or policies. The RAG system will automatically use the updated content.

### Changing the LLM

Modify the model in:
- **Standalone**: `scripts/standalone_rag_chatbot.py` (line with `model_name="gpt-3.5-turbo"`)
- **LangFlow UI**: Click on ChatOpenAI node and change model_name
- **API Client**: Update tweaks in `scripts/run_chatbot.py`

Available models: `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo-preview`

### Adjusting Response Style

Modify the prompt template in:
- **Standalone**: `scripts/standalone_rag_chatbot.py` (template variable)
- **LangFlow**: Edit the Prompt Template node in the UI
- **Flow JSON**: Modify `flows/customer_support_rag.json`

### Tuning Retrieval

Adjust chunk size and overlap in text splitter:
- `chunk_size`: Number of characters per chunk (default: 1000)
- `chunk_overlap`: Overlap between chunks (default: 200)

Adjust number of retrieved documents:
- **Standalone**: Change `k` in `search_kwargs={"k": 3}`
- **LangFlow**: Modify retriever settings in the UI

## 🚀 Next Steps

1. **Add more data sources**: Integrate with databases, APIs, or other document types
2. **Implement authentication**: Add user authentication for production use
3. **Deploy to production**: Use Docker, Kubernetes, or cloud platforms
4. **Add monitoring**: Implement logging, metrics, and alerting
5. **Create web UI**: Build a React/Vue frontend for better UX
6. **Multi-language support**: Add translation capabilities
7. **Voice integration**: Add speech-to-text and text-to-speech

## 📄 License

This is a proof of concept for educational purposes.

## 🤝 Contributing

Feel free to fork, modify, and extend this POC for your own use cases!

---

**Built with ❤️ using LangFlow, LangChain, and OpenAI**
