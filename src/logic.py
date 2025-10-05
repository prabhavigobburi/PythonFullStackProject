import random
# Import database functions from the local src/db.py file
from src.db import add_product, get_all_products, update_product, delete_product

class SkincareManager:
    """
    Manages the business logic for a personalized skincare routine builder.
    Acts as the bridge between the frontend/API and the database operations.
    """

    def __init__(self):
        # The database functions are imported directly, so no class instance is needed here.
        pass
    
    # --- PRODUCT MANAGEMENT (Admin Logic) ---

    def add_new_product(self, name: str, product_type: str, skin_types: list[str], concerns: list[str]):
        """Validates and adds a new product to the database."""
        if not all([name, product_type, skin_types, concerns]):
            return {"Success": False, "message": "All product details are required."}
        
        product = add_product(name, product_type, skin_types, concerns)
        
        if product:
            return {"Success": True, "message": "Product added successfully.", "data": product}
        else:
            return {"Success": False, "message": "Failed to add product."}
    
    def get_products_data(self):
        """Retrieves all products from the database for display or filtering."""
        products = get_all_products()
        if not products:
            return {"Success": False, "message": "No products found."}
        
        return {"Success": True, "data": products}
    
    def modify_product(self, product_id: str, updates: dict):
        """Updates an existing product's details."""
        if not product_id or not updates:
            return {"Success": False, "message": "Product ID and update data are required."}
            
        product = update_product(product_id, updates)
        
        if product:
            return {"Success": True, "message": "Product updated successfully.", "data": product}
        else:
            return {"Success": False, "message": "Failed to update product."}
            
    def remove_product(self, product_id: str):
        """Deletes a product from the database."""
        if not product_id:
            return {"Success": False, "message": "Product ID is required for deletion."}
            
        success = delete_product(product_id)
        
        if success:
            return {"Success": True, "message": "Product deleted successfully."}
        else:
            return {"Success": False, "message": "Failed to delete product."}

    # --- ROUTINE GENERATION (User Logic) ---

    def generate_routine(self, skin_type: str, concern: str):
        """
        Generates a personalized morning and night routine based on user input.
        """
        products_result = self.get_products_data()
        if not products_result.get("Success"):
            return products_result 

        all_products = products_result["data"]
        
        # Filter products: matches the concern AND matches either the specific skin type OR 'All'
        relevant_products = [
            p for p in all_products
            if concern.lower() in [c.lower() for c in p.get('concerns', [])]
            and (skin_type.lower() in [s.lower() for s in p.get('skin_types', [])] or 'all' in [s.lower() for s in p.get('skin_types', [])])
        ]
        
        if not relevant_products:
            return {"Success": False, "message": "No products found for this combination. Please try a different selection."}

        # Categorize products by type
        cleansers = [p for p in relevant_products if p['type'].lower() == 'cleanser']
        toners = [p for p in relevant_products if p['type'].lower() == 'toner']
        serums = [p for p in relevant_products if p['type'].lower() == 'serum']
        moisturizers = [p for p in relevant_products if p['type'].lower() == 'moisturizer']
        sunscreens = [p for p in relevant_products if p['type'].lower() == 'sunscreen']
        night_treatments = [p for p in relevant_products if p['type'].lower() in ['night treatment', 'treatment']]
        
        # --- Build Routines ---
        morning_routine = []
        if cleansers:
            morning_routine.append(random.choice(cleansers))
        if serums:
            morning_routine.append(random.choice(serums))
        if moisturizers:
            morning_routine.append(random.choice(moisturizers))
        if sunscreens:
            morning_routine.append(random.choice(sunscreens))

        night_routine = []
        if cleansers:
            night_routine.append(random.choice(cleansers))
        if toners: # Toners are optional
            night_routine.append(random.choice(toners))
        if night_treatments:
            night_routine.append(random.choice(night_treatments))
        if moisturizers:
            night_routine.append(random.choice(moisturizers))

        return {
            "Success": True,
            "routine": {
                "morning": morning_routine,
                "night": night_routine
            }
        }