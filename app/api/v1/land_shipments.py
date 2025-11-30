from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.models.land_shipment import LandShipment
from app.core.database import get_db
from app.security.auth import check_token
from app.crud import land_shipment as crud
from app.schemas.land_shipment import LandShipmentCreate, LandShipmentUpdate, LandShipmentResponse

router = APIRouter(dependencies=[Depends(check_token)])

@router.get("/", response_model=list[LandShipmentResponse])
def list_shipments(
    client_id: int | None = None,
    product_id: int | None = None,
    warehouse_id: int | None = None,
    plate: str | None = None,
    guide_number: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(LandShipment)

    if client_id is not None:
        query = query.filter(LandShipment.client_id == client_id)

    if product_id is not None:
        query = query.filter(LandShipment.product_id == product_id)

    if warehouse_id is not None:
        query = query.filter(LandShipment.warehouse_id == warehouse_id)
    
    if plate is not None:
        query = query.filter(LandShipment.plate.ilike(f"%{plate}%"))

    if guide_number is not None:
        query = query.filter(LandShipment.guide_number.ilike(f"%{guide_number}%"))

    if date_from is not None:
        query = query.filter(LandShipment.register_date >= date_from)

    if date_to is not None:
        query = query.filter(LandShipment.register_date <= date_to)

    return query.offset(skip).limit(limit).all()

@router.get("/{shipment_id}", response_model=LandShipmentResponse)
def get_shipment(shipment_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, shipment_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return obj

@router.post("/", response_model=LandShipmentResponse, status_code=201)
def create_shipment(data: LandShipmentCreate, db: Session = Depends(get_db)):
    return crud.create(db, data)

@router.put("/{shipment_id}", response_model=LandShipmentResponse)
def update_shipment(shipment_id: int, data: LandShipmentUpdate, db: Session = Depends(get_db)):
    obj = crud.get(db, shipment_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return crud.update(db, obj, data)

@router.delete("/{shipment_id}", status_code=204)
def delete_shipment(shipment_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, shipment_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Shipment not found")
    crud.delete(db, obj)
