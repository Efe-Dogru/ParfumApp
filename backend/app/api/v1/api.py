from fastapi import APIRouter
from app.api.v1.endpoints import (
    perfumes,
    notes,
    main_accords,
    occasions,
    seasons
)

api_router = APIRouter()

api_router.include_router(perfumes.router, prefix="/perfumes", tags=["perfumes"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(main_accords.router, prefix="/main-accords", tags=["main-accords"])
api_router.include_router(occasions.router, prefix="/occasions", tags=["occasions"])
api_router.include_router(seasons.router, prefix="/seasons", tags=["seasons"]) 