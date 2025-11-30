from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.security.auth import check_token
from app.crud import land_shipment as crud
from app.schemas.land_shipment import LandShipmentCreate, LandShipmentUpdate, LandShipmentResponse

router = APIRouter(dependencies=[Depends(check_token)])

@router.get("/", response_model=list[LandShipmentResponse])
def list_shipments(db: Session = Depends(get_db)):
    return crud.list(db)

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
