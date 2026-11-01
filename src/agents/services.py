import random
import json
import time

import src.core.env as env
import src.core.llm as llm
import src.core.prompts as prompts
import src.core.calorie_estimates as calorie_estimates
import src.core.food_search as food_search
# import src.core.supabase as supabase

from google.genai import types
from loguru import logger
from datetime import datetime
from pathlib import Path
from markdown_pdf import MarkdownPdf

from src.core.schemas import (
    FoodExtractionSchema,
    CalorieEstimationSchema,
)

gemini_client = llm.get_gemini_client()
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S-%f")

    
def _extract_food_items(text: str):
    model = env.GEMINI_MODEL
    system_instruction = prompts.load_instruction("agent-extract-food")
    prompt = (f"Ambil semua makanan dan minuman dari pesan pengguna berikut ini: {text}")
    response = gemini_client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_json_schema=FoodExtractionSchema.model_json_schema(),
            thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.LOW), 
        )
    )
    data = FoodExtractionSchema.model_validate(json.loads(response.text))
    return data.food_items

def _build_reference_data(reference_food: dict):
    lines = []
    for food_name, reference in reference_food.items():
        if reference:
            lines.append(f"{food_name}:")
        else:
            lines.append(f"{food_name}: Tidak ada referensi")
            continue

        for food in reference:
            lines.append(
                f"- id: {food['id']}, nama: {food['food_name']}, sumber: {food['source']},"
                f"kalori: {food['calories']}, protein: {food['protein_grams']},"
                f"karbohidrat: {food['carbohydrate_grams']}, lemak: {food['fat_grams']}"
            )

    return "\n".join(lines)

def _estimate_calories(text: str, reference_data: str):
    model = env.GEMINI_MODEL
    system_instruction = prompts.load_instruction("agent-calculate-calories")
    prompt = (f"Perkirakan kalori dari pesan pengguna berikut ini: {text}\n\nData referensi:\n{reference_data}")
    response = gemini_client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_json_schema=CalorieEstimationSchema.model_json_schema(),
            thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.LOW),
        )
    )
    return CalorieEstimationSchema.model_validate(json.loads(response.text))

def _check_estimation(estimation: CalorieEstimationSchema, search_results: dict):
    reference_ids = {result["id"] for results in search_results.values() for result in results}
    for item in estimation.food_estimations:
        item.reference_food_ids = [
            food_id for food_id in item.reference_food_ids if food_id in reference_ids
        ]
    return all(0 <= item.estimated_calories <= 3000 for item in estimation.food_estimations)

def calculate_calories_from_text(text: str):
    """Menghitung perkiraan kalori dari makanan atau minuman yang disebutkan pengguna."""
    logger.info(f"tools: calculate_calories_from_text - {text}")
    food_items = _extract_food_items(text)
    if not food_items:
        return "Tidak ada makanan atau minuman yang ditemukan."

    search_results = {
        name: food_search.search_similar_foods(name) for name in food_items
    }

    reference_data = _build_reference_data(search_results)
    estimation = _estimate_calories(text, reference_data)

    if not estimation.food_estimations or not _check_estimation(estimation, search_results):
        logger.warning("Estimasi kalori tidak valid.")
        return "Estimasi kalori tidak valid. Mohon perjelas makanan dan porsinya."

    total_calories = sum(
        item.estimated_calories for item in estimation.food_estimations
    )

    calorie_estimates.add(
        food_estimations=[item.model_dump() for item in estimation.food_estimations],
        assumptions=estimation.assumptions,
        total_calories=total_calories,
    )

    logger.success("Estimasi kalori berhasil dihitung.")
    lines = [
        f"{item.food_item}, {item.portion_grams} gram, {item.estimated_calories} kalori"
        + (" (perkiraan)" if not item.reference_food_ids else "")
        for item in estimation.food_estimations
    ]
    return "\n".join(lines) + f"\nTotal kalori: {total_calories}\nAsumsi: {estimation.assumptions}"

def get_motivation():
    """Memberikan 1 motivasi berguna untuk pengguna agar tetap semangat"""
    motivations = [
        "Setiap langkah kecil yang kamu ambil hari ini membawa kamu lebih dekat pada tujuanmu.",
        "Konsistensi lebih penting daripada kesempurnaan.",
        "Kamu tidak perlu sempurna, cukup terus melangkah.",
        "Percayalah pada proses dan nikmati setiap kemajuan yang kamu capai.",  
        "Kamu lebih kuat dari yang kamu kira.",
        "Jangan menyerah, kemajuanmu tetap berarti.",
        "Kamu sedang membangun kebiasaan yang akan membawa perubahan besar.",
        "Rayakan setiap kemajuan kecil yang kamu capai.",
        "Kamu mampu mencapai tujuanmu dengan langkah yang konsisten.",
        "Fokus pada kemajuan, bukan kesempurnaan.",
        "Kamu sudah sejauh ini, teruskan langkahmu.",
        "Setiap hari adalah kesempatan baru untuk menjadi versi terbaik dirimu.",
        "Mencatat makananmu hari ini sudah menjadi langkah yang baik.",
        "Perubahan tubuh terjadi bertahap, jangan menilai hasilnya dari satu hari saja.",
        "Pola makan yang baik membuat tubuhmu lebih sehat dan bertenaga."
    ]

    return random.choice(motivations)

if __name__ == "__main__":
    
    sentences = [
        # "white rice 3 spoons",
        "rendang sapi 100 buah",
        # "nasi putih 3 sendok",
        # "telur ayam rebus 2 butir",
        # "tempe goreng 2 buah",
        # "air putih 1 gelas",
        # "tahu goreng 1 buah",
        # "pisang 1 buah",
        # "ayam goreng sayap 3 potong",
        # "nasi goreng",
        # "sate ayam",
        # "soto ayam",
        # "bakso keju",
        # "mi goreng",
        # "gado-gado",
        # "lotek",
        # "rendang 2 potong",
        # "nasi uduk",
        # "bubur ayam setengah porsi",
        # "pisang goreng 2 buah",
        # "bakwan 1",
        # "mendoan",
        # "es teh manis 1 gelas",
        # "kopi susu",
        # "jus alpukat tanpa gula",
        # "susu uht",
        # "mcspicy",
        # "lasagna",
        # "pizza",
        # "hari ini aku makan nasi 3 sendok, ayam kukus dada 2 potong, dan tumis kangkung",
        # "aku makan nasi padang sama es teh manis",
        # "sepatu", 
        # "halo apa kabar?"
    ]

    failed_sentences = []

    for sentence in sentences:
        calorie_estimates.start()
        print(f"Kalimat: {sentence}")
        try:
            print(calculate_calories_from_text(sentence))
            print(json.dumps(calorie_estimates.collect(), indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"GAGAL: {sentence} - {e}")
            failed_sentences.append(sentence)
        print("-" * 40)
        time.sleep(30)

    if failed_sentences:
        print("Kalimat yang gagal diproses:")
        for sentence in failed_sentences:
            print(f"- {sentence}")
    