from langchain_community.vectorstores import FAISS
from pathlib import Path


VECTORSTORE_DIR = Path("vectorstore")


def build_faiss_index(chunks: list[str], embeddings):
    """
    Build FAISS index from text chunks.
    """
    return FAISS.from_texts(chunks, embedding=embeddings)


def save_faiss_index(vectorstore):
    """
    Persist FAISS index to disk.
    """
    VECTORSTORE_DIR.mkdir(exist_ok=True)
    vectorstore.save_local(str(VECTORSTORE_DIR))


def load_faiss_index(embeddings):
    """
    Load FAISS index from disk.
    """
    if not VECTORSTORE_DIR.exists():
        raise FileNotFoundError("FAISS index not found")

    return FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )
