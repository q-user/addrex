import logging

from fastapi import FastAPI

from config.settings import settings

# Set up logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)

# Add routes directly without circular imports
from api.v1.routes.create_address import router as create_address_router
from api.v1.routes.delete_address import router as delete_address_router
from api.v1.routes.get_address import router as get_address_router
from api.v1.routes.update_address import router as update_address_router

# Include routes in the app with v1 prefix
app.include_router(get_address_router, prefix='/v1', tags=['address'])
app.include_router(create_address_router, prefix='/v1', tags=['address'])
app.include_router(update_address_router, prefix='/v1', tags=['address'])
app.include_router(delete_address_router, prefix='/v1', tags=['address'])


@app.get('/')
async def root():
    logger.info('Root endpoint accessed')
    return {'message': 'Welcome to the Phonebook API Service'}


@app.get('/health')
async def health_check():
    logger.info('Health check endpoint accessed')
    return {'status': 'healthy', 'api_version': settings.api_version}
