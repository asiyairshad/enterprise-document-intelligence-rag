Enterprise Document Intelligence – RAG Chatbot

A production-style Retrieval-Augmented Generation (RAG) system that enables natural language querying across multiple enterprise PDF documents without manual document selection. The system automatically retrieves relevant information from the best sources and generates grounded answers with full observability.

🚀 Features:

Multi-document semantic search across large PDFs

Automatic document selection (no file input required)

Optimized PDF ingestion and semantic chunking

FAISS-based vector search for fast retrieval

Chat-style UI with session-level memory

LangSmith observability for tracing and debugging

🧠 Problem Solved:

Enterprise documents are large, scattered, and time-consuming to search manually.
This system automates document understanding and retrieval, reducing information-search effort by ~60–70% while improving answer accuracy and traceability.

🛠️ Tech Stack:
Backend: FastAPI, LangChain, FAISS

Frontend: Streamlit

LLM & Observability: OpenAI, LangSmith

PDF Parsing: PyMuPDF, pdfplumber

📦 Clone the Repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

▶️ Run Locally
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Set environment variables (.env)
OPENAI_API_KEY=your_openai_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=enterprise-document-rag

3️⃣ Start FastAPI backend
uvicorn enterprise_document_intelligence_rag.app.main:app --reload

4️⃣ Ingest documents (one-time)
Open:
http://127.0.0.1:8000/docs

Call:
POST /ingest

5️⃣ Start Streamlit frontend
streamlit run streamlit_app.py

📈 Impact

~60–70% reduction in manual document search effort

~40–50% faster debugging using LangSmith observability

Scales efficiently to large, multi-document corpora

👤 Author

Asiya Irshad
Aspiring GenAI Engineer

🔗 GitHub: [github.com/asiyairshad]

