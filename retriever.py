import os
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import CHROMA_DB_DIR

def get_retriever():
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")
    vectorstore = Chroma(
        persist_directory=str(CHROMA_DB_DIR),
        embedding_function=embeddings,
    )
    return vectorstore.as_retriever(search_kwargs={"k": 2})