from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.knowledge.knowledge import Knowledge
from agno.tools.knowledge import KnowledgeTools
from agno.vectordb.qdrant import Qdrant
from agno.knowledge.embedder.ollama import OllamaEmbedder

# Configuration
QDRANT_URL = "http://localhost:6333"

print(f"Initializing Agent with Qdrant at {QDRANT_URL}...")

# Initialize Qdrant vector database
vector_db = Qdrant(
    embedder=OllamaEmbedder(
            id="embeddinggemma",  # Ollama model name
            host="http://localhost:11434",
            dimensions=768
        ),
    collection="documents",
    url=QDRANT_URL
)

# Initialize Knowledge
knowledge = Knowledge(vector_db=vector_db)

knowledge_tools = KnowledgeTools(
    knowledge=knowledge,
)

# Initialize Agent with Knowledge
agent = Agent(
    name="RAG Document Assistant",
    model=Ollama(
        id="gpt-oss-safeguard:120b", 
        host="http://localhost:11434", 
        options={"temperature": 0.3}
    ),
    tools=[knowledge_tools],
    instructions="""You are a Document Analysis Assistant helping users understand and search through a remote document repository.

When a user asks a question:
1. Search the knowledge base for relevant information using multiple search queries if needed.
2. If initial results are incomplete or insufficient, perform follow-up searches with different phrasing or related terms.
3. Combine insights from multiple search results to provide comprehensive answers.
4. If a query returns no results, try:
   - Broader search terms
   - Synonyms or related concepts
   - Breaking down complex queries into simpler searches
5. Always cite the source document(s) when referencing information.
6. If after multiple searches you cannot find relevant information, clearly state this to the user.
7. Provide relevant excerpts and synthesize findings clearly and concisely.

Remember: Exhaustive searching through the knowledge base produces better answers than stopping at the first result.
""",
    markdown=True,
)

if __name__ == "__main__":
    print("Starting interactive mode...")
    print("Ask questions about your documents. Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            agent.print_response(user_input)
        except KeyboardInterrupt:
            break
