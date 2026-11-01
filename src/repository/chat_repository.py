import src.core.supabase as supabase

from typing import Literal, Optional
from loguru import logger
from datetime import datetime, timedelta, timezone

class ChatRepository:
    def __init__(self):
        self.supabase = supabase.get_supabase_client()

    # buat simpan pesan ke tabel chat histories
    def save_message(self, user_id:int, role: Literal["user", "model"], message_text:str):
        self.supabase.table("chat_histories").insert({
            "user_id": user_id,
            "role": role,
            "message_text": message_text
        }).execute()

    # ambil riwayat chat berdasarkan user_id
    def load_history_by_user_id(self, user_id:int):
        result = (
            self.supabase.table("chat_histories")
            .select("role", "message_text")
            .eq("user_id", user_id)
            # ambil data dari created at, dari yang paling lama ke yang terbaru -> ascending
            .order("created_at", desc=False)
            .execute()
        )

        return result

    # daftarin user ama tambahin anti duplikat, kalo udh ada berhenti di situ klo blm insert datany
    def save_user(self, user_id:int, user_name:str, chat_id:int):
        exist_user = (
            self.supabase.table("chat_users")
            .select("user_id")
            .eq("user_id", user_id)
            .execute()
        )

        if len(exist_user.data) > 0:
            logger.debug(f"User {user_id} already exists in the database.")
            return

        result = self.supabase.table("chat_users").insert({
            "user_id": user_id,
            "username": user_name,
            "chat_id": chat_id
        }).execute()

        return result

    def save_user_profile(self, user_id:int, age:int, gender:str, height:float, activity_level:str, target_weight:Optional[float] = None):

        # cek apakah user udh ada di tabel user_profiles
        exist_user_profile = (
            self.supabase.table("user_profiles")
            .select("user_id")
            .eq("user_id", user_id)
            .execute()
        )

        if len(exist_user_profile.data) > 0:
            logger.debug(f"User profile for {user_id} already exists in the database.")
        
            return self.supabase.table("user_profiles").update({
                "age": age,
                "gender": gender,
                "height": height,
                "activity_level": activity_level,
                "target_weight": target_weight
            }).eq("user_id", user_id).execute()

        result = self.supabase.table("user_profiles").insert({
            "user_id": user_id,
            "age": age,
            "gender": gender,
            "height": height,
            "activity_level": activity_level,
            "target_weight": target_weight
        }).execute()

        return result

    def get_user_profile_by_user_id(self, user_id:int):

        result = (
            self.supabase.table("user_profiles")
            .select("age", "gender", "height", "activity_level", "target_weight")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )

        return result
        
    def save_weight(self, user_id:int, weight:float):

        result = self.supabase.table("weight_logs").insert({
            "user_id": user_id,
            "weight": weight
        }).execute()

        return result

    def get_latest_weight_by_user_id(self, user_id:int):
        result = (
            self.supabase.table("weight_logs")
            .select("weight")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )

        return result

    def save_food_log(self, user_id:int, meal_type: Literal["breakfast", "lunch", "dinner", "snack"], food_estimations: list[dict]):
        if not food_estimations:
            return

        rows = [
            {
                "user_id": user_id,
                "meal_type": meal_type,
                **food_estimation
            }
            for food_estimation in food_estimations
        ]

        result = self.supabase.table("food_logs").insert(rows).execute()

        return result

    def has_food_log_today(self, user_id:int, meal_type: Literal["breakfast", "lunch", "dinner", "snack"]):

        wib = timezone(timedelta(hours=7))
        start_of_day = datetime.now(wib).replace(hour=0, minute=0, second=0, microsecond=0)

        result = (
            self.supabase.table("food_logs")
            .select("id")
            .eq("user_id", user_id)
            .eq("meal_type", meal_type)
            .gte("created_at", start_of_day.isoformat())
            .limit(1)
            .execute()
        )

        return len(result.data) > 0


if __name__ == "__main__":
    chat_repository = ChatRepository()
    chat_repository.save_user(user_id=12345, user_name="testuser", chat_id=67890)
    chat_repository.save_user_profile(user_id=12345, age=25, height=175, gender="male", activity_level="light", target_weight=65)
    chat_repository.save_user_profile(user_id=12345, age=26, height=175, gender="male", activity_level="light")
    print(f"user profile dari user_id 12345: {chat_repository.get_user_profile_by_user_id(user_id=12345).data}")
    chat_repository.save_weight(user_id=12345, weight=70.5)
    chat_repository.save_weight(user_id=12345, weight=69.0)
    print(f"berat terbaru dari user_id 12345: {chat_repository.get_latest_weight_by_user_id(user_id=12345).data}")
    print(f"has food log today (breakfast) dari user_id 12345: {chat_repository.has_food_log_today(user_id=12345, meal_type='breakfast')}")

    chat_repository.save_food_log(
        user_id=12345,
        meal_type="breakfast",
        food_estimations=[]
    )
    print(f"udah ada food log hari ini dari user_id 12345: {chat_repository.has_food_log_today(user_id=12345, meal_type='breakfast')}")

    chat_repository.save_food_log(
        user_id=12345,
        meal_type="breakfast",
        food_estimations=[
            {
                "food_item": "Egg",
                "estimated_calories": 70,
                "protein_grams": 6,
                "carbohydrate_grams": 1,
                "fat_grams": 5,
                "portion_grams": 50,
                "reference_food_ids": []
            },
            {
                "food_item": "Toast",
                "estimated_calories": 80,
                "protein_grams": 3,
                "carbohydrate_grams": 15,
                "fat_grams": 1,
                "portion_grams": 40,
                "reference_food_ids": [1347, 391]
            }
        ]
    )
    print(f"udah ada food log hari ini dari user_id 12345: {chat_repository.has_food_log_today(user_id=12345, meal_type='breakfast')}")


    