import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import DOCUMENTS_DIR, CHROMA_DB_DIR

load_dotenv()

def ingest_documents():
    print("Loading documents...")
    loader = TextLoader(DOCUMENTS_DIR / "guidelines.txt")
    docs = loader.load()

    print("Splitting texts...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)

    print("Generating embeddings and storing in ChromaDB...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB_DIR)
    )
    vectorstore.persist()
    print("Ingestion complete. ChromaDB ready.")

if __name__ == "__main__":
    ingest_documents()