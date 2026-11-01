import math

import src.core.llm as llm
import src.core.supabase as supabase

from google.genai import types
from loguru import logger

gemini_client = llm.get_gemini_client()
supabase_client = supabase.get_supabase_client()

EMBED_MODEL = "gemini-embedding-001"
EMBED_DIM = 768
MATCH_THRESHOLD = 0.8
MATCH_COUNT = 5

def _normalize_vector(vector: list[float]) -> list[float]:
    """Normalisasi vektor embedding agar panjangnya 1""" 
    norm = math.sqrt(sum(x * x for x in vector))

    if norm == 0:
        return vector
    
    return [x / norm for x in vector]

def _embed_food_names(food_names: list[str]) -> list[list[float]]:
    """Generate embedding untuk daftar nama makanan menggunakan Gemini Embedding API"""

    response = gemini_client.models.embed_content(
        model=EMBED_MODEL,
        contents=food_names,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=EMBED_DIM
        )
    )

    return [_normalize_vector(embedding.values) for embedding in response.embeddings]

def search_similar_foods(query: str) -> list[dict]:
    """Cari makanan yang mirip dengan query menggunakan embedding dan Supabase"""

    logger.info(f"Memulai pencarian '{query}'")
    query_embedding = _embed_food_names([query])[0]

    result = supabase_client.rpc("match_food", {
        "query_embedding": query_embedding,
        "match_threshold": MATCH_THRESHOLD,
        "match_count": MATCH_COUNT
    }).execute()

    logger.success(f"Hasil pencarian '{query}': {len(result.data)} makanan ditemukan, selesai")

    return result.data

if __name__ == "__main__":
    queries = ["nasi", "telur", "ayam"]
    for query in queries:
        results = search_similar_foods(query)
        for food in results:
            print(f"Nama makanan: {food['food_name']}, ID: {food['id']}, kalori: {food['calories']}, Skor kemiripan: {food['similarity']}, Sumber: {food['source']}")