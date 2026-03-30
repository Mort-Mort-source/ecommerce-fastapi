from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Product
from app.schemas import Product as ProductSchema

router = APIRouter()

def seed_sample_products(db: Session):
    if db.query(Product).first() is not None:
        return
    sample_products = [
        Product(name="Laptop HP Pavilion", description="Laptop gaming 16GB RAM / 512GB SSD", price=899.99, stock=15, image_url="https://picsum.photos/id/20/300/300"),
        Product(name="iPhone 15 Pro", description="128GB - Color negro titanio", price=999.99, stock=8, image_url="https://picsum.photos/id/29/300/300"),
        Product(name="Audífonos Sony WH-1000XM5", description="Noise cancelling premium", price=149.99, stock=30, image_url="https://picsum.photos/id/30/300/300"),
        Product(name="Mouse Logitech MX Master 3S", description="Inalámbrico, ergonómico", price=29.99, stock=50, image_url="https://picsum.photos/id/201/300/300"),
        Product(name="Teclado Mecánico Keychron K2", description="RGB - Switches Red", price=79.99, stock=20, image_url="https://picsum.photos/id/180/300/300"),
    ]
    db.add_all(sample_products)
    db.commit()
    print("✅ Productos de ejemplo creados")

@router.get("/", response_model=List[ProductSchema])
def get_all_products(db: Session = Depends(get_db)):
    seed_sample_products(db)
    return db.query(Product).all()

@router.get("/{product_id}", response_model=ProductSchema)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product