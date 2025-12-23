from pathlib import Path
from enterprise_document_intelligence_rag.app.embeddings.embedding import get_embeddings
from enterprise_document_intelligence_rag.app.vectorstores.faiss_store import (
    build_faiss_index,
    save_faiss_index
)
from enterprise_document_intelligence_rag.app.ingestion.loader import load_pdf
from enterprise_document_intelligence_rag.app.chunking.chunker import chunk_text

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"


def ingest_all_documents():
    all_chunks = []
    metadatas = []

    for pdf_path in DATA_DIR.glob("*.pdf"):
        text_list = load_pdf(pdf_path.name)
        full_text = " ".join(text_list)
        chunks = chunk_text(full_text)

        for chunk in chunks:
            all_chunks.append(chunk)
            metadatas.append({
                "source": pdf_path.name
            })

    embeddings = get_embeddings()
    vectorstore = build_faiss_index(all_chunks, embeddings, metadatas)

    save_faiss_index(vectorstore)
    return vectorstore
