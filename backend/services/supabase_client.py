import os
from supabase import create_client, Client
from config import Config

url = Config.SUPABASE_URL or ""
key = Config.SUPABASE_KEY or ""

if not url or not key:
    print("Warning: Supabase credentials not found in environment.")

supabase: Client = create_client(url, key)
