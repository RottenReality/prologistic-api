from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.security.auth import check_token
from app.crud import client as crud
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse

router = APIRouter(dependencies=[Depends(check_token)])

@router.get("/", response_model=list[ClientResponse])
def list_clients(db: Session = Depends(get_db)):
    return crud.list(db)

@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, client_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Client not found")
    return obj

@router.post("/", response_model=ClientResponse, status_code=201)
def create_client(data: ClientCreate, db: Session = Depends(get_db)):
    return crud.create(db, data)

@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, data: ClientUpdate, db: Session = Depends(get_db)):
    obj = crud.get(db, client_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Client not found")
    return crud.update(db, obj, data)

@router.delete("/{client_id}", status_code=204)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, client_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Client not found")
    crud.delete(db, obj)