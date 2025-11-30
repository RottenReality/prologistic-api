from sqlalchemy.orm import Session
from app.models.sea_shipment import SeaShipment
from app.schemas.sea_shipment import SeaShipmentCreate, SeaShipmentUpdate
from app.crud.utils import calc_sea_discount

def get(db: Session, shipment_id: int):
    return db.query(SeaShipment).filter(SeaShipment.id == shipment_id).first()

def list(db: Session):
    return db.query(SeaShipment).all()

def create(db: Session, data: SeaShipmentCreate):
    discount, final_price = calc_sea_discount(data.price, data.quantity)

    obj = SeaShipment(
        **data.model_dump(),
        discount=discount,
        final_price=final_price
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update(db: Session, db_obj: SeaShipment, data: SeaShipmentUpdate):
    discount, final_price = calc_sea_discount(data.price, data.quantity)

    update_data = data.model_dump()
    update_data["discount"] = discount
    update_data["final_price"] = final_price

    for key, value in update_data.items():
        setattr(db_obj, key, value)

    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, db_obj: SeaShipment):
    db.delete(db_obj)
    db.commit()
