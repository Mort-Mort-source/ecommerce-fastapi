from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ShipmentResponse(BaseModel):
    id: int
    order_id: int
    user_email: str
    status: str
    tracking_number: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)