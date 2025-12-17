FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download Chisel
RUN wget https://github.com/jpillora/chisel/releases/download/v1.11.3/chisel_1.11.3_linux_amd64.gz && \
    gzip -d chisel_1.11.3_linux_amd64.gz && \
    chmod +x chisel_1.11.3_linux_amd64 && \
    mv chisel_1.11.3_linux_amd64 chisel

# Copy application
COPY ingest.py .
COPY start.sh .
RUN chmod +x start.sh

# Create documents directory
RUN mkdir -p /app/documents

CMD ["./start.sh"]
