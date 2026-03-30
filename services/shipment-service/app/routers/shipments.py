from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import random
import string
from typing import List

from app.database import get_db
from app.models import Shipment
from app.schemas import ShipmentResponse
from app.dependencies import get_current_user

router = APIRouter()

def generate_tracking_number() -> str:
    return "TRK" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


@router.post("/", response_model=ShipmentResponse, status_code=201)
def create_shipment(payload: dict, db: Session = Depends(get_db)):
    order_id = payload.get("order_id")
    user_email = payload.get("user_email")

    if not order_id or not user_email:
        print("❌ Shipment: Faltan datos en payload")
        raise HTTPException(status_code=400, detail="order_id y user_email requeridos")

    # Evitar duplicados
    existing = db.query(Shipment).filter(Shipment.order_id == order_id).first()
    if existing:
        return existing

    shipment = Shipment(
        order_id=order_id,
        user_email=user_email,
        status="pendiente",
        tracking_number=generate_tracking_number()
    )

    db.add(shipment)
    db.commit()
    db.refresh(shipment)

    print(f"✅ Shipment creado | Orden #{order_id} | Tracking: {shipment.tracking_number}")
    return shipment


@router.get("/", response_model=List[ShipmentResponse])
def get_my_shipments(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    shipments = db.query(Shipment).filter(Shipment.user_email == current_user["email"]).all()
    return shipments