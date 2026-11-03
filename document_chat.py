
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import requests

def extract_text_from_pdf(pdf_file):
    """Extract text from an uploaded PDF."""

    reader = PdfReader(pdf_file)

    extracted_text = ""

    for page_number, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""

        extracted_text += (
            f"\n--- Page {page_number + 1} ---\n"
            + page_text
        )

    return extracted_text

def split_text_into_chunks(text, chunk_size=500, overlap=100):
    """Split extracted text into overlapping chunks."""

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks
def store_chunks_in_chromadb(chunks):
    """Generate embeddings and store chunks in ChromaDB."""

    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Create persistent ChromaDB client
    client = chromadb.PersistentClient(path="./chroma_db")

    # Create or access collection
    collection = client.get_or_create_collection(
        name="resume_documents"
    )

    # Generate embeddings
    embeddings = model.encode(chunks).tolist()

    # Store chunks
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings
    )

    print("\nCHUNKS STORED SUCCESSFULLY IN CHROMADB!")
    print("Total stored chunks:", collection.count())

def search_resume(question):
    """Find relevant resume chunks and generate an answer."""

    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path="./chroma_db")

    collection = client.get_or_create_collection(
        name="resume_documents"
    )

    question_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=5
    )

    documents = results["documents"][0]

    if not documents:
        print("No relevant resume information found.")
        return

    context = "\n\n".join(documents)

    print("\nGenerating answer using Ollama...\n")

    answer = generate_answer(question, context)

    print("SMARTCHAT AI ANSWER:")
    print(answer)

def generate_answer(question, context):
    """Generate an answer using Ollama and retrieved resume content."""

    prompt = f"""
    Answer the question using ONLY the resume information provided below.

    Resume information:
    {context}

    Question:
    {question}

    Instructions:
    - Answer clearly and naturally.
    - Do not make up information.
    - If the resume does not contain the answer, say:
      "This information is not available in the resume."
    """

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.2:1b",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a resume assistant. Use only the supplied resume context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    answer = response.json()["message"]["content"]

    return answer


# Test the function
if __name__ == "__main__":
    pdf_path = input("Enter your PDF file path: ")

    text = extract_text_from_pdf(pdf_path)

    print("\nPDF TEXT EXTRACTED SUCCESSFULLY!")
    print("Total characters:", len(text))

    chunks = split_text_into_chunks(text)

    print("\nTEXT SPLIT SUCCESSFULLY!")
    print("Total chunks:", len(chunks))

    store_chunks_in_chromadb(chunks)

    question = input("\nAsk a question about your resume: ")

    search_resume(question)