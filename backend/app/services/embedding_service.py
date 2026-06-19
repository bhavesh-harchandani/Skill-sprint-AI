from openai import OpenAI
from app.core.config import settings
from typing import List

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_embedding(text: str) -> List[float]:
    """Generate embedding for text using OpenAI text-embedding-3-small"""
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        raise

def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for multiple texts"""
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        raise
