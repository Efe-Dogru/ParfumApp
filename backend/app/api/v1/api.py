from fastapi import APIRouter
from app.api.v1.endpoints import perfumes

api_router = APIRouter()

api_router.include_router(perfumes.router, prefix="/perfumes", tags=["perfumes"]) 