from pydantic import BaseModel, ConfigDict
from typing import Optional

class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    image_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)