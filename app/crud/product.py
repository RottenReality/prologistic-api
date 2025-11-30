from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def get(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def list(db: Session):
    return db.query(Product).all()

def create(db: Session, data: ProductCreate):
    obj = Product(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update(db: Session, db_obj: Product, data: ProductUpdate):
    for key, value in data.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, db_obj: Product):
    db.delete(db_obj)
    db.commit()
