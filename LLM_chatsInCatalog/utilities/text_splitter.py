from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text(documents, chunk_size=1000, chunk_overlap=500):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)

    chunk_sizes = [len(chunk.page_content) for chunk in chunks]
    avg_size = sum(chunk_sizes) / len(chunk_sizes)
    min_size = min(chunk_sizes)
    max_size = max(chunk_sizes)

    print(f"\nSplit {len(documents)} documents into {len(chunks)} chunks.")
    print(f"Average chunk size: {avg_size:.2f}")
    print(f"Minimum chunk size: {min_size}")
    print(f"Maximum chunk size: {max_size}")

    return chunks
