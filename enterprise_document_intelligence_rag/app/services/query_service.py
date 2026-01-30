from langchain_openai import ChatOpenAI
from enterprise_document_intelligence_rag.app.core.session_store import SESSION_INDEX
from enterprise_document_intelligence_rag.app.embeddings.embedding import get_embeddings
from enterprise_document_intelligence_rag.app.vectorstores.faiss_store import load_faiss_index


# -------- MODE 1: Enterprise Global Knowledge Base --------

def query_enterprise_kb(question: str):
    embeddings = get_embeddings()
    vectorstore = load_faiss_index(embeddings)

    retriever = vectorstore.as_retriever(search_type="mmr",
    search_kwargs={"k": 6, "lambda_mult": 0.7})
    docs = retriever.invoke(question)

    if not docs:
        return "I could not find relevant information in the document.", []

    sources = list(set(
        doc.metadata.get("source", "enterprise_doc")
        for doc in docs
    ))

    context = "\n\n".join(doc.page_content for doc in docs)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = f"""
You are an assistant answering questions from multiple enterprise documents.
Use ONLY the context below.

Context:
{context}

Question:
{question}
"""

    answer = llm.invoke(prompt).content
    return answer, sources


# -------- MODE 2: User Uploaded Document (ChatGPT style) --------

def query_user_kb(question: str, session_id: str):
    vectorstore = SESSION_INDEX.get(session_id)

    if not vectorstore:
        raise ValueError("Session not found. Please upload a document first.")

    retriever = vectorstore.as_retriever(search_type="mmr",
    search_kwargs={"k": 6, "lambda_mult": 0.7})
    docs = retriever.invoke(question)
    
    if not docs:
        return "I could not find relevant information in the document.", []

    sources = list(set(
    f"{doc.metadata['source']} - page {doc.metadata['page']}"
    for doc in docs
    ))

    context = "\n\n".join(doc.page_content for doc in docs)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = f"""
You are an assistant answering questions from the user's uploaded document.
Use ONLY the context below.

Context:
{context}

Question:
{question}
"""

    answer = llm.invoke(prompt).content
    return answer, sources

