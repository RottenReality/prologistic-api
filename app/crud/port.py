from sqlalchemy.orm import Session
from app.models.port import Port
from app.schemas.port import PortCreate, PortUpdate

def get(db: Session, port_id: int):
    return db.query(Port).filter(Port.id == port_id).first()

def list(db: Session):
    return db.query(Port).all()

def create(db: Session, data: PortCreate):
    obj = Port(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update(db: Session, db_obj: Port, data: PortUpdate):
    for key, value in data.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, db_obj: Port):
    db.delete(db_obj)
    db.commit()
