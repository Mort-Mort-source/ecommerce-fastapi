from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False, unique=True)   # una orden = un envío
    user_email = Column(String, index=True, nullable=False)
    status = Column(String, default="pendiente")              # pendiente → en camino → entregado
    tracking_number = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)