import pandas as pd

from loguru import logger

INDONESIAN_CSV_PATH = "data/raw/indonesia/nutrition.csv"
INDIAN_CSV_PATH = "data/raw/india/Indian_Food_Nutrition_Processed.csv"
USDA_CSV_PATH = "data/raw/global/comprehensive_foods_usda.csv"
HEALTHY_CSV_PATH = "data/raw/global/healthy_foods_database.csv"
OUT_CSV_PATH = "data/processed/food_reference.csv"

USDA_SOURCE = "kaggle_global_food_nutrition_usda"
HEALTHY_SOURCE = "kaggle_global_food_nutrition_healthy"
 
def load_indonesian_foods(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return pd.DataFrame({
        "food_name": df["name"].str.strip().str.lower(),
        "origin": "indonesia",
        "calories": df["calories"],
        "protein_grams": df["proteins"],
        "carbohydrate_grams": df["carbohydrate"],
        "fat_grams": df["fat"],
        "unit": "per_100g",
        "source": "kaggle_indonesian_food_nutrition",
    })
 
 
def load_indian_foods(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return pd.DataFrame({
        "food_name": df["Dish Name"].str.strip().str.lower(),
        "origin": "india",
        "calories": df["Calories (kcal)"],
        "protein_grams": df["Protein (g)"],
        "carbohydrate_grams": df["Carbohydrates (g)"],
        "fat_grams": df["Fats (g)"],
        "unit": "per_100g",
        "source": "kaggle_indian_food_nutrition",
    })
 
 
def load_global_foods(path: str, source: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return pd.DataFrame({
        "food_name": df["food_name"].str.strip().str.lower(),
        "origin": "barat_internasional",
        "calories": df["calories"],
        "protein_grams": df["protein_g"],
        "carbohydrate_grams": df["carbs_g"],
        "fat_grams": df["fat_g"],
        "unit": "per_100g",
        "source": source,
    })
 
 
def run_merge_process():
    indonesian_foods = load_indonesian_foods(INDONESIAN_CSV_PATH)
    indian_foods = load_indian_foods(INDIAN_CSV_PATH)
    usda_foods = load_global_foods(USDA_CSV_PATH, USDA_SOURCE)
    healthy_foods = load_global_foods(HEALTHY_CSV_PATH, HEALTHY_SOURCE)
 
    merged_foods = pd.concat([indonesian_foods, indian_foods, usda_foods, healthy_foods], ignore_index=True)
 
    merged_foods = merged_foods.dropna(subset=["food_name", "calories"])
    merged_foods = merged_foods[merged_foods["calories"] >= 0]

    merged_foods = merged_foods.drop_duplicates(subset=["food_name", "origin", "source"])

    merged_foods.insert(0, "id", range(1, len(merged_foods) + 1))
 
    merged_foods.to_csv(OUT_CSV_PATH, index=False)
    logger.success(f"Selesai. Total {len(merged_foods)} baris tersimpan ke {OUT_CSV_PATH}")
    logger.info(merged_foods["origin"].value_counts())
 
 
if __name__ == "__main__":
    run_merge_process()