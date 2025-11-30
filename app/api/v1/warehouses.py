from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.warehouse import Warehouse
from app.core.database import get_db
from app.security.auth import check_token
from app.crud import warehouse as crud
from app.schemas.warehouse import WarehouseCreate, WarehouseUpdate, WarehouseResponse

router = APIRouter(dependencies=[Depends(check_token)])

@router.get("/", response_model=list[WarehouseResponse])
def list_warehouses(
    name: str | None = None,
    location: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Warehouse)

    if name is not None:
        query = query.filter(Warehouse.name.ilike(f"%{name}%"))

    if location is not None:
        query = query.filter(Warehouse.location.ilike(f"%{location}%"))
        
    return query.offset(skip).limit(limit).all()
    

@router.get("/{warehouse_id}", response_model=WarehouseResponse)
def get_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, warehouse_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return obj

@router.post("/", response_model=WarehouseResponse, status_code=201)
def create_warehouse(data: WarehouseCreate, db: Session = Depends(get_db)):
    return crud.create(db, data)

@router.put("/{warehouse_id}", response_model=WarehouseResponse)
def update_warehouse(warehouse_id: int, data: WarehouseUpdate, db: Session = Depends(get_db)):
    obj = crud.get(db, warehouse_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return crud.update(db, obj, data)

@router.delete("/{warehouse_id}", status_code=204)
def delete_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, warehouse_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    crud.delete(db, obj)
