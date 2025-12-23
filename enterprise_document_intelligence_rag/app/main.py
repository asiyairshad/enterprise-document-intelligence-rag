from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

# ---- LangSmith observability (ONE-TIME SETUP) ----
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv(
    "LANGCHAIN_PROJECT", "enterprise-document-intelligence-rag"
)

from enterprise_document_intelligence_rag.app.api.routes import router

app = FastAPI(title="Enterprise Document Intelligence RAG")

app.include_router(router)
