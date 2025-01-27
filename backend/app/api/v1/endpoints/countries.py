from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.country import Country as CountryModel
from app.schemas.country import Country

router = APIRouter()

@router.get("/", response_model=List[Country])
async def read_countries(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve countries.
    """
    query = select(CountryModel).offset(skip).limit(limit)
    result = await db.execute(query)
    countries = result.scalars().all()
    return countries 