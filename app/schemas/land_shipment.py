from pydantic import BaseModel, Field, validator
from datetime import date, datetime
import re

class LandShipmentBase(BaseModel):
    client_id: int
    product_id: int
    warehouse_id: int
    quantity: int
    register_date: date
    delivery_date: date
    price: float
    plate: str = Field(..., min_lenght=6, max_length=6)
    guide_number: str = Field(..., min_lenght=10, max_length=10)

    @validator("plate")
    def validate_plate(cls, value):
        pattern = r"^[A-Z]{3}[0-9]{3}$"
        if not re.match(pattern, value):
            raise ValueError("Invalid plate format. Expected format: ABC123")
        return value
    
class LandShipmentCreate(LandShipmentBase):
    pass

class LandShipmentUpdate(LandShipmentBase):
    pass

class LandShipmentResponse(LandShipmentBase):
    id: int
    discount: float
    final_price: float
    created_at: datetime

    class Config:
        from_attributes = True