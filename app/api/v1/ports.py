from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.port import Port
from app.core.database import get_db
from app.security.auth import check_token
from app.crud import port as crud
from app.schemas.port import PortCreate, PortUpdate, PortResponse

router = APIRouter(dependencies=[Depends(check_token)])

@router.get("/", response_model=list[PortResponse])
def list_ports(
    name: str | None = None,
    location: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Port)

    if name is not None:
        query = query.filter(Port.name.ilike(f"%{name}%"))

    if location is not None:
        query = query.filter(Port.location.ilike(f"%{location}%"))
        
    return query.offset(skip).limit(limit).all()

@router.get("/{port_id}", response_model=PortResponse)
def get_port(port_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, port_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Port not found")
    return obj

@router.post("/", response_model=PortResponse, status_code=201)
def create_port(data: PortCreate, db: Session = Depends(get_db)):
    return crud.create(db, data)

@router.put("/{port_id}", response_model=PortResponse)
def update_port(port_id: int, data: PortUpdate, db: Session = Depends(get_db)):
    obj = crud.get(db, port_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Port not found")
    return crud.update(db, obj, data)

@router.delete("/{port_id}", status_code=204)
def delete_port(port_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, port_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Port not found")
    crud.delete(db, obj)
