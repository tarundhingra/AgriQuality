import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAG_DIR = BASE_DIR / "rag"
DOCUMENTS_DIR = RAG_DIR / "documents"
CHROMA_DB_DIR = BASE_DIR / "chroma_db"

# LLM Configuration
GEMINI_MODEL = "gemini-3.5-flash-lite"

# File Paths
SUPPLIERS_FILE = DATA_DIR / "suppliers.json"
LOTS_FILE = DATA_DIR / "lots.json"