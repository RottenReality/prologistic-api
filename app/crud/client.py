from sqlalchemy.orm import Session
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate

def get(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()

def list(db: Session):
    return db.query(Client).all()

def create(db: Session, data: ClientCreate):
    obj = Client(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update(db: Session, db_obj: Client, data: ClientUpdate):
    for key, value in data.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, db_obj: Client):
    db.delete(db_obj)
    db.commit()
