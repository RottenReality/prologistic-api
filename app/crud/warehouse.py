from sqlalchemy.orm import Session
from app.models.warehouse import Warehouse
from app.schemas.warehouse import WarehouseCreate, WarehouseUpdate

def get(db: Session, warehouse_id: int):
    return db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()

def list(db: Session):
    return db.query(Warehouse).all()

def create(db: Session, data: WarehouseCreate):
    obj = Warehouse(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update(db: Session, db_obj: Warehouse, data: WarehouseUpdate):
    for key, value in data.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, db_obj: Warehouse):
    db.delete(db_obj)
    db.commit()
