from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.security.auth import check_token
from app.crud import sea_shipment as crud
from app.schemas.sea_shipment import SeaShipmentCreate, SeaShipmentUpdate, SeaShipmentResponse

router = APIRouter(dependencies=[Depends(check_token)])

@router.get("/", response_model=list[SeaShipmentResponse])
def list_shipments(db: Session = Depends(get_db)):
    return crud.list(db)

@router.get("/{shipment_id}", response_model=SeaShipmentResponse)
def get_shipment(shipment_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, shipment_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return obj

@router.post("/", response_model=SeaShipmentResponse, status_code=201)
def create_shipment(data: SeaShipmentCreate, db: Session = Depends(get_db)):
    return crud.create(db, data)

@router.put("/{shipment_id}", response_model=SeaShipmentResponse)
def update_shipment(shipment_id: int, data: SeaShipmentUpdate, db: Session = Depends(get_db)):
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
