import random
from src.db import add_product, get_all_products, update_product, delete_product

class SkincareManager:
    """
    Manages the business logic for a personalized skincare routine builder.
    Acts as the bridge between the frontend/API and database operations.
    """

    def __init__(self):
        # We don't need a class instance for the database since the functions are imported directly.
        pass
    
    # --- PRODUCT LOGIC (Admin Side) ---

    def add_new_product(self, name: str, product_type: str, skin_types: list[str], concerns: list[str]):
        """
        Validates and adds a new product to the database.
        """
        if not all([name, product_type, skin_types, concerns]):
            return {"Success": False, "message": "All product details are required."}
        
        # Call the database function to add the product
        product = add_product(name, product_type, skin_types, concerns)
        
        if product:
            return {"Success": True, "message": "Product added successfully.", "data": product}
        else:
            return {"Success": False, "message": "Failed to add product."}
    
    def get_products_data(self):
        """
        Retrieves all products from the database for display or filtering.
        """
        products = get_all_products()
        if not products:
            return {"Success": False, "message": "No products found."}
        
        return {"Success": True, "data": products}
    
    def modify_product(self, product_id: str, updates: dict):
        """
        Updates an existing product's details.
        """
        if not product_id or not updates:
            return {"Success": False, "message": "Product ID and update data are required."}
            
        product = update_product(product_id, updates)
        
        if product:
            return {"Success": True, "message": "Product updated successfully.", "data": product}
        else:
            return {"Success": False, "message": "Failed to update product."}
            
    def remove_product(self, product_id: str):
        """
        Deletes a product from the database.
        """
        if not product_id:
            return {"Success": False, "message": "Product ID is required for deletion."}
            
        success = delete_product(product_id)
        
        if success:
            return {"Success": True, "message": "Product deleted successfully."}
        else:
            return {"Success": False, "message": "Failed to delete product."}

    # --- ROUTINE BUILDING LOGIC (User Side) ---

    def generate_routine(self, skin_type: str, concern: str):
        """
        Generates a personalized morning and night routine based on user input.
        """
        # Get all products from the database
        products_result = self.get_products_data()
        if not products_result.get("Success"):
            return products_result # Returns the "no products found" message

        all_products = products_result["data"]
        
        # Filter products based on user's skin type and concern
        relevant_products = [
            p for p in all_products
            if skin_type.lower() in [s.lower() for s in p.get('skin_types', [])]
            and concern.lower() in [c.lower() for c in p.get('concerns', [])]
        ]
        
        if not relevant_products:
            return {"Success": False, "message": "No products found for your selection. Try a different combination."}

        # Categorize products by type
        cleansers = [p for p in relevant_products if p['type'].lower() == 'cleanser']
        toners = [p for p in relevant_products if p['type'].lower() == 'toner']
        serums = [p for p in relevant_products if p['type'].lower() == 'serum']
        moisturizers = [p for p in relevant_products if p['type'].lower() == 'moisturizer']
        sunscreens = [p for p in relevant_products if p['type'].lower() == 'sunscreen']
        night_treatments = [p for p in relevant_products if p['type'].lower() == 'night treatment']

        # Build morning routine
        morning_routine = []
        if cleansers:
            morning_routine.append(random.choice(cleansers))
        if serums:
            morning_routine.append(random.choice(serums))
        if moisturizers:
            morning_routine.append(random.choice(moisturizers))
        if sunscreens:
            morning_routine.append(random.choice(sunscreens))

        # Build night routine
        night_routine = []
        if cleansers:
            night_routine.append(random.choice(cleansers))
        if toners:
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
        
