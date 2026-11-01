import time
import math

import src.core.llm as llm
import src.core.supabase as supabase

from google.genai import types
from loguru import logger

gemini_client = llm.get_gemini_client()
supabase_client = supabase.get_supabase_client()

EMBED_MODEL = "gemini-embedding-001"
EMBED_DIM = 768
BATCH_SIZE = 100
DELAY_SECONDS = 60


def _normalize_vector(vector: list[float]) -> list[float]:
    """Normalisasi vektor embedding agar panjangnya 1""" 
    norm = math.sqrt(sum(x * x for x in vector))

    if norm == 0:
        return vector
    
    return [x / norm for x in vector]


def _get_unembedded_foods() -> list[dict]:
    """Ambil data makanan yang belum di-embed dari Supabase"""
    result = supabase_client.table("food_reference").select("id", "food_name").is_("embedding", "null").order("id").limit(BATCH_SIZE).execute()
    return result.data

def _generate_embeddings(food_names: list[str]) -> list[list[float]]:
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

def _save_embeddings(foods: list[dict], embeddings: list[list[float]]):
    """Simpan embedding ke Supabase"""
    for food, vector in zip(foods, embeddings):
        result = supabase_client.table("food_reference").update({"embedding": vector}).eq("id", food["id"]).execute()

        if not result.data:
            message = f"Gagal menyimpan embedding untuk makanan: {food['food_name']} (ID: {food['id']})"
            logger.error(message)
            raise RuntimeError(message)

def run_embedding_process():
    """Proses untuk mengambil makanan yang belum di-embed, generate embedding, dan simpan ke Supabase"""
    logger.info("Memulai proses embedding makanan...")

    total_embedded = 0
    while True:
        foods_to_embed = _get_unembedded_foods()
        if not foods_to_embed:
            logger.success(f"Semua makanan sudah di-embed. Total baris: {total_embedded}")
            break

        embeddings = _generate_embeddings([food["food_name"] for food in foods_to_embed])
        _save_embeddings(foods_to_embed, embeddings)
        total_embedded += len(foods_to_embed)
        logger.info(f"Berhasil menyimpan embedding untuk {total_embedded} makanan. Menunggu {DELAY_SECONDS} detik sebelum melanjutkan...")
        time.sleep(DELAY_SECONDS)


if __name__ == "__main__":
    run_embedding_process()