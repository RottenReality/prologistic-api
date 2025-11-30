from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, ForeignKey
from datetime import datetime
from app.core.database import Base

class SeaShipment(Base):
    __tablename__ = "sea_shipments"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    port_id = Column(Integer, ForeignKey("ports.id"), nullable=False)

    quantity = Column(Integer, nullable=False)
    register_date = Column(Date, nullable=False)
    delivery_date = Column(Date, nullable=False)

    price = Column(Numeric, nullable=False)
    discount = Column(Numeric, nullable=False)
    final_price = Column(Numeric, nullable=False)

    fleet_number = Column(String(8), nullable=False)
    guide_number = Column(String(10), nullable=False, unique=True)

    created_at = Column(DateTime, default=datetime.utcnow)
