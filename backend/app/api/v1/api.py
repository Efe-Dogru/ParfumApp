from fastapi import APIRouter

from app.api.v1.endpoints import (
    perfumes,
    notes,
    main_accords,
    brands,
    types,
    countries,
    families,
    concentrations,
    perfumers
)

api_router = APIRouter()

api_router.include_router(perfumes.router, prefix="/perfumes", tags=["perfumes"])
api_router.include_router(brands.router, prefix="/brands", tags=["brands"])
api_router.include_router(types.router, prefix="/types", tags=["types"])
api_router.include_router(countries.router, prefix="/countries", tags=["countries"])
api_router.include_router(families.router, prefix="/families", tags=["families"])
api_router.include_router(concentrations.router, prefix="/concentrations", tags=["concentrations"])
api_router.include_router(perfumers.router, prefix="/perfumers", tags=["perfumers"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(main_accords.router, prefix="/main-accords", tags=["main-accords"]) 