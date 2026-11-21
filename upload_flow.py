
import os
from pathlib import Path

from src.pdf_loader import load_pdf
from src.data_cleaning import clean_documnets
from src.text_splitters import split_chunks
from src.embedding import get_hf_embeddings
from src.vector_store import chunks_store_to_pinecone


# Project data directory
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "data" / "documents"


def save_uploaded_pdf(uploaded_file):

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Avoid using the original filename directly
    safe_filename = Path(uploaded_file.name).name

    file_path = UPLOAD_DIR / safe_filename

    # Save PDF inside data/documents
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path


def process_pdf(filepath: Path):

    # 1. Extract PDF pages
    documents = load_pdf(filepath)

    # 2. Clean extracted text
    cleaned_documents = clean_documnets(documents)

    # 3. Split into chunks
    chunks = split_chunks(cleaned_documents)

    # 4. Initialize embedding model
    embedding_model = get_hf_embeddings(
        modelname="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 5. Store chunks in Pinecone
    storage_result=chunks_store_to_pinecone(
        os.getenv("PINECONE_INDEX_NAME"),
        embedding_model,
        chunks
    )
  

    return {
        "total_pages": len(documents),
        "total_cleaned_pages": len(cleaned_documents),
        "total_chunks": len(chunks),
        "filename": filepath.name,
        "storage_result": storage_result
    }
