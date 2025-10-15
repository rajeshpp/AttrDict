# Quick Start Guide

Get the LangFlow Customer Support Chatbot running in 5 minutes!

## Prerequisites

- Python 3.8+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Step 1: Setup (2 minutes)

```bash
cd langflow_poc
chmod +x setup.sh
./setup.sh
```

## Step 2: Configure API Key (1 minute)

```bash
nano .env
```

Add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-key-here
```

Save and exit (Ctrl+X, then Y, then Enter)

## Step 3: Run the Chatbot (2 minutes)

### Option A: Standalone Mode (Easiest)

```bash
chmod +x run_standalone.sh
./run_standalone.sh
```

### Option B: LangFlow UI Mode

```bash
chmod +x run_langflow.sh
./run_langflow.sh
```

Then open http://127.0.0.1:7860 in your browser and import `flows/customer_support_rag.json`

## Try These Questions

1. "What is the price of SmartWidget Pro?"
2. "How do I reset my device?"
3. "What is your return policy?"
4. "My device won't connect to WiFi"
5. "How do I contact support?"

## Test Mode

Run automated tests:

```bash
./run_standalone.sh --test
```

## Need Help?

See [README.md](README.md) for detailed documentation and troubleshooting.

---

**That's it! You now have a working RAG chatbot.** 🎉
