from pydantic import BaseModel
from typing import List, Optional

class DocumentElement(BaseModel):
    text: str
    type: Optional[str] = None
    page: Optional[int] = None

class DocumentLoadResponse(BaseModel):
    document_name : str
    elements: List[DocumentElement]