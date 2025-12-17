#!/bin/bash
set -e

# Validate environment variables
if [ -z "$AAAS_TOKEN" ]; then
    echo "Error: AAAS_TOKEN is not set"
    exit 1
fi

if [ -z "$AAAS_TUNNEL_HOST" ]; then
    echo "Error: AAAS_TUNNEL_HOST is not set. Example: localhost:9090"
    exit 1
fi

if [ -z "$REMOTE_PORT" ]; then
    echo "Error: REMOTE_PORT is not set"
    exit 1
fi

echo "Starting Document Ingestion & Tunnel..."
echo "Tunnel Host: $AAAS_TUNNEL_HOST"
echo "Remote Port (Qdrant): $REMOTE_PORT"
echo "Token: [REDACTED]"

# Start ingestion
echo "Running document ingestion..."
python /app/ingest.py

# Start the tunnel to expose Qdrant
echo "Starting Chisel tunnel to expose Qdrant..."
./chisel client --auth "$AAAS_TOKEN" \
    "$AAAS_TUNNEL_HOST" \
    "R:$REMOTE_PORT:qdrant:6333" &

CHISEL_PID=$!

# Keep the container running
echo "Tunnel established. Container will stay running..."
wait $CHISEL_PID
