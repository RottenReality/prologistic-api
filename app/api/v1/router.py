from fastapi import APIRouter

from app.api.v1.clients import router as clients_router
from app.api.v1.products import router as products_router
from app.api.v1.warehouses import router as warehouses_router
from app.api.v1.ports import router as ports_router
from app.api.v1.land_shipments import router as land_shipments_router
from app.api.v1.sea_shipments import router as sea_shipments_router

router = APIRouter(
    prefix="/v1"
)

router.include_router(clients_router, prefix="/clients", tags=["clients"])
router.include_router(products_router, prefix="/products", tags=["products"])
router.include_router(warehouses_router, prefix="/warehouses", tags=["warehouses"])
router.include_router(ports_router, prefix="/ports", tags=["ports"])
router.include_router(land_shipments_router, prefix="/land-shipments", tags=["land shipments"])
router.include_router(sea_shipments_router, prefix="/sea-shipments", tags=["sea shipments"])