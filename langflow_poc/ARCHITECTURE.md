# LangFlow POC Architecture

## System Overview

This POC demonstrates a production-ready RAG (Retrieval Augmented Generation) chatbot for customer support using LangFlow and LangChain.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                      │
├─────────────────────────────────────────────────────────────────┤
│  • CLI Interface (standalone_rag_chatbot.py)                    │
│  • LangFlow Web UI (http://127.0.0.1:7860)                     │
│  • API Client (run_chatbot.py)                                  │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│                   Application Layer                              │
├─────────────────────────────────────────────────────────────────┤
│  • LangFlow Runtime / LangChain Core                            │
│  • Flow Orchestration                                            │
│  • Session Management                                            │
│  • Error Handling & Logging                                      │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│                   RAG Pipeline Layer                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐    ┌──────────────────┐                   │
│  │ Document Loader │───▶│  Text Splitter   │                   │
│  │ (TextLoader)    │    │ (CharacterText-  │                   │
│  │                 │    │  Splitter)       │                   │
│  └─────────────────┘    └────────┬─────────┘                   │
│                                   │                              │
│                         ┌─────────▼──────────┐                  │
│                         │ Embedding Model    │                  │
│                         │ (OpenAI Ada-002)   │                  │
│                         └─────────┬──────────┘                  │
│                                   │                              │
│  ┌───────────────────────────────▼──────────────────────────┐  │
│  │          Vector Store (ChromaDB)                          │  │
│  │  • Document Indexing                                      │  │
│  │  • Similarity Search                                      │  │
│  │  • Metadata Storage                                       │  │
│  └───────────────────────────────┬──────────────────────────┘  │
│                                   │                              │
│                         ┌─────────▼──────────┐                  │
│                         │ Retriever          │                  │
│                         │ (Top-K Search)     │                  │
│                         └─────────┬──────────┘                  │
│                                   │                              │
│                         ┌─────────▼──────────┐                  │
│                         │ Prompt Template    │                  │
│                         │ (Context + Query)  │                  │
│                         └─────────┬──────────┘                  │
│                                   │                              │
│                         ┌─────────▼──────────┐                  │
│                         │ Language Model     │                  │
│                         │ (GPT-3.5-turbo)    │                  │
│                         └─────────┬──────────┘                  │
│                                   │                              │
│                         ┌─────────▼──────────┐                  │
│                         │ Response Generator │                  │
│                         └────────────────────┘                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│                   External Services Layer                        │
├─────────────────────────────────────────────────────────────────┤
│  • OpenAI API (Embeddings & Chat)                               │
│  • ChromaDB (Vector Storage)                                    │
│  • File System (Knowledge Base)                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. User Interface Layer

**Purpose**: Provide multiple ways for users to interact with the chatbot

**Components**:
- **CLI Interface**: Direct Python script for quick testing
- **LangFlow Web UI**: Visual flow builder and testing interface
- **API Client**: Programmatic access via REST API

**Technologies**: Python, FastAPI (via LangFlow), HTTP/REST

---

### 2. Application Layer

**Purpose**: Orchestrate the RAG pipeline and manage application logic

**Components**:
- **LangFlow Runtime**: Executes visual flows created in the UI
- **LangChain Core**: Provides RAG pipeline components
- **Session Manager**: Maintains conversation context
- **Error Handler**: Graceful error handling and logging

**Technologies**: LangFlow, LangChain, Python

---

### 3. RAG Pipeline Layer

**Purpose**: Implement the core RAG (Retrieval Augmented Generation) logic

#### 3.1 Document Processing

**Document Loader** (`TextLoader`):
- Reads knowledge base from `data/knowledge_base.txt`
- Handles various file formats
- Extracts text content

**Text Splitter** (`CharacterTextSplitter`):
- Splits documents into manageable chunks
- Chunk size: 1000 characters
- Overlap: 200 characters (preserves context)
- Ensures chunks fit within embedding model limits

#### 3.2 Embedding & Retrieval

**Embedding Model** (OpenAI `text-embedding-ada-002`):
- Converts text to 1536-dimensional vectors
- Captures semantic meaning
- Enables similarity search

**Vector Store** (ChromaDB):
- Stores document embeddings
- Performs fast similarity search
- Persists to disk for reuse
- Collection: "customer_support"

**Retriever**:
- Searches vector store for relevant documents
- Returns top-K most similar chunks (K=3)
- Uses cosine similarity for matching

#### 3.3 Generation

**Prompt Template**:
- Combines retrieved context with user query
- Provides instructions to the LLM
- Maintains consistent response format

**Language Model** (GPT-3.5-turbo):
- Generates natural language responses
- Temperature: 0.7 (balanced creativity/consistency)
- Context window: 4096 tokens

**Response Generator**:
- Formats final output
- Handles edge cases
- Returns structured response

---

### 4. External Services Layer

**OpenAI API**:
- Embeddings: `text-embedding-ada-002`
- Chat: `gpt-3.5-turbo` or `gpt-4`
- Rate limits: Managed by client
- Authentication: API key via environment variables

**ChromaDB**:
- Local vector database
- Persistent storage in `chroma_db/`
- Fast similarity search with HNSW index

**File System**:
- Knowledge base: `data/knowledge_base.txt`
- Flow definitions: `flows/*.json`
- Configuration: `.env`

---

## Data Flow

### 1. Indexing Phase (One-time setup)

```
knowledge_base.txt
    │
    ├─▶ Load Document
    │
    ├─▶ Split into Chunks
    │       ├─ Chunk 1: "ACME Corp Product..."
    │       ├─ Chunk 2: "Q: How do I reset..."
    │       └─ Chunk N: "Return Policy..."
    │
    ├─▶ Generate Embeddings
    │       ├─ Vector 1: [0.123, -0.456, ...]
    │       ├─ Vector 2: [0.789, 0.234, ...]
    │       └─ Vector N: [-0.345, 0.678, ...]
    │
    └─▶ Store in ChromaDB
            └─ Collection: customer_support
```

### 2. Query Phase (Runtime)

```
User Query: "How do I reset my device?"
    │
    ├─▶ Generate Query Embedding
    │       └─ [0.234, -0.567, ...]
    │
    ├─▶ Search Vector Store (Top-3)
    │       ├─ Match 1: "Q: How do I reset..." (score: 0.92)
    │       ├─ Match 2: "Press and hold..." (score: 0.87)
    │       └─ Match 3: "Troubleshooting..." (score: 0.81)
    │
    ├─▶ Build Prompt
    │       Context: [Match 1, Match 2, Match 3]
    │       Query: "How do I reset my device?"
    │       Template: "You are a helpful assistant..."
    │
    ├─▶ Generate Response (GPT-3.5)
    │       └─ "To reset your SmartWidget Pro..."
    │
    └─▶ Return to User
```

---

## Scalability Considerations

### Current Limitations

- **Single-threaded**: Processes one query at a time
- **Local storage**: ChromaDB runs locally
- **No caching**: Each query re-retrieves from vector store
- **API rate limits**: OpenAI API has rate limits

### Scaling Strategies

**Horizontal Scaling**:
- Deploy multiple LangFlow instances behind load balancer
- Use shared vector store (Pinecone, Weaviate, Qdrant)
- Implement request queuing (Redis, RabbitMQ)

**Vertical Scaling**:
- Increase chunk size for fewer API calls
- Use batch processing for embeddings
- Cache frequently asked questions
- Implement response caching

**Performance Optimization**:
- Pre-compute embeddings for entire knowledge base
- Use faster embedding models (e.g., Sentence Transformers)
- Implement hybrid search (keyword + vector)
- Add semantic caching layer

---

## Security Considerations

### Current Implementation

- API keys in `.env` (not committed to git)
- Local-only ChromaDB (no network exposure)
- No user authentication (POC only)

### Production Recommendations

1. **Authentication & Authorization**:
   - Implement OAuth 2.0 or JWT
   - Role-based access control (RBAC)
   - API key rotation

2. **Data Security**:
   - Encrypt vector store at rest
   - Use HTTPS for all API calls
   - Sanitize user inputs
   - Implement rate limiting

3. **Privacy**:
   - Don't log sensitive information
   - Implement data retention policies
   - GDPR/CCPA compliance
   - User consent for data processing

4. **Infrastructure**:
   - Use secrets manager (AWS Secrets Manager, HashiCorp Vault)
   - Network isolation (VPCs, security groups)
   - Regular security audits
   - DDoS protection

---

## Monitoring & Observability

### Recommended Metrics

**Performance**:
- Query latency (p50, p95, p99)
- Embedding generation time
- Vector search time
- LLM response time

**Quality**:
- Retrieval accuracy
- Response relevance scores
- User feedback ratings
- Fallback rate (questions outside knowledge base)

**System Health**:
- API error rates
- Rate limit hits
- ChromaDB performance
- Memory usage

### Recommended Tools

- **Logging**: Python logging, ELK stack
- **Metrics**: Prometheus, Grafana
- **Tracing**: OpenTelemetry, Jaeger
- **Alerting**: PagerDuty, Slack integration

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| UI | LangFlow Web UI | Visual flow builder |
| UI | Python CLI | Command-line interface |
| Framework | LangFlow | Flow orchestration |
| Framework | LangChain | RAG components |
| Embeddings | OpenAI Ada-002 | Text to vectors |
| LLM | GPT-3.5-turbo | Response generation |
| Vector Store | ChromaDB | Similarity search |
| Storage | File System | Knowledge base |
| Config | python-dotenv | Environment management |
| API | FastAPI | RESTful API (via LangFlow) |

---

## Future Enhancements

1. **Multi-modal Support**: Add image, audio, video processing
2. **Multi-language**: Support for multiple languages
3. **Advanced RAG**: Implement HyDE, self-query, multi-query
4. **Agent Capabilities**: Add tool use, function calling
5. **Memory**: Implement conversation memory, user profiles
6. **Analytics**: User behavior tracking, A/B testing
7. **Integration**: CRM, ticketing systems, knowledge bases
8. **Voice**: Speech-to-text, text-to-speech
9. **Real-time**: WebSocket support for streaming responses
10. **Federation**: Multi-source retrieval from various knowledge bases

---

## Conclusion

This architecture provides a solid foundation for a production RAG chatbot while remaining simple enough for learning and experimentation. The modular design allows easy customization and scaling as requirements grow.
