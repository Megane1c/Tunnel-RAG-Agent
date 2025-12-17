"""
Document ingestion script.
Ingests local markdown files into Qdrant vector database.

This runs on the client side (in the Docker container) on startup.
"""

import os
import logging
import glob
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.markdown_reader import MarkdownReader
from agno.knowledge.chunking.markdown import MarkdownChunking
from agno.vectordb.qdrant import Qdrant
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.ollama import OllamaEmbedder

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ingestion")

# Configuration from environment
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
OLLAMA_URL = os.getenv("OLLAMA_URL")
DOCS_DIR = "/app/documents"
COLLECTION_NAME = "documents"


def ingest():
    """Ingest documents from DOCS_DIR into Qdrant using Agno."""
    logger.info(f"Connecting to Qdrant at {QDRANT_URL}")
    logger.info(f"Ingesting documents from: {DOCS_DIR}")
    
    # Initialize Qdrant vector database
    vector_db = Qdrant(
        embedder=OllamaEmbedder(
            id="embeddinggemma",  # Ollama model name
            host=OLLAMA_URL,
            dimensions=768
        ),
        collection=COLLECTION_NAME,
        url=QDRANT_URL
    )

    contents_db = SqliteDb(
        db_file="data.db",
        knowledge_table="knowledge_contents"
    )

    reader = MarkdownReader(
    chunking_strategy=MarkdownChunking(
        chunk_size=1024,
        overlap=200
    ))
    
    # Initialize Knowledge module
    knowledge = Knowledge(vector_db=vector_db, contents_db=contents_db)
    
    # Check if docs directory exists
    if not os.path.exists(DOCS_DIR):
        logger.warning(f"Docs directory not found: {DOCS_DIR}")
        return
    
    # Get markdown files
    md_files = glob.glob(os.path.join(DOCS_DIR, "**/*.md"), recursive=True)
    
    if not md_files:
        logger.warning("No markdown files found to ingest")
        return
    
    logger.info(f"Found {len(md_files)} markdown files")
    
    # Ingest each markdown file
    try:
        logger.info("Starting ingestion...")
        for md_file in md_files:
            filename = os.path.basename(md_file)
            logger.info(f"Ingesting: {filename}")

            knowledge.add_content(
                name=filename,
                path=md_file,
                reader=reader,
                metadata={"source": filename}
            )
        logger.info(f"Ingestion complete: {len(md_files)} documents ingested")
    except Exception as e:
        logger.error(f"Error during ingestion: {e}")
        raise


if __name__ == "__main__":
    logger.info("Starting document ingestion...")
    ingest()
    logger.info("Ingestion finished")
