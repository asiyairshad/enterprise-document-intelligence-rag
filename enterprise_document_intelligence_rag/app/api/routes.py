from fastapi import APIRouter, HTTPException, UploadFile, File
import uuid

from enterprise_document_intelligence_rag.app.services.ingestion_service import ingest_all_documents,ingest_texts_to_faiss
from enterprise_document_intelligence_rag.app.services.query_service import query_enterprise_kb, query_user_kb
from enterprise_document_intelligence_rag.app.core.session_store import SESSION_INDEX
from enterprise_document_intelligence_rag.app.ingestion.loader import load_pdf
from pathlib import Path
from shutil import copyfile
from enterprise_document_intelligence_rag.app.ingestion.loader import DATA_DIR

router = APIRouter()


@router.get("/")
def health_check():
    return {"status": "Enterprise RAG system running"}


# -------- ENTERPRISE MODE (global KB) --------

@router.post("/ingest")
def ingest_documents():
    try:
        ingest_all_documents()
        return {"message": "All documents ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query-enterprise")
def query_enterprise(question: str):
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        answer, sources = query_enterprise_kb(question)
        return {"answer": answer, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------- USER MODE (ChatGPT-style upload) --------

@router.post("/upload")
def upload_document(file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())

    from pathlib import Path
    temp_path = Path.cwd() / f"{session_id}.pdf"

    contents = file.file.read()
    with open(temp_path, "wb") as f:
        f.write(contents)

    dest = DATA_DIR / temp_path.name
    
    texts = load_pdf(temp_path)

    index = ingest_texts_to_faiss(texts)

    SESSION_INDEX[session_id] = index
    return {"session_id": session_id}


@router.post("/query-user")
def query_user(question: str, session_id: str):
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        answer, sources = query_user_kb(question, session_id)
        return {"answer": answer, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

