import os
from langchain_community.document_loaders import PyPDFLoader

def load_documents(file_path):
    documents = []
    for filename in os.listdir(file_path):
        if filename.endswith(".pdf"):
            full_path = os.path.join(file_path, filename)
            loader = PyPDFLoader(full_path)
            documents.extend(loader.load())
    return documents
