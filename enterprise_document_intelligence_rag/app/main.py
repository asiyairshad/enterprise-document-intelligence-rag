from fastapi import FastAPI
from dotenv import load_dotenv
import os
from enterprise_document_intelligence_rag.app.api.routes import router

load_dotenv()

app = FastAPI(title="Enterprise Document Intelligence RAG")
app.include_router(router)
