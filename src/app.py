# import os
# import supabase
# from dotenv import load_dotenv

# load_dotenv()

# supabase_client = supabase.create_client(
#     supabase_url=os.getenv("SUPABASE_URL"),
#     supabase_key=os.getenv("SUPABASE_KEY"),
# )

# # test

# result = supabase_client.table("food_nutrition_data").select("*").ilike("nama_makanan", "%nasi goreng%").execute()

# print("Koneksi berhasil")
# print(f"Jumalah data yang diambil: {len(result.data)}")