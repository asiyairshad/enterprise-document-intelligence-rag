from typing import Dict
from langchain_community.vectorstores import FAISS


SESSION_INDEX: Dict[str, FAISS] = {}
