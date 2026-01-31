from fastapi import APIRouter, HTTPException, UploadFile, File
import uuid
from pathlib import Path

from enterprise_document_intelligence_rag.app.services.ingestion_service import (
    ingest_all_documents,
    ingest_texts_to_faiss
)
from enterprise_document_intelligence_rag.app.services.query_service import (
    query_enterprise_kb,
    query_user_kb
)
from enterprise_document_intelligence_rag.app.core.session_store import SESSION_INDEX
from enterprise_document_intelligence_rag.app.ingestion.loader import load_pdf

router = APIRouter()


@router.get("/")
def health_check():
    return {"status": "Enterprise RAG system running"}


@router.post("/ingest")
def ingest_documents():
    ingest_all_documents()
    return {"message": "All documents ingested successfully"}


@router.post("/query-enterprise")
def query_enterprise(question: str):
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    answer, sources = query_enterprise_kb(question)
    return {"answer": answer, "sources": sources}


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())
    temp_path = Path(f"/tmp/{session_id}.pdf")

    contents = await file.read()
    with open(temp_path, "wb") as f:
        f.write(contents)

    texts = load_pdf(temp_path)
    index = ingest_texts_to_faiss(texts)
    SESSION_INDEX[session_id] = index

    temp_path.unlink()
    return {"session_id": session_id}


@router.post("/query-user")
def query_user(question: str, session_id: str):
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if session_id not in SESSION_INDEX:
        raise HTTPException(status_code=404, detail="Invalid session_id")

    answer, sources = query_user_kb(question, session_id)
    return {"answer": answer, "sources": sources}
