from fastapi import APIRouter

from app.api.v1.clients import router as clients_router
from app.api.v1.products import router as products_router

router = APIRouter(
    prefix="/v1"
)

router.include_router(clients_router, prefix="/clients", tags=["clients"])
router.include_router(products_router, prefix="/products", tags=["products"])