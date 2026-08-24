from pydantic import BaseModel, Field
from typing import Literal, Optional

class EvaluateUserIntentionSchema(BaseModel):
    intention: Literal["calorie_estimation", "menu_recommendation", "diet_guide", "motivation", "general_chat"] = Field(..., description="pilihan salah satu intention yang dibutuhkan pengguna")

class UserProfileSchema(BaseModel):
    age: int = Field(..., description="usia pengguna")
    gender: Literal["male", "female"] = Field(..., description="jenis kelamin pengguna")
    height: float = Field(..., description="tinggi badan pengguna dalam sentimeter")
    target_weight: Optional[float] = Field(None, description="target berat badan pengguna dalam kilogram")
    
class MealTypeSummarySchema(BaseModel): # ringkasan jenis makanan
    meal_type: Literal["breakfast", "lunch", "dinner", "snack"] = Field(..., description="jenis waktu makan")
    calories_avg: float = Field(..., description="rata-rata kalori yang dikonsumsi pada jenis waktu makan tersebut")
    fat_grams_avg: float = Field(..., description="rata-rata jumlah lemak yang dikonsumsi pada jenis waktu makan tersebut dalam gram")
    protein_grams_avg: float = Field(..., description="rata-rata jumlah protein yang dikonsumsi pada jenis waktu makan tersebut dalam gram")
    carbohydrate_grams_avg: float = Field(..., description="rata-rata jumlah karbohidrat yang dikonsumsi pada jenis waktu makan tersebut dalam gram")
    total_logged_meals: int = Field(..., description="jumlah total makanan yang dicatat pada jenis waktu makan tersebut")


class CalorieEstimationSchema(BaseModel): # estimasi kalori
    food_item: str = Field(..., description="nama makanan yang dikonsumsi")
    estimated_calories: float = Field(..., description="jumlah kalori dalam makanan yang dikonsumsi")
    fat_grams: float = Field(..., description="jumlah lemak dalam makanan yang dikonsumsi dalam gram")
    protein_grams: float = Field(..., description="jumlah protein dalam makanan yang dikonsumsi dalam gram")
    carbohydrate_grams: float = Field(..., description="jumlah karbohidrat dalam makanan yang dikonsumsi dalam gram")

class MenuRecommendationSchema(BaseModel): # rekomendasi menu
    menu_name: str = Field(..., description="nama menu yang direkomendasikan")
    ingredients: list[str] = Field(..., description="daftar bahan-bahan yang dibutuhkan untuk menu tersebut")
    estimated_calories: float = Field(..., description="jumlah kalori yang diperkirakan dalam menu tersebut")
    fat_grams: float = Field(..., description="jumlah lemak dalam menu tersebut dalam gram")
    protein_grams: float = Field(..., description="jumlah protein dalam menu tersebut dalam gram")
    carbohydrate_grams: float = Field(..., description="jumlah karbohidrat dalam menu tersebut dalam gram")
    recipe_instructions: str = Field(..., description="instruksi cara memasak menu tersebut")

class DietReportSchema(BaseModel): # laporan diet
    username: str = Field(..., description="nama pengguna")
    start_date: str = Field(..., description="tanggal mulai diet dalam format YYYY-MM-DD")
    end_date: str = Field(..., description="tanggal akhir diet dalam format YYYY-MM-DD")
    daily_calorie_intake: float = Field(..., description="rata-rata asupan kalori harian selama periode diet")
    weight_progress: float = Field(..., description="perubahan berat badan selama periode diet dalam kilogram")
    consistency_log: str = Field(..., description="catatan konsistensi diet selama periode diet, misalnya 'baik', 'cukup', 'kurang'")
    summary_by_mealtime: list[MealTypeSummarySchema] = Field(..., description="ringkasan asupan makanan berdasarkan jenis waktu makan selama periode diet")
    markdown_content: str = Field(..., description="seluruh laporan diet dalam format markdown, termasuk ringkasan dan rekomendasi")
