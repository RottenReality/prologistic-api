from pydantic import BaseModel, EmailStr
from datetime import datetime

class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone: str

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True