# Tunnel RAG Agent POC

This project demonstrates a secure, tunneled connection between an AI Agent and a private document repository using [Chisel](https://github.com/jpillora/chisel). The agent queries documents stored in a remote Qdrant vector database via a secure reverse tunnel, without exposing the documents to the public internet.

The sample documents are markdown files from the client-side repository, representing knowledge bases.

## Architecture

```
Client (remote network)             Server (agent host)
┌─────────────────────┐            ┌──────────────────┐
│  Qdrant (local)     │            │  Ollama API      │
│  Ingestion script   │◄──────────►│  Agno Agent      │
│  Docs folder        │            │                  │
│  Chisel client      │  (tunnel)  │  Chisel Server   │
└─────────────────────┘            └──────────────────┘
```

-   **Server**: 
    - Chisel Server (Reverse Proxy)
    - Agno Agent with Knowledge module
    - Ollama (for embeddings and chat)
-   **Client**: 
    - Qdrant Vector Database (stores embeddings locally)
    - Ingestion script (chunks docs, generates embeddings, stores in Qdrant)
    - Chisel Client (creates reverse tunnel, exposes Qdrant to server)

## Prerequisites

-   Docker & Docker Compose
-   `wget` (to download Chisel)
-   Python 3.10+ (for the Agent)
-   Ollama running locally with embedding and chat models

## Quick Start Guide

### 1. Setup the Tunnel Server

First, download the Chisel binary.

```bash
# Download Chisel (Linux amd64)
wget https://github.com/jpillora/chisel/releases/download/v1.11.3/chisel_1.11.3_linux_amd64.gz

# Unzip and make executable
gzip -d chisel_1.11.3_linux_amd64.gz
mv chisel_1.11.3_linux_amd64 chisel
chmod +x chisel
```

Now, start the server.

```bash
# Run in a dedicated terminal
./chisel server --authfile tunnel-rag-agent/users.json --reverse --port 9090
```

### 2. Start the Client (Client Side)

Open a **new terminal** and run:

```bash
cd tunnel-rag-agent/client-bridge

# Start the compose
docker compose up
```

The ingestion script will automatically:
1. Scan `./docs` for markdown files
2. Chunk and embed documents using Ollama
3. Store embeddings in Qdrant
4. Establish reverse tunnel to expose Qdrant to the server

*Wait until you see `client: Connected` in the logs and `Ingestion complete` message.*

### 3. Run the AI Agent

Open a **third terminal** and run:

```bash
cd tunnel-rag-agent

# Install dependencies
pip install agno ollama qdrant-client

# Run the Agent
python run_agent.py
```

The agent will connect to Qdrant via the tunnel and answer questions about your documents.

### 4. Sample Questions

Try asking the agent questions about the documents in `client-bridge/docs/`:

1.  What are the main topics covered in the documents?
2.  Summarize the sample-book.


## Acknowledgements

-   **[Agno](https://github.com/agno-agi/agno)**: For the powerful Agentic AI framework.
-   **[Chisel](https://github.com/jpillora/chisel)**: For the fast, secure TCP tunnel over HTTP.
-   **[Qdrant](https://github.com/qdrant/qdrant)**: For the high-performance vector database.
-   **[files-hub](https://github.com/my-sample-files/files-hub)**: For the sample markdown files.
