
import uuid

import chromadb
from sentence_transformers import SentenceTransformer

from document_chat import (
    extract_text_from_pdf,
    split_text_into_chunks
)

from database import save_document


# ---------------- CONFIGURATION ----------------

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "chat_documents"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Load model once instead of loading it for every upload/search
model = SentenceTransformer(EMBEDDING_MODEL)

# Connect to persistent ChromaDB
client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)


# ---------------- PDF PROCESSING ----------------

def process_pdf(pdf_file, session_id, access_type):
    """
    Extract, split, embed and store an uploaded PDF.

    access_type must be 'private' or 'shared'.
    """

    if access_type not in ("private", "shared"):
        raise ValueError("Access type must be 'private' or 'shared'.")

    filename = pdf_file.name

    # Extract PDF text
    text = extract_text_from_pdf(pdf_file)

    if not text.strip():
        raise ValueError(
            f"No readable text found in {filename}. "
            "The PDF may be scanned or image-based."
        )

    # Split text into chunks
    chunks = split_text_into_chunks(text)

    if not chunks:
        raise ValueError("No text chunks could be created.")

    # Create a unique ID for this PDF
    document_id = str(uuid.uuid4())

    # Generate embeddings
    embeddings = model.encode(chunks).tolist()

    # Create unique IDs for every chunk
    chunk_ids = [
        f"{document_id}_{index}"
        for index in range(len(chunks))
    ]

    # Store access information with every chunk
    metadatas = []

    for index in range(len(chunks)):
        metadatas.append({
            "document_id": document_id,
            "filename": filename,
            "session_id": session_id or "",
            "access_type": access_type,
            "chunk_index": index
        })

    # Store chunks in ChromaDB
    collection.add(
        ids=chunk_ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    # Store document information in SQLite
    save_document(
        document_id=document_id,
        filename=filename,
        session_id=session_id if access_type == "private" else None,
        access_type=access_type
    )

    return {
        "document_id": document_id,
        "filename": filename,
        "chunks": len(chunks),
        "access_type": access_type
    }


# ---------------- DOCUMENT RETRIEVAL ----------------

def search_documents(question, session_id, n_results=5):
    """
    Search shared documents and private documents
    belonging to the active chat.
    """

    if not session_id:
        return []

    question_embedding = model.encode(question).tolist()

    # Retrieve chunks from:
    # 1. Shared documents
    # 2. Private documents belonging to this chat

    where_filter = {
        "$or": [
            {"access_type": "shared"},
            {
                "$and": [
                    {"access_type": "private"},
                    {"session_id": session_id}
                ]
            }
        ]
    }

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results,
        where=where_filter,
        include=["documents", "metadatas", "distances"]
    )

    if not results["documents"] or not results["documents"][0]:
        return []

    retrieved_chunks = []

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        retrieved_chunks.append({
            "content": document,
            "filename": metadata["filename"],
            "document_id": metadata["document_id"],
            "access_type": metadata["access_type"],
            "distance": distance
        })

    return retrieved_chunks


# ---------------- CONTEXT CREATION ----------------

def create_document_context(retrieved_chunks):
    """
    Combine retrieved chunks into context for the AI.
    """

    if not retrieved_chunks:
        return ""

    context_parts = []

    for chunk in retrieved_chunks:
        context_parts.append(
            f"Source: {chunk['filename']}\n"
            f"Content:\n{chunk['content']}"
        )

    return "\n\n".join(context_parts)
