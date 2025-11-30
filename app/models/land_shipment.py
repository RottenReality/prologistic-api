from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, ForeignKey
from datetime import datetime
from app.core.database import Base

class LandShipment(Base):
    __tablename__ = "land_shipments"

    id = Column(Integer, primary_key=True, index=True)
    
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)

    quantity = Column(Integer, nullable=False)
    register_date = Column(Date, nullable=False)
    delivery_date = Column(Date, nullable=False)

    price = Column(Numeric, nullable=False)
    discount = Column(Numeric, nullable=False)
    final_price = Column(Numeric, nullable=False)

    plate = Column(String(6), nullable=False)
    guide_number = Column(String(10), nullable=False, unique=True)

    created_at = Column(DateTime, default=datetime.utcnow)