from fastapi import APIRouter
from enterprise_document_intelligence_rag.app.services.ingestion_service import ingest_and_chunk, ingest_and_index
from enterprise_document_intelligence_rag.app.services.query_service import query_vectorstore
router = APIRouter()


@router.get("/")
def home():
    return {"message": "RAG System running"}


@router.post("/ingest")
def ingest(path: str):
    chunks = ingest_and_chunk(path)
    return {
        "chunks_count": len(chunks),
        "preview": chunks[0][:200] if chunks else "No chunks"
    }

@router.post("/query")
def query_doc(question: str, path:str):
    vectorstore = ingest_and_index(path)
    answer = query_vectorstore(vectorstore, question)

    return{"answer": answer}