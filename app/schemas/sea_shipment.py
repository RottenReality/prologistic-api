from pydantic import BaseModel, Field, validator
from datetime import date, datetime
import re

class SeaShipmentBase(BaseModel):
    client_id: int
    product_id: int
    port_id: int
    quantity: int
    register_date: date
    delivery_date: date
    price: float
    fleet_number: str = Field(..., min_length=8, max_length=8)
    guide_number: str = Field(..., min_length=10, max_length=10)

    @validator("fleet_number")
    def validate_fleet(cls, value):
        pattern = r"^[A-Z]{3}[0-9]{4}[A-Z]$"
        if not re.match(pattern, value):
            raise ValueError("Invalid fleet number. Expected ABC1234D")
        return value

class SeaShipmentCreate(SeaShipmentBase):
    pass

class SeaShipmentUpdate(SeaShipmentBase):
    pass

class SeaShipmentResponse(SeaShipmentBase):
    id: int
    discount: float
    final_price: float
    created_at: datetime

    class Config:
        from_attributes = True
