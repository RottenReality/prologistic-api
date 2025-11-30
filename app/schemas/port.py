from pydantic import BaseModel
from datetime import datetime

class PortBase(BaseModel):
    name: str
    location: str

class PortCreate(PortBase):
    pass

class PortUpdate(PortBase):
    pass

class PortResponse(PortBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True