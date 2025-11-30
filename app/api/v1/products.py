from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product
from app.core.database import get_db
from app.security.auth import check_token
from app.crud import product as crud
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(dependencies=[Depends(check_token)])

@router.get("/", response_model=list[ProductResponse])
def list_products(
    name: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    
    return query.offset(skip).limit(limit).all()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Product not found")
    return obj

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    return crud.create(db, data)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    obj = crud.get(db, product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.update(db, obj, data)

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    obj = crud.get(db, product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Product not found")
    crud.delete(db, obj)
