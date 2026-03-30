from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import httpx

from app.database import get_db
from app.models import CartItem
from app.schemas import CartItemCreate, CartItemUpdate, CartItemResponse, CartResponse
from app.dependencies import get_current_user

router = APIRouter()

PRODUCT_SERVICE_URL = "http://product-service:8002/products"

async def get_product(product_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRODUCT_SERVICE_URL}/{product_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return response.json()

@router.post("/", response_model=CartItemResponse)
async def add_to_cart(
    item: CartItemCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = await get_product(item.product_id)
    
    cart_item = db.query(CartItem).filter(
        CartItem.user_email == current_user["email"],
        CartItem.product_id == item.product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = CartItem(
            user_email=current_user["email"],
            product_id=item.product_id,
            quantity=item.quantity,
            price=product["price"]
        )
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart_item)
    
    return CartItemResponse(
        id=cart_item.id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity,
        price=cart_item.price,
        subtotal=cart_item.price * cart_item.quantity
    )

@router.get("/", response_model=CartResponse)
def get_cart(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(CartItem).filter(CartItem.user_email == current_user["email"]).all()
    
    cart_items = []
    total = 0.0
    for item in items:
        subtotal = item.price * item.quantity
        total += subtotal
        cart_items.append(CartItemResponse(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price,
            subtotal=subtotal
        ))
    
    return CartResponse(items=cart_items, total=total)

@router.patch("/{item_id}", response_model=CartItemResponse)
def update_cart_item(
    item_id: int,
    update: CartItemUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_email == current_user["email"]
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item del carrito no encontrado")
    
    if update.quantity <= 0:
        db.delete(cart_item)
        db.commit()
        return CartItemResponse(
            id=cart_item.id,
            product_id=cart_item.product_id,
            quantity=0,
            price=cart_item.price,
            subtotal=0
        )  # devolvemos vacío para no romper frontend
    
    cart_item.quantity = update.quantity
    db.commit()
    db.refresh(cart_item)
    
    return CartItemResponse(
        id=cart_item.id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity,
        price=cart_item.price,
        subtotal=cart_item.price * cart_item.quantity
    )

@router.delete("/{item_id}")
def delete_cart_item(
    item_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_email == current_user["email"]
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item del carrito no encontrado")
    
    db.delete(cart_item)
    db.commit()
    return {"message": "Producto eliminado del carrito"}

# Nuevo endpoint útil para Order Service
@router.delete("/")
def clear_cart(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Vacía todo el carrito del usuario"""
    db.query(CartItem).filter(CartItem.user_email == current_user["email"]).delete()
    db.commit()
    return {"message": "Carrito vaciado correctamente"}