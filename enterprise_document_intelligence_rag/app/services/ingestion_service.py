from enterprise_document_intelligence_rag.app.ingestion.loader import load_pdf
from enterprise_document_intelligence_rag.app.chunking.chunker import chunk_text
from enterprise_document_intelligence_rag.app.core.logger import get_logger
from enterprise_document_intelligence_rag.app.core.exceptions import IngestionError
from enterprise_document_intelligence_rag.app.embeddings.embedding import get_embeddings
from enterprise_document_intelligence_rag.app.vectorstores.faiss_store import build_faiss_index
from enterprise_document_intelligence_rag.app.embeddings.embedding import get_embeddings
from enterprise_document_intelligence_rag.app.vectorstores.faiss_store import (
    build_faiss_index,
    save_faiss_index,
)


logger = get_logger(__name__)


def ingest_and_chunk(relative_path: str) -> list[str]:
    """
    Loads a document, extracts text, and chunks it for RAG ingestion.
    """

    logger.info(f"Starting ingestion for: {relative_path}")

    try:
        text_list = load_pdf(relative_path)

        if not text_list:
            raise IngestionError("No text extracted from document")

        full_text = " ".join(text_list)

        if not full_text.strip():
            raise IngestionError("Extracted text is empty")

        chunks = chunk_text(full_text)

        logger.info(f"Ingestion complete. Chunks created: {len(chunks)}")

        return chunks

    except IngestionError:
        # Known, expected ingestion issues
        raise

    except Exception as e:
        logger.exception("Unexpected ingestion failure")
        raise IngestionError(str(e))

def ingest_and_index(path:str):
    """
    Ingest document and build FAISS vectorstore.
    """
    text_list = load_pdf(path)
    full_text = " ".join(text_list)

    chunks = chunk_text(full_text)

    embeddings = get_embeddings()
    vectorstore = build_faiss_index(chunks, embeddings)

    save_faiss_index(vectorstore)

    return vectorstore
