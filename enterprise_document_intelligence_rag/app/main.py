from dotenv import load_dotenv
load_dotenv()  # ✅ MUST be at the very top

from fastapi import FastAPI
from enterprise_document_intelligence_rag.app.api.routes import router

app = FastAPI(title="Enterprise Document Intelligence RAG")

app.include_router(router)
