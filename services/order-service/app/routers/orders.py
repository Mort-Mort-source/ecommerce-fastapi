from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import httpx
from typing import List

from app.database import get_db
from app.models import Order, OrderItem
from app.schemas import OrderResponse
from app.dependencies import get_current_user

router = APIRouter()

CART_SERVICE_URL = "http://cart-service:8003/cart"
SHIPMENT_SERVICE_URL = "http://shipment-service:8005/shipments"


@router.post("/", response_model=OrderResponse)
async def create_order(
    authorization: str = Header(None),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"🔹 Creando orden para usuario: {current_user['email']}")

    if not authorization or not authorization.startswith("Bearer "):
        print("❌ Token no recibido o mal formado")
        raise HTTPException(status_code=401, detail="Token de autorización requerido")

    token = authorization.split(" ")[1]
    print(f"🔹 Token extraído correctamente")

    # 1. Obtener el carrito (intentamos con y sin trailing slash + follow redirects)
    cart_data = None
    urls_to_try = [CART_SERVICE_URL, CART_SERVICE_URL.rstrip('/') + "/"]

    for url in urls_to_try:
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                cart_response = await client.get(
                    url,
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                print(f"🔹 Probando {url} → Status: {cart_response.status_code}")

                if cart_response.status_code == 200:
                    cart_data = cart_response.json()
                    print(f"✅ Carrito obtenido correctamente. Items: {len(cart_data.get('items', []))}")
                    break
        except Exception as e:
            print(f"❌ Error al conectar a {url}: {e}")

    if not cart_data:
        raise HTTPException(status_code=400, detail="No se pudo obtener el carrito del usuario")

    if not cart_data.get("items"):
        raise HTTPException(status_code=400, detail="El carrito está vacío")

    # 2. Crear la orden
    order = Order(user_email=current_user["email"], total=cart_data["total"])
    db.add(order)
    db.commit()
    db.refresh(order)

    # 3. Guardar los items de la orden
    for item in cart_data["items"]:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            price=item["price"]
        )
        db.add(order_item)
    db.commit()

    # 4. Vaciar el carrito
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            await client.delete(
                CART_SERVICE_URL,
                headers={"Authorization": f"Bearer {token}"}
            )
        print("✅ Carrito vaciado correctamente")
    except Exception as e:
        print(f"⚠️ No se pudo vaciar el carrito: {e}")

    # 5. Crear envío automáticamente
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            shipment_response = await client.post(
                SHIPMENT_SERVICE_URL,
                json={"order_id": order.id, "user_email": current_user["email"]},
                headers={"Content-Type": "application/json"}
            )
            print(f"📦 Shipment Service respondió con código: {shipment_response.status_code}")
            if shipment_response.status_code in (200, 201):
                print("✅ Envío creado correctamente")
            else:
                print(f"⚠️ Shipment Service error: {shipment_response.text}")
    except Exception as e:
        print(f"⚠️ Error creando envío: {e}")
        # No fallamos la orden si el envío falla

    # 6. Preparar respuesta
    items_response = [
        {
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": item.price,
            "subtotal": item.price * item.quantity
        } for item in order.items
    ]

    print(f"✅ Orden #{order.id} creada exitosamente")
    return OrderResponse(
        id=order.id,
        user_email=order.user_email,
        total=order.total,
        status=order.status,
        created_at=order.created_at,
        items=items_response
    )


@router.get("/", response_model=List[OrderResponse])
def get_my_orders(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).filter(Order.user_email == current_user["email"]).all()
    
    # Convertimos manualmente para incluir 'subtotal'
    result = []
    for order in orders:
        items_response = []
        for item in order.items:
            subtotal = item.price * item.quantity
            items_response.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.price,
                "subtotal": subtotal
            })
        
        result.append(OrderResponse(
            id=order.id,
            user_email=order.user_email,
            total=order.total,
            status=order.status,
            created_at=order.created_at,
            items=items_response
        ))
    
    return result