from fastapi import APIRouter

# API version 1 router
api_v1 = APIRouter(prefix='/v1')

# Import and include individual route routers
from .routes.create_address import router as create_address_router
from .routes.delete_address import router as delete_address_router
from .routes.get_address import router as get_address_router
from .routes.update_address import router as update_address_router

# Include routes in the v1 router
api_v1.include_router(get_address_router)
api_v1.include_router(create_address_router)
api_v1.include_router(update_address_router)
api_v1.include_router(delete_address_router)
