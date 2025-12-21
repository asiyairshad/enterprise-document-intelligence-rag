class IngestionError(Exception):
    """Raised when PDF ingestion fails or text extraction fails."""
    pass
class ChunkingError(Exception):
    """Raised when document chunking fails."""
    pass

class EmbeddingError(Exception):
    """Raised when embedding generation fails."""
    pass
class RetrievalError(Exception):
    """Raised when document retrieval fails."""
    pass
class APIError(Exception):
    """Raised when there is an error in the API layer."""
    pass
class vectorStoreError(Exception):
    """Raised when there is an error with the vector store operations."""
    pass
class RAGError(Exception):
    """Raised when there is a general error in the RAG process."""
    pass