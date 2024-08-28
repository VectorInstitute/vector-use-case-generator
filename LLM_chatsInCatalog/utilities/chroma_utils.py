import os
import shutil
import time
from langchain_community.vectorstores import Chroma
from langchain_cohere import CohereEmbeddings

def save_to_chroma(chunks, chroma_path, api_key):
    # Clear out the database first
    if os.path.exists(chroma_path):
        max_retries = 5
        for attempt in range(max_retries):
            try:
                shutil.rmtree(chroma_path)
                print("Successfully removed Chroma")
                break
            except PermissionError as e:
                if attempt < max_retries - 1:
                    print(f"\n\n\n Retry {attempt + 1} of {max_retries} for deleting Chroma database.\n\n")
                    time.sleep(1)
                else:
                    print("Failed to delete Chroma database:", e)
                    return

    embeddings = CohereEmbeddings(cohere_api_key=api_key)
    db = Chroma.from_documents(
        chunks, embeddings, persist_directory=chroma_path
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {chroma_path}.")
