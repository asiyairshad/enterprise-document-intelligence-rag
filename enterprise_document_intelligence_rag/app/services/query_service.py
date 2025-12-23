from langchain_openai import ChatOpenAI
from enterprise_document_intelligence_rag.app.vectorstores.faiss_store import load_faiss_index
from enterprise_document_intelligence_rag.app.embeddings.embedding import get_embeddings


def query_knowledge_base(question: str):
    embeddings = get_embeddings()
    vectorstore = load_faiss_index(embeddings)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
    docs = retriever.invoke(question)

    sources = list(set(doc.metadata["source"] for doc in docs))

    context = "\n\n".join(doc.page_content for doc in docs)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = f"""
You are an assistant answering questions from multiple documents.
Use ONLY the context below.

Context:
{context}

Question:
{question}
"""

    answer = llm.invoke(prompt).content

    return answer, sources
