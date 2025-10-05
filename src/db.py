import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase credentials from .env file
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Initialize the Supabase Client
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the .env file.")
    
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- CRUD Functions for Skincare Products ---

def add_product(name: str, product_type: str, skin_types: list[str], concerns: list[str]):
    """Adds a new product to the database."""
    try:
        data = {
            "name": name,
            "type": product_type,
            "skin_types": skin_types,
            "concerns": concerns
        }
        # The .execute() call ensures the insertion happens
        response = supabase.table("products").insert(data).execute()
        # Returns the newly inserted product data
        return response.data[0]
    except Exception as e:
        print(f"Error adding product: {e}")
        return None

def get_all_products():
    """Retrieves all products from the database."""
    try:
        # Select all columns (*) from the products table
        response = supabase.table("products").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error retrieving products: {e}")
        return []

def update_product(product_id: str, updates: dict):
    """Updates an existing product by its unique ID."""
    try:
        # The filter is on the 'id' (UUID) column
        response = supabase.table("products").update(updates).eq("id", product_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error updating product: {e}")
        return None

def delete_product(product_id: str):
    """Deletes a product by its unique ID."""
    try:
        # The filter is on the 'id' (UUID) column
        response = supabase.table("products").delete().eq("id", product_id).execute()
        # Returns True if at least one row was affected
        return len(response.data) > 0
    except Exception as e:
        print(f"Error deleting product: {e}")
        return False