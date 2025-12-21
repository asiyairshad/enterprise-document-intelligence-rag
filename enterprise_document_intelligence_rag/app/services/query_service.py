from langchain_openai import ChatOpenAI

def query_vectorstore(vectorstore, question:str):
    retriever = vectorstore.as_retriever(search_kwargs={"k":5})

    docs = retriever.invoke(question)

    llm = ChatOpenAI(model = "gpt-4o-mini", temperature = 0)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
    Answer the question using only the content below .
    If you don't know the answer, just say that you don't know.
    Do not make up an answer.

    context:{context}
    question:{question}
    """

    return llm.invoke(prompt).content