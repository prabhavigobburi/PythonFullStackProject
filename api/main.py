from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Adjust the system path to allow importing from the project's root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import SkincareManager

# -----------------------------------------------------------App Setup------------------------------------------------
app = FastAPI(title="Personalized Skincare API", version="1.0")

# ------------------------------------------------------------Allow Frontend(Streamlit/React) to call the API------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Creating a SkincareManager Instance (business logic)
skincare_manager = SkincareManager()

# ------Data Models ------

class RoutineRequest(BaseModel):
    """Schema for a user's routine generation request."""
    skin_type: str
    concern: str

class ProductCreate(BaseModel):
    """Schema for creating a new product."""
    name: str
    product_type: str
    skin_types: list[str]
    concerns: list[str]

class ProductUpdate(BaseModel):
    """Schema for updating an existing product."""
    updates: dict

# -----------------------------------------------------------API Endpoints------------------------------------------------

@app.get("/", tags=["Home"])
def home():
    """Check if the API is running."""
    return {"message": "Personalized Skincare API is running."}

# ---------------------------------------------------------- Routine Endpoints (User Side) ------------------------------------------------

@app.post("/routine", tags=["Routine"])
def generate_skincare_routine(request: RoutineRequest):
    """
    Generates a personalized morning and night skincare routine.
    """
    response = skincare_manager.generate_routine(request.skin_type, request.concern)
    
    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=404,
            detail=response.get("message") or "Could not generate routine."
        )

# ---------------------------------------------------------- Product Endpoints (Admin Side) ------------------------------------------------

@app.post("/products", tags=["Products"])
def create_product(product: ProductCreate):
    """
    Adds a new product to the database.
    """
    response = skincare_manager.add_new_product(
        name=product.name,
        product_type=product.product_type,
        skin_types=product.skin_types,
        concerns=product.concerns
    )
    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=400, detail=response.get("message") or "Failed to add product."
        )

@app.get("/products", tags=["Products"])
def get_all_products_from_db():
    """
    Fetches all products from the database.
    """
    response = skincare_manager.get_products_data()
    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=404, detail=response.get("message") or "No products found."
        )

@app.put("/products/{product_id}", tags=["Products"])
def update_product_details(product_id: str, product_updates: ProductUpdate):
    """
    Updates an existing product's details.
    """
    response = skincare_manager.modify_product(product_id, product_updates.updates)
    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=404, detail=response.get("message") or "Product not found or failed to update."
        )

@app.delete("/products/{product_id}", tags=["Products"])
def delete_product_by_id(product_id: str):
    """
    Deletes a product from the database.
    """
    response = skincare_manager.remove_product(product_id)
    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=404, detail=response.get("message") or "Product not found or failed to delete."
        )