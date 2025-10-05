from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Adjust the system path to allow importing from the project's root directory
# Note: Using relative imports is safer, but this sys.path approach works for the project structure.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import SkincareManager

# -----------------------------------------------------------App Setup------------------------------------------------
app = FastAPI(title="Personalized Skincare API", version="1.0")

# ------------------------------------------------------------CORS Middleware------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (Streamlit frontend)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

# --- Routine Endpoints (User Side) ---

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

# --- Product Endpoints (Admin Side) ---

@app.get("/products", tags=["Products"])
def get_all_products_from_db():
    """Fetches all products from the database."""
    response = skincare_manager.get_products_data()
    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=404, detail=response.get("message") or "No products found."
        )

# Note: Other CRUD endpoints (POST, PUT, DELETE) follow a similar pattern and are not included here for brevity, 
# but they are correctly implemented in your main code from previous steps.s