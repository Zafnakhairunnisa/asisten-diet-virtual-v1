from pydantic import BaseModel, Field
from typing import Literal, Optional

# class EvaluateUserIntentionSchema(BaseModel):
#     intention: Literal["calorie_estimation", "diet_guide", "motivation", "general_chat"] = Field(..., description="pilihan salah satu intention yang dibutuhkan pengguna")

class UserProfileSchema(BaseModel):
    age: int = Field(..., description="usia pengguna")
    gender: Literal["male", "female"] = Field(..., description="jenis kelamin pengguna")
    height: float = Field(..., description="tinggi badan pengguna dalam sentimeter")
    activity_level: Literal["sedentary", "light", "moderate", "active"] =  Field(..., description="tingkat aktivitas fisik harian pengguna")
    target_weight: Optional[float] = Field(None, description="target berat badan pengguna dalam kilogram")
    
class MealTypeSummarySchema(BaseModel): # ringkasan jenis makanan
    meal_type: Literal["breakfast", "lunch", "dinner", "snack"] = Field(..., description="jenis waktu makan")
    calories_avg: float = Field(..., description="rata-rata kalori yang dikonsumsi pada jenis waktu makan tersebut")
    fat_grams_avg: float = Field(..., description="rata-rata jumlah lemak yang dikonsumsi pada jenis waktu makan tersebut dalam gram")
    protein_grams_avg: float = Field(..., description="rata-rata jumlah protein yang dikonsumsi pada jenis waktu makan tersebut dalam gram")
    carbohydrate_grams_avg: float = Field(..., description="rata-rata jumlah karbohidrat yang dikonsumsi pada jenis waktu makan tersebut dalam gram")
    total_logged_meals: int = Field(..., description="jumlah total makanan yang dicatat pada jenis waktu makan tersebut")

class FoodExtractionSchema(BaseModel): # ekstraksi nama makanan 
    food_items: list[str] = Field(..., description="daftar nama makanan dan minuman yang disebutkan pengguna, tanpa porsi, (misalnya '2 tusuk sate ayam' menjadi 'sate ayam'). Isi list kosong [] jika tidak ada makanan atau minuman.")

class FoodItemEstimationSchema(BaseModel): # estimasi kalori per item makanan
    food_item: str = Field(..., description="nama makanan yang dikonsumsi")
    portion_grams: float = Field(..., description="perkiraan porsi makanan yang dikonsumsi dalam gram")
    estimated_calories: float = Field(..., description="jumlah kalori dalam makanan yang dikonsumsi untuk porsi portion_grams bukan per 100 gram")
    fat_grams: float = Field(..., description="jumlah lemak dalam makanan yang dikonsumsi dalam gram untuk porsi portion_grams bukan per 100 gram")
    protein_grams: float = Field(..., description="jumlah protein dalam makanan yang dikonsumsi dalam gram untuk porsi portion_grams bukan per 100 gram")
    carbohydrate_grams: float = Field(..., description="jumlah karbohidrat dalam makanan yang dikonsumsi dalam gram untuk porsi portion_grams bukan per 100 gram")
    reference_food_ids: list[int] = Field(..., description="ID makanan referensi yang digunakan untuk estimasi kalori, lemak, protein, dan karbohidrat. Minuman campuran berisi id semua bahannya. Jika tidak ada referensi, maka isi list kosong [].")


class CalorieEstimationSchema(BaseModel): # estimasi kalori
    food_estimations: list[FoodItemEstimationSchema] = Field(..., description="daftar makanan yang dikonsumsi beserta estimasi kalori, lemak, protein, dan karbohidratnya")
    assumptions: str = Field(..., description="asumsi yang digunakan untuk estimasi kalori, lemak, protein, dan karbohidrat, termasuk asumsi porsi dan makanan mana yang angkanya perkiraan")

# class MenuRecommendationSchema(BaseModel): # rekomendasi menu
#     menu_name: str = Field(..., description="nama menu yang direkomendasikan")
#     ingredients: list[str] = Field(..., description="daftar bahan-bahan yang dibutuhkan untuk menu tersebut")
#     estimated_calories: float = Field(..., description="jumlah kalori yang diperkirakan dalam menu tersebut")
#     fat_grams: float = Field(..., description="jumlah lemak dalam menu tersebut dalam gram")
#     protein_grams: float = Field(..., description="jumlah protein dalam menu tersebut dalam gram")
#     carbohydrate_grams: float = Field(..., description="jumlah karbohidrat dalam menu tersebut dalam gram")
#     recipe_instructions: str = Field(..., description="instruksi cara memasak menu tersebut")

class DietReportSchema(BaseModel): # laporan diet
    username: str = Field(..., description="nama pengguna")
    start_date: str = Field(..., description="tanggal mulai diet dalam format YYYY-MM-DD")
    end_date: str = Field(..., description="tanggal akhir diet dalam format YYYY-MM-DD")
    daily_calorie_intake: float = Field(..., description="rata-rata asupan kalori harian selama periode diet")
    weight_progress: Optional[float] = Field(None, description="perubahan berat badan pengguna selama periode diet, dalam kilogram, jika tersedia")
    consistency_log: str = Field(..., description="catatan konsistensi diet selama periode diet, misalnya 'baik', 'cukup', 'kurang'")
    summary_by_mealtime: list[MealTypeSummarySchema] = Field(..., description="ringkasan asupan makanan berdasarkan jenis waktu makan selama periode diet")
    markdown_content: str = Field(..., description="seluruh laporan diet dalam format markdown, termasuk ringkasan dan rekomendasi")
