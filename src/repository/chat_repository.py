import src.core.supabase as supabase

from typing import Literal
from loguru import logger

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
            return  # berhenti

        result = self.supabase.table("chat_users").insert({
            "user_id": user_id,
            "username": user_name,
            "chat_id": chat_id
        }).execute()

        return result

    
