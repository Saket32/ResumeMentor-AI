from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Sample text
sentences = [
    "I have experience in backend engineering.",
    "I have worked with Python and data processing.",
    "I enjoy cooking and travelling."
]

# Generate embeddings
embeddings = model.encode(sentences)

print("EMBEDDINGS GENERATED SUCCESSFULLY!")

print("Number of sentences:", len(embeddings))
print("Vector dimensions:", len(embeddings[0]))

print("\nFirst embedding:")
print(embeddings[0])