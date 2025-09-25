import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase credentials from .env file
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def add_product(name: str, product_type: str, skin_types: list[str], concerns: list[str]):
    try:
        data = {
            "name": name,
            "type": product_type,
            "skin_types": skin_types,
            "concerns": concerns
        }
        response = supabase.table("products").insert(data).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error adding product: {e}")
        return None

def get_all_products():
    try:
        response = supabase.table("products").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error retrieving products: {e}")
        return []

def update_product(product_name: str, updates: dict):
    try:
        # Change the filter from "id" to "name"
        response = supabase.table("products").update(updates).eq("name", product_name).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error updating product: {e}")
        return None

def delete_product(product_name: str):
    try:
        # Change the filter from "id" to "name"
        response = supabase.table("products").delete().eq("name", product_name).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error deleting product: {e}")
        return False

