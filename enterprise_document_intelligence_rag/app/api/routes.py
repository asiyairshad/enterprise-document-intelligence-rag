from fastapi import APIRouter, HTTPException
from enterprise_document_intelligence_rag.app.services.ingestion_service import ingest_all_documents
from enterprise_document_intelligence_rag.app.services.query_service import query_knowledge_base

router = APIRouter()


@router.get("/")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "Enterprise RAG system running"}


@router.post("/ingest")
def ingest_documents():
    """
    Ingest ALL PDFs present in data/raw into a single FAISS index.
    """
    try:
        ingest_all_documents()
        return {"message": "All documents ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query")
def query_documents(question: str):
    """
    Query across ALL ingested documents.
    """
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        answer, sources = query_knowledge_base(question)
        return {
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
