from sqlalchemy.orm import Session
from app.models.land_shipment import LandShipment
from app.schemas.land_shipment import LandShipmentCreate, LandShipmentUpdate
from app.crud.utils import calc_land_discount

def get(db: Session, shipment_id: int):
    return db.query(LandShipment).filter(LandShipment.id == shipment_id).first()

def list(db: Session):
    return db.query(LandShipment).all()

def create(db: Session, data: LandShipmentCreate):
    discount, final_price = calc_land_discount(data.price, data.quantity)

    obj = LandShipment(
        **data.model_dump(),
        discount=discount,
        final_price=final_price
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update(db: Session, db_obj: LandShipment, data: LandShipmentUpdate):
    discount, final_price = calc_land_discount(data.price, data.quantity)

    update_data = data.model_dump()
    update_data["discount"] = discount
    update_data["final_price"] = final_price

    for key, value in update_data.items():
        setattr(db_obj, key, value)

    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, db_obj: LandShipment):
    db.delete(db_obj)
    db.commit()
