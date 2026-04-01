from fastapi import FastAPI
from pydantic import BaseModel
from services.moderation import moderate_product

app = FastAPI()

class ProductModerationRequest(BaseModel):
    name: str
    description: str
    category: str
    image_path: str | None = None

@app.get("/")
def home():
    return {"message": "Moderation service is running"}

@app.post("/moderate/product")
def moderate(request: ProductModerationRequest):
    result = moderate_product(
        name=request.name,
        description=request.description,
        category=request.category,
        image_path=request.image_path,
    )
    return result