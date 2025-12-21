from pathlib import Path
import fitz  # PyMuPDF
import pdfplumber

from enterprise_document_intelligence_rag.app.core.exceptions import IngestionError
from enterprise_document_intelligence_rag.app.core.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]  # enterprise_document_intelligence_rag/app
DATA_DIR = BASE_DIR / "data" / "raw"



def load_pdf(relative_path: str) -> list[str]:
    """
    Production-grade PDF loader with fallback strategy.
    """

    pdf_path = DATA_DIR / relative_path
    logger.info(f"Resolved PDF path: {pdf_path}")

    if not pdf_path.exists():
        raise IngestionError(f"PDF not found: {pdf_path}")

    # ---------- PRIMARY: PyMuPDF ----------
    try:
        logger.info("Trying PyMuPDF parser")
        texts = []

        with fitz.open(pdf_path) as doc:
            for page in doc:
                text = page.get_text("text")
                if text and text.strip():
                    texts.append(text.strip())

        if texts:
            logger.info(f"Extracted {len(texts)} pages using PyMuPDF")
            return texts

    except Exception as e:
        logger.warning(f"PyMuPDF failed: {e}")

    # ---------- FALLBACK: pdfplumber ----------
    try:
        logger.info("Trying pdfplumber fallback")
        texts = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text and text.strip():
                    texts.append(text.strip())

        if texts:
            logger.info(f"Extracted {len(texts)} pages using pdfplumber")
            return texts

    except Exception as e:
        logger.warning(f"pdfplumber failed: {e}")

    # ---------- FAILURE ----------
    raise IngestionError(
        "Unable to extract text from PDF using standard parsers. "
        "Document may be scanned and require OCR."
    )
