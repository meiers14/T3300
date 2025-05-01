import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("ui5-index")

def embed(text: str) -> list[float]:
    return client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    ).data[0].embedding

def search_similar_chunks(query: str, top_k: int = 5):
    vector = embed(query)
    results = index.query(vector=vector, top_k=top_k, include_metadata=True)

    return [
        {
            "title": match["metadata"].get("title", ""),
            "type": match["metadata"].get("type", ""),
            "score": match["score"]
        }
        for match in results["matches"]
    ]