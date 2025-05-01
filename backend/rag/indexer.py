import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = "ui5-index"
MAX_CHARS = 15000
BATCH_SIZE = 100

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index(index_name)

chunk_path = os.path.join(os.path.dirname(__file__), "chunks.jsonl")
with open(chunk_path, "r", encoding="utf-8") as f:
    all_chunks = [json.loads(line) for line in f]

valid_chunks = [c for c in all_chunks if len(c["code"]) <= MAX_CHARS]
skipped = len(all_chunks) - len(valid_chunks)

for i in range(0, len(valid_chunks), BATCH_SIZE):
    batch = valid_chunks[i:i + BATCH_SIZE]
    texts = [c["code"] for c in batch]
    ids = [c["id"] for c in batch]
    metadatas = [{"title": c["title"], "type": c["type"]} for c in batch]

    response = client.embeddings.create(
        input=texts,
        model="text-embedding-ada-002"
    )
    embeddings = [d.embedding for d in response.data]

    index.upsert(vectors=list(zip(ids, embeddings, metadatas)))
    print(f"Batch {i // BATCH_SIZE + 1} von {len(valid_chunks) // BATCH_SIZE + 1} gespeichert.")

print(f"Insgesamt gespeichert: {len(valid_chunks)} Chunks")
print(f"Übersprungen wegen Länge: {skipped} Chunks")
